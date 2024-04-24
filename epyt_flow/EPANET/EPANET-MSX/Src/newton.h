/******************************************************************************
**  MODULE:        NEWTON.H
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   header file for the equation solver contained in newton.c.
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.00
**  LAST UPDATE:   04/14/2021
******************************************************************************/

#ifndef NEWTON_H
#define NEWTON_H

typedef struct
{
    int      Nmax;          // max. number of equations
    int* Indx;         // permutation vector of row indexes     
    double* F;            // function & adjustment vector
    double* W;            // work vector
    double** J;           // Jacobian matrix
}MSXNewton;

// Opens the equation solver system
int  newton_open(int n);

// Closes the equation solver system
void newton_close(void);

// Applies the solver to a specific system of equations
int  newton_solve(double x[], int n, int maxit, int numsig,  
                  void (*func)(double, double*, int, double*));

#endif