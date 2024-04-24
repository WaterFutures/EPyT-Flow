/************************************************************************
**  MODULE:        MSXFUNCS.H
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   Definitions of functions loaded from compiled chemistry file.
**  COPYRIGHT:     Copyright (C) 2007 Feng Shang, Lewis Rossman, and James Uber.
**                 All Rights Reserved. See license information in LICENSE.TXT.
**  AUTHORS:       See Authors
**  VERSION:       2.0.00
**  LAST UPDATE:   04/14/2021
***********************************************************************/

#ifndef MSXFUNCS_H
#define MSXFUNCS_H

// Define pointers for each group of chemistry functions
typedef void (*MSXGETRATES)(double *, double *, double * , double *, double *);
typedef void (*MSXGETEQUIL)(double *, double *, double * , double *, double *);
typedef void (*MSXGETFORMULAS)(double *, double *, double *, double *);

// Declare each chemistry function
extern MSXGETRATES    MSXgetPipeRates;
extern MSXGETRATES    MSXgetTankRates;
extern MSXGETEQUIL    MSXgetPipeEquil;
extern MSXGETEQUIL    MSXgetTankEquil;
extern MSXGETFORMULAS MSXgetPipeFormulas;
extern MSXGETFORMULAS MSXgetTankFormulas;

// Functions that load and free the chemistry functions
int  MSXfuncs_load(char *);
void MSXfuncs_free(void);

// Function that executes a command line program
int MSXfuncs_run(char * );

#endif
