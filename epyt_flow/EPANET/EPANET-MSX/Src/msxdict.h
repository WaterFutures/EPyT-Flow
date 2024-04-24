/************************************************************************
**  MODULE:        MSXDICT.H
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   Dictionary of key words used by the
**                 EPANET Multi-Species Extension toolkit.
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.00                                               
**  LAST UPDATE:   09/29/08
***********************************************************************/

#ifndef MSXDICT_H
#define MSXDICT_H


// NOTE: the entries in MsxsectWords must match the entries in the enumeration
//       variable SectionType defined in msxtypes.h.
static char *MsxSectWords[] = {"[TITLE", "[SPECIE",  "[COEFF",  "[TERM",
                               "[PIPE",  "[TANK",    "[SOURCE", "[QUALITY",
                               "[PARAM", "[PATTERN", "[OPTION", 
                               "[REPORT", "[DIFFU", NULL};
static char *ReportWords[]  = {"NODE", "LINK", "SPECIE", "FILE", "PAGESIZE", NULL};
static char *OptionTypeWords[] = {"AREA_UNITS", "RATE_UNITS", "SOLVER", "COUPLING",
                                  "TIMESTEP", "RTOL", "ATOL", "COMPILER", "SEGMENTS","PECLET",NULL};  
static char *CompilerWords[]   = {"NONE", "VC", "GC", NULL};                      
static char *SourceTypeWords[] = {"CONC", "MASS", "SETPOINT", "FLOW", NULL};      
static char *MixingTypeWords[] = {"MIXED", "2COMP", "FIFO", "LIFO", NULL};
static char *MassUnitsWords[]  = {"MG", "UG", "MOLE", "MMOL", NULL};
static char *AreaUnitsWords[]  = {"FT2", "M2", "CM2", NULL};
static char *TimeUnitsWords[]  = {"SEC", "MIN", "HR", "DAY", NULL};
static char *SolverTypeWords[] = {"EUL", "RK5", "ROS2", NULL};
static char *CouplingWords[]   = {"NONE", "FULL", NULL};
static char *ExprTypeWords[]   = {"", "RATE", "FORMULA", "EQUIL", NULL};
static char *HydVarWords[]     = {"", "D", "Q", "U", "Re",
                                  "Us", "Ff", "Av", "Kc", "Len", NULL};	/*Len added Feng Shang 01/27/2023*/
static char YES[]  = "YES";
static char NO[]   = "NO";
static char ALL[]  = "ALL";
static char NONE[] = "NONE";

#endif