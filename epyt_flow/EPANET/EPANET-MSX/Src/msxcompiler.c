/*******************************************************************************
**  MODULE:        MSXCOMPILER.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   compiles chemistry functions to a dynamic library file.
**  COPYRIGHT:     Copyright (C) 2006 Feng Shang, Lewis Rossman, and James Uber.
**                 All Rights Reserved. See license information in LICENSE.TXT.
**  AUTHORS:       L. Rossman, US EPA - NRMRL
**  VERSION:       2.0.00
**  LAST UPDATE:   04/14/2021
*******************************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "msxtypes.h"
#include "msxutils.h"
#include "msxfuncs.h"

// --- define WINDOWS

#undef WINDOWS
#ifdef _WIN32
  #define WINDOWS
#endif
#ifdef __WIN32__
  #define WINDOWS
#endif
#ifdef WIN32
  #define WINDOWS
#endif

//  Local variables
//-----------------
char *Fname;                 // Prefix used for all file names
char TempName[L_tmpnam];
char srcFile[MAXFNAME];      // Name of source code file
char objFile[MAXFNAME];      // Name of object file
char libFile[MAXFNAME];      // Name of library file
int  Compiled;               // Flag for compilation step

//  External variables
//--------------------
extern MSXproject  MSX;       // MSX project data

//  Imported functions
//--------------------
char * MSXchem_getVariableStr(int i, char *s);
//void   MSXrpt_writeLine(char *line);

//  Exported functions
//--------------------
int  MSXcompiler_open(void);
void MSXcompiler_close(void);

//  Local functions
//-----------------
static void  writeSrcFile(FILE* f);

//=============================================================================

int MSXcompiler_open()
/*
**  Purpose:
**    compiles MSX chemistry functions into a dynamic link library
**    and loads the functions into the running application
**
**  Input:
**    none
**
**  Returns:
**    an error code (0 if no error).
*/
{
    char cmd[256];
    char arch[100];
    FILE* f;
    int   err;

// --- initialize

    Fname = NULL;
    Compiled = FALSE;

// --- get the name of a temporary file with directory path stripped from it
//     and replace any '.' characters in it (for the Borland compiler to work)

        Fname = MSXutils_getTempName(TempName) ;

// --- assign names to source code and compiled files

        strcpy(srcFile, Fname);
        strcat(srcFile, ".c");
        strcpy(objFile, Fname);
        strcat(objFile, ".o");
#ifdef WINDOWS
        strcpy(libFile, Fname);
        strcat(libFile, ".dll");
#else
        strcpy(libFile, "lib");
        strcat(libFile, Fname);
        strcat(libFile, ".so");
#endif

// --- write the chemistry functions to the source code file

    f = fopen(srcFile, "wt");
    if ( f == NULL ) return ERR_COMPILE_FAILED;
    writeSrcFile(f);
    fclose(f);

// --- compile the source code file to a dynamic link library file

#ifdef WINDOWS
#ifdef _WIN64
    strcpy(arch, "x64");
#else
    strcpy(arch, "x86");
#endif
        if ( MSX.Compiler == VC )
        {            
            sprintf(cmd, "runvc.bat %s %s", srcFile, arch);
            err = MSXfuncs_run(cmd);
        }

        else if ( MSX.Compiler == GC )
        {
    	    sprintf(cmd, "gcc -c -O3 %s", srcFile);
	        err = MSXfuncs_run(cmd);
	        sprintf(cmd, "gcc -lm -shared -o %s %s", libFile, objFile);
    	    err = MSXfuncs_run(cmd);
        }
        else return ERR_COMPILE_FAILED;
#else
        if ( MSX.Compiler == GC )
        {
            sprintf(cmd, "gcc -c -fPIC -O3 %s", srcFile);
            err = system(cmd);
            sprintf(cmd, "gcc -lm -shared -o %s %s", libFile, objFile);
            err = system(cmd);
        }
        else return ERR_COMPILE_FAILED;
#endif
    Compiled = (err == 0);                                                     // ttaxon - 9/7/10

// --- load the compiled chemistry functions from the library file

	if(Compiled)
	{
		err = MSXfuncs_load(libFile);
	    if ( err == 1 ) return ERR_COMPILE_FAILED;
		if ( err == 2 ) return ERR_COMPILED_LOAD;
	} 
	else 
	{
		MSXcompiler_close();
		return ERR_COMPILE_FAILED;
	}
    return 0;
}

//=============================================================================

void MSXcompiler_close()
/*
**  Purpose:
**    frees resources used to load chemistry functions from the shared
**    library and deletes all files used to compile and link the library.
**
**  Input:
**    none
**
**  Returns:
**    none.
*/
{
    char cmd[256];
    if ( Compiled ) MSXfuncs_free();
    if ( Fname )
    {
#ifdef WINDOWS
        // --- delete all files created from compilation
        //     (VC++ creates more than just an obj and dll file)
        sprintf(cmd, "cmd /c del %s.*", Fname);
        MSXfuncs_run(cmd);
#else
        remove(TempName);
        remove(srcFile);
        remove(objFile);
        remove(libFile);
#endif
    }
}
//=============================================================================

void  writeSrcFile(FILE* f)
/*
**  Purpose:
**    writes C statements to the chemistry function source code file
**
**  Input:
**    f = pointer to the source code file
**
**  Returns:
**    none.
**
**  Note: this function uses mathexpr_getStr() from mathexpr.c to
**        reconstruct math expressions that were previously parsed
**        into a stack of atomic terms by mathexpr_create(). The
**        mathexpr_getStr function calls MSXchem_getVariableStr (in 
**        msxchem.c) to return a symbol for a particular variable that
**        is used in the reconstucted expression in place of the
**        variable's original name. For example, if NH3 were the name
**        of the 2nd chemical species, then in the source code written
**        here it would be denoted as c[2]; the third hydraulic variable,
**        Velocity, would appear as h[3]. Similar notation is used for
**        constants (k[]) and parameters (p[]).
*/
{
    int i;
    char e[1024];
    char headers[] =

" /*  Machine Generated EPANET-MSX File - Do Not Edit */ \n\n"
" #include <math.h> \n"
" \n"
" #undef WINDOWS \n"
" #ifdef _WIN32 \n"
"   #define WINDOWS \n"
" #endif \n"
" #ifdef __WIN32__ \n"
"   #define WINDOWS \n"
" #endif \n"
" #ifdef WIN32 \n"
"   #define WINDOWS \n"
" #endif \n"
" \n"
" #ifdef WINDOWS \n"
"   #define DLLEXPORT __declspec(dllexport) \n"
" #else \n"
"   #define DLLEXPORT \n"
" #endif \n"
"  \n"
" void  DLLEXPORT  MSXgetPipeRates(double *, double *, double *, double *, double *); \n"
" void  DLLEXPORT  MSXgetTankRates(double *, double *, double *, double *, double *); \n"
" void  DLLEXPORT  MSXgetPipeEquil(double *, double *, double *, double *, double *); \n"
" void  DLLEXPORT  MSXgetTankEquil(double *, double *, double *, double *, double *); \n"
" void  DLLEXPORT  MSXgetPipeFormulas(double *, double *, double *, double *); \n"
" void  DLLEXPORT  MSXgetTankFormulas(double *, double *, double *, double *); \n"
" double term(int, double *, double *, double *, double *); \n";

    char mathFuncs[] = 

    " double coth(double); \n"
    " double cot(double); \n"
    " double acot(double); \n"
    " double step(double); \n"
    " double sgn(double); \n"
    " \n"
    " double coth(double x) { \n"
    "   return (exp(x) + exp(-x)) / (exp(x) - exp(-x)); } \n"
    " double cot(double x) { \n"
    "   return 1.0 / tan(x); } \n"
    " double acot(double x) { \n"
    "   return 1.57079632679489661923 - atan(x); } \n"
    " double step(double x) { \n"
    "   if (x <= 0.0) return 0.0; \n"
    "   return 1.0; } \n"
    " double sgn(double x) { \n"
    "   if (x < 0.0) return -1.0; \n"
    "   if (x > 0.0) return 1.0; \n"
    "   return 0.0; } \n";


// --- write headers & non-intrinsic math functions to file

    fprintf(f, "%s", headers);
    fprintf(f, "%s", mathFuncs);

// --- write term functions

    fprintf(f,
"\n double term(int i, double c[], double k[], double p[], double h[])\n { \n");
    if ( MSX.Nobjects[TERM] > 0 )
    {
       fprintf(f, "     switch(i) { \n");
        for (i=1; i<=MSX.Nobjects[TERM]; i++)
        {
            fprintf(f, "     case %d: return %s; \n",
            i, mathexpr_getStr(MSX.Term[i].expr, e, MSXchem_getVariableStr));
        }
        fprintf(f, "     } \n");
    }
    fprintf(f, "     return 0.0; \n }\n");

// --- write pipe rate functions

    fprintf(f,
"\n void DLLEXPORT MSXgetPipeRates(double c[], double k[], double p[], double h[], double f[])\n { \n");
    for (i=1; i<=MSX.Nobjects[SPECIES]; i++)
    {
        if ( MSX.Species[i].pipeExprType == RATE )
            fprintf(f, "     f[%d] = %s; \n", i, mathexpr_getStr(MSX.Species[i].pipeExpr, e,
                MSXchem_getVariableStr));
    }
    fprintf(f, " }\n");
    
// --- write tank rate functions

    fprintf(f,
"\n void DLLEXPORT MSXgetTankRates(double c[], double k[], double p[], double h[], double f[])\n { \n");
    for (i=1; i<=MSX.Nobjects[SPECIES]; i++)
    {
        if ( MSX.Species[i].tankExprType == RATE )
            fprintf(f, "     f[%d] = %s; \n", i, mathexpr_getStr(MSX.Species[i].tankExpr, e,
                MSXchem_getVariableStr));
    }
    fprintf(f, " }\n");

// --- write pipe equilibrium functions

    fprintf(f,
"\n void DLLEXPORT MSXgetPipeEquil(double c[], double k[], double p[], double h[], double f[])\n { \n");
    for (i=1; i<=MSX.Nobjects[SPECIES]; i++)
    {
        if ( MSX.Species[i].pipeExprType == EQUIL )
            fprintf(f, "     f[%d] = %s; \n", i, mathexpr_getStr(MSX.Species[i].pipeExpr, e,
                MSXchem_getVariableStr));
    }
    fprintf(f, " }\n");
    
// --- write tank equilibrium functions

    fprintf(f,
"\n void DLLEXPORT MSXgetTankEquil(double c[], double k[], double p[], double h[], double f[])\n { \n");
    for (i=1; i<=MSX.Nobjects[SPECIES]; i++)
    {
        if ( MSX.Species[i].tankExprType == EQUIL )
            fprintf(f, "     f[%d] = %s; \n", i, mathexpr_getStr(MSX.Species[i].tankExpr, e,
                MSXchem_getVariableStr));
    }
    fprintf(f, " }\n");

// --- write pipe formula functions

    fprintf(f,
"\n void DLLEXPORT MSXgetPipeFormulas(double c[], double k[],  double p[], double h[])\n { \n");
    for (i=1; i<=MSX.Nobjects[SPECIES]; i++)
    {
        if ( MSX.Species[i].pipeExprType == FORMULA )
            fprintf(f, "     c[%d] = %s; \n", i, mathexpr_getStr(MSX.Species[i].pipeExpr, e,
                MSXchem_getVariableStr));
    }
    fprintf(f, " }\n");
    
// --- write tank formula functions

    fprintf(f,
"\n void DLLEXPORT MSXgetTankFormulas(double c[], double k[], double p[], double h[])\n { \n");
    for (i=1; i<=MSX.Nobjects[SPECIES]; i++)
    {
        if ( MSX.Species[i].tankExprType == FORMULA )
            fprintf(f, "     c[%d] = %s; \n", i, mathexpr_getStr(MSX.Species[i].tankExpr, e,
                MSXchem_getVariableStr));
    }
    fprintf(f, " }\n");
    fprintf(f, "\n");
}
