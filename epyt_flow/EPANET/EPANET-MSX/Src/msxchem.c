/*******************************************************************************
**  MODULE:        MSXCHEM.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   Water quality chemistry functions.
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.00
**  LAST UPDATE:   04/14/2021
*******************************************************************************/

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

#include "msxtypes.h"
#include "rk5.h"
#include "ros2.h"
#include "newton.h"
#include "msxfuncs.h"                                                          

//  External variables
//--------------------
extern MSXproject  MSX;                // MSX project data


//  Constants
//-----------
int    MAXIT = 20;                     // Max. number of iterations used
                                       // in nonlinear equation solver
int    NUMSIG = 3;                     // Number of significant digits in
                                       // nonlinear equation solver error

//  Local variables
//-----------------
static Pseg   TheSeg;                  // Current water quality segment
static int    TheLink;                 // Index of current link
static int    TheNode;                 // Index of current node
static int    TheTank;                 // Index of current tank                
static int    NumSpecies;              // Total number of species
static int    NumPipeRateSpecies;      // Number of species with pipe rates
static int    NumTankRateSpecies;      // Number of species with tank rates
static int    NumPipeFormulaSpecies;   // Number of species with pipe formulas
static int    NumTankFormulaSpecies;   // Number of species with tank formulas
static int    NumPipeEquilSpecies;     // Number of species with pipe equilibria
static int    NumTankEquilSpecies;     // Number of species with tank equilibria
static int    *PipeRateSpecies;        // Species governed by pipe reactions
static int    *TankRateSpecies;        // Species governed by tank reactions
static int    *PipeEquilSpecies;       // Species governed by pipe equilibria
static int    *TankEquilSpecies;       // Species governed by tank equilibria
static int    LastIndex[MAX_OBJECTS];  // Last index of given type of variable
static double *Atol;                   // Absolute concentration tolerances
static double *Rtol;                   // Relative concentration tolerances
static double *Yrate;                  // Rate species concentrations
static double *Yequil;                 // Equilibrium species concentrations
static double HydVar[MAX_HYD_VARS];    // Values of hydraulic variables
static double *F;                      // Function values                      
static double *ChemC1;

#pragma omp threadprivate(TheSeg, TheLink, TheNode, TheTank, Yrate, Yequil, HydVar, F, ChemC1)

//  Exported functions
//--------------------
int    MSXchem_open(void);
int    MSXchem_react(double dt);
int    MSXchem_equil(int zone, int k, double *c);
char*  MSXchem_getVariableStr(int i, char *s);                                 
void   MSXchem_close(void);

// Imported functions
//-------------------
int    MSXcompiler_open(void);                                                 
void   MSXcompiler_close(void);                                                
double MSXerr_validate(double x, int index, int element, int exprType);        

//  Local functions
//-----------------
static void   setSpeciesChemistry(void);
static void   setTankChemistry(void);
//static void   evalHydVariables(int k);           
static int    evalPipeReactions(int k, double dt);
static int    evalTankReactions(int k, double dt);
static int    evalPipeEquil(double *c);
static int    evalTankEquil(double *c);
static void   evalPipeFormulas(double *c);
static void   evalTankFormulas(double *c);
static double getPipeVariableValue(int i);
static double getTankVariableValue(int i);
static void   getPipeDcDt(double t, double y[], int n, double deriv[]);
static void   getTankDcDt(double t, double y[], int n, double deriv[]);
static void   getPipeEquil(double t, double y[], int n, double f[]);
static void   getTankEquil(double t, double y[], int n, double f[]);
static int    isValidNumber(double x);                                         //(L.Rossman - 11/03/10)


//=============================================================================

int  MSXchem_open()
/*
**  Purpose:
**    opens the multi-species chemistry system.
**
**  Input:
**    none.
**
**  Returns:
**    an error code (0 if no error).
*/
{
    int m;
    int numWallSpecies;
    int numBulkSpecies;
    int numTankExpr;
    int numPipeExpr;
    int errcode = 0;

    // --- allocate memory

    PipeRateSpecies = NULL;
    TankRateSpecies = NULL;
    PipeEquilSpecies = NULL;
    TankEquilSpecies = NULL;
    Atol = NULL;
    Rtol = NULL;
    Yrate = NULL;
    Yequil = NULL;
    NumSpecies = MSX.Nobjects[SPECIES];
    m = NumSpecies + 1;
    PipeRateSpecies = (int*)calloc(m, sizeof(int));
    TankRateSpecies = (int*)calloc(m, sizeof(int));
    PipeEquilSpecies = (int*)calloc(m, sizeof(int));
    TankEquilSpecies = (int*)calloc(m, sizeof(int));
    Atol = (double*)calloc(m, sizeof(double));
    Rtol = (double*)calloc(m, sizeof(double));
    CALL(errcode, MEMCHECK(PipeRateSpecies));
    CALL(errcode, MEMCHECK(TankRateSpecies));
    CALL(errcode, MEMCHECK(PipeEquilSpecies));
    CALL(errcode, MEMCHECK(TankEquilSpecies));
    CALL(errcode, MEMCHECK(Atol));
    CALL(errcode, MEMCHECK(Rtol));

#pragma omp parallel
{
    Yrate = (double*)calloc(m, sizeof(double));
    Yequil = (double*)calloc(m, sizeof(double));
    F = (double*)calloc(m, sizeof(double));                             
    ChemC1 = (double*)calloc(m, sizeof(double));
#pragma omp critical
    {
        CALL(errcode, MEMCHECK(Yrate));
        CALL(errcode, MEMCHECK(Yequil));
        CALL(errcode, MEMCHECK(F));
        CALL(errcode, MEMCHECK(ChemC1));
    }
}
    if ( errcode ) return errcode;

// --- assign species to each type of chemical expression

    setSpeciesChemistry();
    numPipeExpr = NumPipeRateSpecies + NumPipeFormulaSpecies + NumPipeEquilSpecies;
    numTankExpr = NumTankRateSpecies + NumTankFormulaSpecies + NumTankEquilSpecies;

// --- use pipe chemistry for tanks if latter was not supplied

    if ( numTankExpr == 0 )
    {
        setTankChemistry();
        numTankExpr = numPipeExpr;
    }

// --- check if enough equations were specified

    numWallSpecies = 0;
    numBulkSpecies = 0;
    for (m=1; m<=NumSpecies; m++)
    {
        if ( MSX.Species[m].type == WALL ) numWallSpecies++;
        if ( MSX.Species[m].type == BULK ) numBulkSpecies++;
    }
    if ( numPipeExpr != NumSpecies )       return ERR_NUM_PIPE_EXPR;
    if ( numTankExpr != numBulkSpecies   ) return ERR_NUM_TANK_EXPR;

// --- open the ODE solver;
//     arguments are max. number of ODE's,
//     max. number of steps to be taken,
//     1 if automatic step sizing used (or 0 if not used)

    if ( MSX.Solver == RK5 )
    {
        if ( rk5_open(NumSpecies, 1000, 1) == FALSE )
            return ERR_INTEGRATOR_OPEN;
    }
    if ( MSX.Solver == ROS2 )
    {
        if ( ros2_open(NumSpecies, 1) == FALSE )
            return ERR_INTEGRATOR_OPEN;
    }

// --- open the algebraic eqn. solver

    m = MAX(NumPipeEquilSpecies, NumTankEquilSpecies);
    if ( newton_open(m) == FALSE ) return ERR_NEWTON_OPEN;

// --- assign entries to LastIndex array

    LastIndex[SPECIES] = MSX.Nobjects[SPECIES];
    LastIndex[TERM] = LastIndex[SPECIES] + MSX.Nobjects[TERM];
    LastIndex[PARAMETER] = LastIndex[TERM] + MSX.Nobjects[PARAMETER];
    LastIndex[CONSTANT] = LastIndex[PARAMETER] + MSX.Nobjects[CONSTANT];

// --- compile chemistry function dynamic library if specified                 

    if ( MSX.Compiler )
    {
        errcode = MSXcompiler_open();
        if ( errcode ) return errcode;
    }
    return 0;
}

//=============================================================================

void MSXchem_close()
/*
**  Purpose:
**    closes the multi-species chemistry system.
**
**  Input:
**    none.
*/
{
    if (MSX.Compiler)	MSXcompiler_close();                                   
    if (MSX.Solver == RK5) rk5_close();
    if (MSX.Solver == ROS2) ros2_close();
    newton_close();
    FREE(PipeRateSpecies);
    FREE(TankRateSpecies);
    FREE(PipeEquilSpecies);
    FREE(TankEquilSpecies);
    FREE(Atol);
    FREE(Rtol);

#pragma omp parallel
{
    FREE(ChemC1);
    FREE(Yrate);
    FREE(Yequil);
    FREE(F);                                                                   
}

}

//=============================================================================

int MSXchem_react(double dt)
/*
**  Purpose:
**    computes reactions in all pipes and tanks.
**
**  Input:
**    dt = current WQ time step (sec).
**
**  Returns:
**    an error code or 0 if no error.
*/
{
    int k, m;
    int errcode = 0;

// --- save tolerances of pipe rate species

    for (k=1; k<=NumPipeRateSpecies; k++)
    {
        m = PipeRateSpecies[k];
        Atol[k] = MSX.Species[m].aTol;
        Rtol[k] = MSX.Species[m].rTol;
    }

// --- examine each link
#pragma omp parallel
{
    #pragma omp for private(k)
    for (k = 1; k <= MSX.Nobjects[LINK]; k++)
    {
        // --- skip non-pipe links

        if (MSX.Link[k].len == 0.0) continue;

        // --- evaluate hydraulic variables

        //evalHydVariables(k);
        for (int hi = 1; hi < MAX_HYD_VARS; hi++)
            HydVar[hi] = MSX.Link[k].HydVar[hi];
         // --- compute pipe reactions

         errcode = evalPipeReactions(k, dt);
        //if (errcode) return errcode;
    }
}
    if (errcode) return errcode;

// --- save tolerances of tank rate species

    for (k=1; k<=NumTankRateSpecies; k++)
    {
        m = TankRateSpecies[k];
        Atol[k] = MSX.Species[m].aTol;
        Rtol[k] = MSX.Species[m].rTol;
    }

// --- examine each tank

    for (k=1; k<=MSX.Nobjects[TANK]; k++)
    {
    // --- skip reservoirs

        if (MSX.Tank[k].a == 0.0) continue;

    // --- compute tank reactions

        errcode = evalTankReactions(k, dt);
        if ( errcode ) return errcode;
    }
    return errcode;
}

//=============================================================================

int MSXchem_equil(int zone, int k, double *c)
/*
**  Purpose:
**    computes equilibrium concentrations for a set of chemical species.
**
**  Input:
**    zone = reaction zone (NODE or LINK)
**    k = pipe or tank index 
**    c[] = array of species concentrations
**
**  Output:
**    updated value of c[].
**
**  Returns:
**    an error code or 0 if no errors.
*/
{
    int errcode = 0;
    if ( zone == LINK )
    {
        TheLink = k;
        for (int vi = 1; vi < MAX_HYD_VARS; vi++)
            HydVar[vi] = MSX.Link[k].HydVar[vi];
        if ( NumPipeEquilSpecies > 0 ) errcode = evalPipeEquil(c);
        evalPipeFormulas(c);
    }
    if ( zone == NODE )
    {
        TheTank = k;
        TheNode = MSX.Tank[k].node;
        if ( NumTankEquilSpecies > 0 ) errcode = evalTankEquil(c);
        evalTankFormulas(c);
    }
    return errcode;
}

//=============================================================================

char* MSXchem_getVariableStr(int i, char *s)                                   
/*
**  Purpose:
**    returns a string representation of a variable used in the chemistry
**    functions appearing in the C source code file used to compile
**    these functions
**
**  Input:
**    i = variable's index in the LastIndex array
**    s = string to hold variable's symbol
**
**  Output:
**    returns a pointer to s
*/
{
// --- WQ species have index between 1 & # of species

    if ( i <= LastIndex[SPECIES] ) sprintf(s, "c[%d]", i);

// --- intermediate term expressions come next

    else if ( i <= LastIndex[TERM] )
    {
        i -= LastIndex[TERM-1];
        sprintf(s, "term(%d, c, k, p, h)", i);
    }

// --- reaction parameter indexes come after that

    else if ( i <= LastIndex[PARAMETER] )
    {
        i -= LastIndex[PARAMETER-1];
        sprintf(s, "p[%d]", i);
    }

// --- followed by constants

    else if ( i <= LastIndex[CONSTANT] )
    {
        i -= LastIndex[CONSTANT-1];
        sprintf(s, "k[%d]", i);
    }

// --- and finally by hydraulic variables

    else 
    {
        i -= LastIndex[CONSTANT];
        sprintf(s, "h[%d]", i);
    }
    return s;
}

//=============================================================================

void setSpeciesChemistry()
/*
**  Purpose:
**    determines which species are described by reaction rate
**    expressions, equilibrium expressions, or simple formulas.
**
**  Input:
**    none.
**
**  Output:
**    updates arrays of different chemistry types.
*/
{
    int m;
    NumPipeRateSpecies = 0;
    NumPipeFormulaSpecies = 0;
    NumPipeEquilSpecies = 0;
    NumTankRateSpecies = 0;
    NumTankFormulaSpecies = 0;
    NumTankEquilSpecies = 0;
    for (m=1; m<=NumSpecies; m++)
    {
        switch ( MSX.Species[m].pipeExprType )
        {
          case RATE:
            NumPipeRateSpecies++;
            PipeRateSpecies[NumPipeRateSpecies] = m;
            break;

          case FORMULA:
            NumPipeFormulaSpecies++;
            break;

          case EQUIL:
            NumPipeEquilSpecies++;
            PipeEquilSpecies[NumPipeEquilSpecies] = m;
            break;
        }
        switch ( MSX.Species[m].tankExprType )
        {
          case RATE:
            NumTankRateSpecies++;
            TankRateSpecies[NumTankRateSpecies] = m;
            break;

          case FORMULA:
            NumTankFormulaSpecies++;
            break;

          case EQUIL:
            NumTankEquilSpecies++;
            TankEquilSpecies[NumTankEquilSpecies] = m;
            break;
        }
    }
}

//=============================================================================

void setTankChemistry()
/*
**  Purpose:
**    assigns pipe chemistry expressions to tank chemistry for
**    each chemical species.
**
**  Input:
**    none.
**
**  Output:
**    updates arrays of different tank chemistry types.
*/
{
    int m;
    for (m=1; m<=NumSpecies; m++)
    {
        MSX.Species[m].tankExpr = MSX.Species[m].pipeExpr;
        MSX.Species[m].tankExprType = MSX.Species[m].pipeExprType;
    }
    NumTankRateSpecies = NumPipeRateSpecies;
    for (m=1; m<=NumTankRateSpecies; m++)
    {
        TankRateSpecies[m] = PipeRateSpecies[m];
    }
    NumTankFormulaSpecies = NumPipeFormulaSpecies;
    NumTankEquilSpecies = NumPipeEquilSpecies;
    for (m=1; m<=NumTankEquilSpecies; m++)
    {
        TankEquilSpecies[m] = PipeEquilSpecies[m];
    }
}



//=============================================================================

int evalPipeReactions(int k, double dt)
/*
**  Purpose:
**    updates species concentrations in each WQ segment of a pipe
**    after reactions occur over time step dt.
**
**  Input:
**    k = link index
**    dt = time step (sec).
**
**  Output:
**    updates values in the concentration vector C[] associated
**    with a pipe's WQ segments.
**
**  Returns:
**    an error code or 0 if no error.
**
**  Re-written to accommodate compiled functions (1.1)                         
*/
{
    int i, m;
    int errcode = 0, ierr = 0;
    double tstep = (double)dt / MSX.Ucf[RATE_UNITS];
    double c, dh;

// --- start with the most downstream pipe segment

    TheLink = k;
    TheSeg = MSX.FirstSeg[TheLink];
    while ( TheSeg )
    {
        for (m = 1; m <= NumSpecies; m++)
        {
            ChemC1[m] = TheSeg->c[m];
            TheSeg->lastc[m] = TheSeg->c[m];
        }
        ierr = 0;

    // --- react each reacting species over the time step

        if ( dt > 0.0 )
        {

        // --- place current concentrations of species that react in vector Yrate

            for (i=1; i<=NumPipeRateSpecies; i++)
            {
                m = PipeRateSpecies[i];
                Yrate[i] = TheSeg->c[m];
            }
        
        // --- Euler integrator

            if ( MSX.Solver == EUL )
            {
                getPipeDcDt(0, Yrate, NumPipeRateSpecies, Yrate);
                for (i=1; i<=NumPipeRateSpecies; i++)
                {
                    m = PipeRateSpecies[i];
                    c = TheSeg->c[m] + Yrate[i]*tstep;
                    TheSeg->c[m] = MAX(c, 0.0);
                }
            }

        // --- other integrators
            else
            {
                dh = TheSeg->hstep;

            // --- Runge-Kutta integrator

                if ( MSX.Solver == RK5 )
                    ierr = rk5_integrate(Yrate, NumPipeRateSpecies, 0, tstep,
                                         &dh, Atol, Rtol, getPipeDcDt);

            // --- Rosenbrock integrator

                if ( MSX.Solver == ROS2 )
                    ierr = ros2_integrate(Yrate, NumPipeRateSpecies, 0, tstep,
                                          &dh, Atol, Rtol, getPipeDcDt);

            // --- save new concentration values of the species that reacted

                for (m=1; m<=NumSpecies; m++) TheSeg->c[m] = ChemC1[m];
                for (i=1; i<=NumPipeRateSpecies; i++)
                {
                    m = PipeRateSpecies[i];
                    TheSeg->c[m] = MAX(Yrate[i], 0.0);
                }
                TheSeg->hstep = dh;
            }
            if ( ierr < 0 ) return 
                ERR_INTEGRATOR;

            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            {
                if (MSX.Species[m].type == BULK)
                {
                    MSX.Link[k].reacted[m] += TheSeg->v * (TheSeg->c[m] - TheSeg->lastc[m]) * LperFT3;
                }
                else if (MSX.Link[k].diam > 0)
                {
                    MSX.Link[k].reacted[m] += TheSeg->v * 4.0 / MSX.Link[k].diam * MSX.Ucf[AREA_UNITS] * (TheSeg->c[m] - TheSeg->lastc[m]);
                }
                TheSeg->lastc[m] = TheSeg->c[m];
            }
        }

    // --- compute new equilibrium concentrations within segment

        errcode = MSXchem_equil(LINK, k, TheSeg->c);
        if ( errcode ) return errcode;

    // --- move to the segment upstream of the current one
        TheSeg = TheSeg->prev;
    }
    return errcode;
}

//=============================================================================

int evalTankReactions(int k, double dt)
/*
**  Purpose:
**    updates species concentrations in a given storage tank
**    after reactions occur over time step dt.
**
**  Input:
**    k = tank index
**    dt = time step (sec).
**
**  Output:
**    updates values in the concentration vector Tank[k].c[]
**    for tank k.
**
**  Returns:
**    an error code or 0 if no error.
**
**  Re-written to accommodate compiled functions (1.1)                         
*/
{
    int i, m;
    int errcode = 0, ierr = 0;
    double tstep = (double)dt / MSX.Ucf[RATE_UNITS];
    double c, dh;

// --- evaluate each volume segment in the tank

    TheTank = k;
    TheNode = MSX.Tank[k].node;
    i = MSX.Nobjects[LINK] + k;
    TheSeg = MSX.FirstSeg[i];
    while ( TheSeg )
    {
        for (m = 1; m <= NumSpecies; m++)
        {
            ChemC1[m] = TheSeg->c[m];
            TheSeg->lastc[m] = TheSeg->c[m];
        }
        ierr = 0;

    // --- react each reacting species over the time step

        if ( dt > 0.0 )
        {

        // --- place current concentrations of species that react in vector Yrate
            for (i=1; i<=NumTankRateSpecies; i++)
            {
                m = TankRateSpecies[i];
  //              Yrate[i] = MSX.Tank[k].c[m];
                Yrate[i] = TheSeg->c[m];
            }

        // --- Euler integrator

            if ( MSX.Solver == EUL )
            {
                getTankDcDt(0, Yrate, NumTankRateSpecies, Yrate);
                for (i=1; i<=NumTankRateSpecies; i++)
                {
                    m = TankRateSpecies[i];
                    c = TheSeg->c[m] + Yrate[i]*tstep;
                    TheSeg->c[m] = MAX(c, 0.0);
                }
            }

        // --- other integrators
            else
            {
                dh = MSX.Tank[k].hstep;

            // --- Runge-Kutta integrator

                if ( MSX.Solver == RK5 )
                    ierr = rk5_integrate(Yrate, NumTankRateSpecies, 0, tstep,
                                         &dh, Atol, Rtol, getTankDcDt);

            // --- Rosenbrock integrator

                if ( MSX.Solver == ROS2 )
                    ierr = ros2_integrate(Yrate, NumTankRateSpecies, 0, tstep,
                                          &dh, Atol, Rtol, getTankDcDt);

            // --- save new concentration values of the species that reacted

                for (m=1; m<=NumSpecies; m++) TheSeg->c[m] = ChemC1[m];
                for (i=1; i<=NumTankRateSpecies; i++)
                {
                    m = TankRateSpecies[i];
                    TheSeg->c[m] = MAX(Yrate[i], 0.0);
                }
                TheSeg->hstep = dh;
            }
            if ( ierr < 0 ) return 
                ERR_INTEGRATOR;
        }

    // --- compute new equilibrium concentrations within segment

        errcode = MSXchem_equil(NODE, k, TheSeg->c);
        if ( errcode ) return errcode;

    // --- move to the next tank segment
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        {
            if (MSX.Species[m].type == BULK)
            {
                MSX.Tank[k].reacted[m] += TheSeg->v * (TheSeg->c[m] - TheSeg->lastc[m]) * LperFT3;
            }
            TheSeg->lastc[m] = TheSeg->c[m];
        }

        TheSeg = TheSeg->prev;
    }
    return errcode;
}

//=============================================================================

int evalPipeEquil(double *c)
/*
**  Purpose:
**    computes equilibrium concentrations for water in a pipe segment.
**
**  Input:
**    c[] = array of starting species concentrations
**
**  Output:
**    c[] = array of equilibrium concentrations.
**
**  Returns:
**    an error code or 0 if no error.
*/
{
    int i, m;
    int errcode;
    for (m=1; m<=NumSpecies; m++) ChemC1[m] = c[m];
    for (i=1; i<=NumPipeEquilSpecies; i++)
    {
        m = PipeEquilSpecies[i];
        Yequil[i] = c[m];
    }
    errcode = newton_solve(Yequil, NumPipeEquilSpecies, MAXIT, NUMSIG,
                           getPipeEquil);
    if ( errcode < 0 ) return ERR_NEWTON;
    for (i=1; i<=NumPipeEquilSpecies; i++)
    {
        m = PipeEquilSpecies[i];
        c[m] = Yequil[i];
        ChemC1[m] = c[m];
    }
    return 0;
}


//=============================================================================

int evalTankEquil(double *c)
/*
**  Purpose:
**    computes equilibrium concentrations for water in a tank.
**
**  Input:
**    c[] = array of starting species concentrations
**
**  Output:
**    c[] = array of equilibrium concentrations.
**
**  Returns:
**    an error code or 0 if no error.
*/
{
    int i, m;
    int errcode;
    for (m=1; m<=NumSpecies; m++) ChemC1[m] = c[m];
    for (i=1; i<=NumTankEquilSpecies; i++)
    {
        m = TankEquilSpecies[i];
        Yequil[i] = c[m];
    }
    errcode = newton_solve(Yequil, NumTankEquilSpecies, MAXIT, NUMSIG,
                           getTankEquil);
    if ( errcode < 0 ) return ERR_NEWTON;
    for (i=1; i<=NumTankEquilSpecies; i++)
    {
        m = TankEquilSpecies[i];
        c[m] = Yequil[i];
        ChemC1[m] = c[m];
    }
    return 0;
}

//=============================================================================

void evalPipeFormulas(double *c)
/*
**  Purpose:
**    evaluates species concentrations in a pipe segment that are simple
**    formulas involving other known species concentrations.
**
**  Input:
**    c[] = array of current species concentrations.
**
**  Output:
**    c[] = array of updated concentrations.
**
**  Re-written to accommodate compiled functions (1.1)
*/
{
    int m;
    double x;
    
    for (m=1; m<=NumSpecies; m++) ChemC1[m] = c[m];
// --- use compiled functions if available                                     

    if ( MSX.Compiler )
    {
	    MSXgetPipeFormulas(ChemC1, MSX.K, MSX.Link[TheLink].param, HydVar);
        for (m=1; m<=NumSpecies; m++)
        {
            if (MSX.Species[m].pipeExprType == FORMULA)
                c[m] = MSXerr_validate(ChemC1[m], m, LINK, FORMULA);
        }
    	return;
    }

    for (m=1; m<=NumSpecies; m++)
    {
        if ( MSX.Species[m].pipeExprType == FORMULA )
        {
			x = mathexpr_eval(MSX.Species[m].pipeExpr, getPipeVariableValue);
			c[m] = MSXerr_validate(x, m, LINK, FORMULA);
        }
    }
}

//=============================================================================

void evalTankFormulas(double *c)
/*
**  Purpose:
**    evaluates species concentrations in a tank that are simple
**    formulas involving other known species concentrations.
**
**  Input:
**    c[] = array of current species concentrations.
**
**  Output:
**    c[] = array of updated concentrations.
**
**  Re-written to accommodate compiled functions (1.1)
*/
{
    int m;
    double x;

    for (m=1; m<=NumSpecies; m++) ChemC1[m] = c[m];

// --- use compiled functions if available                                    

    if ( MSX.Compiler )
    {
	    MSXgetTankFormulas(ChemC1, MSX.K, MSX.Link[TheLink].param, HydVar);
        for (m=1; m<=NumSpecies; m++)
        {
            if (MSX.Species[m].tankExprType == FORMULA)
                c[m] = MSXerr_validate(ChemC1[m], m, TANK, FORMULA);
        }
    	return;
    }

    for (m=1; m<=NumSpecies; m++)
    {
        if ( MSX.Species[m].tankExprType == FORMULA )
        {
            x = mathexpr_eval(MSX.Species[m].tankExpr, getTankVariableValue);
			c[m] = MSXerr_validate(x, m, TANK, FORMULA);
        }
    }
}

//=============================================================================

double getPipeVariableValue(int i)
/*
**  Purpose:
**    finds the value of a species, a parameter, or a constant for 
**    the pipe link being analyzed.
**
**  Input:
**    i = variable index.
**
**  Returns:
**    the current value of the indexed variable.
*/
{
	double x;

// --- WQ species have index i between 1 & # of species
//     and their current values are stored in vector ChemC1 

    if ( i <= LastIndex[SPECIES] )
    {
    // --- if species represented by a formula then evaluate it

        if ( MSX.Species[i].pipeExprType == FORMULA )
        {
			x = mathexpr_eval(MSX.Species[i].pipeExpr, getPipeVariableValue);
            return MSXerr_validate(x, i, LINK, FORMULA);                       
        }

    // --- otherwise return the current concentration

        else return ChemC1[i];
    }

// --- intermediate term expressions come next

    else if ( i <= LastIndex[TERM] )
    {
        i -= LastIndex[TERM-1];
		x = mathexpr_eval(MSX.Term[i].expr, getPipeVariableValue);
        return MSXerr_validate(x, i, 0, TERM);                                 
    }

// --- reaction parameter indexes come after that

    else if ( i <= LastIndex[PARAMETER] )
    {
        i -= LastIndex[PARAMETER-1];
        return MSX.Link[TheLink].param[i];
    }

// --- followed by constants

    else if ( i <= LastIndex[CONSTANT] )
    {
        i -= LastIndex[CONSTANT-1];
        return MSX.Const[i].value;
    }

// --- and finally by hydraulic variables
    else 
    {
        i -= LastIndex[CONSTANT];
        if (i < MAX_HYD_VARS) return HydVar[i];
        else return 0.0;
    }
}

//=============================================================================

double getTankVariableValue(int i)
/*
**  Purpose:
**    finds the value of a species, a parameter, or a constant for 
**    the current node being analyzed.
**
**  Input:
**    i = variable index.
**
**  Returns:
**    the current value of the indexed variable.
**
**  Modified to check for NaN values (L.Rossman - 11/03/10).
*/
{
    int j;
	double x;

// --- WQ species have index i between 1 & # of species
//     and their current values are stored in vector ChemC1

    if ( i <= LastIndex[SPECIES] )
    {
    // --- if species represented by a formula then evaluate it

        if ( MSX.Species[i].tankExprType == FORMULA )
        {
			x = mathexpr_eval(MSX.Species[i].tankExpr, getTankVariableValue);
            return MSXerr_validate(x, i, TANK, FORMULA);                       
        }

    // --- otherwise return the current concentration

        else return ChemC1[i];
    }

// --- intermediate term expressions come next

    else if ( i <= LastIndex[TERM] )
    {
        i -= LastIndex[TERM-1];
		x = mathexpr_eval(MSX.Term[i].expr, getTankVariableValue);
        return MSXerr_validate(x, i, 0, TERM);                                 
    }

// --- next come reaction parameters associated with Tank nodes

    else if (i <= LastIndex[PARAMETER] )
    {
        i -= LastIndex[PARAMETER-1];
        j = MSX.Node[TheNode].tank;
        if ( j > 0 )
        {
            return MSX.Tank[j].param[i];
        }
        else return 0.0;
    }

// --- and then come constants

    else if (i <= LastIndex[CONSTANT] )
    {
        i -= LastIndex[CONSTANT-1];
        return MSX.Const[i].value;
    }
    else return 0.0;
}

//=============================================================================

void getPipeDcDt(double t, double y[], int n, double deriv[])
/*
**  Purpose:
**    finds reaction rate (dC/dt) for each reacting species in a pipe.
**
**  Input:
**    t = current time (not used)
**    y[] = vector of reacting species concentrations
**    n = number of reacting species.
**
**  Output:
**    deriv[] = vector of reaction rates of each reacting species.
*/
{
    int i, m;
	double x;

// --- assign species concentrations to their proper positions in the global
//     concentration vector ChemC1

    for (i=1; i<=n; i++)
    {
        m = PipeRateSpecies[i];
        ChemC1[m] = y[i];
    }

// --- update equilibrium species if full coupling in use

    if ( MSX.Coupling == FULL_COUPLING )
    {
        if ( MSXchem_equil(LINK, TheLink, ChemC1) > 0 )     // check for error condition
        {
            for (i=1; i<=n; i++) deriv[i] = 0.0;
            return;
        }
    }

// --- use compiled functions if available                                     

    if ( MSX.Compiler )
    {
	    MSXgetPipeRates(ChemC1, MSX.K, MSX.Link[TheLink].param, HydVar, F);
        for (i=1; i<=n; i++)
        {
            m = PipeRateSpecies[i];
            deriv[i] = MSXerr_validate(F[m], m, LINK, RATE);                   
        }
	    return;
    }

// --- evaluate each pipe reaction expression

    for (i=1; i<=n; i++)
    {
        m = PipeRateSpecies[i];
		x = mathexpr_eval(MSX.Species[m].pipeExpr, getPipeVariableValue);
        deriv[i] = MSXerr_validate(x, m, LINK, RATE);                          
    }
}

//=============================================================================

void getTankDcDt(double t, double y[], int n, double deriv[])
/*
**  Purpose:
**    finds reaction rate (dC/dt) for each reacting species in a tank.
**
**  Input:
**    t = current time (not used)
**    y[] = vector of reacting species concentrations
**    n = number of reacting species.
**
**  Output:
**    deriv[] = vector of reaction rates of each reacting species.
*/
{
    int i, m;
	double x;

// --- assign species concentrations to their proper positions in the global
//     concentration vector ChemC1
    
    for (i=1; i<=n; i++)
    {
        m = TankRateSpecies[i];
        ChemC1[m] = y[i];
    }

// --- update equilibrium species if full coupling in use

    if ( MSX.Coupling == FULL_COUPLING )
    {
        if ( MSXchem_equil(NODE, TheTank, ChemC1) > 0 )     // check for error condition
        {
            for (i=1; i<=n; i++) deriv[i] = 0.0;
            return;
        }
    }

// --- use compiled functions if available                                     

    if ( MSX.Compiler )
    {
	    MSXgetTankRates(ChemC1, MSX.K, MSX.Tank[TheTank].param, HydVar, F);
        for (i=1; i<=n; i++)
        {
            m = TankRateSpecies[i];
            deriv[i] = MSXerr_validate(F[m], m, TANK, RATE);                   
        }
	    return;
    }

// --- evaluate each tank reaction expression

    for (i=1; i<=n; i++)
    {
        m = TankRateSpecies[i];
		x = mathexpr_eval(MSX.Species[m].tankExpr, getTankVariableValue);
        deriv[i] = MSXerr_validate(x, m, TANK, RATE);                          
    }
}

//=============================================================================

void getPipeEquil(double t, double y[], int n, double f[])
/*
**  Purpose:
**    evaluates equilibrium expressions for pipe chemistry.
**
**  Input:
**    t = current time (not used)
**    y[] = vector of equilibrium species concentrations
**    n = number of equilibrium species.
**
**  Output:
**    f[] = vector of equilibrium function values.
*/
{
    int i, m;
	double x;

// --- assign species concentrations to their proper positions in the global
//     concentration vector ChemC1

    for (i=1; i<=n; i++)
    {
        m = PipeEquilSpecies[i];
        ChemC1[m] = y[i];
    }

// --- use compiled functions if available                                     

    if ( MSX.Compiler )
    {
	    MSXgetPipeEquil(ChemC1, MSX.K, MSX.Link[TheLink].param, HydVar, F);
        for (i=1; i<=n; i++)
        {
            m = PipeEquilSpecies[i];
		    f[i] = MSXerr_validate(F[m], m, LINK, EQUIL);                      
        }
    	return;
    }

// --- evaluate each pipe equilibrium expression

    for (i=1; i<=n; i++)
    {
        m = PipeEquilSpecies[i];
		x = mathexpr_eval(MSX.Species[m].pipeExpr, getPipeVariableValue);
		f[i] = MSXerr_validate(x, m, LINK, EQUIL);                             
    }
}

//=============================================================================

void getTankEquil(double t, double y[], int n, double f[])
/*
**  Purpose:
**    evaluates equilibrium expressions for tank chemistry.
**
**  Input:
**    t = current time (not used)
**    y[] = vector of equilibrium species concentrations
**    n = number of equilibrium species
**
**  Output:
**    f[] = vector of equilibrium function values.
*/
{
    int i, m;
    double x;

// --- assign species concentrations to their proper positions in the global
//     concentration vector ChemC1

    for (i=1; i<=n; i++)
    {
        m = TankEquilSpecies[i];
        ChemC1[m] = y[i];
    }

// --- use compiled functions if available                                     

    if ( MSX.Compiler )
    {
	    MSXgetTankEquil(ChemC1, MSX.K, MSX.Tank[TheTank].param, HydVar, F);
        for (i=1; i<=n; i++)
        {
            m = TankEquilSpecies[i];
		    f[i] = MSXerr_validate(F[m], m, TANK, EQUIL);                      
        }
	    return;
    }

// --- evaluate each tank equilibrium expression

    for (i=1; i<=n; i++)
    {
        m = TankEquilSpecies[i];
		x = mathexpr_eval(MSX.Species[m].tankExpr, getTankVariableValue);
		f[i] = MSXerr_validate(x, m, TANK, EQUIL);                             
    }
}

