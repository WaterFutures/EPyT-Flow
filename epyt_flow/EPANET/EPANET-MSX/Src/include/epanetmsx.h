/******************************************************************************
**  MODULE:        EPANETMSX.H
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   C/C++ header file for EPANET Multi-Species Extension Toolkit
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.0 
**  LAST UPDATE:   11/01/10
*******************************************************************************/

#include "epanet2.h"                   // EPANET toolkit header file

#ifndef EPANETMSX_H
#define EPANETMSX_H

#ifndef MSXDLLEXPORT
#ifdef _WIN32
#ifdef epanetmsx_EXPORTS
#define MSXDLLEXPORT __declspec(dllexport) __stdcall
#else
#define MSXDLLEXPORT __declspec(dllimport) __stdcall
#endif
#elif defined(__CYGWIN__)
#define MSXDLLEXPORT __stdcall
#else
#define MSXDLLEXPORT
#endif
#endif

// --- Declare the EPANETMSX toolkit functions
#if defined(__cplusplus)
extern "C" {
#endif

// --- define MSX constants

#define MSX_NODE      0
#define MSX_LINK      1
#define MSX_TANK      2
#define MSX_SPECIES   3
#define MSX_TERM      4
#define MSX_PARAMETER 5
#define MSX_CONSTANT  6
#define MSX_PATTERN   7

#define MSX_BULK      0
#define MSX_WALL      1

#define MSX_NOSOURCE  -1
#define MSX_CONCEN     0
#define MSX_MASS       1
#define MSX_SETPOINT   2
#define MSX_FLOWPACED  3

// --- declare MSX functions

int  MSXDLLEXPORT MSXENopen(const char *inpFile, const char *rptFile,
                 const char *outFile);
int  MSXDLLEXPORT MSXopen(char *fname);
int  MSXDLLEXPORT MSXsolveH(void);
int  MSXDLLEXPORT MSXusehydfile(char *fname);
int  MSXDLLEXPORT MSXsolveQ(void);
int  MSXDLLEXPORT MSXinit(int saveFlag);
int  MSXDLLEXPORT MSXstep(double *t, double *tleft);
int  MSXDLLEXPORT MSXsaveoutfile(char *fname);
int  MSXDLLEXPORT MSXsavemsxfile(char *fname);
int  MSXDLLEXPORT MSXreport(void);
int  MSXDLLEXPORT MSXclose(void);
int  MSXDLLEXPORT MSXENclose(void);

int  MSXDLLEXPORT MSXgetindex(int type, char *id, int *index);
int  MSXDLLEXPORT MSXgetIDlen(int type, int index, int *len);
int  MSXDLLEXPORT MSXgetID(int type, int index, char *id, int len);
int  MSXDLLEXPORT MSXgetcount(int type, int *count);
int  MSXDLLEXPORT MSXgetspecies(int index, int *type, char *units, double *aTol,
               double *rTol);
int  MSXDLLEXPORT MSXgetconstant(int index, double *value);
int  MSXDLLEXPORT MSXgetparameter(int type, int index, int param, double *value);
int  MSXDLLEXPORT MSXgetsource(int node, int species, int *type, double *level,
               int *pat);
int  MSXDLLEXPORT MSXgetpatternlen(int pat, int *len);
int  MSXDLLEXPORT MSXgetpatternvalue(int pat, int period, double *value);
int  MSXDLLEXPORT MSXgetinitqual(int type, int index, int species, double *value);
int  MSXDLLEXPORT MSXgetqual(int type, int index, int species, double *value);
int  MSXDLLEXPORT MSXgeterror(int code, char *msg, int len);

int  MSXDLLEXPORT MSXsetconstant(int index, double value);
int  MSXDLLEXPORT MSXsetparameter(int type, int index, int param, double value);
int  MSXDLLEXPORT MSXsetinitqual(int type, int index, int species, double value);
int  MSXDLLEXPORT MSXsetsource(int node, int species, int type, double level,
               int pat);
int  MSXDLLEXPORT MSXsetpatternvalue(int pat, int period, double value);
int  MSXDLLEXPORT MSXsetpattern(int pat, double mult[], int len);
int  MSXDLLEXPORT MSXaddpattern(char *id);


#if defined(__cplusplus)
  }
#endif

#endif
