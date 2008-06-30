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

bool compareRealArrays(double *a1, double *a2, int num)
/*------------------------------------------------------------*//*!
  Do an element-wise comparison of two double arrays.
  Both should have num items.
  Returns  true if all elements are equal and false otherwise.

  \param  a1        pointer to array
  \param  a2        pointer to array
  \param  num       number of doubles in each array

  \author Michelle Strout 6/30/08
*//*--------------------------------------------------------------*/
{
    bool retval = true;
    int i;
    for (i=0; i<num; i++) {
        if (a1[i]!=a2[i]) { retval = false; }
    }
    return retval;
}

void pointerUpdate(int *index_array, int ia_size, int *new2old, int n_nodes)
/*------------------------------------------------------------*//*!
  Takes the mapping specified by permutationi, 
  new2old (maps new data position
  to old), and modifies the index_array values so that they point
  to the new locations.
              
  \param  index_array   contains values that index into data arrays
  \param  ia_size   size of the index array
  \param  new2old   mapping from new data position to old data position
  \param  n_nodes   number of entries in all arrays

  \author Michelle Strout 6/30/08
*//*--------------------------------------------------------------*/
{
    int *temp;
    MALLOC(temp, int, ia_size);

    int i;
    for (i=0; i<ia_size; i++) {
        // index array should not index out of data array
        assert(index_array[i]<n_nodes);
        // copy old array into a temp
        temp[i] = index_array[i];
    }

    // do pointer update for original array
    for (i=0; i<ia_size; i++) {
        index_array[i] = temp[new2old[i]]; 
    }
        
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

