/*! \file
 
    util.h

    Declarations of general utility macros and functions.
*/

#ifndef _IEGEN_UTIL_H
#define _IEGEN_UTIL_H

#include <stdlib.h>
#include <stdio.h>
#include <strings.h>    // needed for bcopy
#include <assert.h>

//! p is the pointer, typ is the data type, and sz is the number of that type
#define MALLOC(p, typ, sz)  { if (!(p = (typ *)malloc((sz) * sizeof(typ)))) { \
                                    printf("MALLOC: No more space!!\n"); exit(1); } }

#define FREE(x, typ, sz)  {if (sz != 0 && x !=NULL) free(x);}

#define MAXBUF 256

// --------------------- Testing

//! Print the values of the integer array as space delimited to stdout.
void printArray(int *array, int num);
void printRealArray(double *array, int num);

//! Compare the values of two different double arrays and return true if equal.
bool compareRealArrays(double *a1, double *a2, int num);

// --------------------- Functionality for reordering data

//! Makes index arrays point to new data locations.
void pointerUpdate(int *index_array, int ia_size, int *old2new, int n_nodes);

//! Reorder an array in place using the mapping in old2new array.
void reorderArray(unsigned char *ptr, int elem_size, int n_nodes, int *old2new);


#define REPOSITION(tmp, x, n_nodes, u_sz, ind) { \
    int i, j;                                   \
    bcopy (x, tmp, n_nodes*u_sz);               \
    if (u_sz % sizeof(double) == 0) {           \
      double *dtmp=(double*)tmp, *dx=(double*)x;\
      int du_sz = u_sz/sizeof(double);          \
      if (du_sz == 1) {                         \
        for (i=0; i<n_nodes; i++)               \
          dx[i] = dtmp[ind[i]];                 \
      } else {                                  \
        for (i=0; i<n_nodes; i++)               \
        for (j=0; j<du_sz; j++)                 \
          dx[i*du_sz+j] = dtmp[ind[i]*du_sz+j]; \
      }                                         \
    }                                           \
    else if (u_sz % sizeof(int) == 0) {         \
      int *itmp = (int*)tmp, *ix = (int*)x;     \
      int iu_sz = u_sz/sizeof(int);             \
      if (iu_sz == 1) {                         \
        for (i=0; i<n_nodes; i++)               \
          ix[i] = itmp[ind[i]];                 \
      } else {                                  \
        for (i=0; i<n_nodes; i++)               \
        for (j=0; j<iu_sz; j++)                 \
          ix[i*iu_sz+j] = itmp[ind[i]*iu_sz+j]; \
      }                                         \
    }                                           \
    else {                                      \
      if (u_sz == 1) {                          \
        for (i=0; i<n_nodes; i++)               \
          x[i] = tmp[ind[i]];                   \
      } else {                                  \
        for (i=0; i<n_nodes; i++)               \
        for (j=0; j<u_sz; j++)                  \
          x[i*u_sz+j] = tmp[ind[i]*u_sz+j];     \
      }                                         \
    }                                           \
}

#endif
