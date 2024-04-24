/******************************************************************************
**  MODULE:        MSXOUT.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   I/O routines for the binary output file used by the
**                 EPANET Multi-Species Extension toolkit.         
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.00
**  LAST UPDATE:   08/30/2022
******************************************************************************/

#include <stdio.h>
#include <string.h>
#include <math.h>

#if defined(macintosh) || defined(Macintosh) || defined(__APPLE__) && defined(__MACH__)
#include <stdlib.h>
#endif

#include "msxtypes.h"

//  External variables
//--------------------
extern MSXproject  MSX;                // MSX project data

//  Local variables
//-----------------
static long  ResultsOffset;            // Offset byte where results begin
static long  NodeBytesPerPeriod;       // Bytes per time period used by all nodes
static long  LinkBytesPerPeriod;       // Bytes per time period used by all links

//  Imported functions
//--------------------
double MSXqual_getNodeQual(int j, int m);
double MSXqual_getLinkQual(int k, int m);

//  Exported functions
//--------------------
int   MSXout_open(void);
int   MSXout_saveInitialResults(void);
int   MSXout_saveResults(void);
int   MSXout_saveFinalResults(void);
float MSXout_getNodeQual(int k, int j, int m);
float MSXout_getLinkQual(int k, int j, int m);

//  Local functions
//-----------------
static int   saveStatResults(void);
static void  getStatResults(int objType, int m, double* stats1,
             double* stats2, REAL4* x);


//=============================================================================

int MSXout_open()
/*
**  Purpose:
**    opens an MSX binary output file.
**
**  Input:
**    none.
**
**  Returns:
**    an error code (or 0 if no error).
*/
{
// --- close output file if already opened

    if (MSX.OutFile.file != NULL) fclose(MSX.OutFile.file); 

// --- try to open the file

    if ( (MSX.OutFile.file = fopen(MSX.OutFile.name, "w+b")) == NULL)
    {
        return ERR_OPEN_OUT_FILE;
    }

// --- open a scratch output file for statistics

    if ( MSX.Statflag == SERIES ) MSX.TmpOutFile.file = MSX.OutFile.file;
    else if ( (MSX.TmpOutFile.file = fopen(MSX.TmpOutFile.name, "w+b")) == NULL)
    {
        return ERR_OPEN_OUT_FILE;
    }

// --- write initial results to file

    MSX.Nperiods = 0;
    MSXout_saveInitialResults();
    return 0;
}

//=============================================================================

int MSXout_saveInitialResults()
/*
**  Purpose:
**    saves general information to beginning of MSX binary output file.
**
**  Input:
**    none.
**
**  Returns:
**    an error code (or 0 if no error).
*/
{
    int   m;
    INT4  n;
    INT4  magic = MAGICNUMBER;
    INT4  version = VERSION;
    FILE* f = MSX.OutFile.file;

    rewind(f);
    fwrite(&magic, sizeof(INT4), 1, f);                     //Magic number
    fwrite(&version, sizeof(INT4), 1, f);                   //Version number
    n = (INT4)MSX.Nobjects[NODE];
    fwrite(&n, sizeof(INT4), 1, f);                         //Number of nodes
    n = (INT4)MSX.Nobjects[LINK];
    fwrite(&n, sizeof(INT4), 1, f);                         //Number of links
    n = (INT4)MSX.Nobjects[SPECIES];
    fwrite(&n, sizeof(INT4), 1, f);                         //Number of species
    n = (INT4)MSX.Rstep;
    fwrite(&n, sizeof(INT4), 1, f);                         //Reporting step size
    for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
    {
        n = (INT4)strlen(MSX.Species[m].id);
        fwrite(&n, sizeof(INT4), 1, f);                     //Length of species ID
        fwrite(MSX.Species[m].id, sizeof(char), n, f);      //Species ID string                                                   
        fwrite(&MSX.Species[m].units, sizeof(char), MAXUNITS, f);   //Species mass units
    }
    ResultsOffset = ftell(f);
    NodeBytesPerPeriod = MSX.Nobjects[NODE]*MSX.Nobjects[SPECIES]*sizeof(REAL4);
    LinkBytesPerPeriod = MSX.Nobjects[LINK]*MSX.Nobjects[SPECIES]*sizeof(REAL4);
    return 0;
}
    

//=============================================================================

int MSXout_saveResults()
/*
**  Purpose:
**    saves computed species concentrations for each node and link at the
**    current time period to the temporary MSX binary output file (which
**    will be the same as the permanent MSX binary file if time series
**    values were specified as the reported statistic, which is the
**    default case).
**
**  Input:
**    none.
**
**  Returns:
**    an error code (or 0 if no error).
*/
{
    int   m, j;
    REAL4 x;
    for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
    {
        for (j=1; j<=MSX.Nobjects[NODE]; j++)
        {
            x = (REAL4)MSXqual_getNodeQual(j, m);
            fwrite(&x, sizeof(REAL4), 1, MSX.TmpOutFile.file);
        }
    }
    for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
    {
        for (j=1; j<=MSX.Nobjects[LINK]; j++)
        {
            x = (REAL4)MSXqual_getLinkQual(j, m);
            fwrite(&x, sizeof(REAL4), 1, MSX.TmpOutFile.file);
        }
    }
    return 0;
}

//=============================================================================

int MSXout_saveFinalResults()
/*
**  Purpose:
**    saves any statistical results plus the following information to the end
**    of the MSX binary output file:
**    - byte offset into file where WQ results for each time period begins,
**    - total number of time periods written to the file,
**    - any error code generated by the analysis (0 if there were no errors),
**    - the Magic Number to indicate that the file is complete.
**
**  Input:
**    none.
**
**  Returns:
**    an error code (or 0 if no error).
*/
{
    INT4  n;
    INT4  magic = MAGICNUMBER;
    int   err = 0;

// --- save statistical results to the file

    if ( MSX.Statflag != SERIES ) err = saveStatResults();
    if ( err > 0 ) return err;

// --- write closing records to the file

    n = (INT4)ResultsOffset;
    fwrite(&n, sizeof(INT4), 1, MSX.OutFile.file);
    n = (INT4)MSX.Nperiods;
    fwrite(&n, sizeof(INT4), 1, MSX.OutFile.file);
    n = (INT4)MSX.ErrCode;
    fwrite(&n, sizeof(INT4), 1, MSX.OutFile.file);
    fwrite(&magic, sizeof(INT4), 1, MSX.OutFile.file);
    return 0;
}

//=============================================================================

float MSXout_getNodeQual(int k, int j, int m)
/*
**  Purpose:
**    retrieves a result for a specific node from the MSX binary output file.
**
**  Input:
**    k = time period index
**    j = node index
**    m = species index.
**
**  Returns:
**    the requested species concentration. 
*/
{
    REAL4 c;
    long bp = ResultsOffset + k * (NodeBytesPerPeriod + LinkBytesPerPeriod);
    bp += ((m-1)*MSX.Nobjects[NODE] + (j-1)) * sizeof(REAL4);
    fseek(MSX.OutFile.file, bp, SEEK_SET);
    fread(&c, sizeof(REAL4), 1, MSX.OutFile.file);
    return (float)c;
}

//=============================================================================

float MSXout_getLinkQual(int k, int j, int m)
/*
**  Purpose:
**    retrieves a result for a specific link from the MSX binary output file.
**
**  Input:
**    k = time period index
**    j = link index
**    m = species index.
**
**  Returns:
**    the requested species concentration. 
*/
{
    REAL4 c;
    long bp = ResultsOffset + ((k+1)*NodeBytesPerPeriod) + (k*LinkBytesPerPeriod);
    bp += ((m-1)*MSX.Nobjects[LINK] + (j-1)) * sizeof(REAL4);
    fseek(MSX.OutFile.file, bp, SEEK_SET);
    fread(&c, sizeof(REAL4), 1, MSX.OutFile.file);
    return (float)c;
}

//=============================================================================

int  saveStatResults()
/*
**  Purpose:
**    saves time statistic results (average, min., max., or range) for each
**    node and link to the permanent binary output file.
**
**  Input:
**    none.
**
**  Returns:
**    an error code (or 0 if no error).
*/
{
    int     m, err = 0;
    REAL4*  x = NULL;
    double* stats1 = NULL;
    double* stats2 = NULL;

// --- create arrays used to store statistics results

    if ( MSX.Nperiods <= 0 ) return err;
    m = MAX(MSX.Nobjects[NODE], MSX.Nobjects[LINK]);
    x = (REAL4 *) calloc(m+1, sizeof(REAL4));
    stats1 = (double *) calloc(m+1, sizeof(double));
    stats2 = (double *) calloc(m+1, sizeof(double));

// --- get desired statistic for each node & link and save to binary file

    if ( x && stats1 && stats2 )
    {
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++ )
        {
            getStatResults(NODE, m, stats1, stats2, x);
            fwrite(x+1, sizeof(REAL4), MSX.Nobjects[NODE], MSX.OutFile.file);
        }
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        {
            getStatResults(LINK, m, stats1, stats2, x);    
            fwrite(x+1, sizeof(REAL4), MSX.Nobjects[LINK], MSX.OutFile.file);
        }
        MSX.Nperiods = 1;
    }
    else err = ERR_MEMORY;

// --- free allocated arrays

    FREE(x);
    FREE(stats1);
    FREE(stats2);
    return err;
}

//=============================================================================

void getStatResults(int objType, int m, double * stats1, double * stats2,
                    REAL4 * x)
/*
**  Purpose:
**    reads all results for a given type of object from the temporary
**    binary output file and computes the required statistic (average,
**    min., max., or range) for each object.
**
**  Input:
**    objType = type of object (nodes or links)
**    m = species index
**    stats1, stats2 = work arrays used to hold intermediate values
**    x = array used to store results read from file.
**
**  Output:
**    x = array that contains computed statistic for each object.
*/
{
    int  j, k;
    int  n = MSX.Nobjects[objType];
    long bp;

// --- initialize work arrays
    
    for (j = 1; j <= n; j++)
    {
        stats1[j] = 0.0;
        stats2[j] = 0.0; 
    }

// --- for all time periods

    for (k = 0; k < MSX.Nperiods; k++)
    {

    // --- position file at start of time period

        bp = k*(NodeBytesPerPeriod + LinkBytesPerPeriod);
        if ( objType == NODE )
        {
            bp += (m-1) * MSX.Nobjects[NODE] * sizeof(REAL4);
        }
        if ( objType == LINK)
        {
            bp += NodeBytesPerPeriod + 
                  (m-1) * MSX.Nobjects[LINK] * sizeof(REAL4);
        }
        fseek(MSX.TmpOutFile.file, bp, SEEK_SET);

    // --- read concentrations and update stats for all objects

        fread(x+1, sizeof(REAL4), n, MSX.TmpOutFile.file);
        if ( MSX.Statflag == AVGERAGE )
        { 
            for (j = 1; j <= n; j++) stats1[j] += x[j];
        }
        else for (j = 1; j <= n; j++)
        {
            stats1[j] = MIN(stats1[j], x[j]); 
            stats2[j] = MAX(stats2[j], x[j]); 
        }
    }

// --- place final stat value for each object in x

    if ( MSX.Statflag == AVGERAGE )
    {
        for ( j = 1; j <= n; j++) stats1[j] /= (double)MSX.Nperiods;
    }
    if ( MSX.Statflag == RANGE )
    {
        for ( j = 1; j <= n; j++)
            stats1[j] = fabs(stats2[j] - stats1[j]);
    }
    if ( MSX.Statflag == MAXIMUM)
    {
        for ( j = 1; j <= MSX.Nobjects[NODE]; j++) stats1[j] = stats2[j]; 
    }
    for (j = 1; j <= n; j++) x[j] = (REAL4)stats1[j];
}
