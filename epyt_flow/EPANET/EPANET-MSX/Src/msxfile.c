/*******************************************************************************
**  MODULE:        MSXFILE.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   writes MSX project data to a MSX input file.
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.00
**  LAST UPDATE:   04/14/2021
*******************************************************************************/

#include <stdio.h>
#include <string.h>

#include "msxtypes.h"
#include "msxutils.h"
#include "msxdict.h"
#include "epanet2.h"

//  External variables
//--------------------
extern MSXproject  MSX;                // MSX project data

//  Exported functions
//--------------------
int MSXfile_save(FILE *f);

//  Local functions
//-----------------
static void  saveSpecies(FILE *f);
static void  saveCoeffs(FILE *f);
static int   saveInpSections(FILE *f);
static void  saveParams(FILE *f);
static void  saveQuality(FILE *f);
static void  saveSources(FILE *f);
static void  savePatterns(FILE *f);

//=============================================================================

int MSXfile_save(FILE *f)
/*
**  Purpose:
**    saves current MSX project data to file.
**
**  Input:
**    f = pointer to MSX file where data are saved.
*/
{
    int errcode;
    fprintf(f, "[TITLE]");
    fprintf(f, "\n%s\n", MSX.Title);
    saveSpecies(f);
    saveCoeffs(f);
    errcode = saveInpSections(f);
    saveParams(f);
    saveQuality(f);
    saveSources(f);
    savePatterns(f);
    return errcode;
}

//=============================================================================

void  saveSpecies(FILE *f)
{
    int  i, n;
    fprintf(f, "\n[SPECIES]");
    n = MSX.Nobjects[SPECIES];
    for (i=1; i<=n; i++)
    {
        if ( MSX.Species[i].type == BULK ) fprintf(f, "\nBULK    ");
        else                               fprintf(f, "\nWALL    ");
        fprintf(f, "%-32s %-15s %e %e",
            MSX.Species[i].id, MSX.Species[i].units,
            MSX.Species[i].aTol, MSX.Species[i].rTol);
    }
}

//=============================================================================

void  saveCoeffs(FILE *f)
{
    int  i, n;
    fprintf(f, "\n\n[COEFFICIENTS]");
    n = MSX.Nobjects[CONSTANT];
    for (i=1; i<=n; i++)
    {
        fprintf(f, "\nCONSTANT    %-32s  %e",
            MSX.Const[i].id, MSX.Const[i].value);
    }
    n = MSX.Nobjects[PARAMETER];
    for (i=1; i<=n; i++)
    {
        fprintf(f, "\nPARAMETER   %-32s  %e",
            MSX.Param[i].id, MSX.Param[i].value);
    }
}

//=============================================================================

int  saveInpSections(FILE *f)
{
    char   line[MAXLINE+1];
    char   writeLine;
    int    newsect;

    if ((MSX.MsxFile.file = fopen(MSX.MsxFile.name,"rt")) == NULL) return ERR_OPEN_MSX_FILE;
    rewind(MSX.MsxFile.file);

    fprintf(f,"\n\n");
    writeLine = FALSE;
    while ( fgets(line, MAXLINE, MSX.MsxFile.file) != NULL )
    {
        if (*line == '[' )
        {
            writeLine = TRUE;
            newsect = MSXutils_findmatch(line, MsxSectWords);
            if ( newsect >= 0 ) switch(newsect)
            {
              case s_OPTION:
              case s_TERM:
              case s_PIPE:
              case s_TANK:
              case s_REPORT:
                break;
              default:
                writeLine = FALSE;
            }
        }
        if ( writeLine) fprintf(f, "%s", line);
    }
    if ( MSX.MsxFile.file ) fclose(MSX.MsxFile.file);
    MSX.MsxFile.file = NULL;
    return 0;
}

//=============================================================================

void  saveParams(FILE *f)
{
    int    i, j, k;
    double x;
    char   id[MAXLINE+1];

    if ( MSX.Nobjects[PARAMETER] > 0 )
    {
        fprintf(f, "\n\n[PARAMETERS]");
        for (j=1; j<=MSX.Nobjects[PARAMETER]; j++)
        {
            x = MSX.Param[j].value;
            for (i=1; i<=MSX.Nobjects[LINK]; i++)
            {
                if ( MSX.Link[i].param[j] != x )
                {
                    ENgetlinkid(i, id);
                    fprintf(f, "\nPIPE    %-32s  %-32s  %e",
                        id, MSX.Param[j].id, MSX.Link[i].param[j]);
                }
            }
            for (i=1; i<=MSX.Nobjects[TANK]; i++)
            {
                if ( MSX.Tank[i].param[j] != x )
                {
                    k = MSX.Tank[i].node;
                    ENgetnodeid(k, id);
                    fprintf(f, "\nTANK    %-32s  %-32s  %e",
                        id, MSX.Param[j].id, MSX.Tank[i].param[j]);
                }
            }
        }
    }
}

//=============================================================================

void  saveQuality(FILE *f)
{
    int    i, j;
    char   id[MAXLINE+1];

    fprintf(f, "\n\n[QUALITY]");
    for (j=1; j<=MSX.Nobjects[SPECIES]; j++)
    {
		if (MSX.C0[j] > 0.0)
			fprintf(f, "\nGLOBAL  %-32s  %e",
                    MSX.Species[j].id, MSX.C0[j]);

        for (i=1; i<=MSX.Nobjects[NODE]; i++)
        {
            if ( MSX.Node[i].c0[j] > 0.0 && MSX.Node[i].c0[j] != MSX.C0[j])
            {
                ENgetnodeid(i, id);
                fprintf(f, "\nNODE    %-32s  %-32s  %e",
                    id, MSX.Species[j].id, MSX.Node[i].c0[j]);
            }
        }
        for (i=1; i<=MSX.Nobjects[LINK]; i++)
        {
            if ( MSX.Link[i].c0[j] > 0.0 && MSX.Link[i].c0[j] != MSX.C0[j])			
            {
                ENgetlinkid(i, id);
                fprintf(f, "\nLINK    %-32s  %-32s  %e",
                    id, MSX.Species[j].id, MSX.Link[i].c0[j]);
            }
        }
    }
}

//=============================================================================

void  saveSources(FILE *f)
{
    int     i;
    Psource source;
    char    id[MAXLINE+1];

    fprintf(f, "\n\n[SOURCES]");
    for (i=1; i<=MSX.Nobjects[NODE]; i++)
    {
        source = MSX.Node[i].sources;
        while ( source )
        {
            if ( source->c0 > 0.0 && source->type > -1)   //Feng Shang 09/23/2008
            {
                ENgetnodeid(i, id);
                fprintf(f, "\n%-10s  %-32s  %-32s  %e",
                    SourceTypeWords[source->type], id,
                    MSX.Species[source->species].id, source->c0);
                if ( source->pat > 0 )
                    fprintf(f, "  %-32s", MSX.Pattern[source->pat].id);
            }
            source = source->next;
        }
    }
}

//=============================================================================

void  savePatterns(FILE *f)
{
    int  i, count;
    SnumList *listItem;

    if ( MSX.Nobjects[PATTERN] > 0 ) fprintf(f, "\n\n[PATTERNS]");
    for (i=1; i<=MSX.Nobjects[PATTERN]; i++)
    {
        count = 0;
        listItem = MSX.Pattern[i].first;
        while (listItem)
        {
            if ( count % 6 == 0 )
            {
                fprintf(f, "\n%-32s", MSX.Pattern[i].id);
            }
            fprintf(f, "  %e", listItem->value);
            count++;
            listItem = listItem->next;
        }
    }
}
