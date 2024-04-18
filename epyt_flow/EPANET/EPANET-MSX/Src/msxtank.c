/******************************************************************************
**  MODULE:        MSXTANK.C
**  PROJECT:       EPANET-MSX
**  DESCRIPTION:   Storage tank mixing routines. 
**  AUTHORS:       see AUTHORS
**  Copyright:     see AUTHORS
**  License:       see LICENSE
**  VERSION:       2.0.00
**  LAST UPDATE:   04/14/2021
******************************************************************************/

#include <stdio.h>
#include <math.h>

#include "msxtypes.h"

//  External variables
//--------------------
extern MSXproject  MSX;                // MSX project data

//  Imported functions
//--------------------
extern void  MSXqual_removeSeg(Pseg seg);
extern Pseg  MSXqual_getFreeSeg(double v, double c[]);
extern void  MSXqual_addSeg(int k, Pseg seg);
extern int   MSXqual_isSame(double c1[], double c2[]);
extern int   MSXchem_equil(int zone, int k, double *c);
extern void  MSXqual_reversesegs(int k);

//  Exported functions
//--------------------
void   MSXtank_mix1(int i, double vin, double *massin, double vnet);
void   MSXtank_mix2(int i, double vin, double *massin, double vnet);
void   MSXtank_mix3(int i, double vin, double *massin, double vnet);
void   MSXtank_mix4(int i, double vin, double *massin, double vnet);


//=============================================================================

void  MSXtank_mix1(int i, double vin, double *massin, double vnet)
/*
**  Purpose:
**    computes new WQ at end of time step in a completely mixed tank
**    (after contents have been reacted).
**                     
**  Input:
**    i   = tank index
**    vin = volume of inflow to tank (ft3)
**    massin = massinflow
**    vnet  = inflow - outflow     
*/
{
    int    k, m, n;
    double c;
    double vnew;
    Pseg   seg;

// --- blend inflow with contents

    n = MSX.Tank[i].node;
    k = MSX.Nobjects[LINK] + i;
    seg = MSX.FirstSeg[k];
    if (seg)
    {
        vnew = seg->v + vin;
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        {
            if (MSX.Species[m].type != BULK) continue;
            c = seg->c[m];
            if (vnew > 0.0) 
                c = (c*seg->v*LperFT3+massin[m])/(vnew*LperFT3);
         
            c = MAX(0.0, c);
            seg->c[m] = c;
            MSX.Tank[i].c[m] = c;
        }
        seg->v += vnet;
        seg->v = MAX(0, seg->v);
    }

// --- update species equilibrium 

    if ( vin > 0.0 ) MSXchem_equil(NODE, i, MSX.Tank[i].c);
}

//=============================================================================

void  MSXtank_mix2(int i, double vin, double *massin, double vnet)
/*
**   Purpose: 2-compartment tank model                      
**
**   Input:   i = tank index
**            vIn = volume of inflow to tank (ft3)
**            massin = massinflow
**            vnet  = inflow - outflow
*/
{
    int     k, m, n;
    double  vt,                         //transferred volume        
            vmz;                        //full mixing zone volume
    Pseg    mixzone,                      // Mixing zone segment
            stagzone;                     // Stagnant zone segment

// --- find inflows & outflows 

    n = MSX.Tank[i].node;

// --- get segments for each zone

    k = MSX.Nobjects[LINK] + i;
    mixzone = MSX.LastSeg[k];
    stagzone = MSX.FirstSeg[k];
    if (mixzone == NULL || stagzone == NULL) return;


    // Full mixing zone volume
    vmz = MSX.Tank[i].vMix;

    vt = 0.0;


// --- case of net filling (vnet > 0)

    if (vnet > 0.0)
    {
        vt = MAX(0.0, (mixzone->v + vnet - vmz));
        if (vin > 0)
        {
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            {
                if (MSX.Species[m].type != BULK) continue;

                // --- new quality in mixing zone
                mixzone->c[m] = (mixzone->c[m] * mixzone->v * LperFT3 + massin[m]) / ((mixzone->v + vin)*LperFT3);
                mixzone->c[m] = MAX(0.0, mixzone->c[m]);
            }
        }
        if (vt > 0)
        {
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            {
                if (MSX.Species[m].type != BULK) continue;

                // --- new quality in stagnant zone

                stagzone->c[m] = (stagzone->c[m] * stagzone->v + mixzone->c[m] * vt) / (stagzone->v + vt);
                stagzone->c[m] = MAX(0.0, stagzone->c[m]);
            }



        }
    }
    else if (vnet < 0) //tank is draining
    {
        if (stagzone->v > 0.0) vt = MIN(stagzone->v, (-vnet));
        if (vin + vt > 0.0)
        {
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            {
                if (MSX.Species[m].type != BULK) continue;

                // --- new quality in mixing zone
                mixzone->c[m] = (mixzone->c[m] * mixzone->v * LperFT3 + massin[m] + stagzone->c[m]*vt*LperFT3) / ((mixzone->v + vin + vt)*LperFT3);
                mixzone->c[m] = MAX(0.0, mixzone->c[m]);
            }
        }
    }
        
    // Update segment volumes
    if (vt > 0.0)
    {
        mixzone->v = vmz;
        if (vnet > 0.0) stagzone->v += vt;
        else            stagzone->v = MAX(0.0, ((stagzone->v) - vt));
    }
    else
    {
        mixzone->v += vnet;
        mixzone->v = MIN(mixzone->v, vmz);
        mixzone->v = MAX(0.0, mixzone->v);
        stagzone->v = 0.0;
    }

    if (mixzone->v > 0.0) MSXchem_equil(NODE, i, mixzone->c);
    if (stagzone->v > 0.0) MSXchem_equil(NODE, i, stagzone->c);

// --- use quality of mixed compartment (mixzone) to represent quality
//     of tank since this is where outflow begins to flow from

    for (m=1; m<=MSX.Nobjects[SPECIES]; m++) MSX.Tank[i].c[m] = mixzone->c[m];
}

//=============================================================================

void  MSXtank_mix3(int i, double vin, double *massin, double vnet)
/*
**   Purpose: computes concentrations in the segments that form a
**            first-in-first-out (FIFO) tank model.
**                    
**   Input:   i   = tank index
**            vIn = volume of inflow to tank (ft3)
**            massin = mass inflow
**            vnet = inflow - outflow    
*/
{
   int    k, m, n;
   double vout, vseg, vsum;
   Pseg   seg;

// --- find inflows & outflows

    k = MSX.Nobjects[LINK] + i;
    n = MSX.Tank[i].node;
    vout = vin - vnet;
    
    if (MSX.LastSeg[k] == NULL || MSX.FirstSeg[k] == NULL) return;

    if (vin > 0.0)
    {

    // --- quality is the same, so just add flow volume to last seg
        seg = MSX.LastSeg[k];
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        {
            MSX.C1[m] = massin[m] / (vin*LperFT3);
        }
        if (seg != NULL && MSXqual_isSame(seg->c, MSX.C1))
        {
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
                seg->c[m] = (seg->c[m] * seg->v + MSX.C1[m] * vin) / (seg->v + vin);
            seg->v += vin;
        }
     // --- Otherwise add a new seg to tank
        else 
        {
            seg = MSXqual_getFreeSeg(vin, MSX.C1);
            MSXqual_addSeg(k, seg);
        }
    }


// --- initialize outflow volume & concentration

    vsum = 0.0;
    for (m=1; m<=MSX.Nobjects[SPECIES]; m++) 
        MSX.C1[m] = 0.0;
// --- withdraw flow from first segment

    while (vout > 0.0)
    {
    // --- get volume of current first segment
        seg = MSX.FirstSeg[k];
        if (seg == NULL) break;
        vseg = seg->v;
        vseg = MIN(vseg, vout);
        if ( seg == MSX.LastSeg[k] ) vseg = vout;

    // --- update mass & volume removed
        vsum += vseg;
        for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
        {
            MSX.C1[m] += (seg->c[m]) * vseg * LperFT3;
        }

    // --- decrease vOut by volume of first segment
        vout -= vseg;

    // --- remove segment if all its volume is consumed
        if (vout >= 0.0 && vseg >= seg->v)
        {
            if (seg->prev)
            {
                MSX.FirstSeg[k] = seg->prev;
             //   MSXqual_removeSeg(seg);
                seg->prev = MSX.FreeSeg;
                MSX.FreeSeg = seg;

            }
        }

    // --- otherwise just adjust volume of first segment
        else  seg->v -= vseg;
    }

// --- use quality from first segment to represent overall
//     quality of tank since this is where outflow flows from

    for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
    {
        if (vsum > 0.0) MSX.Tank[i].c[m] = MSX.C1[m]/(vsum * LperFT3);
        else if (MSX.FirstSeg[k] == NULL) MSX.Tank[i].c[m] = 0.0;
        else            MSX.Tank[i].c[m] = MSX.FirstSeg[k]->c[m];
    }
// --- add new last segment for new flow entering tank
}

//=============================================================================

void  MSXtank_mix4(int i, double vin, double *massin, double vnet)
/*
**----------------------------------------------------------
**   Input:   i = tank index
**            vin = volume of inflow to tank (ft3)
**            massin = mass inflow
**            vnet = vin - vout     
**   Output:  none
**   Purpose: Last In-First Out (LIFO) tank model                     
**----------------------------------------------------------
*/
{
   int    k, m, n;
   double vsum, vseg;
   Pseg   seg;

// --- find inflows & outflows

    k = MSX.Nobjects[LINK] + i;
    n = MSX.Tank[i].node;

    if (MSX.LastSeg[k] == NULL || MSX.FirstSeg[k] == NULL) return;

// --- keep track of total volume & mass removed from tank

    vsum = 0.0;
    if (vin > 0)
    {
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            MSX.C1[m] = massin[m] / (vin*LperFT3);
    }
    else
    {
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            MSX.C1[m] = 0;
    }

    for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
        MSX.Tank[i].c[m] = MSX.LastSeg[k]->c[m];

    seg = MSX.LastSeg[k];
// --- if tank filling, then create a new last segment
    if ( vnet > 0.0 )
    {

    // --- inflow quality = last segment quality so just expand last segment
        if (seg != NULL && MSXqual_isSame(seg->c, MSX.C1))
        {
            for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
                seg->c[m] = (seg->c[m] * seg->v + MSX.C1[m] * vnet) / (seg->v + vnet);
            seg->v += vnet;
        }

    // --- otherwise add a new last segment to tank

        else
        {
            seg = MSXqual_getFreeSeg(vnet, MSX.C1);
            MSXqual_addSeg(k, seg);
        }

    // --- quality of tank is that of inflow

        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            MSX.Tank[i].c[m] = MSX.LastSeg[k]->c[m];

    }

// --- if tank emptying then remove last segments until vNet consumed

    else if (vnet < 0.0)
    {
        for (m = 1; m <= MSX.Nobjects[SPECIES]; m++)
            MSX.C1[m] = 0;
    // --- keep removing volume from last segments until vNet is removed
        vsum = 0;
        vnet = -vnet;
        MSXqual_reversesegs(k);
        while (vnet > 0.0)
        {

        // --- get volume of current last segment
            seg = MSX.FirstSeg[k];
            if ( seg == NULL ) break;
            vseg = seg->v;
            vseg = MIN(vseg, vnet);
            if ( seg == MSX.LastSeg[k] ) vseg = vnet;

        // --- update mass & volume removed
            vsum += vseg;
            for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
                MSX.C1[m] += (seg->c[m])*vseg*LperFT3;

        // --- reduce vNet by volume of last segment
            vnet -= vseg;

        // --- remove segment if all its volume is used up
            if (vnet >= 0.0 && vseg >= seg->v)
            {
                if (seg->prev)
                {
                    MSX.FirstSeg[k] = seg->prev;
                    MSXqual_removeSeg(seg);

                }
            }
        // --- otherwise just reduce volume of last segment
            else
            {
                seg->v -= vseg;
            }
        }
        MSXqual_reversesegs(k);
    // --- tank quality is mixture of flow released and any inflow
        
        vsum = vsum + vin;
        for (m=1; m<=MSX.Nobjects[SPECIES]; m++)
        {
            if (vsum > 0.0)
                MSX.Tank[i].c[m] = (MSX.C1[m] + massin[m]) / (vsum*LperFT3);
        }
    }
}         
