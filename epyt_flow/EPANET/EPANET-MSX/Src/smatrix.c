/*
*******************************************************************
Modified from:

SMATRIX.C -- Sparse matrix routines for EPANET program, VERSION:    2.0.0.      
                                                                   

DATE:       5/8/00
AUTHOR:     L. Rossman
            US EPA - NRMRL
                                                                   
This module contains the sparse matrix routines used to solve    
a network's hydraulic equations. The entry points into this      
module are:                                                      
   msx_createsparse() -- called from openhyd() in HYDRAUL.C           
   msx_freesparse()   -- called from closehyd() in HYDRAUL.C           
   msx_linsolve()     -- called from netsolve() in HYDRAUL.C          
                                                                   
Createsparse() does the following:                               
   1. for each node, builds an adjacency list that identifies    
      all links connected to the node (see buildlists())         
   2. re-orders the network's nodes to minimize the number       
      of non-zero entries in the hydraulic solution matrix       
      (see reorder())                                            
   3. converts the adjacency lists into a compact scheme         
      for storing the non-zero coeffs. in the lower diagonal     
      portion of the solution matrix (see storesparse())         
Freesparse() frees the memory used for the sparse matrix.        
Linsolve() solves the linearized system of hydraulic equations.  

********************************************************************
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#include "hash.h"
#include "msxtypes.h"
#include "smatrix.h"
#include "dispersion.h"
#define  EXTERN  extern



//  External variables
//--------------------
extern MSXproject  MSX;                // MSX project data
#define ERRCODE(x) (errcode = ((errcode>100) ? (errcode) : (x)))




int  msx_createsparse()
/*
**--------------------------------------------------------------
** Input:   none                                                
** Output:  returns error code                                  
** Purpose: creates sparse representation of coeff. matrix      
**--------------------------------------------------------------
*/
{
   int errcode = 0;
   int njuncs = MSX.Nobjects[NODE] - MSX.Nobjects[TANK];

   /* Allocate data structures */
   ERRCODE(allocsparse());
   if (errcode) return(errcode);

   /* Build node-link adjacency lists with parallel links removed. */

   ERRCODE(buildlists(TRUE));   //TRUE localadjlists in 2.2
   if (!errcode)
   {
      xparalinks();    /* Remove parallel links */
      countdegree();   /* Find degree of each junction */
   }                   /* (= # of adjacent links)  */

   /* Re-order nodes to minimize number of non-zero coeffs.    */
   /* in factorized solution matrix. At same time, adjacency   */
   /* list is updated with links representing non-zero coeffs. */
   MSX.Dispersion.Ncoeffs = MSX.Nobjects[LINK];
   ERRCODE(reordernodes());

   /* Allocate memory for sparse storage of positions of non-zero */
   /* coeffs. and store these positions in vector NZSUB. */
   ERRCODE(storesparse(njuncs));

   /* Free memory used for adjacency lists and sort */
   /* row indexes in NZSUB to optimize msx_linsolve().  */
   if (!errcode) freelists();
   ERRCODE(ordersparse(njuncs));

   MSX.Dispersion.Aij = (double*)calloc(MSX.Dispersion.Ncoeffs + 1, sizeof(double));
   MSX.Dispersion.Aii = (double*)calloc(MSX.Nobjects[NODE]+1, sizeof(double));
   MSX.Dispersion.F = (double*)calloc(MSX.Nobjects[NODE]+1, sizeof(double));
   MSX.Dispersion.temp = (double*)calloc(MSX.Nobjects[NODE] + 1, sizeof(double));
   MSX.Dispersion.link = (int*)calloc(MSX.Nobjects[NODE] + 1, sizeof(int));
   MSX.Dispersion.first = (int*)calloc(MSX.Nobjects[NODE] + 1, sizeof(int));
   ERRCODE(MEMCHECK(MSX.Dispersion.Aij));
   ERRCODE(MEMCHECK(MSX.Dispersion.Aii));
   ERRCODE(MEMCHECK(MSX.Dispersion.F));
   ERRCODE(MEMCHECK(MSX.Dispersion.temp));
   ERRCODE(MEMCHECK(MSX.Dispersion.link));
   ERRCODE(MEMCHECK(MSX.Dispersion.first));

 //  MSX.Dispersion.md = (double*)calloc(MSX.Nobjects[SPECIES] + 1, sizeof(double));
 
   MSX.Dispersion.pipeDispersionCoeff = (double*)calloc(MSX.Nobjects[LINK] + 1, sizeof(double));
 


   ERRCODE(MEMCHECK(MSX.Dispersion.ld));
   ERRCODE(MEMCHECK(MSX.Dispersion.md));
 
 
   dispersion_open();

   /* Re-build adjacency lists without removing parallel */
   /* links for use in future connectivity checking.     */
   ERRCODE(buildlists(FALSE));   //FALSE buildadjlists in 2.2

   /* Free allocated memory */
   free(MSX.Dispersion.Degree);
   return(errcode);
}                        /* End of msx_createsparse */


int  allocsparse()
/*
**--------------------------------------------------------------
** Input:   none                                              
** Output:  returns error code                                
** Purpose: allocates memory for indexing the solution matrix 
**--------------------------------------------------------------
*/
{
   int errcode = 0;
   int nnodes = MSX.Nobjects[NODE];
   int nlinks = MSX.Nobjects[LINK];
   MSX.Dispersion.Aii = NULL;
   MSX.Dispersion.Aij = NULL;
   MSX.Dispersion.F = NULL;
   MSX.Dispersion.temp = NULL;
   MSX.Dispersion.link = NULL;
   MSX.Dispersion.first = NULL;

   MSX.Dispersion.Adjlist = (Padjlist *) calloc(nnodes+1,  sizeof(Padjlist));
   MSX.Dispersion.Order  = (int *)   calloc(nnodes+1,  sizeof(int));
   MSX.Dispersion.Row    = (int *)   calloc(nnodes+1,  sizeof(int));
   MSX.Dispersion.Ndx    = (int *)   calloc(nlinks+1,  sizeof(int));
   ERRCODE(MEMCHECK(MSX.Dispersion.Adjlist));
   ERRCODE(MEMCHECK(MSX.Dispersion.Order));
   ERRCODE(MEMCHECK(MSX.Dispersion.Row));
   ERRCODE(MEMCHECK(MSX.Dispersion.Ndx));
   return(errcode);
}


void  msx_freesparse()
/*
**----------------------------------------------------------------
** Input:   None                                                
** Output:  None                                                
** Purpose: Frees memory used for sparse matrix storage         
**----------------------------------------------------------------
*/
{
   freelists();
   FREE(MSX.Dispersion.Adjlist);
   FREE(MSX.Dispersion.Order);
   FREE(MSX.Dispersion.Row);
   FREE(MSX.Dispersion.Ndx);
   FREE(MSX.Dispersion.XLNZ);
   FREE(MSX.Dispersion.NZSUB);
   FREE(MSX.Dispersion.LNZ);
   FREE(MSX.Dispersion.Aii);
   FREE(MSX.Dispersion.Aij);
   FREE(MSX.Dispersion.F);
   FREE(MSX.Dispersion.link);
   FREE(MSX.Dispersion.first);
   FREE(MSX.Dispersion.temp);

   FREE(MSX.Dispersion.md);
 
   FREE(MSX.Dispersion.pipeDispersionCoeff);
   dispersion_close();




}                        /* End of msx_freesparse */


int  buildlists(int paraflag)
/*
**--------------------------------------------------------------
** Input:   paraflag = TRUE if list marks parallel links      
** Output:  returns error code                                
** Purpose: builds linked list of links adjacent to each node 
**--------------------------------------------------------------
*/
{
   int    i,j,k;
   int    pmark = 0;
   int    errcode = 0;
   int    nlinks = MSX.Nobjects[LINK];
   Padjlist  alink;
   
   freelists();
   MSX.Dispersion.Adjlist = (Padjlist*)calloc(MSX.Nobjects[NODE] + 1, sizeof(Padjlist));
   if (MSX.Dispersion.Adjlist == NULL) return 101;
   for (i = 0; i <= MSX.Nobjects[NODE]; i++)
       MSX.Dispersion.Adjlist[i] = NULL;

   /* For each link, update adjacency lists of its end nodes */
   for (k=1; k<=nlinks; k++)
   {
      i = MSX.Link[k].n1;
      j = MSX.Link[k].n2;
      if (paraflag) pmark = paralink(i,j,k);  /* Parallel link check */

      /* Include link in start node i's list */
      alink = (struct Sadjlist *) malloc(sizeof(struct Sadjlist));
      if (alink == NULL) return(101);
      if (!pmark) alink->node = j;
      else        alink->node = 0;           /* Parallel link marker */
      alink->link = k;
      alink->next = MSX.Dispersion.Adjlist[i];
      MSX.Dispersion.Adjlist[i] = alink;

      /* Include link in end node j's list */
      alink = (struct Sadjlist *) malloc(sizeof(struct Sadjlist));
      if (alink == NULL) return(101);
      if (!pmark) alink->node = i;
      else        alink->node = 0;           /* Parallel link marker */
      alink->link = k;
      alink->next = MSX.Dispersion.Adjlist[j];
      MSX.Dispersion.Adjlist[j] = alink;
   }
   if (errcode)freelists();
   return(errcode);
}                        /* End of buildlists */


int  paralink(int i, int j, int k)
/*
**--------------------------------------------------------------
** Input:   i = index of start node of link                    
**          j = index of end node of link                    
**          k = link index                                    
** Output:  returns 1 if link k parallels another link, else 0
** Purpose: checks for parallel links between nodes i and j   
**                                                            
**--------------------------------------------------------------
*/
{
   Padjlist alink;
   for (alink = MSX.Dispersion.Adjlist[i]; alink != NULL; alink = alink->next)
   {
      if (alink->node == j)     /* Link || to k (same end nodes) */
      {
         MSX.Dispersion.Ndx[k] = alink->link;  /* Assign Ndx entry to this link */
         return(1);
      }
   }
   MSX.Dispersion.Ndx[k] = k;                  /* Ndx entry if link not parallel */
   return(0);
}                        /* End of paralink */


void  xparalinks()
/*
**--------------------------------------------------------------
** Input:   none                                                
** Output:  none                                                
** Purpose: removes parallel links from nodal adjacency lists   
**--------------------------------------------------------------
*/
{
   int    i;
   Padjlist  alink,       /* Current item in adjacency list */
             blink;       /* Previous item in adjacency list */
   int nnodes = MSX.Nobjects[NODE];

   /* Scan adjacency list of each node */
   for (i=1; i<=nnodes; i++)
   {
      alink = MSX.Dispersion.Adjlist[i];              /* First item in list */
      blink = NULL;
      while (alink != NULL)
      {
         if (alink->node == 0)      /* Parallel link marker found */
         {
            if (blink == NULL)      /* This holds at start of list */
            {
               MSX.Dispersion.Adjlist[i] = alink->next;
               free(alink);             /* Remove item from list */
               alink = MSX.Dispersion.Adjlist[i];
            }
            else                    /* This holds for interior of list */
            {
               blink->next = alink->next;
               free(alink);             /* Remove item from list */
               alink = blink->next;
            }
         }
         else
         {
            blink = alink;          /* Move to next item in list */
            alink = alink->next;
         }
      }
   }
}                        /* End of xparalinks */


void  freelists()
/*
**--------------------------------------------------------------
** Input:   none                                                
** Output:  none                                                
** Purpose: frees memory used for nodal adjacency lists         
**--------------------------------------------------------------
*/
{
   int   i;
   Padjlist alink;
   int nnodes = MSX.Nobjects[NODE];

   if (MSX.Dispersion.Adjlist == NULL)
       return;
   for (i=0; i<=nnodes; i++)
   {
      for (alink = MSX.Dispersion.Adjlist[i]; alink != NULL; alink = MSX.Dispersion.Adjlist[i])
      {
         MSX.Dispersion.Adjlist[i] = alink->next;
         free(alink);
      }
   }
   free(MSX.Dispersion.Adjlist);
   MSX.Dispersion.Adjlist = NULL;
}                        /* End of freelists */


void  countdegree()
/*
**----------------------------------------------------------------
** Input:   none                                                
** Output:  none                                                
** Purpose: counts number of nodes directly connected to each node            
**----------------------------------------------------------------
*/
{
    int   i;
    Padjlist alink;

    int nnodes = MSX.Nobjects[NODE];
    int njuncs = MSX.Nobjects[NODE]-MSX.Nobjects[TANK];
    int errcode;

    errcode = 0;

    MSX.Dispersion.Degree = (int *)calloc(MSX.Nobjects[NODE] + 1, sizeof(int));
    ERRCODE(MEMCHECK(MSX.Dispersion.Degree));
    memset(MSX.Dispersion.Degree,0,(nnodes+1)*sizeof(int));

   /* NOTE: For purposes of node re-ordering, Tanks (nodes with  */
   /*       indexes above Njuncs) have zero degree of adjacency. */

    for (i=1; i<=njuncs; i++)
        for (alink = MSX.Dispersion.Adjlist[i]; alink != NULL; alink = alink->next)
            if (alink->node > 0) MSX.Dispersion.Degree[i]++;
}


int   reordernodes()
/*
**--------------------------------------------------------------
** Input:   none                                                
** Output:  returns 1 if successful, 0 if not                   
** Purpose: re-orders nodes to minimize # of non-zeros that     
**          will appear in factorized solution matrix           
**--------------------------------------------------------------
*/
{
   int k, knode, m, n;
   int nnodes = MSX.Nobjects[NODE];
   int njuncs = MSX.Nobjects[NODE] - MSX.Nobjects[TANK];
   for (k=1; k<=nnodes; k++)
   {
      MSX.Dispersion.Row[k] = k;
      MSX.Dispersion.Order[k] = k;
   }
   n = njuncs;
   for (k=1; k<=n; k++)                   /* Examine each junction    */
   {
      m = mindegree(k,n);                 /* Node with lowest degree  */
      knode = MSX.Dispersion.Order[m];                   /* Node's index             */
      if (!growlist(knode)) return(101);  /* Augment adjacency list   */
      MSX.Dispersion.Order[m] = MSX.Dispersion.Order[k];                /* Switch order of nodes    */
      MSX.Dispersion.Order[k] = knode;
      MSX.Dispersion.Degree[knode] = 0;                  /* In-activate node         */
   }
   for (k=1; k<=n; k++)                   /* Assign nodes to rows of  */
     MSX.Dispersion.Row[MSX.Dispersion.Order[k]] = k;                   /*   coeff. matrix          */
   return(0);
}                        /* End of reordernodes */


int  mindegree(int k, int n)
/*
**--------------------------------------------------------------
** Input:   k = first node in list of active nodes              
**          n = total number of junction nodes                  
** Output:  returns node index with fewest direct connections     
** Purpose: finds active node with fewest direct connections
**--------------------------------------------------------------
*/
{
   int i, m;
   int min = n,
       imin = n;

   for (i=k; i<=n; i++)
   {
      m = MSX.Dispersion.Degree[MSX.Dispersion.Order[i]];
      if (m < min)
      {
         min = m;
         imin = i;
      }
   }
   return(imin);
}                        /* End of mindegree */


int  growlist(int knode)
/*
**--------------------------------------------------------------
** Input:   knode = node index                                  
** Output:  returns 1 if successful, 0 if not                   
** Purpose: creates new entries in knode's adjacency list for   
**          all unlinked pairs of active nodes that are         
**          adjacent to knode                                   
**--------------------------------------------------------------
*/
{
   int   node;
   Padjlist alink;

   /* Iterate through all nodes connected to knode */
   for (alink = MSX.Dispersion.Adjlist[knode]; alink != NULL; alink = alink -> next)
   {
      node = alink->node;       /* End node of connecting link  */
      if (MSX.Dispersion.Degree[node] > 0)     /* End node is active           */
      {
         MSX.Dispersion.Degree[node]--;        /* Reduce degree of adjacency   */
         if (!newlink(alink))   /* Add to adjacency list        */
            return(0);
      }
   }
   return(1);
}                        /* End of growlist */


int  newlink(Padjlist alink)
/*
**--------------------------------------------------------------
** Input:   alink = element of node's adjacency list            
** Output:  returns 1 if successful, 0 if not                   
** Purpose: links end of current adjacent link to end nodes of  
**          all links that follow it on adjacency list          
**--------------------------------------------------------------
*/
{
   int   inode, jnode;
   Padjlist blink;

   /* Scan all entries in adjacency list that follow anode. */
   inode = alink->node;             /* End node of connection to anode */
   for (blink = alink->next; blink != NULL; blink = blink->next)
   {
      jnode = blink->node;          /* End node of next connection */

      /* If jnode still active, and inode not connected to jnode, */
      /* then add a new connection between inode and jnode.       */
      if (MSX.Dispersion.Degree[jnode] > 0)        /* jnode still active */
      {
         if (!linked(inode,jnode))  /* inode not linked to jnode */
         {

            /* Since new connection represents a non-zero coeff. */
	    /* in the solution matrix, update the coeff. count.  */
            MSX.Dispersion.Ncoeffs++;

	    /* Update adjacency lists for inode & jnode to */
	    /* reflect the new connection.                 */
            if (!addlink(inode,jnode,MSX.Dispersion.Ncoeffs)) return(0);
            if (!addlink(jnode,inode,MSX.Dispersion.Ncoeffs)) return(0);
            MSX.Dispersion.Degree[inode]++;
            MSX.Dispersion.Degree[jnode]++;
         }
      }
   }
   return(1);
}                        /* End of newlink */


int  linked(int i, int j)
/*
**--------------------------------------------------------------
** Input:   i = node index                                      
**          j = node index                                      
** Output:  returns 1 if nodes i and j are linked, 0 if not     
** Purpose: checks if nodes i and j are already linked.         
**--------------------------------------------------------------
*/
{
   Padjlist alink;
   for (alink = MSX.Dispersion.Adjlist[i]; alink != NULL; alink = alink->next)
      if (alink->node == j) return(1);
   return(0);
}                        /* End of linked */


int  addlink(int i, int j, int n)
/*
**--------------------------------------------------------------
** Input:   i = node index                                      
**          j = node index                                      
**          n = link index                                      
** Output:  returns 1 if successful, 0 if not                   
** Purpose: augments node i's adjacency list with node j        
**--------------------------------------------------------------
*/
{
   Padjlist alink;
   alink = (struct Sadjlist *) malloc(sizeof(struct Sadjlist));
   if (alink == NULL) return(0);
   alink->node = j;
   alink->link = n;
   alink->next = MSX.Dispersion.Adjlist[i];
   MSX.Dispersion.Adjlist[i] = alink;
   return(1);
}                        /* End of addlink */


int  storesparse(int n)
/*
**--------------------------------------------------------------
** Input:   n = number of rows in solution matrix               
** Output:  returns error code                                  
** Purpose: stores row indexes of non-zeros of each column of   
**          lower triangular portion of factorized matrix       
**--------------------------------------------------------------
*/
{
   Padjlist alink;
   int   i, ii, j, k, l, m;
   int   errcode = 0;

   /* Allocate sparse matrix storage */
   MSX.Dispersion.XLNZ  = (int *) calloc(n+2, sizeof(int));
   MSX.Dispersion.NZSUB = (int *) calloc(MSX.Dispersion.Ncoeffs+2, sizeof(int));
   MSX.Dispersion.LNZ   = (int *) calloc(MSX.Dispersion.Ncoeffs+2, sizeof(int));
   ERRCODE(MEMCHECK(MSX.Dispersion.XLNZ));
   ERRCODE(MEMCHECK(MSX.Dispersion.NZSUB));
   ERRCODE(MEMCHECK(MSX.Dispersion.LNZ));
   if (errcode) return(errcode);

   /* Generate row index pointers for each column of matrix */
   k = 0;
   MSX.Dispersion.XLNZ[1] = 1;
   for (i=1; i<=n; i++)             /* column */
   {
       m = 0;
       ii = MSX.Dispersion.Order[i];
       for (alink = MSX.Dispersion.Adjlist[ii]; alink != NULL; alink = alink->next)
       {
          j = MSX.Dispersion.Row[alink->node];    /* row */
          l = alink->link;
          if (j > i && j <= n)
          {
             m++;
             k++;
             MSX.Dispersion.NZSUB[k] = j;
             MSX.Dispersion.LNZ[k] = l;
          }
       }
       MSX.Dispersion.XLNZ[i+1] = MSX.Dispersion.XLNZ[i] + m;
   }
   return(errcode);
}                        /* End of storesparse */


int  ordersparse(int n)
/*
**--------------------------------------------------------------
** Input:   n = number of rows in solution matrix               
** Output:  returns eror code                                   
** Purpose: puts row indexes in ascending order in NZSUB        
**--------------------------------------------------------------
*/
{
   int  i, k;
   int  *xlnzt, *nzsubt, *lnzt, *nzt;
   int  errcode = 0;

   xlnzt  = (int *) calloc(n+2, sizeof(int));
   nzsubt = (int *) calloc(MSX.Dispersion.Ncoeffs+2, sizeof(int));
   lnzt   = (int *) calloc(MSX.Dispersion.Ncoeffs+2, sizeof(int));
   nzt    = (int *) calloc(n+2, sizeof(int));
   ERRCODE(MEMCHECK(xlnzt));
   ERRCODE(MEMCHECK(nzsubt));
   ERRCODE(MEMCHECK(lnzt));
   ERRCODE(MEMCHECK(nzt));
   if (!errcode)
   {

      /* Count # non-zeros in each row */
      for (i=1; i<=n; i++) nzt[i] = 0;
      for (i=1; i<=n; i++)
      {
          for (k=MSX.Dispersion.XLNZ[i]; k<MSX.Dispersion.XLNZ[i+1]; k++) nzt[MSX.Dispersion.NZSUB[k]]++;
      }
      xlnzt[1] = 1;
      for (i=1; i<=n; i++) xlnzt[i+1] = xlnzt[i] + nzt[i];

      /* Transpose matrix twice to order column indexes */
      transpose(n,MSX.Dispersion.XLNZ,MSX.Dispersion.NZSUB,MSX.Dispersion.LNZ,xlnzt,nzsubt,lnzt,nzt);
      transpose(n,xlnzt,nzsubt,lnzt,MSX.Dispersion.XLNZ,MSX.Dispersion.NZSUB,MSX.Dispersion.LNZ,nzt);
   }

   /* Reclaim memory */
   free(xlnzt);
   free(nzsubt);
   free(lnzt);
   free(nzt);
   return(errcode);
}                        /* End of ordersparse */


void  transpose(int n, int *il, int *jl, int *xl, int *ilt, int *jlt,
                int *xlt, int *nzt)
/*
**---------------------------------------------------------------------
** Input:   n = matrix order                                           
**          il,jl,xl = sparse storage scheme for original matrix       
**          nzt = work array                                           
** Output:  ilt,jlt,xlt = sparse storage scheme for transposed matrix  
** Purpose: Determines sparse storage scheme for transpose of a matrix 
**---------------------------------------------------------------------
*/
{
   int  i, j, k, kk;

   for (i=1; i<=n; i++) nzt[i] = 0;
   for (i=1; i<=n; i++)
   {
      for (k=il[i]; k<il[i+1]; k++)
      {
         j = jl[k];
         kk = ilt[j] + nzt[j];
         jlt[kk] = i;
         xlt[kk] = xl[k];
         nzt[j]++;
      }
   }
}                        /* End of transpose */


int  msx_linsolve(int n, double *Aii, double *Aij, double *B)
/*
**--------------------------------------------------------------
** Input:   n    = number of equations                          
**          Aii  = diagonal entries of solution matrix          
**          Aij  = non-zero off-diagonal entries of matrix      
**          B    = right hand side coeffs.                      
** Output:  B    = solution values                              
**          returns 0 if solution found, or index of            
**          equation causing system to be ill-conditioned       
** Purpose: solves sparse symmetric system of linear            
**          equations using Cholesky factorization              
**                                                              
** NOTE:   This procedure assumes that the solution matrix has  
**         been symbolically factorized with the positions of   
**         the lower triangular, off-diagonal, non-zero coeffs. 
**         stored in the following integer arrays:              
**            XLNZ  (start position of each column in NZSUB)    
**            NZSUB (row index of each non-zero in each column) 
**            LNZ   (position of each NZSUB entry in Aij array) 
**                                                              
**  This procedure has been adapted from subroutines GSFCT and  
**  GSSLV in the book "Computer Solution of Large Sparse        
**  Positive Definite Systems" by A. George and J. W-H Liu      
**  (Prentice-Hall, 1981).                                      
**--------------------------------------------------------------
*/
{
  
   int    i, istop, istrt, isub, j, k, kfirst, newk;
   int    errcode = 0;
   double bj, diagj, ljk;

   memset(MSX.Dispersion.temp,0,(n+1)*sizeof(double));
   memset(MSX.Dispersion.link,0,(n+1)*sizeof(int));

   /* Begin numerical factorization of matrix A into L */
   /*   Compute column L(*,j) for j = 1,...n */
   for (j=1; j<=n; j++)
   {
      /* For each column L(*,k) that affects L(*,j): */
      diagj = 0.0;
      newk = MSX.Dispersion.link[j];
      k = newk;
      while (k != 0)
      {

         /* Outer product modification of L(*,j) by  */
         /* L(*,k) starting at first[k] of L(*,k).   */
         newk = MSX.Dispersion.link[k];
         kfirst = MSX.Dispersion.first[k];
         ljk = Aij[MSX.Dispersion.LNZ[kfirst]];
         diagj += ljk*ljk;
         istrt = kfirst + 1;
         istop = MSX.Dispersion.XLNZ[k+1] - 1;
         if (istop >= istrt)
         {

	     /* Before modification, update vectors 'first' */
	     /* and 'link' for future modification steps.   */
            MSX.Dispersion.first[k] = istrt;
            isub = MSX.Dispersion.NZSUB[istrt];
            MSX.Dispersion.link[k] = MSX.Dispersion.link[isub];
            MSX.Dispersion.link[isub] = k;

	    /* The actual mod is saved in vector 'temp'. */
            for (i=istrt; i<=istop; i++)
            {
               isub = MSX.Dispersion.NZSUB[i];
               MSX.Dispersion.temp[isub] += Aij[MSX.Dispersion.LNZ[i]]*ljk;
            }
         }
         k = newk;
      }

      /* Apply the modifications accumulated */
      /* in 'temp' to column L(*,j).         */
      diagj = Aii[j] - diagj;
      if (diagj <= 0.0)        /* Check for ill-conditioning */
      {
         errcode = j;
         return errcode;
      }
      diagj = sqrt(diagj);
      Aii[j] = diagj;
      istrt = MSX.Dispersion.XLNZ[j];
      istop = MSX.Dispersion.XLNZ[j+1] - 1;
      if (istop >= istrt)
      {
         MSX.Dispersion.first[j] = istrt;
         isub = MSX.Dispersion.NZSUB[istrt];
         MSX.Dispersion.link[j] = MSX.Dispersion.link[isub];
         MSX.Dispersion.link[isub] = j;
         for (i=istrt; i<=istop; i++)
         {
            isub = MSX.Dispersion.NZSUB[i];
            bj = (Aij[MSX.Dispersion.LNZ[i]] - MSX.Dispersion.temp[isub])/diagj;
            Aij[MSX.Dispersion.LNZ[i]] = bj;
            MSX.Dispersion.temp[isub] = 0.0;
         }
      }
   }      /* next j */

   /* Foward substitution */
   for (j=1; j<=n; j++)
   {
      bj = B[j]/Aii[j];
      B[j] = bj;
      istrt = MSX.Dispersion.XLNZ[j];
      istop = MSX.Dispersion.XLNZ[j+1] - 1;
      if (istop >= istrt)
      {
         for (i=istrt; i<=istop; i++)
         {
            isub = MSX.Dispersion.NZSUB[i];
            B[isub] -= Aij[MSX.Dispersion.LNZ[i]]*bj;
         }
      }
   }

   /* Backward substitution */
   for (j=n; j>=1; j--)
   {
      bj = B[j];
      istrt = MSX.Dispersion.XLNZ[j];
      istop = MSX.Dispersion.XLNZ[j+1] - 1;
      if (istop >= istrt)
      {
         for (i=istrt; i<=istop; i++)
         {
            isub = MSX.Dispersion.NZSUB[i];
            bj -= Aij[MSX.Dispersion.LNZ[i]]*B[isub];
         }
      }
      B[j] = bj/Aii[j];
   }

   return(errcode);
}                        /* End of msx_linsolve */


/************************ END OF SMATRIX.C ************************/

