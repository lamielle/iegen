/*! \file

    util.c

    Implementations for various utility functions such as reordering
    data arrays.
*/

#include "util.h"

void printArray(int *array, int num)
/*------------------------------------------------------------*//*!
  Integers are printed space delimited followed by a newline.  

  \param  array     pointer to array
  \param  num       number of integers in the array

  \author Michelle Strout 6/30/08
*//*--------------------------------------------------------------*/
{
    int i;
    for (i=0; i<num; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");
}

void reorderArrays(int n, long (*repos)[2], int *new2old, int n_nodes)
/*------------------------------------------------------------*//*!
  Takes the mapping specified by permutationi, 
  new2old (maps new data position
  to old), and remaps the n arrays pointed to in repos.  repos[i][0]
  points to the array and repos[i][1] specifies the size of
  each value in the array.
              
  \param  n   number of arrays
  \param  repos     info about arrays
  \param  new2old   mapping from new data position to old data position
  \param  n_nodes   number of entries in all arrays

  \author Michelle Strout 6/30/08, more modifications
          Michelle Strout 10/4/02, adapted from N_POSITION code
          in Hwansoo Han's code MISC/misc.h
*//*--------------------------------------------------------------*/
{
    int i, siz, siz0=0;
    unsigned char *ptr, *tx;
    if (repos != NULL) {   
      for (i = 0; i < n; i++) {   
        ptr = (unsigned char *)(repos[i][0]);            
        siz = (int) (repos[i][1]);
        if (siz > siz0) {
            FREE(tx, unsigned char, n_nodes*siz0)
            MALLOC (tx, unsigned char, n_nodes*siz)
        }
        REPOSITION(tx, ptr, n_nodes, siz, new2old)
        siz0 = siz;
      }
      FREE(tx, unsigned char, n_nodes*siz0)
    }
}

