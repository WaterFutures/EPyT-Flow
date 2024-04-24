/*******************************************************************************
**  MODULE:        MSXTOOLKIT.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   Contains the exportable set of functions that comprise the
**                 EPANET Multi-Species Extension toolkit.
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.00
**  LAST UPDATE:   04/14/2021
**
**  These functions can be used in conjunction with the original EPANET
**  toolkit functions to model water quality fate and transport of
**  multiple interacting chemcial species within piping networks. See the
**  MSXMAIN.C module for an example of how these functions were used to
**  extend the original command line version of EPANET to include multiple
**  chemical species. Consult the EPANET and EPANET-MSX Users Manuals for
**  detailed descriptions of the input data file formats required by both
**  the original EPANET and its multi-species extension.
*******************************************************************************/

#include <stdio.h>
#include <string.h>
#include <float.h>
#include <stdlib.h>

#include "msxtypes.h"
#include "msxutils.h"                                                          
#include "epanet2.h"
#include "epanetmsx.h"

//  External variables
//--------------------
extern MSXproject  MSX;                // MSX project data

//  Imported functions
//--------------------
int    MSXproj_open(char *fname);
int    MSXproj_close(void);
int    MSXproj_addObject(int type, char *id, int n);
int    MSXproj_findObject(int type, char *id);
char * MSXproj_findID(int type, char *id);
char * MSXproj_getErrmsg(int errcode);
int    MSXqual_open(void);
int    MSXqual_init(void);
int    MSXqual_step(double *t, double *tleft);
int    MSXqual_close(void);
double MSXqual_getNodeQual(int j, int m);
double MSXqual_getLinkQual(int k, int m);
int    MSXrpt_write(void);
int    MSXfile_save(FILE *f);

//=============================================================================

int MSXDLLEXPORT   MSXENopen(const char *inpFile, const char *rptFile, const char *outFile)
/*
**  Purpose:
**    pass-thru to open the EPANET toolkit system
**
**  Input:
**    inpFile = name of the EPANET input file
**    rptFile = name of the EPANET report file
**    outFile = name of the EPANET binary file
**
**  Returns:
**    an error code (or 0 for no error);
*/
{
    int err = 0;
    err = ENopen(inpFile, rptFile, outFile);
    return err;
}

int MSXDLLEXPORT   MSXENclose(void)
/*
**  Purpose:
**    pass-thru to open the EPANET toolkit system
**
*/
{
    int err = 0;
    err = ENclose();
    return err;
}


int  MSXDLLEXPORT  MSXopen(char *fname)
/*
**  Purpose:
**    opens the EPANET-MSX toolkit system.
**
**  Input:
**    fname = name of an MSX input file.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    int err = 0;
    if (MSX.ProjectOpened) return(ERR_MSX_OPENED);
    CALL(err, MSXproj_open(fname));
    CALL(err, MSXqual_open());

    if ( err )
    {
        ENwriteline(MSXproj_getErrmsg(err));
        ENwriteline("");
    }

    return err;
}

//=============================================================================

int   MSXDLLEXPORT  MSXsolveH()
/*
**  Purpose:
**    solves for system hydraulics which are written to a temporary file.
**
**  Input:
**    none.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    int err = 0;

// --- check that an MSX project was opened

    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;

// --- close & remove any existing hydraulics file

    if ( MSX.HydFile.file )
    {
        fclose(MSX.HydFile.file);
        MSX.HydFile.file = NULL;
    }
    if ( MSX.HydFile.mode == SCRATCH_FILE ) remove(MSX.HydFile.name);

// --- create a temporary hydraulics file

    MSXutils_getTempName(MSX.HydFile.name);                                    
    MSX.HydFile.mode = SCRATCH_FILE;                                           //(LR-10/05/08)

// --- use EPANET to solve for & save hydraulics results

    CALL(err, ENsolveH());
    CALL(err, ENsavehydfile(MSX.HydFile.name));
    CALL(err, MSXusehydfile(MSX.HydFile.name));
    return err;
}

//=============================================================================

int   MSXDLLEXPORT  MSXusehydfile(char *fname)
/*
**  Purpose:
**    registers a hydraulics solution file with the MSX system.
**
**  Input:
**    fname = name of binary hydraulics results file.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    INT4 magic;
    INT4 version;
    INT4 n;

// --- check that an MSX project was opened

    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;

// --- close any existing hydraulics file 

    if ( MSX.HydFile.file )
    {
        fclose(MSX.HydFile.file);
        if ( MSX.HydFile.mode == SCRATCH_FILE ) remove(MSX.HydFile.name);      //(LR-10/05/08)   
    } 
	

// --- open hydraulics file

    //MSX.HydFile.mode = USED_FILE;                                            
    MSX.HydFile.file = fopen(fname, "rb");
    if (!MSX.HydFile.file) return ERR_OPEN_HYD_FILE;

// --- check that file is really a hydraulics file for current project

    fread(&magic, sizeof(INT4), 1, MSX.HydFile.file);
    if ( magic != MAGICNUMBER ) return ERR_READ_HYD_FILE;
    fread(&version, sizeof(INT4), 1, MSX.HydFile.file);
    fread(&n, sizeof(INT4), 1, MSX.HydFile.file);
    if ( n != MSX.Nobjects[NODE] ) return ERR_READ_HYD_FILE;
    fread(&n, sizeof(INT4), 1, MSX.HydFile.file);
    if ( n != MSX.Nobjects[LINK] ) return ERR_READ_HYD_FILE;
    fseek(MSX.HydFile.file, 3*sizeof(INT4), SEEK_CUR);

// --- read length of simulation period covered by file

    fread(&n, sizeof(INT4), 1, MSX.HydFile.file);
    MSX.Dur = 1000 * n;
    MSX.HydOffset = ftell(MSX.HydFile.file);
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXsolveQ()
/*
**  Purpose:
**    runs a MSX water quality analysis over the entire simulation period.
**
**  Input:
**    none.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    double t, tleft = 0;
    int err = 0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    CALL(err, MSXinit(1));
    do CALL(err, MSXstep(&t, &tleft));
    while (tleft > 0 && err == 0);
    return err;
}

//=============================================================================

int  MSXDLLEXPORT  MSXinit(int saveFlag)
/*
**  Purpose:
**    initializes a MSX water quality analysis.
**
**  Input:
**    saveFlag = 1 if results saved to binary file, 0 if not.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    int err= 0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    MSX.Saveflag = saveFlag;
    err = MSXqual_init();
    return err;
}

//=============================================================================

int  MSXDLLEXPORT  MSXstep(double *t, double *tleft)
/*
**  Purpose:
**    advances the WQ simulation over a single time step.
**
**  Input:
**    none
**
**  Output:
**    *t = current simulation time at the end of the step (sec)
**    *tleft = time left in the simulation (sec)
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    return MSXqual_step(t, tleft);
}

//=============================================================================

int  MSXDLLEXPORT  MSXsaveoutfile(char *fname)
/*
**  Purpose:
**    saves all results of the WQ simulation to a binary file.
**
**  Input:
**    fname = name of the binary results file.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    FILE *f;
    int   c;

    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( !MSX.OutFile.file ) return ERR_OPEN_OUT_FILE;
    if ( (f = fopen(fname,"w+b") ) == NULL) return ERR_OPEN_OUT_FILE;
    fseek(MSX.OutFile.file, 0, SEEK_SET);
    while ( (c = fgetc(MSX.OutFile.file)) != EOF) fputc(c, f);
    fclose(f);
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXreport()
/*
**  Purpose:
**    writes requested WQ simulation results to a text file.
**
**  Input:
**    none
**
**  Returns:
**    an error code (or 0 for no error).
**
**  Notes:
**    Results are written to the EPANET report file unless a specific
**    water quality report file is named in the [REPORT] section of
**    the MSX input file.
*/
{
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( MSX.Rptflag ) return MSXrpt_write();
    else return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXclose()
/*
**  Purpose:
**    closes the EPANET-MSX toolkit system.
**
**  Input:
**    none
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    MSXqual_close();
    MSXproj_close();
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXgetindex(int type, char *id, int *index)
/*
**  Purpose:
**    retrieves the index of a named MSX object.
**
**  Input:
**    type = object type code
**    id = name of water quality species.
**
**  Output:
**    index = index (base 1) in the list of all objects of the given type.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    int i;
    *index = 0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    switch(type)
    {
        case MSX_SPECIES:   i = MSXproj_findObject(SPECIES, id);   break;
        case MSX_CONSTANT:  i = MSXproj_findObject(CONSTANT, id);  break;
        case MSX_PARAMETER: i = MSXproj_findObject(PARAMETER, id); break;
        case MSX_PATTERN:   i = MSXproj_findObject(PATTERN, id);   break;
        default:            return ERR_INVALID_OBJECT_TYPE;
    }
    if ( i < 1 ) return ERR_UNDEFINED_OBJECT_ID;
    *index = i;
    return 0;
}
//=============================================================================

int  MSXDLLEXPORT  MSXgetIDlen(int type, int index, int *len)
/*
**  Purpose:
**    retrieves the number of characters in the ID name of an MSX object.
**
**  Input:
**    type =  object type code
**    index = index (base 1) of the object in list of all objects of the
**            given type.
**
**  Output:
**    len = number of characters in the object's ID name.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    int i;
    *len = 0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    switch(type)
    {
        case MSX_SPECIES:   i = SPECIES;   break;
        case MSX_CONSTANT:  i = CONSTANT;  break;
        case MSX_PARAMETER: i = PARAMETER; break;
        case MSX_PATTERN:   i = PATTERN;   break;
        default:            return ERR_INVALID_OBJECT_TYPE;
    }
    if ( index < 1 || index > MSX.Nobjects[i] ) return ERR_INVALID_OBJECT_INDEX;
    switch(i)
    {
        case SPECIES:   *len = (int) strlen(MSX.Species[index].id); break;
        case CONSTANT:  *len = (int) strlen(MSX.Const[index].id);   break;
        case PARAMETER: *len = (int) strlen(MSX.Param[index].id);   break;
        case PATTERN:   *len = (int) strlen(MSX.Pattern[index].id); break;
    }
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXgetID(int type, int index, char *id, int len)
/*
**  Purpose:
**    retrieves the name of an object given its index.
**
**  Input:
**    type  = object type code
**    index = index (base 1) of the object in list of all objects of the
**            given type
**    len   = maximum number of characters that id can hold.
**
**  Output:
**    id = name of the object.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    int i;
    strcpy(id, "");
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    switch(type)
    {
        case MSX_SPECIES:   i = SPECIES;   break;
        case MSX_CONSTANT:  i = CONSTANT;  break;
        case MSX_PARAMETER: i = PARAMETER; break;
        case MSX_PATTERN:   i = PATTERN;   break;
        default:            return ERR_INVALID_OBJECT_TYPE;
    }
    if ( index < 1 || index > MSX.Nobjects[i] ) return ERR_INVALID_OBJECT_INDEX;
    switch(i)
    {
        case SPECIES:   strncpy(id, MSX.Species[index].id, len);  break;
        case CONSTANT:  strncpy(id, MSX.Const[index].id, len);   break;
        case PARAMETER: strncpy(id, MSX.Param[index].id, len);   break;
        case PATTERN:   strncpy(id, MSX.Pattern[index].id, len); break;
    }
	id[len] = '\0';                                                            //(L. Rossman - 11/01/10)
    return 0;
}

//=============================================================================

int MSXDLLEXPORT  MSXgetcount(int type, int *count)
/*
**  Purpose:
**    retrieves the number of objects of a specific type.
**
**  Input:
**    type =  object type code
**
**  Output:
**    count = number of objects of the given type.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    *count = 0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    switch(type)
    {
        case MSX_SPECIES:   *count = MSX.Nobjects[SPECIES];   break;
        case MSX_CONSTANT:  *count = MSX.Nobjects[CONSTANT];  break;
        case MSX_PARAMETER: *count = MSX.Nobjects[PARAMETER]; break;
        case MSX_PATTERN:   *count = MSX.Nobjects[PATTERN];   break;
        default:            return ERR_INVALID_OBJECT_TYPE;
    }
    return 0;
}

//=============================================================================

int MSXDLLEXPORT  MSXgetspecies(int index, int *type, char *units,
                             double *aTol, double * rTol)
/*
**  Purpose:
**    retrieves the attributes of a chemical species.
**
**  Input:
**    index = index (base 1) of the species in the list of all species.
**
**  Output:
**    type = MSX_BULK (0) for a bulk flow species or MSX_WALL (1) for a
**           surface species;
**    units = character string containing the mass units defined for the species -
**            must be sized in the calling program to accept up to 15 bytes
**            plus a null termination character
**    aTol = absolute concentration tolerance (concentration units);
**    rTol = relative concentration tolerance (unitless)
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    *type  = 0;
    strcpy(units, "");
    *aTol  = 0.0;
    *rTol  = 0.0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( index < 1 || index > MSX.Nobjects[SPECIES] ) return ERR_INVALID_OBJECT_INDEX;
    *type  = MSX.Species[index].type;
    strncpy(units, MSX.Species[index].units, MAXUNITS);
    *aTol  = MSX.Species[index].aTol;
    *rTol  = MSX.Species[index].rTol;
    return 0;
}

//=============================================================================

int MSXDLLEXPORT  MSXgetconstant(int index, double *value)
/*
**  Purpose:
**    retrieves the value of a particular reaction constant.
**
**  Input:
**    index = index (base 1) of the constant in the list of all constants.
**
**  Output:
**    value = value assigned to the constant.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    *value = 0.0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( index < 1 || index > MSX.Nobjects[CONSTANT] ) return ERR_INVALID_OBJECT_INDEX;
    *value = MSX.Const[index].value;
    return 0;
}

//=============================================================================

int MSXDLLEXPORT MSXgetparameter(int type, int index, int param, double *value)
/*
**  Purpose:
**    retrieves the value of a particular reaction parameter for a given pipe
**    or tank within the pipe network.
**
**  Input:
**    type = MSX_NODE (0) for a node or MSX_LINK (1) for a link;
**    index = index (base 1) assigned to the node or link;
**    param = index (base 1) assigned to the reaction parameter.
**
**  Output:
**    value = value assigned to the parameter.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    int j;
    *value = 0.0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( param < 1 || param > MSX.Nobjects[PARAMETER] ) return ERR_INVALID_OBJECT_INDEX;
    if ( type == MSX_NODE )
    {
        if ( index < 1 || index > MSX.Nobjects[NODE] ) return ERR_INVALID_OBJECT_INDEX;
        j = MSX.Node[index].tank;
        if ( j > 0 ) *value = MSX.Tank[j].param[param];
    }
    else if ( type == MSX_LINK )
    {
        if ( index < 1 || index > MSX.Nobjects[LINK] ) return ERR_INVALID_OBJECT_INDEX;
        *value = MSX.Link[index].param[param];
    }
    else return ERR_INVALID_OBJECT_TYPE;
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT MSXgetsource(int node, int species, int *type, double *level,
                            int *pat)
/*
**  Purpose:
**    retrieves information on any external source of a particular chemical
**    species assigned to a specific node of the pipe network.
**
**  Input:
**    node = index number (base 1) assigned to the node of interest;
**    species = index number (base 1) of the species of interest;
**
**  Output:
**    type = one of the following of external source type codes:
**           MSX_NOSOURCE  = -1 for no source,
**           MSX_CONCEN    =  0 for a concentration source,
**           MSX_MASS      =  1 for a mass booster source,
**           MSX_SETPOINT  =	2 for a setpoint source,
**           MSX_FLOWPACED =	3 for a flow paced source;
**    level = the baseline concentration (or mass flow rate) of the species
**            in the source;
**    pat = the index of the time pattern assigned to the species at the source
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    Psource source;
    *type  = MSX_NOSOURCE;
    *level = 0.0;
    *pat   = 0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( node < 1 || node > MSX.Nobjects[NODE] ) return ERR_INVALID_OBJECT_INDEX;
    if ( species < 1 || species > MSX.Nobjects[SPECIES] ) return ERR_INVALID_OBJECT_INDEX;
    source = MSX.Node[node].sources;
    while ( source )
    {
        if ( source->species == species )
        {
            *type  = source->type;
            *level = source->c0;
            *pat   = source->pat;
            break;
        }
        source = source->next;
    }
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXgetpatternlen(int pat, int *len)
/*
**  Purpose:
**    retrieves the number of time periods within a source time pattern.
**
**  Input:
**    pat = the index number (base 1) of the time pattern;
**
**  Output:
**    len = the number of time periods that appear in the pattern.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    *len = 0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( pat < 1 || pat > MSX.Nobjects[PATTERN] ) return ERR_INVALID_OBJECT_INDEX;
    *len = MSX.Pattern[pat].length;
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXgetpatternvalue(int pat, int period, double *value)
/*
**  Purpose:
**    retrieves the multiplier at a specific time period for a given
**    source time pattern.
**
**  Input:
**    pat = the index number (base 1) of the time pattern;
**    period = the index of the time period (starting from 1) whose
**             multiplier is being sought;
**
**  Output:
**    value = the value of the pattern's multiplier in the desired period.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    int n = 1;
    *value = 0.0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( pat < 1 || pat > MSX.Nobjects[PATTERN] ) return ERR_INVALID_OBJECT_INDEX;
    if ( period <= MSX.Pattern[pat].length )
    {
        MSX.Pattern[pat].current = MSX.Pattern[pat].first;
        while ( MSX.Pattern[pat].current )
        {
            if ( n == period )
            {
                *value = MSX.Pattern[pat].current->value;
                return 0;
            }
            MSX.Pattern[pat].current = MSX.Pattern[pat].current->next;
            n++;
        }
    }
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXgetinitqual(int type, int index, int species, double *value)
/*
**  Purpose:
**    retrieves the initial concentration of a particular chemical species
**    assigned to a specific node or link of the pipe network.
**
**  Input:
**    type = MSX_NODE (0) for a node or MSX_LINK (1) for a link;
**    index = index (base 1) of the node or link of interest;
**    species = index (base 1) of the species of interest.
**
**  Output:
**    value = initial concentration of the species at the node or link.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    *value = 0.0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( species < 1 || species > MSX.Nobjects[SPECIES] ) return ERR_INVALID_OBJECT_INDEX;
    if ( type == MSX_NODE )
    {
        if ( index < 1 || index > MSX.Nobjects[NODE] ) return ERR_INVALID_OBJECT_INDEX;
        *value = MSX.Node[index].c0[species];
    }
    else if ( type == MSX_LINK )
    {
        if ( index < 1 || index > MSX.Nobjects[LINK] ) return ERR_INVALID_OBJECT_INDEX;
        *value = MSX.Link[index].c0[species];
    }
    else return ERR_INVALID_OBJECT_TYPE;
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXgetqual(int type, int index, int species, double *value)
/*
**  Purpose:
**    retrieves the current concentration of a species at a particular node
**    or link of the pipe network.
**
**  Input:
**    type = MSX_NODE (0) for a node or MSX_LINK (1) for a link;
**    index = index (base 1) of the node or link of interest;.
**    species = index (base 1) of the species of interest.
**
**  Output:
**    value = species concentration at the node or link.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    *value = 0.0;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( species < 1 || species > MSX.Nobjects[SPECIES] ) return ERR_INVALID_OBJECT_INDEX;
    if ( type == MSX_NODE )
    {
        if ( index < 1 || index > MSX.Nobjects[NODE] ) return ERR_INVALID_OBJECT_INDEX;
        *value = MSXqual_getNodeQual(index, species);
    }
    else if ( type == MSX_LINK )
    {
        if ( index < 1 || index > MSX.Nobjects[LINK] ) return ERR_INVALID_OBJECT_INDEX;
        *value = MSXqual_getLinkQual(index, species);
    }
    else return ERR_INVALID_OBJECT_TYPE;
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXgeterror(int code, char *msg, int len)
/*
**  Purpose:
**    retrieves text of an error message.
**
**  Input:
**    code = error code number
**    len = maximum length of string errmsg.
**
**  Output:
**    msg  = text of error message.
**
**  Returns:
**    an error code which is always 0.
*/
{
    strncpy(msg, MSXproj_getErrmsg(code), len);
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXsetconstant(int index, double value)
/*
**  Purpose:
**    assigns a new value to a specific reaction constant.
**
**  Input:
**    index = index (base 1) of the constant in the list of all constants;
**    value = the new value to be assigned to the constant.
**
**  Output:
**    none.
**
**  Returns:
**    an error code or 0 for no error.
*/
{
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( index < 1 || index > MSX.Nobjects[CONSTANT] ) return ERR_INVALID_OBJECT_INDEX;
    MSX.Const[index].value = value;
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXsetparameter(int type, int index, int param, double value)
/*
**  Purpose:
**    assigns a value to a particular reaction parameter for a given pipe
**    or tank within the pipe network.
**
**  Input:
**    type = MSX_NODE (0) for a node or MSX_LINK (1) for a link;
**    index = index (base 1) assigned to the node or link;
**    param = index (base 1) assigned to the reaction parameter;
**    value = value to be assigned to the parameter.
**
**  Output:
**    none.
**
**  Returns:
**    an error code or 0 for no error.
*/
{
    int j;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( param < 1 || param > MSX.Nobjects[PARAMETER] ) return ERR_INVALID_OBJECT_INDEX;
    if ( type == MSX_NODE )
    {
        if ( index < 1 || index > MSX.Nobjects[NODE] ) return ERR_INVALID_OBJECT_INDEX;
        j = MSX.Node[index].tank;
        if ( j > 0 ) MSX.Tank[j].param[param] = value;
    }
    else if ( type == MSX_LINK )
    {
        if ( index < 1 || index > MSX.Nobjects[LINK] ) return ERR_INVALID_OBJECT_INDEX;
        MSX.Link[index].param[param] = value;
    }
    else return ERR_INVALID_OBJECT_TYPE;
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXsetinitqual(int type, int index, int species, double value)
/*
**  Purpose:
**    assigns an initial concentration of a particular chemical species
**    to a specific node or link of the pipe network.
**
**  Input:
**    type = MSX_NODE (0) for a node or MSX_LINK (1) for a link;
**    index = index (base 1) of the node or link of interest;
**    species = index (base 1) of the species of interest.
**    value = initial concentration of the species at the node or link.
**
**  Output:
**    none.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( species < 1 || species > MSX.Nobjects[SPECIES] ) return ERR_INVALID_OBJECT_INDEX;
    if ( type == MSX_NODE )
    {
        if ( index < 1 || index > MSX.Nobjects[NODE] ) return ERR_INVALID_OBJECT_INDEX;
        if ( MSX.Species[species].type == BULK )
            MSX.Node[index].c0[species] = value;
    }
    else if ( type == MSX_LINK )
    {
        if ( index < 1 || index > MSX.Nobjects[LINK] ) return ERR_INVALID_OBJECT_INDEX;
        MSX.Link[index].c0[species] = value;
    }
    else return ERR_INVALID_OBJECT_TYPE;
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXsetsource(int node, int species, int type, double level,
                             int pat)
/*
**  Purpose:
**    sets the attributes of an external source of a particular chemical
**    species to a specific node of the pipe network.
**
**  Input:
**    node = index number (base 1) assigned to the node of interest;
**    species = index number (base 1) of the species of interest;
**    type = one of the following of external source type codes:
**           MSX_NOSOURCE  = -1 for no source,
**           MSX_CONCEN    =  0 for a concentration source,
**           MSX_MASS      =  1 for a mass booster source,
**           MSX_SETPOINT  =	2 for a setpoint source,
**           MSX_FLOWPACED =	3 for a flow paced source;
**    level = the baseline concentration (or mass flow rate) of the species
**            in the source;
**    pat = the index of the time pattern assigned to the species at the source
**
**  Output:
**    none.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    Psource source;

// --- check for valid source parameters

    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( node < 1 || node > MSX.Nobjects[NODE] ) return ERR_INVALID_OBJECT_INDEX;
    if ( species < 1 || species > MSX.Nobjects[SPECIES] ) return ERR_INVALID_OBJECT_INDEX;
    if ( pat > MSX.Nobjects[PATTERN] ) return ERR_INVALID_OBJECT_INDEX;
    if ( pat < 0 ) pat = 0;
    if ( type < MSX_NOSOURCE ||
         type > MSX_FLOWPACED ) return ERR_INVALID_OBJECT_PARAMS;
    if ( MSX.Species[species].type != BULK ) return ERR_INVALID_OBJECT_PARAMS;
    if ( level < 0.0 ) return ERR_INVALID_OBJECT_PARAMS;

// --- check if a source for this species already exists at the node

    source = MSX.Node[node].sources;
    while ( source )
    {
        if ( source->species == species ) break;
        source = source->next;
    }

// --- if no current source exists then create a new one

    if ( source == NULL )
    {
        source = (struct Ssource *) malloc(sizeof(struct Ssource));
        if ( source == NULL ) return ERR_MEMORY;
        source->next = MSX.Node[node].sources;
        MSX.Node[node].sources = source;
    }

// --- assign parameters to the source

    source->type   = (char)type;
    source->species = species;
    source->c0     = level;
    source->pat    = pat;
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXsetpatternvalue(int pat, int period, double value)
/*
**  Purpose:
**    assigns a new value to the multiplier for a specific time period in
**    a given time pattern.
**
**  Input:
**    pat = the index number (base 1) of the time pattern;
**    period = the time period (starting from 1) whose multiplier is
**             being replaced;
**    value = the new value of the pattern's multiplier in the desired period.
**
**  Output:
**    none.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    int n = 1;

// --- check that pattern & period exists

    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( pat < 1 || pat > MSX.Nobjects[PATTERN] ) return ERR_INVALID_OBJECT_INDEX;
    if ( period <= 0 || period > MSX.Pattern[pat].length )
        return ERR_INVALID_OBJECT_PARAMS;

// --- find desired time period in the pattern

    MSX.Pattern[pat].current = MSX.Pattern[pat].first;
    while ( MSX.Pattern[pat].current )
    {
        if ( n == period )
        {
            MSX.Pattern[pat].current->value = value;
            return 0;
        }
        MSX.Pattern[pat].current = MSX.Pattern[pat].current->next;
        n++;
    }
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXaddpattern(char *id)
/*
**  Purpose:
**    adds a new MSX time pattern to the project.
**
**  Input:
**    id = C-style character string with the ID name of the new pattern.
**
**  Output:
**    none.
**
**  Returns:
**    an error code (or 0 for no error).
**
**  Notes:
**    the new pattern is appended to the end of the existing patterns.
*/
{
    int i, n;
    Spattern *tmpPat;

// --- check if a pattern with same id already exists

    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( MSXproj_findObject(PATTERN, id) >= 1 ) return ERR_INVALID_OBJECT_PARAMS;

// --- allocate memory for a new array of patterns

    n = MSX.Nobjects[PATTERN] + 1;
    tmpPat = (Spattern *) calloc((size_t)n+1, sizeof(Spattern));
    if ( tmpPat == NULL ) return ERR_MEMORY;

// --- copy contents of old pattern array to new one

    for (i=1; i<=MSX.Nobjects[PATTERN]; i++)
    {
        tmpPat[i].id      = MSX.Pattern[i].id;
        tmpPat[i].length  = MSX.Pattern[i].length;
        tmpPat[i].first   = MSX.Pattern[i].first;
        tmpPat[i].current = MSX.Pattern[i].current;
    }

// --- add info for the new pattern

    if ( MSXproj_addObject(PATTERN, id, n) < 0 )
    {
        free(tmpPat);
        return ERR_MEMORY;
    }
    tmpPat[n].id = MSXproj_findID(PATTERN, id);
    tmpPat[n].length = 0;
    tmpPat[n].first = NULL;
    tmpPat[n].current = NULL;

// --- replace old pattern array with new one

    FREE(MSX.Pattern);
    MSX.Pattern = tmpPat;
    MSX.Nobjects[PATTERN]++;
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT  MSXsetpattern(int pat, double mult[], int len)
/*
**  Purpose:
**    Assigns a new set of multipliers to a given time pattern.
**
**  Input:
**    pat = the index number (base 1) of the time pattern;
**    mult[] = an array of multiplier values (base 0) to replace those
**             previously used by the pattern;
**    len = the number of entries in the multiplier array mult.
**
**  Output:
**    none.
**
**  Returns:
**    an error code (or 0 for no error).
*/
{
    int i;
    SnumList *listItem;

// --- check that pattern exists

    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ( pat < 1 || pat > MSX.Nobjects[PATTERN] ) return ERR_INVALID_OBJECT_INDEX;
    if ( len < 0) len = 0;

// --- delete current multipliers

    listItem = MSX.Pattern[pat].first;
    while (listItem)
    {
        MSX.Pattern[pat].first = listItem->next;
        free(listItem);
        listItem = MSX.Pattern[pat].first;
    }
    MSX.Pattern[pat].first = NULL;

// --- create a new set of multipliers

    MSX.Pattern[pat].length = 0;
    for ( i = 0; i < len; i++ )
    {
        listItem = (SnumList *) malloc(sizeof(SnumList));
        if ( listItem == NULL ) return ERR_MEMORY;
        listItem->value = mult[i];
        listItem->next = NULL;
        if ( MSX.Pattern[pat].first == NULL )
        {
            MSX.Pattern[pat].current = listItem;
            MSX.Pattern[pat].first = listItem;
        }
        else
        {
            MSX.Pattern[pat].current->next = listItem;
            MSX.Pattern[pat].current = listItem;
        }
        MSX.Pattern[pat].length++;
    }
	
    MSX.Pattern[pat].interval = 0;			  //Feng Shang   04/17/2008
    MSX.Pattern[pat].current = MSX.Pattern[pat].first;    //Feng Shang   04/17/2008
    return 0;
}

//=============================================================================

int  MSXDLLEXPORT MSXsavemsxfile(char *fname)
{
    int errcode;
    FILE *f;
    if ( !MSX.ProjectOpened ) return ERR_MSX_NOT_OPENED;
    if ((f = fopen(fname,"wt")) == NULL) return ERR_OPEN_OUT_FILE;
    errcode = MSXfile_save(f);
    fclose(f);
    return errcode;
}
