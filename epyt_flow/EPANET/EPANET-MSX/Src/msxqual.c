/******************************************************************************
**  MODULE:        MSXQUAL.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   Water quality routing routines.
**  COPYRIGHT:     Copyright (C) 2007 Feng Shang, Lewis Rossman, and James Uber.
**                 All Rights Reserved. See license information in LICENSE.TXT.
**  AUTHORS:       See AUTHORS
**  VERSION:       2.0.00
**  LAST UPDATE:   08/30/2022
******************************************************************************/

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

#include "msxtypes.h"
//#include "mempool.h"
#include "msxutils.h"
#include "dispersion.h"

// Macros to identify upstream & downstream nodes of a link
// under the current flow and to compute link volume
//
#define   UP_NODE(x)   ( (MSX.FlowDir[(x)]==POSITIVE) ? MSX.Link[(x)].n1 : MSX.Link[(x)].n2 )
#define   DOWN_NODE(x) ( (MSX.FlowDir[(x)]==POSITIVE) ? MSX.Link[(x)].n2 : MSX.Link[(x)].n1 )
#define   LINKVOL(k)   ( 0.785398*MSX.Link[(k)].len*SQR(MSX.Link[(k)].diam) )

//  External variables
//--------------------
extern MSXproject  MSX;                // MSX project data

//  Local variables
//-----------------
//static Pseg           FreeSeg;         // pointer to unused pipe segment
//static Pseg           *NewSeg;         // new segment added to each pipe
//static char           *FlowDir;        // flow direction for each pipe
//static double         *VolIn;          // inflow flow volume to each node
//static double         **MassIn;        // mass inflow of each species to each node
//static double         **X;             // work matrix
//static char           HasWallSpecies;  // wall species indicator
//static char           OutOfMemory;     // out of memory indicator
//static alloc_handle_t *QualPool;       // memory pool

// Stagnant flow tolerance
const double Q_STAGNANT = 0.005 / GPMperCFS;     // 0.005 gpm = 1.114e-5 cfs

//  Imported functions
//--------------------
int    MSXchem_open(void);
void   MSXchem_close(void);
extern int    MSXchem_react(double dt);
extern int    MSXchem_equil(int zone, int k, double *c);

extern void   MSXtank_mix1(int i, double vin, double *massin, double vnet);
extern void   MSXtank_mix2(int i, double vin, double *massin, double vnet);
extern void   MSXtank_mix3(int i, double vin, double *massin, double vnet);
extern void   MSXtank_mix4(int i, double vIn, double *massin, double vnet);



int    MSXout_open(void);
int    MSXout_saveResults(void);
int    MSXout_saveFinalResults(void);

void   MSXerr_clearMathError(void);                                            
int    MSXerr_mathError(void);                                                 
char*  MSXerr_writeMathErrorMsg(void);                                         

//  Exported functions
//--------------------
int    MSXqual_open(void);
int    MSXqual_init(void);
int    MSXqual_step(double *t, double *tleft);
int    MSXqual_close(void);
double MSXqual_getNodeQual(int j, int m);
double MSXqual_getLinkQual(int k, int m);
int    MSXqual_isSame(double c1[], double c2[]);
void   MSXqual_removeSeg(Pseg seg);
Pseg   MSXqual_getFreeSeg(double v, double c[]);
void   MSXqual_addSeg(int k, Pseg seg);
void   MSXqual_reversesegs(int k);

//  Local functions
//-----------------
static int    getHydVars(void);
static int    transport(int64_t tstep);
static void   initSegs(void);
static int    flowdirchanged(void);
static void   advectSegs(double dt);
static void   getNewSegWallQual(int k, double dt, Pseg seg);
static void   shiftSegWallQual(int k, double dt);
static void   sourceInput(int n, double vout, double dt);
static void   addSource(int n, Psource source, double v, double dt);
static double getSourceQual(Psource source);
static void   removeAllSegs(int k);

static void topological_transport(double dt);
static void findnodequal(int n, double volin, double* massin, double volout, double tstep);
static void noflowqual(int n);
static void evalnodeinflow(int, double, double*, double*);
static void evalnodeoutflow(int k, double* upnodequal, double tstep);
static int sortNodes();
static int selectnonstacknode(int numsorted, int* indegree);
static void findstoredmass(double* mass);

static void   evalHydVariables(int k);
//=============================================================================

int  MSXqual_open()
/*
**   Purpose:
**     opens the WQ routing system.
**
**   Returns:
**     an error code (0 if no errors).
*/
{
    int errcode = 0;
    int n;

    // --- set flags

    MSX.QualityOpened = FALSE;
    MSX.Saveflag = 0;
    MSX.OutOfMemory = FALSE;
    MSX.HasWallSpecies = FALSE;

    // --- initialize array pointers to null

    MSX.C1 = NULL;
    MSX.FirstSeg = NULL;
    MSX.LastSeg = NULL;
    MSX.NewSeg = NULL;
    MSX.FlowDir = NULL;
    MSX.MassIn = NULL;


    // --- open the chemistry system

    errcode = MSXchem_open();
    if (errcode > 0) return errcode;

    // --- allocate a memory pool for pipe segments

    MSX.QualPool = AllocInit();
    if (MSX.QualPool == NULL) return ERR_MEMORY;

// --- allocate memory used for species concentrations

    MSX.C1 = (double *) calloc(MSX.Nobjects[SPECIES]+1, sizeof(double));
   
    MSX.MassBalance.initial = (double*)calloc(MSX.Nobjects[SPECIES] + 1, sizeof(double));
    MSX.MassBalance.inflow =  (double*)calloc(MSX.Nobjects[SPECIES] + 1, sizeof(double));
    MSX.MassBalance.indisperse = (double*)calloc(MSX.Nobjects[SPECIES] + 1, sizeof(double));
    MSX.MassBalance.outflow = (double*)calloc(MSX.Nobjects[SPECIES] + 1, sizeof(double));
    MSX.MassBalance.reacted = (double*)calloc(MSX.Nobjects[SPECIES] + 1, sizeof(double));
    MSX.MassBalance.final   = (double*)calloc(MSX.Nobjects[SPECIES] + 1, sizeof(double));
    MSX.MassBalance.ratio   = (double*)calloc(MSX.Nobjects[SPECIES] + 1, sizeof(double));

// --- allocate memory used for pointers to the first, last,
//     and new WQ segments in each link and tank

    n = MSX.Nobjects[LINK] + MSX.Nobjects[TANK] + 1;
    MSX.FirstSeg = (Pseg *) calloc(n, sizeof(Pseg));
    MSX.LastSeg  = (Pseg *) calloc(n, sizeof(Pseg));
    MSX.NewSeg = (Pseg *) calloc(n, sizeof(Pseg));

// --- allocate memory used for flow direction in each link

    MSX.FlowDir  = (FlowDirection *) calloc(n, sizeof(FlowDirection));

// --- allocate memory used to accumulate mass and volume
//     inflows to each node

    n = MSX.Nobjects[NODE] + 1;
    MSX.MassIn   = (double *) calloc(MSX.Nobjects[SPECIES]+1, sizeof(double));
    MSX.SourceIn = (double*)calloc(MSX.Nobjects[SPECIES] + 1, sizeof(double));

// --- allocate memory for topologically sorted nodes

    MSX.SortedNodes = (int*)calloc(n, sizeof(int));

// --- check for successful memory allocation

    CALL(errcode, MEMCHECK(MSX.C1));
    CALL(errcode, MEMCHECK(MSX.FirstSeg));
    CALL(errcode, MEMCHECK(MSX.LastSeg));
    CALL(errcode, MEMCHECK(MSX.NewSeg));
    CALL(errcode, MEMCHECK(MSX.FlowDir));
    CALL(errcode, MEMCHECK(MSX.MassIn));
    CALL(errcode, MEMCHECK(MSX.SourceIn));
    CALL(errcode, MEMCHECK(MSX.SortedNodes));
    CALL(errcode, MEMCHECK(MSX.MassBalance.initial));
    CALL(errcode, MEMCHECK(MSX.MassBalance.inflow));
    CALL(errcode, MEMCHECK(MSX.MassBalance.indisperse));
    CALL(errcode, MEMCHECK(MSX.MassBalance.outflow));
    CALL(errcode, MEMCHECK(MSX.MassBalance.reacted));
    CALL(errcode, MEMCHECK(MSX.MassBalance.final));
    CALL(errcode, MEMCHECK(MSX.MassBalance.ratio));

// --- check if wall species are present

    for (n=1; n<=MSX.Nobjects[SPECIES]; n++)
    {
        if ( MSX.Species[n].type == WALL ) MSX.HasWallSpecies = TRUE;
    }
    if ( !errcode ) MSX.QualityOpened = TRUE;
    return(errcode);
}

//=============================================================================

int  MSXqual_init()
/*
**  Purpose:
**     re-initializes the WQ routing system.
**
**  Input:
**    none.
**
**  Returns:
**    an error code (or 0 if no errors).
*/
{
    int i, n, m;
    int errcode = 0;

// --- initialize node concentrations, tank volumes, & source mass flows

    for (i=1; i<=MSX.Nobjects[NODE]; i++)
    {
        for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
            MSX.Node[i].c[m] = MSX.Node[i].c0[m];
    }
    for (i = 1; i <= MSX.Nobjects[LINK]; i++)
    {
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            MSX.Link[i].reacted[m] = 0.0;
    }

    for (i=1; i<=MSX.Nobjects[TANK]; i++)
    {
        MSX.Tank[i].hstep = 0.0;
        MSX.Tank[i].v = MSX.Tank[i].v0;
        n = MSX.Tank[i].node;
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        {
            MSX.Tank[i].c[m] = MSX.Node[n].c0[m];
            MSX.Tank[i].reacted[m] = 0.0;
        }
    }

    for (i=1; i<=MSX.Nobjects[PATTERN]; i++)
    {
        MSX.Pattern[i].interval = 0;
        MSX.Pattern[i].current = MSX.Pattern[i].first;
    }

// --- copy expression constants to vector MSX.K[]                             

    for (i=1; i<=MSX.Nobjects[CONSTANT]; i++)
    {
        MSX.K[i] = MSX.Const[i].value;
    }

// --- check if a separate WQ report is required

    MSX.Rptflag = 0;
    n = 0;
    for (i=1; i<=MSX.Nobjects[NODE]; i++) n += MSX.Node[i].rpt;
    for (i=1; i<=MSX.Nobjects[LINK]; i++) n += MSX.Link[i].rpt;
    if ( n > 0 )
    {
        n = 0;
        for (m=1; m<=MSX.Nobjects[SPECIES]; m++) n += MSX.Species[m].rpt;
    }
    if ( n > 0 ) MSX.Rptflag = 1;
    if ( MSX.Rptflag ) MSX.Saveflag = 1;

// --- reset memory pool

    AllocSetPool(MSX.QualPool);
    MSX.FreeSeg = NULL;
    AllocReset();

// --- re-position hydraulics file

    fseek(MSX.HydFile.file, MSX.HydOffset, SEEK_SET);

// --- set elapsed times to zero

    MSX.Htime = 0;                         //Hydraulic solution time
    MSX.Qtime = 0;                         //Quality routing time
    MSX.Rtime = MSX.Rstart * 1000;         //Reporting time
    MSX.Nperiods = 0;                      //Number fo reporting periods

    for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
    {
        MSX.MassBalance.initial[m] = 0.0;
        MSX.MassBalance.final[m] = 0.0;
        MSX.MassBalance.inflow[m] = 0.0;
        MSX.MassBalance.indisperse[m] = 0.0;
        MSX.MassBalance.outflow[m] = 0.0;
        MSX.MassBalance.reacted[m] = 0.0;
        MSX.MassBalance.ratio[m] = 0.0;
    }

// --- open binary output file if results are to be saved

    if ( MSX.Saveflag ) errcode = MSXout_open();
    return errcode;
}

//=============================================================================

int MSXqual_step(double *t, double *tleft)
/*
**  Purpose:
**    updates WQ conditions over a single WQ time step.
**
**  Input:
**    none.
**
**  Output:
**    *t = current simulation time (sec)
**    *tleft = time left in simulation (sec)
**
**  Returns:
**    an error code:
**      0 = no error
**      501 = memory error
**      307 = can't read hydraulics file
**      513 = can't integrate reaction rates
*/
{
    int  k, errcode = 0, flowchanged;
    int m;
    double smassin, smassout, sreacted;
    int64_t  hstep, tstep, dt;
    
// --- set the shared memory pool to the water quality pool
//     and the overall time step to nominal WQ time step

    AllocSetPool(MSX.QualPool);
    tstep = MSX.Qstep;
    if (MSX.Qtime + tstep > MSX.Dur) tstep = MSX.Dur - MSX.Qtime;

// --- repeat until the end of the time step

    do
    {
    // --- find the time until the next hydraulic event occurs
        dt = tstep;
        hstep = MSX.Htime - MSX.Qtime;

    // --- check if next hydraulic event occurs within the current time step

        if (hstep <= dt)
        {

        // --- reduce current time step to end at next hydraulic event
            dt = hstep;

        // --- route WQ over this time step
            if ( dt > 0 ) CALL(errcode, transport(dt));
            MSX.Qtime += dt;

        // --- retrieve new hydraulic solution
            if (MSX.Qtime == MSX.Htime)
            {
                CALL(errcode, getHydVars());

                for (int kl = 1; kl <= MSX.Nobjects[LINK]; kl++)
                {
                    // --- skip non-pipe links

                    if (MSX.Link[kl].len == 0.0) continue;

                    // --- evaluate hydraulic variables

                    evalHydVariables(kl);
                }

                if (MSX.Qtime < MSX.Dur)
                {
                    // --- initialize pipe segments (at time 0) or else re-orient segments
                    //     to accommodate any flow reversals
                    if (MSX.Qtime == 0)
                    {
                        flowchanged = 1;
                        initSegs();
                    }
                    else 
                        flowchanged = flowdirchanged();

                    if (flowchanged)
                    {
                        CALL(errcode, sortNodes());
                    }
                }
            }

        // --- report results if its time to do so
            if (MSX.Saveflag && MSX.Qtime == MSX.Rtime)
            {
                CALL(errcode, MSXout_saveResults());
                MSX.Rtime += MSX.Rstep * 1000;
                MSX.Nperiods++;
            }
        }

    // --- otherwise just route WQ over the current time step

        else
        {
            CALL(errcode, transport(dt));
            MSX.Qtime += dt;
        }

    // --- reduce overall time step by the size of the current time step

        tstep -= dt;
        if (MSX.OutOfMemory) errcode = ERR_MEMORY;
    } while (!errcode && tstep > 0);

// --- update the current time into the simulation and the amount remaining

    *t = MSX.Qtime / 1000.;
    *tleft = (MSX.Dur - MSX.Qtime) / 1000.;

// --- if there's no time remaining, then save the final records to output file

    if ( *tleft <= 0 && MSX.Saveflag )
    {
        findstoredmass(MSX.MassBalance.final);
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        {
            sreacted = 0.0;
            for (k = 1; k <= MSX.Nobjects[LINK]; k++)
                sreacted += MSX.Link[k].reacted[m];
            for (k = 1; k <= MSX.Nobjects[TANK]; k++)
                sreacted += MSX.Tank[k].reacted[m];

            MSX.MassBalance.reacted[m] = sreacted;
            smassin = MSX.MassBalance.initial[m] + MSX.MassBalance.inflow[m] + MSX.MassBalance.indisperse[m];
            smassout = MSX.MassBalance.outflow[m]+MSX.MassBalance.final[m];
            if (sreacted < 0)  //loss
                smassout -= sreacted;
            else
                smassin += sreacted;

            if (smassin == 0)
                MSX.MassBalance.ratio[m] = 1.0;
            else
                MSX.MassBalance.ratio[m] = smassout / smassin;
        }
        CALL(errcode, MSXout_saveFinalResults());
    }
    return errcode;
}

//=============================================================================

double  MSXqual_getNodeQual(int j, int m)
/*
**   Purpose:
**     retrieves WQ for species m at node n.
**
**   Input:
**     j = node index
**     m = species index.
**
**   Returns:
**     WQ value of node.
*/
{
    int k;

// --- return 0 for WALL species

    if ( MSX.Species[m].type == WALL ) return 0.0;

// --- if node is a tank, return its internal concentration

    k = MSX.Node[j].tank;
    if (k > 0 && MSX.Tank[k].a > 0.0)
    {
        return MSX.Tank[k].c[m];
    }

// --- otherwise return node's concentration (which includes
//     any contribution from external sources)

    return MSX.Node[j].c[m];
}

//=============================================================================

double  MSXqual_getLinkQual(int k, int m)
/*
**   Purpose:
**     computes average quality in link k.
**
**   Input:
**     k = link index
**     m = species index.
**
**   Returns:
**     WQ value of link.
*/
{
    double  vsum = 0.0,
            msum = 0.0;
    Pseg    seg;

    seg = MSX.FirstSeg[k];
    while (seg != NULL)
    {
        vsum += seg->v;
        msum += (seg->c[m])*(seg->v);
        seg = seg->prev;
    }
    if (vsum > 0.0) return(msum/vsum);
    else
    {
        return (MSXqual_getNodeQual(MSX.Link[k].n1, m) +
                MSXqual_getNodeQual(MSX.Link[k].n2, m)) / 2.0;
    }
}

//=============================================================================

int MSXqual_close()
/*
**   Purpose:
**     closes the WQ routing system.
**
**   Input:
**     none.
**
**   Returns:
**     error code (0 if no error).
*/
{
    int errcode = 0;
    if (!MSX.ProjectOpened) return 0;
    MSXchem_close();

    FREE(MSX.C1);
    FREE(MSX.FirstSeg);
    FREE(MSX.LastSeg);
    FREE(MSX.NewSeg);
    FREE(MSX.FlowDir);
    FREE(MSX.SortedNodes);
    FREE(MSX.MassIn);
    FREE(MSX.SourceIn);
    if ( MSX.QualPool)
    {
        AllocSetPool(MSX.QualPool);
        AllocFreePool();
    }
    FREE(MSX.MassBalance.initial);
    FREE(MSX.MassBalance.inflow);
    FREE(MSX.MassBalance.indisperse);
    FREE(MSX.MassBalance.outflow);
    FREE(MSX.MassBalance.reacted);
    FREE(MSX.MassBalance.final);
    FREE(MSX.MassBalance.ratio);

    MSX.QualityOpened = FALSE;
    return errcode;
}

//=============================================================================

int  MSXqual_isSame(double c1[], double c2[])
/*
**   Purpose:
**     checks if two sets of concentrations are the same
**
**   Input:
**     c1[] = first set of species concentrations
**     c2[] = second set of species concentrations
**
**   Returns:
**     1 if the concentrations are all within a specific tolerance of each
**     other or 0 if they are not.
*/
{
    int m;
    for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
    {
        if (fabs(c1[m] - c2[m]) >= MSX.Species[m].aTol ) return 0;
    }
    return 1;
}


//=============================================================================

int  getHydVars()
/*
**   Purpose:
**     retrieves hydraulic solution and time step for next hydraulic event
**     from a hydraulics file.
**
**   Input:
**     none.
**
**   Returns:
**     error code
**
**   NOTE:
**     A hydraulic solution consists of the current time
**     (hydtime), nodal demands (D) and heads (H), link
**     flows (Q), and link status values and settings (which are not used).
*/
{
    int  errcode = 0;
    long hydtime, hydstep;
    INT4 n;

// --- read hydraulic time, demands, heads, and flows from the file

    if (fread(&n, sizeof(INT4), 1, MSX.HydFile.file) < 1)
        return ERR_READ_HYD_FILE;
    hydtime = (long)n;
    n = MSX.Nobjects[NODE];
    if (fread(MSX.D+1, sizeof(REAL4), n, MSX.HydFile.file) < (unsigned)n)
        return ERR_READ_HYD_FILE;
    if (fread(MSX.H+1, sizeof(REAL4), n, MSX.HydFile.file) < (unsigned)n)
        return ERR_READ_HYD_FILE;
    n = MSX.Nobjects[LINK];
    if (fread(MSX.Q+1, sizeof(REAL4), n, MSX.HydFile.file) < (unsigned)n)
        return ERR_READ_HYD_FILE;
    if (fread(MSX.S + 1, sizeof(REAL4), n, MSX.HydFile.file) < (unsigned)n) //03/17/2022
        return ERR_READ_HYD_FILE;
    
    for (int pi = 1; pi <= n; pi++)    //06/10/2021 Shang
        if (fabs(MSX.Q[pi]) < Q_STAGNANT)
            MSX.Q[pi] = 0.0;

// --- skip over link settings

    fseek(MSX.HydFile.file, 1*n*sizeof(REAL4), SEEK_CUR);

// --- read time step until next hydraulic event

    if (fread(&n, sizeof(INT4), 1, MSX.HydFile.file) < 1)
        return ERR_READ_HYD_FILE;
    hydstep = (long)n;

// --- update elapsed time until next hydraulic event

    MSX.Htime = hydtime + hydstep;
    MSX.Htime *= 1000;

/*
    if (MSX.Qtime < MSX.Dur)
    {
        if (MSX.Qtime == 0)
        {
            flowchanged = 1;
            initSegs();
        }
        else flowchanged = flowdirchanged();
    }
    return flowchanged;*/

    return errcode;
}

//=============================================================================

int  transport(int64_t tstep)
/*
**  Purpose:
**    transports constituent mass through pipe network
**    under a period of constant hydraulic conditions.
**
**  Input:
**    tstep = length of current time step (sec).
**
**  Returns:
**    an error code or 0 if no error.
*/
{
    int64_t qtime, dt64;
    double dt;
    int  errcode = 0;

// --- repeat until time step is exhausted

    MSXerr_clearMathError();                // clear math error flag           
    qtime = 0;
    while (!MSX.OutOfMemory &&
           !errcode &&
           qtime < tstep)
    {                                       // Qstep is nominal quality time step
        dt64 = MIN(MSX.Qstep, tstep-qtime); // get actual time step
        qtime += dt64;                      // update amount of input tstep taken
        dt = dt64 / 1000.;                  // time step as fractional seconds
        
        errcode = MSXchem_react(dt);        // react species in each pipe & tank
        if ( errcode ) return errcode;
        advectSegs(dt);                     // advect segments in each pipe
        
        topological_transport(dt);          //replace accumulate, updateNodes, sourceInput and release

		if (MSXerr_mathError())             // check for any math error        
		{
			MSXerr_writeMathErrorMsg();
			errcode = ERR_ILLEGAL_MATH;
		}
   }
   return errcode;
}

//=============================================================================

void  initSegs()
/*
**   Purpose:
**     initializes water quality in pipe segments.
**
**   Input:
**     none.
*/
{
    int     j, k, m;
    double  v;

// --- examine each link

    for (k=1; k<=MSX.Nobjects[LINK]; k++)
    {
    // --- establish flow direction

        if (fabs(MSX.Q[k]) < Q_STAGNANT)
            MSX.FlowDir[k] = ZERO_FLOW;
        else if (MSX.Q[k] > 0.0)
            MSX.FlowDir[k] = POSITIVE;
        else 
            MSX.FlowDir[k] = NEGATIVE;

    // --- start with no segments

        MSX.LastSeg[k] = NULL;
        MSX.FirstSeg[k] = NULL;
        MSX.NewSeg[k] = NULL;

    // --- use quality of downstream node for BULK species
    //     if no initial link quality supplied

//        j = DOWN_NODE(k);
        j = MSX.Link[k].n2;
        for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
        {
            if ( MSX.Link[k].c0[m] != MISSING )
                MSX.C1[m] = MSX.Link[k].c0[m];
            else if ( MSX.Species[m].type == BULK )
                MSX.C1[m] = MSX.Node[j].c0[m];
            else MSX.C1[m] = 0.0;
        }

    // --- fill link with a single segment of this quality

        MSXchem_equil(LINK, k, MSX.C1);
        v = LINKVOL(k);
        if (v > 0.0)
        {
            int ninitsegs = MIN(100, MSX.MaxSegments);
  
            for (int ns = 0; ns < ninitsegs; ns++)
                MSXqual_addSeg(k, MSXqual_getFreeSeg(v / (1.0*ninitsegs), MSX.C1));
        }
    }

// --- initialize segments in tanks

    for (j=1; j<=MSX.Nobjects[TANK]; j++)
    {
    // --- skip reservoirs

        if ( MSX.Tank[j].a == 0.0 ) continue;

    // --- tank segment pointers are stored after those for links

        k = MSX.Tank[j].node;
        for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
            MSX.C1[m] = MSX.Node[k].c0[m];
        k = MSX.Nobjects[LINK] + j;
        MSX.LastSeg[k] = NULL;
        MSX.FirstSeg[k] = NULL;

        MSXchem_equil(NODE, j, MSX.C1);

    // --- add 2 segments for 2-compartment model

        if (MSX.Tank[j].mixModel == MIX2)
        {
            v = MAX(0, MSX.Tank[j].v - MSX.Tank[j].vMix);
            MSXqual_addSeg(k, MSXqual_getFreeSeg(v, MSX.C1));
            v = MSX.Tank[j].v - v;
            MSXqual_addSeg(k, MSXqual_getFreeSeg(v, MSX.C1));
        }

    // --- add one segment for all other models

        else
        {
            v = MSX.Tank[j].v;
            MSXqual_addSeg(k, MSXqual_getFreeSeg(v, MSX.C1));
        }
    }

    findstoredmass(MSX.MassBalance.initial);    // initial mass
}

//=============================================================================

int  flowdirchanged()
/*
**   Purpose:
**     re-orients pipe segments (if flow reverses).
**
**   Input:
**     none.
*/
{
    int    k, flowchanged=0;
    FlowDirection  newdir;
 

// --- examine each link

    for (k=1; k<=MSX.Nobjects[LINK]; k++)
    {
    // --- find new flow direction

        newdir = POSITIVE;
        if (fabs(MSX.Q[k]) < Q_STAGNANT) 
            newdir = ZERO_FLOW;
        else if (MSX.Q[k] < 0.0) newdir = NEGATIVE;

    // --- if direction changes, then reverse the order of segments
    //     (first to last) and save new direction
              
        if (newdir*MSX.FlowDir[k] < 0)
        {
            MSXqual_reversesegs(k);
        }
        if (newdir != MSX.FlowDir[k])
        {
            flowchanged = 1;            
        }
        MSX.FlowDir[k] = newdir;
    }
    return flowchanged;
}


//=============================================================================

void advectSegs(double dt)
/*
**   Purpose:
**     advects WQ segments within each pipe.
**
**   Input:
**     dt = current WQ time step (sec).
*/
{
    int k, m;

// --- examine each link

    for (k=1; k<=MSX.Nobjects[LINK]; k++)
    {
    // --- zero out WQ in new segment to be added at entrance of link

        for (m=1; m<=MSX.Nobjects[SPECIES]; m++) MSX.C1[m] = 0.0;

    // --- get a free segment to add to entrance of link

        MSX.NewSeg[k] = MSXqual_getFreeSeg(0.0, MSX.C1);

    // --- skip zero-length links (pumps & valves) & no-flow links

        if ( MSX.NewSeg[k] == NULL ||
             MSX.Link[(k)].len == 0.0 || MSX.Q[k] == 0.0 ) continue;

    // --- find conc. of wall species in new segment to be added
    //     and adjust conc. of wall species to reflect shifted
    //     positions of existing segments

        if ( MSX.HasWallSpecies )
        {
            getNewSegWallQual(k, dt, MSX.NewSeg[k]);
            shiftSegWallQual(k, dt);
        }
    }
}

//=============================================================================

void getNewSegWallQual(int k, double dt, Pseg newseg)
/*
**  Purpose:
**     computes wall species concentrations for a new WQ segment that
**     enters a pipe from its upstream node.
**
**  Input:
**    k = link index
**    dt = current WQ time step (sec)
**    newseg = pointer to a new, unused WQ segment
**
**  Output:
**    newseg->c[] = wall species concentrations in the new WQ segment
*/
{
    Pseg  seg;
    int   m;
    double v, vin, vsum, vadded, vleft;

// --- get volume of inflow to link

    if ( newseg == NULL ) return;
    v = LINKVOL(k);
	vin = ABS(MSX.Q[k])*dt;
    if (vin > v) vin = v;

// --- start at last (most upstream) existing WQ segment

	seg = MSX.LastSeg[k];
	vsum = 0.0;
    vleft = vin;
    for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
    {
        if ( MSX.Species[m].type == WALL ) newseg->c[m] = 0.0;
    }

// --- repeat while some inflow volume still remains

    while ( vleft > 0.0 && seg != NULL )
    {

    // --- find volume added by this segment

        vadded = seg->v;
        if ( vadded > vleft ) vadded = vleft;

    // --- update total volume added and inflow volume remaining

        vsum += vadded;
        vleft -= vadded;

    // --- add wall species mass contributed by this segment to new segment

        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        {
            if ( MSX.Species[m].type == WALL ) newseg->c[m] += vadded*seg->c[m];
        }

    // --- move to next downstream WQ segment

        seg = seg->next;
    }

// --- convert mass of wall species in new segment to concentration

    if ( vsum > 0.0 )
    {
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        {
            if ( MSX.Species[m].type == WALL ) newseg->c[m] /= vsum;
        }
    }
}

//=============================================================================

void shiftSegWallQual(int k, double dt)
/*
**  Purpose:
**    recomputes wall species concentrations in segments that remain
**    within a pipe after flow is advected over current time step.
**
**  Input:
**    k = link index
**    dt = current WQ time step (sec)
*/
{
    Pseg  seg1, seg2;
    int   m;
    double v, vin, vstart, vend, vcur, vsum;

// --- find volume of water displaced in pipe

    v = LINKVOL(k);
	vin = ABS((double)MSX.Q[k])*dt;
    if (vin > v) vin = v;

// --- set future start position (measured by pipe volume) of original last segment

    vstart = vin;

// --- examine each segment, from upstream to downstream

    for( seg1 = MSX.LastSeg[k]; seg1 != NULL; seg1 = seg1->next )
    {

        // --- initialize a "mixture" WQ
        //     if vstart >= v the segment seg1 will be out of the pipe,
        //     so no need to track wall concentration of this segment
        if (vstart >= v) break;   //2020 moved up
        
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++) MSX.C1[m] = 0.0;

    // --- find the future end position of this segment

        vend = vstart + seg1->v;   //
        if (vend > v) vend = v;
        vcur = vstart;
        vsum = 0;

    // --- find volume taken up by the segment after it moves down the pipe

        for (seg2 = MSX.LastSeg[k]; seg2 != NULL; seg2 = seg2->next)
        {
            if ( seg2->v == 0.0 ) continue;
            vsum += seg2->v;
            if ( vsum >= vstart && vsum <= vend )  //DS end of seg2 is between vstart and vend 
            {
                for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
                {
                    if ( MSX.Species[m].type == WALL )
                        MSX.C1[m] += (vsum - vcur) * seg2->c[m];
                }
                vcur = vsum;
            }
            if ( vsum >= vend ) break;  //DS of seg2 is at DS of vend 
        }

    // --- update the wall species concentrations in the segment

        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        {
            if ( MSX.Species[m].type != WALL ) continue;
            if (seg2 != NULL) MSX.C1[m] += (vend - vcur) * seg2->c[m]; //only part of seg2
            seg1->c[m] = MSX.C1[m] / (vend - vstart);
            if ( seg1->c[m] < 0.0 ) seg1->c[m] = 0.0;
        }

    // --- re-start at the current end location

        vstart = vend;
    //    if ( vstart >= v ) break;   //2020 moved up
    }
}


//=============================================================================

void sourceInput(int n, double volout, double dt)
/*
**  Purpose:
**    computes contribution (if any) of mass additions from WQ
**    sources at each node.
**
**  Input:
**    n = nodeindex
**    dt = current WQ time step (sec)
*/
{
    int m;
    double  qout, qcutoff;
    Psource source;

// --- establish a flow cutoff which indicates no outflow from a node

    qcutoff = 10.0*TINY;

// --- consider each node

    // --- skip node if no WQ source

    source = MSX.Node[n].sources;
    if (source == NULL) return;


    qout = volout / dt;

    // --- evaluate source input only if node outflow > cutoff flow
    if (qout <= qcutoff) return;

    // --- add contribution of each source species
    for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        MSX.SourceIn[m] = 0.0;   
    while (source)
    {
        addSource(n, source, volout, dt);
        source = source->next;
    }

    // --- compute a new chemical equilibrium at the source node
    MSXchem_equil(NODE, 0, MSX.Node[n].c);
 
    for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)   
    {
        MSX.MassBalance.inflow[m] += MSX.SourceIn[m] * LperFT3;
    }
}

//=============================================================================

void addSource(int n, Psource source, double volout, double dt)
/*
**  Purpose:
**    updates concentration of particular species leaving a node
**    that receives external source input.
**
**  Input:
**    n = index of source node
**    source = pointer to WQ source data
**    volout = volume of water leaving node during current time step
**    dt     = current WQ time step (sec)
*/
{
    int     m;
    double  massadded, s;

// --- only analyze bulk species

    m = source->species;
    massadded = 0.0;
    if (source->c0 > 0.0 && MSX.Species[m].type == BULK)
    {

    // --- mass added depends on type of source

        s = getSourceQual(source);
        switch(source->type)
        {
        // Concen. Source:
        // Mass added = source concen. * -(demand)

          case CONCEN:

          // Only add source mass if demand is negative
              if (MSX.Node[n].tank <=0 && MSX.D[n] < 0.0) massadded = -s*MSX.D[n]*dt;

          // If node is a tank then set concen. to 0.
          // (It will be re-set to true value later on)

          //  if (MSX.Node[n].tank > 0) MSX.Node[n].c[m] = 0.0;
              break;

        // Mass Inflow Booster Source:

          case MASS:
              massadded = s*dt/LperFT3;
              break;

        // Setpoint Booster Source:
        // Mass added is difference between source
        // & node concen. times outflow volume

          case SETPOINT:
              if (s > MSX.Node[n].c[m])
                  massadded = (s - MSX.Node[n].c[m])*volout;
              break;

        // Flow-Paced Booster Source:
        // Mass added = source concen. times outflow volume

          case FLOWPACED:
              massadded = s*volout;
              break;
        }

    // --- adjust nodal concentration to reflect source addition
        MSX.Node[n].c[m] += massadded / volout;
        MSX.SourceIn[m] += massadded;
    }
}


//=============================================================================

double  getSourceQual(Psource source)
/*
**   Input:   j = source index
**   Output:  returns source WQ value
**   Purpose: determines source concentration in current time period
*/
{
    int    i;
    long   k;
    double c, f = 1.0;

// --- get source concentration (or mass flow) in original units
    c = source->c0;

// --- convert mass flow rate from min. to sec.
    if (source->type == MASS) c /= 60.0;

// --- apply time pattern if assigned
    i = source->pat;
    if (i == 0) return(c);
    k = (int)((MSX.Qtime + MSX.Pstart*1000) / (MSX.Pstep*1000)) % MSX.Pattern[i].length;
    if (k != MSX.Pattern[i].interval)
    {
        if ( k < MSX.Pattern[i].interval )
        {
            MSX.Pattern[i].current = MSX.Pattern[i].first;
            MSX.Pattern[i].interval = 0;
        }
        while (MSX.Pattern[i].current && MSX.Pattern[i].interval < k)
        {
             MSX.Pattern[i].current = MSX.Pattern[i].current->next;
             MSX.Pattern[i].interval++;
        }
    }
    if (MSX.Pattern[i].current) f = MSX.Pattern[i].current->value;
    return c*f;
}

//=============================================================================

void  removeAllSegs(int k)
/*
**   Purpose:
**     removes all segments in a pipe link.
**
**   Input:
**     k = link index.
*/
{
    Pseg seg;
    seg = MSX.FirstSeg[k];
    while (seg != NULL)
    {
        MSX.FirstSeg[k] = seg->prev;
        MSXqual_removeSeg(seg);
        seg = MSX.FirstSeg[k];
    }
    MSX.LastSeg[k] = NULL;
    if (k <= MSX.Nobjects[LINK])
        MSX.Link[k].nsegs =  0;
}

void topological_transport(double dt)
{
    int j, n, k, m;
    double volin, volout;
    Padjlist  alink;


    // Analyze each node in topological order
    for (j = 1; j <= MSX.Nobjects[NODE]; j++)
    {
        // ... index of node to be processed
        n = MSX.SortedNodes[j];

        // ... zero out mass & flow volumes for this node
        volin = 0.0;
        volout = 0.0;
        memset(MSX.MassIn, 0, (MSX.Nobjects[SPECIES] + 1) * sizeof(double));
        memset(MSX.SourceIn, 0, (MSX.Nobjects[SPECIES] + 1) * sizeof(double));

        // ... examine each link with flow into the node
        for (alink = MSX.Adjlist[n]; alink != NULL; alink = alink->next)
        {
            // ... k is index of next link incident on node n
            k = alink->link;

            // ... link has flow into node - add it to node's inflow
            //     (m is index of link's downstream node)
            m = MSX.Link[k].n2;
            if (MSX.FlowDir[k] < 0) m = MSX.Link[k].n1;
            if (m == n)
            {
                evalnodeinflow(k, dt, &volin, MSX.MassIn);
            }

            // ... link has flow out of node - add it to node's outflow
            else volout += fabs(MSX.Q[k]);
        }

        // ... if node is a junction, add on any external outflow (e.g., demands)
        if (MSX.Node[n].tank == 0)
        {
            volout += fmax(0.0, MSX.D[n]);
        }

        // ... convert from outflow rate to volume
        volout *= dt;

        // ... find the concentration of flow leaving the node
        findnodequal(n, volin, MSX.MassIn, volout, dt);

        // ... examine each link with flow out of the node
        for (alink = MSX.Adjlist[n]; alink != NULL; alink = alink->next)
        {
            // ... link k incident on node n has upstream node m equal to n
            k = alink->link;
            m = MSX.Link[k].n1;
            if (MSX.FlowDir[k] < 0) m = MSX.Link[k].n2;
            if (m == n)
            {
                // ... send flow at new node concen. into link
                evalnodeoutflow(k, MSX.Node[n].c, dt);
            }
        }

    }
    /*Advection-Reaction Done, Dispersion Starts*/
    //1. Linear relationship for each pipe
    //2. Compose the nodal equations
    //3. Solve the matrix to update nodal concentration
    //4. Update segment concentration
    for (int m = 1; m <= MSX.Nobjects[SPECIES]; m++)
    {
        if (MSX.Dispersion.md[m] > 0 || MSX.Dispersion.ld[m] > 0)
        {
            dispersion_pipe(m, dt);
            solve_nodequal(m, dt);
            segqual_update(m, dt);
        }
    }
}


void evalnodeoutflow(int k, double * upnodequal, double tstep)
/*
**--------------------------------------------------------------
**   Input:   k = link index
**            c = quality from upstream node
**            tstep = time step
**   Output:  none
**   Purpose: releases flow volume and mass from the upstream
**            node of a link over a time step.
**--------------------------------------------------------------
*/
{

    double v;
    Pseg seg;
    int m;
    int useNewSeg = 0;

    // Find flow volume (v) released over time step
    v = fabs(MSX.Q[k]) * tstep;
    if (v == 0.0) return;

    // Release flow and mass into upstream end of the link

    for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
    {
        if (MSX.Species[m].type == BULK)
            MSX.NewSeg[k]->c[m] = upnodequal[m];
    }

    // ... case where link has a last (most upstream) segment
    seg = MSX.LastSeg[k];

    if (seg)
    {
        if (!MSXqual_isSame(seg->c, upnodequal) && MSX.Link[k].nsegs < MSX.MaxSegments)
        {
            useNewSeg = 1;
        }
        else
            useNewSeg = 0;

//        if (MSX.DispersionFlag == 1 && MSX.Link[k].nsegs >= MSX.MaxSegments)
//            useNewSeg = 0;
 
        if (useNewSeg == 0)
        {
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            {
                if (MSX.Species[m].type == BULK)
                   seg->c[m] = (seg->c[m]*seg->v+upnodequal[m]*v)/(seg->v+v);
            }
            seg->v += v;
            MSXqual_removeSeg(MSX.NewSeg[k]);
        }

        // --- otherwise add the new seg to the end of the link

        else
        {
            MSX.NewSeg[k]->v = v;
            MSXqual_addSeg(k, MSX.NewSeg[k]);
        }
    }

    // ... link has no segments so add one
    else
    {
        MSX.NewSeg[k]->v = v;
        MSXqual_addSeg(k, MSX.NewSeg[k]);
    }

}


void  evalnodeinflow(int k, double tstep, double* volin, double* massin)
    /*
    **--------------------------------------------------------------
    **   Input:   k = link index
    **            tstep = quality routing time step
    **   Output:  volin = flow volume entering a node
    **            massin = constituent mass entering a node
    **   Purpose: adds the contribution of a link's outflow volume
    **            and constituent mass to the total inflow into its
    **            downstream node over a time step.
    **--------------------------------------------------------------
    */
{

    double q, v, vseg;
    int sindex;
    Pseg seg;

    // Get flow rate (q) and flow volume (v) through link
    q = MSX.Q[k];
    v = fabs(q) * tstep;

    // Transport flow volume v from link's leading segments into downstream
    // node, removing segments once their full volume is consumed
    while (v > 0.0)
    {
        seg = MSX.FirstSeg[k];
        if (!seg) break;

        // ... volume transported from first segment is smaller of
        //     remaining flow volume & segment volume
        vseg = seg->v;
        vseg = MIN(vseg, v);

        // ... update total volume & mass entering downstream node
        *volin += vseg;
        for (sindex = 1; sindex <= MSX.Nobjects[SPECIES]; sindex++)
            massin[sindex] += vseg * seg->c[sindex] * LperFT3;

        // ... reduce remaining flow volume by amount transported
        v -= vseg;

        // ... if all of segment's volume was transferred
        if (v >= 0.0 && vseg >= seg->v)
        {
            // ... replace this leading segment with the one behind it
            MSX.FirstSeg[k] = seg->prev;
            MSX.Link[k].nsegs--;
            if (MSX.FirstSeg[k] == NULL) MSX.LastSeg[k] = NULL;
            else MSX.FirstSeg[k]->next = NULL; //03/19/2024 added to break the linked segments 
		    
            // ... recycle the used up segment
            seg->prev = MSX.FreeSeg;
            MSX.FreeSeg = seg;
        }

        // ... otherwise just reduce this segment's volume
        else seg->v -= vseg;
    }
}


void findnodequal(int n, double volin, double* massin, double volout, double tstep)
    /*
    **--------------------------------------------------------------
    **   Input:   n = node index
    **            volin = flow volume entering node
    **            massin = mass entering node
    **            volout = flow volume leaving node
    **            tstep = length of current time step
    **   Output:  returns water quality in a node's outflow
    **   Purpose: computes a node's new quality from its inflow
    **            volume and mass, including any source contribution.
    **--------------------------------------------------------------
    */
{
    int m, j;
    // Node is a junction - update its water quality
    j = MSX.Node[n].tank;
    if (j <= 0)
    {
        // ... dilute inflow with any external negative demand
        volin -= fmin(0.0, MSX.D[n]) * tstep;

        // ... new concen. is mass inflow / volume inflow
        if (volin > 0.0)
        {
            for(m = 1; m <= MSX.Nobjects[SPECIES]; m++)
                MSX.Node[n].c[m] = massin[m] / volin / LperFT3;
        }

        // ... if no inflow adjust quality for reaction in connecting pipes
        else 
            noflowqual(n);

        MSXchem_equil(NODE, 0, MSX.Node[n].c);

    }
    else
    {
        // --- use initial quality for reservoirs

        if (MSX.Tank[j].a == 0.0)
        {
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            {
                MSX.Node[n].c[m] = MSX.Node[n].c0[m];
            }
            MSXchem_equil(NODE, 0, MSX.Node[n].c);
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            {
               
                MSX.MassBalance.inflow[m] += MSX.Node[n].c[m] * volout * LperFT3;
                MSX.MassBalance.outflow[m] += massin[m];
            }
        }

        // --- otherwise update tank WQ based on mixing model

        else
        {
            if (volin > 0.0)
            {
                for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
                {
                    MSX.C1[m] = massin[m] / volin / LperFT3;
                }
            }
            else for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
                MSX.C1[m] = 0.0;
            switch (MSX.Tank[j].mixModel)
            {
            case MIX1: MSXtank_mix1(j, volin, massin, volin-volout);
                break;
            case MIX2: MSXtank_mix2(j, volin, massin, volin-volout);
                break;
            case FIFO: MSXtank_mix3(j, volin, massin, volin-volout);
                break;
            case LIFO: MSXtank_mix4(j, volin, massin, volin-volout);
                break;
            }
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            {
                MSX.Node[n].c[m] = MSX.Tank[j].c[m];
            }
            MSX.Tank[j].v += (double)MSX.D[n] * tstep;
        }
    }

    // Find quality contribued by any external chemical source
    sourceInput(n, volout, tstep);
    if (MSX.Node[n].tank == 0)
    {
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            if(MSX.Species[m].type == BULK)
                MSX.MassBalance.outflow[m] += MAX(0.0, MSX.D[n]) * tstep * MSX.Node[n].c[m]*LperFT3;
    }
}


int sortNodes()
/*
**--------------------------------------------------------------
**   Input:   none
**   Output:  returns an error code
**   Purpose: topologically sorts nodes from upstream to downstream.
**   Note:    links with negligible flow are ignored since they can
**            create spurious cycles that cause the sort to fail.
**--------------------------------------------------------------
*/
{

    int i, j, k, n;
    int* indegree = NULL;
    int* stack = NULL;
    int stacksize = 0;
    int numsorted = 0;
    int errcode = 0;
    FlowDirection dir;
    Padjlist  alink;

    // Allocate an array to count # links with inflow to each node
    // and for a stack to hold nodes waiting to be processed
    indegree = (int*)calloc(MSX.Nobjects[NODE] + 1, sizeof(int));
    stack = (int*)calloc(MSX.Nobjects[NODE] + 1, sizeof(int));
    if (indegree && stack)
    {
        // Count links with "non-negligible" inflow to each node
        for (k = 1; k <= MSX.Nobjects[LINK]; k++)
        {
            dir = MSX.FlowDir[k];
            if (dir == POSITIVE) n = MSX.Link[k].n2;
            else if (dir == NEGATIVE) n = MSX.Link[k].n1;
            else continue;
            indegree[n]++;
        }

        // Place nodes with no inflow onto a stack
        for (i = 1; i <= MSX.Nobjects[NODE]; i++)
        {
            if (indegree[i] == 0)
            {
                stacksize++;
                stack[stacksize] = i;
            }
        }

        // Examine each node on the stack until none are left
        while (numsorted < MSX.Nobjects[NODE])
        {
            // ... if stack is empty then a cycle exists
            if (stacksize == 0)
            {
                //  ... add a non-sorted node connected to a sorted one to stack
                j = selectnonstacknode(numsorted, indegree);
                if (j == 0) break;  // This shouldn't happen.
                indegree[j] = 0;
                stacksize++;
                stack[stacksize] = j;
            }

            // ... make the last node added to the stack the next
            //     in sorted order & remove it from the stack
            i = stack[stacksize];
            stacksize--;
            numsorted++;
            MSX.SortedNodes[numsorted] = i;

            // ... for each outflow link from this node reduce the in-degree
            //     of its downstream node
            for (alink = MSX.Adjlist[i]; alink != NULL; alink = alink->next)
            {
                // ... k is the index of the next link incident on node i
                k = alink->link;

                // ... skip link if flow is negligible
                if (MSX.FlowDir[k] == 0) continue;

                // ... link has flow out of node (downstream node n not equal to i)
                n = MSX.Link[k].n2;
                if (MSX.FlowDir[k] < 0) n = MSX.Link[k].n1;

                // ... reduce degree of node n
                if (n != i && indegree[n] > 0)
                {
                    indegree[n]--;

                    // ... no more degree left so add node n to stack
                    if (indegree[n] == 0)
                    {
                        stacksize++;
                        stack[stacksize] = n;
                    }
                }
            }
        }
    }
    else errcode = 101;
    if (numsorted < MSX.Nobjects[NODE]) errcode = 120;
    FREE(indegree);
    FREE(stack);
    return errcode;
}

int selectnonstacknode(int numsorted, int* indegree)
/*
**--------------------------------------------------------------
**   Input:   numsorted = number of nodes that have been sorted
**            indegree = number of inflow links to each node
**   Output:  returns a node index
**   Purpose: selects a next node for sorting when a cycle exists.
**--------------------------------------------------------------
*/
{

    int i, m, n;
    Padjlist  alink;

    // Examine each sorted node in last in - first out order
    for (i = numsorted; i > 0; i--)
    {
        // For each link connected to the sorted node
        m = MSX.SortedNodes[i];
        for (alink = MSX.Adjlist[m]; alink != NULL; alink = alink->next)
        {
            // ... n is the node of link k opposite to node m
            n = alink->node;

            // ... select node n if it still has inflow links
            if (indegree[n] > 0) return n;
        }
    }

    // If no node was selected by the above process then return the
    // first node that still has inflow links remaining
    for (i = 1; i <= MSX.Nobjects[NODE]; i++)
    {
        if (indegree[i] > 0) return i;
    }

    // If all else fails return 0 indicating that no node was selected
    return 0;
}

void  noflowqual(int n)
/*
**--------------------------------------------------------------
**   Input:   n = node index
**   Output:  quality for node n
**   Purpose: sets the quality for a junction node that has no
**            inflow to the average of the quality in its
**            adjoining link segments.
**   Note:    this function is only used for reactive substances.
**--------------------------------------------------------------
*/
{

    int k, m, inflow, kount = 0;
    double c = 0.0;
    FlowDirection dir;
    Padjlist  alink;

    for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        MSX.Node[n].c[m] = 0.0;
    // Examine each link incident on the node
    for (alink = MSX.Adjlist[n]; alink != NULL; alink = alink->next)
    {
        // ... index of an incident link
        k = alink->link;
        dir = MSX.FlowDir[k];

        // Node n is link's downstream node - add quality
        // of link's first segment to average
        if (MSX.Link[k].n2 == n && dir >= 0) inflow = TRUE;
        else if (MSX.Link[k].n1 == n && dir < 0)  inflow = TRUE;
        else inflow = FALSE;
        if (inflow == TRUE && MSX.FirstSeg[k] != NULL)
        {
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
                MSX.Node[n].c[m] += MSX.FirstSeg[k]->c[m];
            kount++;
        }

        // Node n is link's upstream node - add quality
        // of link's last segment to average
        else if (inflow == FALSE && MSX.LastSeg[k] != NULL)
        {
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
                MSX.Node[n].c[m] += MSX.LastSeg[k]->c[m];
            kount++;
        }
    }
    if (kount > 0) 
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            MSX.Node[n].c[m] = MSX.Node[n].c[m] / (double)kount;
}

void findstoredmass(double * mass)
/*
**--------------------------------------------------------------
**   Input:   none
**   Output:  returns total constituent mass stored in the network
**   Purpose: finds the current mass stored in
**            all pipes and tanks.
**--------------------------------------------------------------
*/
{

    int    i, k, m;
    Pseg   seg;

    for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
    {
        mass[m] = 0;
    }

    // Mass residing in each pipe
    for (k = 1; k <= MSX.Nobjects[LINK]; k++)
    {
        // Sum up the quality and volume in each segment of the link
        seg = MSX.FirstSeg[k];
        while (seg != NULL)
        {
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            {
                if (MSX.Species[m].type == BULK)
                    mass[m] += seg->c[m] * seg->v * LperFT3;  //M/L * ft3 * L/Ft3 = M
                else
                    mass[m] += seg->c[m] * seg->v * 4.0 / MSX.Link[k].diam * MSX.Ucf[AREA_UNITS]; //Mass per area unit * ft3 / ft * area unit per ft2;
            }
            seg = seg->prev;
        }
    }

    // Mass residing in each tank
    for (i = 1; i <= MSX.Nobjects[TANK]; i++)
    {
        // ... skip reservoirs
        if (MSX.Tank[i].a == 0.0) continue;

        // ... add up mass in each volume segment
        else
        {
            k = MSX.Nobjects[LINK] + i;
            seg = MSX.FirstSeg[k];
            while (seg != NULL)
            {
                for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
                {
                    if (MSX.Species[m].type == BULK)
                        mass[m] += seg->c[m] * seg->v * LperFT3;
                }
                seg = seg->prev;
            }
        }
    }
}

void MSXqual_reversesegs(int k)
/*
**--------------------------------------------------------------
**   Input:   k = link index
**   Output:  none
**   Purpose: re-orients a link's segments when flow reverses.
**--------------------------------------------------------------
*/
{
    Pseg  seg, cseg, pseg;

    seg = MSX.FirstSeg[k];
    MSX.FirstSeg[k] = MSX.LastSeg[k];
    MSX.LastSeg[k] = seg;
    pseg = NULL;
    while (seg != NULL)
    {
        cseg = seg->prev;
        seg->prev = pseg;
        seg->next = cseg;
        pseg = seg;
        seg = cseg;
    }
}



//=============================================================================

void MSXqual_removeSeg(Pseg seg)
/*
**   Purpose:
**     places a WQ segment back into the memory pool of segments.
**
**   Input:
**     seg = pointer to a WQ segment.
*/
{
    if ( seg == NULL ) return;
    seg->prev = MSX.FreeSeg;
    seg->next = NULL;
    MSX.FreeSeg = seg;
}

//=============================================================================

Pseg MSXqual_getFreeSeg(double v, double c[])
/*
**   Purpose:
**     retrieves an unused water quality volume segment from the memory pool.
**
**   Input:
**     v = segment volume (ft3)
**     c[] = segment quality
**
**   Returns:
**     a pointer to an unused water quality segment.
*/
{
    Pseg seg;
    int  m;

// --- try using the last discarded segment if one is available

    if (MSX.FreeSeg != NULL)
    {
        seg = MSX.FreeSeg;
        MSX.FreeSeg = seg->prev;
    }

// --- otherwise create a new segment from the memory pool

    else
    {
        seg = (struct Sseg *) Alloc(sizeof(struct Sseg));
        if (seg == NULL)
        {
            MSX.OutOfMemory = TRUE;
            return NULL;
        }
        seg->c = (double *) Alloc((MSX.Nobjects[SPECIES]+1)*sizeof(double));
        seg->lastc = (double *)Alloc((MSX.Nobjects[SPECIES] + 1) * sizeof(double));
        if ( seg->c == NULL||seg->lastc == NULL)
        {
            MSX.OutOfMemory = TRUE;
            return NULL;
        }
    }

// --- assign volume, WQ, & integration time step to the new segment

    seg->v = v;
    for (m=1; m<=MSX.Nobjects[SPECIES]; m++) seg->c[m] = c[m];
    seg->hstep = 0.0;
    return seg;
}

//=============================================================================

void  MSXqual_addSeg(int k, Pseg seg)
/*
**   Purpose:
**     adds a new segment to the upstream end of a link.
**
**   Input:
**     k = link index
**     seg = pointer to a free WQ segment.
*/

{
    seg->prev = NULL;
    seg->next = NULL;
    if (MSX.FirstSeg[k] == NULL) MSX.FirstSeg[k] = seg;
    if (MSX.LastSeg[k] != NULL)
    {
        MSX.LastSeg[k]->prev = seg;
        seg->next = MSX.LastSeg[k];
    }
    MSX.LastSeg[k] = seg;
    if (k <= MSX.Nobjects[LINK])
        MSX.Link[k].nsegs++;
}

void evalHydVariables(int k)
/*
**  Purpose:
**    retrieves current values of hydraulic variables for the
**    current link being analyzed.
**
**  Input:
**    k = link index
**
**  Output:
**    updates values stored in vector HydVar[]
*/
{
    double dh;                         // headloss in ft
    double diam = MSX.Link[k].diam;    // diameter in ft
    double length = MSX.Link[k].len;   // length in ft
    double av;                         // area per unit volume

// --- pipe diameter and length in user's units (ft or m)
    MSX.Link[k].HydVar[DIAMETER] = diam * MSX.Ucf[LENGTH_UNITS];
    MSX.Link[k].HydVar[LENGTH] = length * MSX.Ucf[LENGTH_UNITS];

    // --- flow rate in user's units
    MSX.Link[k].HydVar[FLOW] = fabs(MSX.Q[k]) * MSX.Ucf[FLOW_UNITS];

    // --- flow velocity in ft/sec
    if (diam == 0.0) MSX.Link[k].HydVar[VELOCITY] = 0.0;
    else MSX.Link[k].HydVar[VELOCITY] = fabs(MSX.Q[k]) * 4.0 / PI / SQR(diam);

    // --- Reynolds number
    MSX.Link[k].HydVar[REYNOLDS] = MSX.Link[k].HydVar[VELOCITY] * diam / VISCOS;

    // --- flow velocity in user's units (ft/sec or m/sec)
    MSX.Link[k].HydVar[VELOCITY] *= MSX.Ucf[LENGTH_UNITS];

    // --- Darcy Weisbach friction factor
    if (MSX.Link[k].len == 0.0) MSX.Link[k].HydVar[FRICTION] = 0.0;
    else
    {
        dh = ABS(MSX.H[MSX.Link[k].n1] - MSX.H[MSX.Link[k].n2]);
        MSX.Link[k].HydVar[FRICTION] = 39.725 * dh * pow(diam, 5.0) /
            MSX.Link[k].len / SQR((double)MSX.Q[k]);
    }

    // --- shear velocity in user's units (ft/sec or m/sec)
    MSX.Link[k].HydVar[SHEAR] = MSX.Link[k].HydVar[VELOCITY] * sqrt(MSX.Link[k].HydVar[FRICTION] / 8.0);

    // --- pipe surface area / volume in area_units/L
    MSX.Link[k].HydVar[AREAVOL] = 1.0;
    if (diam > 0.0)
    {
        av = 4.0 / diam;                // ft2/ft3
        av *= MSX.Ucf[AREA_UNITS];     // area_units/ft3
        av /= LperFT3;                 // area_units/L
        MSX.Link[k].HydVar[AREAVOL] = av;
    }

    MSX.Link[k].HydVar[ROUGHNESS] = MSX.Link[k].roughness;
}
