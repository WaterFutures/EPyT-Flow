/************************************************************************
**  MODULE:        RK5.H
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   Header file for the ODE solver contained in RK5.C.
**  AUTHOR:        L. Rossman, US EPA - NRMRL
**  VERSION:       2.0.00                                               
**  LAST UPDATE:   04/14/2021
***********************************************************************/

#ifndef RK5_H
#define RK5_H

typedef struct
{
    int      Nmax;          // max. number of equations
    int      Itmax;         // max. number of integration steps
    int      Adjust;        // use adjustable step size
    double* Ak;           // work arrays
    double* K1;
    double* K2;
    double* K3;
    double* K4;
    double* K5;
    double* K6;
    double* Ynew;         // updated solution
    void     (*Report) (double, double*, int);
}MSXRungeKutta;
// Opens the ODE solver system
int  rk5_open(int n, int itmax, int adjust);

// Closes the ODE solver system
void rk5_close(void);

// Applies the solver to integrate a specific system of ODEs
int  rk5_integrate(double y[], int n, double t, double tnext,
                   double* htry, double atol[], double rtol[],
                   void (*func)(double, double*, int, double*));

#endif