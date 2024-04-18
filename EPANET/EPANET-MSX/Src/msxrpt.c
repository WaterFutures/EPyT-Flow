/******************************************************************************
**  MODULE:        MSXRPT.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   report writing routines for the EPANET Multi-Species
**                 Extension toolkit.
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.00
**  LAST UPDATE:   04/14/2021
******************************************************************************/

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <math.h>

#include "msxtypes.h"
#include "epanet2.h"

// Constants
//----------
#define SERIES_TABLE  0
#define STATS_TABLE   1

//  External variables
//--------------------
extern MSXproject  MSX;                // MSX project data

//  Local variables
//-----------------
static char *Logo[] =
    {"******************************************************************",
     "*                      E P A N E T  -  M S X                     *",
     "*                   Multi-Species Water Quality                  *",
     "*                   Analysis for Pipe  Networks                  *",
     "*                           Version 2.0.0                        *",     //2.0.00
     "******************************************************************"};

static char PageHdr[] = "  Page %d                                    ";
static char *StatsHdrs[] =
    {"", "Average Values  ", "Minimum Values  ",
         "Maximum Values  ", "Range of Values "};
static char Line[MAXLINE+1];
static long LineNum;
static long PageNum;
static int  *RptdSpecies;
static struct TableHdrStruct
{
    char Line1[MAXLINE+1];
    char Line2[MAXLINE+1];
    char Line3[MAXLINE+1];
    char Line4[MAXLINE+1];
    char Line5[MAXLINE+1];
} TableHdr;
static char IDname[MAXLINE+1];

//  Imported functions
//--------------------
void  MSXinp_getSpeciesUnits(int m, char *units);
float MSXout_getNodeQual(int k, int j, int m);
float MSXout_getLinkQual(int k, int j, int m);

//  Exported functions
//--------------------
int   MSXrpt_write(void);
void  MSXrpt_writeLine(char *line);                                            

//  Local functions
//-----------------
static void  createSeriesTables(void);
static void  createStatsTables(void);
static void  createTableHdr(int objType, int tableType);
static void  writeTableHdr(void);
static void  writeNodeTable(int j, int tableType);
static void  writeLinkTable(int j, int tableType);
static void  getHrsMins(int k, int *hrs, int *mins);
static void  newPage(void);
static void  writeLine(char *line);

static void writemassbalance();

//=============================================================================

int  MSXrpt_write()
{
    INT4  magic = 0;
    int  j;
    int recordsize = sizeof(INT4);

// --- check that results are available

    if ( MSX.Nperiods < 1 )    return 0;
    if ( MSX.OutFile.file == NULL ) return ERR_OPEN_OUT_FILE;
    fseek(MSX.OutFile.file, -recordsize, SEEK_END);
    fread(&magic, sizeof(INT4), 1, MSX.OutFile.file);
    if ( magic != MAGICNUMBER ) return ERR_IO_OUT_FILE;

// --- write program logo & project title

    PageNum = 1;
    LineNum = 1;
    newPage();
    for (j=0; j<=5; j++) writeLine(Logo[j]);
    writeLine("");
    writeLine(MSX.Title);

// --- generate the appropriate type of table

    if ( MSX.Statflag == SERIES ) createSeriesTables();
    else createStatsTables();

    writemassbalance();

    writeLine("");
    return 0;
}

//=============================================================================

void  MSXrpt_writeLine(char *line)                                             
{                                                                              
    writeLine(line);                                                           
}                                                                              

//=============================================================================

void createSeriesTables()
{
    int  j;

// --- report on all requested nodes

    for (j=1; j<=MSX.Nobjects[NODE]; j++)
    {
        if ( !MSX.Node[j].rpt ) continue;
        ENgetnodeid(j, IDname);
        createTableHdr(NODE, SERIES_TABLE);
        writeNodeTable(j, SERIES_TABLE);
    }

// --- report on all requested links

    for (j=1; j<=MSX.Nobjects[LINK]; j++)
    {
        if ( !MSX.Link[j].rpt ) continue;
        ENgetlinkid(j, IDname);
        createTableHdr(LINK, SERIES_TABLE);
        writeLinkTable(j, SERIES_TABLE);
    }
}

//=============================================================================

void createStatsTables()
{
    int  j;
    int  count;

// --- check if any nodes to be reported

    count = 0;
    for (j = 1; j <= MSX.Nobjects[NODE]; j++) count += MSX.Node[j].rpt;

// --- report on all requested nodes

    if ( count > 0 )
    {
        createTableHdr(NODE, STATS_TABLE);
        for (j = 1; j <= MSX.Nobjects[NODE]; j++)
        {
            if ( MSX.Node[j].rpt ) writeNodeTable(j, STATS_TABLE);
        }
    }

// --- check if any links to be reported

    count = 0;
    for (j = 1; j <= MSX.Nobjects[LINK]; j++) count += MSX.Link[j].rpt;

// --- report on all requested links

    if ( count > 0 )
    {
        createTableHdr(LINK, STATS_TABLE);
        for (j = 1; j <= MSX.Nobjects[LINK]; j++)
        {
            if ( MSX.Link[j].rpt ) writeLinkTable(j, STATS_TABLE);
        }
    }
}

//=============================================================================

void createTableHdr(int objType, int tableType)
{
    int   m;
    char  s1[MAXLINE+1];
    char  s2[MAXLINE+1];

    if ( tableType == SERIES_TABLE )
    {
        if ( objType == NODE )
            sprintf(TableHdr.Line1, "<<< Node %s >>>", IDname);
        else
            sprintf(TableHdr.Line1, "<<< Link %s >>>", IDname);
        strcpy(TableHdr.Line2, "Time   ");
        strcpy(TableHdr.Line3, "hr:min ");
        strcpy(TableHdr.Line4, "-------");
    }
    if ( tableType == STATS_TABLE )
    {
        strcpy(TableHdr.Line1, "");
        sprintf(TableHdr.Line2, "%-16s", StatsHdrs[tableType]);
        if ( objType == NODE ) strcpy(TableHdr.Line3, "for Node        ");
        else                   strcpy(TableHdr.Line3, "for Link        ");
        strcpy(TableHdr.Line4, "----------------");
    }
    for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
    {
        if ( !MSX.Species[m].rpt ) continue;
        if ( objType == NODE && MSX.Species[m].type == WALL ) continue;
        sprintf(s1, "  %10s", MSX.Species[m].id);
        strcat(TableHdr.Line2, s1);
        strcat(TableHdr.Line4, "  ----------");
        MSXinp_getSpeciesUnits(m, s1);
        sprintf(s2, "  %10s", s1);
        strcat(TableHdr.Line3, s2);
    }
    if ( MSX.PageSize > 0 && MSX.PageSize - LineNum < 8 ) newPage();
    else writeTableHdr();
}

//=============================================================================

void  writeTableHdr()
{
    if ( MSX.PageSize > 0 && MSX.PageSize - LineNum < 6 ) newPage();
    writeLine("");
    writeLine(TableHdr.Line1);
    writeLine("");
    writeLine(TableHdr.Line2);
    writeLine(TableHdr.Line3);
    writeLine(TableHdr.Line4);
}

//=============================================================================

void  writeNodeTable(int j, int tableType)
{
    int   k, m, hrs, mins;
    char  s[MAXLINE+1];
    float c;

    for (k=0; k<MSX.Nperiods; k++)
    {
        if ( tableType == SERIES_TABLE )
        {
            getHrsMins(k, &hrs, &mins);
            sprintf(Line, "%4d:%02d", hrs, mins);
        }
        if ( tableType == STATS_TABLE )
        {
            ENgetnodeid(j, IDname);
            sprintf(Line, "%-16s", IDname);
        }
        for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
        {
            if ( !MSX.Species[m].rpt ) continue;
            if ( MSX.Species[m].type == WALL ) continue;
            c = MSXout_getNodeQual(k, j, m);
            sprintf(s, "  %10.*f", MSX.Species[m].precision, c);
            strcat(Line, s);
        }
        writeLine(Line);
    }
}

//=============================================================================

void  writeLinkTable(int j, int tableType)
{
    int   k, m, hrs, mins;
    char  s[MAXLINE+1];
    float c;

    for (k=0; k<MSX.Nperiods; k++)
    {
        if ( tableType == SERIES_TABLE )
        {
            getHrsMins(k, &hrs, &mins);
            sprintf(Line, "%4d:%02d", hrs, mins);
        }
        if ( tableType == STATS_TABLE )
        {
            ENgetlinkid(j, IDname);
            sprintf(Line, "%-16s", IDname);
        }
        for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
        {
            if ( !MSX.Species[m].rpt ) continue;
            c = MSXout_getLinkQual(k, j, m);
            sprintf(s, "  %10.*f", MSX.Species[m].precision, c);
            strcat(Line, s);
        }
        writeLine(Line);
    }
}

//=============================================================================

void getHrsMins(int k, int *hrs, int *mins)
{
    long m, h;

    m = (MSX.Rstart + k*MSX.Rstep) / 60;
    h = m / 60;
    m = m - 60*h;
    *hrs = h;
    *mins = m;
}

//=============================================================================

void  newPage()
{
    char  s[MAXLINE+1];
    LineNum = 1;
    sprintf(s,
            "\nPage %-3d                                             EPANET-MSX 2.0.0",   //2.0.0
            PageNum);
    writeLine(s);
    writeLine("");
    if ( PageNum > 1 ) writeTableHdr();
    PageNum++;
}

//=============================================================================

void  writeLine(char *line)
{
    if ( LineNum == MSX.PageSize ) newPage();
    if ( MSX.RptFile.file ) fprintf(MSX.RptFile.file, "  %s\n", line);   //(modified, FS-01/07/2008)
    else ENwriteline(line);
    LineNum++;
}


void writemassbalance()
/*
**-------------------------------------------------------------
**   Input:   none
**   Output:  none
**   Purpose: writes water quality mass balance ratio
**            (Outflow + Final Storage) / Inflow + Initial Storage)
**            to report file.
**-------------------------------------------------------------
*/
{

    char s1[MAXMSG + 1];
    int  kunits = 0;

    for (int m = 1; m <= MSX.Nobjects[SPECIES]; m++)
    {
        if (MSX.Species[m].pipeExprType != RATE)
            continue;
        
        snprintf(s1, MAXMSG, "\n");
        writeLine(s1);
        snprintf(s1, MAXMSG, "Water Quality Mass Balance: %s (%s)", MSX.Species[m].id, MSX.Species[m].units);
        writeLine(s1);
        snprintf(s1, MAXMSG, "================================");
        writeLine(s1);
        snprintf(s1, MAXMSG, "Initial Mass:      %12.5e", MSX.MassBalance.initial[m]);
        writeLine(s1);
        snprintf(s1, MAXMSG, "Mass Inflow:       %12.5e", MSX.MassBalance.inflow[m]+ MSX.MassBalance.indisperse[m]);
        writeLine(s1);
    //    snprintf(s1, MAXMSG, "Mass Dispersed Inflow:       %12.5e", MSX.MassBalance.indisperse[m]);
    //    writeLine(s1);
        snprintf(s1, MAXMSG, "Mass Outflow:      %12.5e", MSX.MassBalance.outflow[m]);
        writeLine(s1);
        snprintf(s1, MAXMSG, "Mass Reacted:      %12.5e", MSX.MassBalance.reacted[m]);
        writeLine(s1);
        snprintf(s1, MAXMSG, "Final Mass:        %12.5e", MSX.MassBalance.final[m]);
        writeLine(s1);
        snprintf(s1, MAXMSG, "Mass Ratio:         %-.5f", MSX.MassBalance.ratio[m]);
        writeLine(s1);
        snprintf(s1, MAXMSG, "================================\n");
        writeLine(s1);
    }
}








