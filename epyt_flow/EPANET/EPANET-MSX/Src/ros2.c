/*******************************************************************************
**  MODULE:        ROS2.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   a second order Rosenbrock 2(1) method for solving stiff sets of
**                 ordinary differential equations.
**  AUTHOR:        L. Rossman, US EPA - NRMRL
**  VERSION:       2.0.00
**  LAST UPDATE:   04/14/2021
**
**  This code is based on material presented in:
**    Verwer, J.G., Spee, E.J., Blom, J.G. and Hundsdorfer, W.H.,
**    "A second order Rosenbrock method applied to photochemical dispersion
**    problems", SIAM J. Sci. Comput., 20:1456-1480, July 1999.
*******************************************************************************/

#include <stdlib.h>
#include <math.h>
#include "msxutils.h"
#include "ros2.h"

#define fmin(x,y) (((x)<=(y)) ? (x) : (y))     /* minimum of x and y    */
#define fmax(x,y) (((x)>=(y)) ? (x) : (y))     /* maximum of x and y    */

//  Local variables
//-----------------
MSXRosenbrock MSXRosenbrockSolver;

#pragma omp threadprivate(MSXRosenbrockSolver)

//=============================================================================

int ros2_open(int n, int adjust)
/*
**  Purpose:
**    Opens the ROS2 integrator.
**
**  Input:
**    n = number of equations to be solved
**    adjust = 1 if step size adjustment used, 0 if not
**
**  Returns:
**    1 if successful, 0 if not.
*/
{
    int errorcode = 1;
    int n1 = n + 1;

#pragma omp parallel
{
    MSXRosenbrockSolver.Nmax = n;
    MSXRosenbrockSolver.Adjust = adjust;
    MSXRosenbrockSolver.K1 = NULL;
    MSXRosenbrockSolver.K2 = NULL;
    MSXRosenbrockSolver.Jindx = NULL;
    MSXRosenbrockSolver.Ynew = NULL;
    MSXRosenbrockSolver.A = NULL;
    MSXRosenbrockSolver.K1 = (double*)calloc(n1, sizeof(double));
    MSXRosenbrockSolver.K2 = (double*)calloc(n1, sizeof(double));
    MSXRosenbrockSolver.Jindx = (int*)calloc(n1, sizeof(int));
    MSXRosenbrockSolver.Ynew = (double*)calloc(n1, sizeof(double));
    MSXRosenbrockSolver.A = createMatrix(n1, n1);
#pragma omp critical
    {
        if (!MSXRosenbrockSolver.Jindx || !MSXRosenbrockSolver.Ynew ||
            !MSXRosenbrockSolver.K1 || !MSXRosenbrockSolver.K2) errorcode = 0;
        if (!MSXRosenbrockSolver.A) errorcode = 0;
    }
}

    return errorcode;
}

//=============================================================================

void ros2_close()
/*
**  Purpose:
**    closes the ROS2 integrator.
**
**  Input:
**    none.
*/
{

#pragma omp parallel
{

    if (MSXRosenbrockSolver.Jindx) { free(MSXRosenbrockSolver.Jindx); MSXRosenbrockSolver.Jindx = NULL; }
    if (MSXRosenbrockSolver.Ynew) { free(MSXRosenbrockSolver.Ynew); MSXRosenbrockSolver.Ynew = NULL; }
    if (MSXRosenbrockSolver.K1) { free(MSXRosenbrockSolver.K1); MSXRosenbrockSolver.K1 = NULL; }
    if (MSXRosenbrockSolver.K2) { free(MSXRosenbrockSolver.K2); MSXRosenbrockSolver.K2 = NULL; }
    freeMatrix(MSXRosenbrockSolver.A);
    MSXRosenbrockSolver.A = NULL;
}

}

//=============================================================================
      
int ros2_integrate(double y[], int n, double t, double tnext,
                   double* htry, double atol[], double rtol[],
                   void (*func)(double, double*, int, double*))
/*
**  Purpose:
**    integrates a system of ODEs over a specified time interval.
**
**  Input:
**    y[1..n] = vector of dependent variable values at the start
**              of the integration interval
**    n = number of dependent variables
**    t = time value at the start of the interval
**    tnext = time value at the end of the interval
**    htry = initial step size to be taken
**    atol[1..n] = vector of absolute tolerances on the variables y
**    rtol[1..n] = vector of relative tolerances on the variables y
**    func = name of the function that computes dy/dt for each y
**
**  Output:
**    htry = size of the last full time step taken.
**
**  Returns:
**    the number of times that func() was called, -1 if 
**    the Jacobian is singular, or -2 if the step size
**    shrinks to 0.
**
**  Notes:
**  1. The arguments to the function func() are:
**      t = current time
**      y[1..n] = vector of dependent variable values
**      n = number of dependent variables
**      dfdy[1..n] = vector of derivative values computed.
**
**  2. The arrays used in this function are 1-based, so
**     they must have been sized to n+1 when first created.
*/
{      
    double UROUND = 2.3e-16;
    double g, ghinv, ghinv1, dghinv, ytol;
    double h, hold, hmin, hmax, tplus;
    double ej, err, factor, facmax;
    int    nfcn, njac, naccept, nreject, j;
    int    isReject;
	int    adjust = MSXRosenbrockSolver.Adjust;

// --- Initialize counters, etc.

    g = 1.0 + 1.0 / sqrt(2.0);
    ghinv1 = 0.0;
    tplus = t;
    isReject = 0;
    naccept  = 0;
    nreject  = 0;
    nfcn     = 0;
    njac     = 0;

// --- Initial step size

    hmax = tnext - t;
    hmin = 1.e-8;
    h = *htry;
    if ( h == 0.0 )
    {
        func(t, y, n, MSXRosenbrockSolver.K1);
        nfcn += 1;
        adjust = 1;
        h = tnext - t;
        for (j=1; j<=n; j++)
        {
            ytol = atol[j] + rtol[j]*fabs(y[j]);
            if (MSXRosenbrockSolver.K1[j] != 0.0) h = fmin(h, (ytol/fabs(MSXRosenbrockSolver.K1[j])));
        }
    }
    h = fmax(hmin, h);
    h = fmin(hmax, h);

// --- Start the time loop 

    while ( t < tnext )
    {
    // --- check for zero step size

        if (0.10*fabs(h) <= fabs(t)*UROUND) return -2;

    // --- adjust step size if interval exceeded

        tplus = t + h;
        if ( tplus > tnext )
        {
            h = tnext - t;
            tplus = tnext;
        }

    // --- Re-compute the Jacobian if step size accepted

        if ( isReject == 0 )
        {
            jacobian(y, n, MSXRosenbrockSolver.K1, MSXRosenbrockSolver.K2, MSXRosenbrockSolver.A, func);
            njac++;
            nfcn += 2*n;
            ghinv1 = 0.0;
        }

    // --- Update the Jacobian to reflect new step size

        ghinv = -1.0 / (g*h);
        dghinv = ghinv - ghinv1;
        for (j=1; j<=n; j++)
        {
            MSXRosenbrockSolver.A[j][j] += dghinv;
        }
        ghinv1 = ghinv;
        if ( !factorize(MSXRosenbrockSolver.A, n, MSXRosenbrockSolver.K1, MSXRosenbrockSolver.Jindx) ) return -1;

    // --- Stage 1 solution

        func(t, y, n, MSXRosenbrockSolver.K1);
        nfcn += 1;
        for (j=1; j<=n; j++) MSXRosenbrockSolver.K1[j] *= ghinv;
        solve(MSXRosenbrockSolver.A, n, MSXRosenbrockSolver.Jindx, MSXRosenbrockSolver.K1);

    // --- Stage 2 solution

        for (j=1; j<=n; j++)
        {
            MSXRosenbrockSolver.Ynew[j] = y[j] + h* MSXRosenbrockSolver.K1[j];
        }
        func(t, MSXRosenbrockSolver.Ynew, n, MSXRosenbrockSolver.K2);
        nfcn += 1;
        for (j=1; j<=n; j++)
        {
            MSXRosenbrockSolver.K2[j] = (MSXRosenbrockSolver.K2[j] - 2.0* MSXRosenbrockSolver.K1[j])*ghinv;
        }
        solve(MSXRosenbrockSolver.A, n, MSXRosenbrockSolver.Jindx, MSXRosenbrockSolver.K2);

    // --- Overall solution

        for (j=1; j<=n; j++)
        {
            MSXRosenbrockSolver.Ynew[j] = y[j] + 1.5*h* MSXRosenbrockSolver.K1[j] + 0.5*h* MSXRosenbrockSolver.K2[j];
        }

    // --- Error estimation

        hold = h;
        err = 0.0;
        if ( adjust )
        {
            for (j=1; j<=n; j++)
            {
                ytol = atol[j] + rtol[j]*fabs(MSXRosenbrockSolver.Ynew[j]);
	            ej = fabs(MSXRosenbrockSolver.Ynew[j] - y[j] - h* MSXRosenbrockSolver.K1[j])/ytol;
                err = err + ej*ej; 
            }
            err = sqrt(err/n);
            err = fmax(UROUND, err);

        // --- Choose the step size

            factor = 0.9 / sqrt(err);
            if (isReject) facmax = 1.0;
            else          facmax = 10.0;
            factor = fmin(factor, facmax);
            factor = fmax(factor, 1.0e-1);
            h = factor*h;
            h = fmin(hmax, h);
        }

    // --- Reject/accept the step

        if ( err > 1.0 )
        {
            isReject = 1;
            nreject++;
            h = 0.5*h;
        }
        else
        {
            isReject = 0;
            for (j=1; j<=n; j++)
            {
                y[j] = MSXRosenbrockSolver.Ynew[j];
                if ( y[j] <= UROUND ) y[j] = 0.0;
            }
            if ( adjust ) *htry = h;
            t = tplus;    
            naccept++;
        }
        
// --- End of the time loop 

    }
    return nfcn;
}
