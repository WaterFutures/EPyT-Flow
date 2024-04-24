
#ifndef SMATRIX_H
#define SMATRIX_H

#include "msxtypes.h"

/* ----------- SMATRIX.C ---------------*/
int     msx_createsparse(void);               /* Creates sparse matrix      */
int     allocsparse(void);                /* Allocates matrix memory    */
void    msx_freesparse(void);                 /* Frees matrix memory        */
int     buildlists(int);                  /* Builds adjacency lists     */
int     paralink(int, int, int);          /* Checks for parallel links  */
void    xparalinks(void);                 /* Removes parallel links     */
void    freelists(void);                  /* Frees adjacency lists      */
void    countdegree(void);                /* Counts links at each node  */
int     reordernodes(void);               /* Finds a node re-ordering   */
int     mindegree(int, int);              /* Finds min. degree node     */
int     growlist(int);                    /* Augments adjacency list    */
int     newlink(Padjlist);                /* Adds fill-ins for a node   */
int     linked(int, int);                 /* Checks if 2 nodes linked   */
int     addlink(int, int, int);           /* Creates new fill-in        */
int     storesparse(int);                 /* Stores sparse matrix       */
int     ordersparse(int);                 /* Orders matrix storage      */
void    transpose(int, int*, int*,        /* Transposes sparse matrix   */
    int*, int*, int*, int*, int*);
int     msx_linsolve(int, double*, double*, /* Solution of linear eqns.   */
    double*);               /* via Cholesky factorization */

#endif