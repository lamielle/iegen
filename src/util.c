/*! \file

    util.c

    Implementations for various utility functions such as reordering
    data arrays.
*/

#include "util.h"

static bool debug = true;

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

void printRealArray(double *array, int num)
/*------------------------------------------------------------*//*!
  Doubles are printed space delimited followed by a newline.  

  \param  array     pointer to array
  \param  num       number of doubles in the array

  \author Michelle Strout 6/30/08
*//*--------------------------------------------------------------*/
{
    int i;
    for (i=0; i<num; i++) {
        printf("%g ", array[i]);
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

void pointerUpdate(int *index_array, int ia_size, int *old2new, int n_nodes)
/*------------------------------------------------------------*//*!
  Takes the mapping specified by the reordering function old2new, which
  maps old data positions to new positions
  and modifies the index_array values so that they point
  to the new locations.
              
  \param  index_array   contains values that index into data arrays
  \param  ia_size   size of the index array
  \param  old2new   mapping from new data position to old data position
  \param  n_nodes   number of entries in all arrays

  \author Michelle Strout 6/30/08
*//*--------------------------------------------------------------*/
{
    if (debug) {
        printf("\nIn pointerUpdate: old2new = ");
        printArray(old2new, ia_size);
    }

    int *temp;
    MALLOC(temp, int, ia_size);

    int i;
    for (i=0; i<ia_size; i++) {
        // index array should not index out of data array
        assert(index_array[i]<n_nodes);
        // copy old array into a temp
        temp[i] = index_array[i];
    }

    if (debug) {
        printf("\nIn pointerUpdate: temp = ");
        printArray(temp, ia_size);
    }

    // do pointer update for original array
    for (i=0; i<ia_size; i++) {
        index_array[i] = old2new[temp[i]]; 
    }
        
}

void reorderArray(unsigned char *ptr, int elem_size, int n_nodes, int *old2new)
/*------------------------------------------------------------*//*!
  Takes the mapping specified by the reordering function old2new, which
  maps old data positions
  to new positions, and remaps the arrays pointed to by ptr.  
              
  \param  ptr           pointer to array
  \param  elem_size     size of each element in array
  \param  n_nodes       number of entries in all arrays
  \param  old2new       mapping from old data position to new data position

  \author Michelle Strout 6/30/08
*//*--------------------------------------------------------------*/
{
    assert(elem_size>0);
    assert(ptr!=NULL);
    assert(old2new!=NULL);
    assert(n_nodes>0);

    // create a temporary array 
    unsigned char * temp;
    MALLOC (temp, unsigned char, n_nodes*elem_size)
    
    // call macro that does reordering.  It uses temp.
    int * new2old;
    MALLOC(new2old, int, n_nodes);
    int i;
    for (i=0; i<n_nodes; i++) {
        new2old[old2new[i]] = i;
    }
    REPOSITION(temp, ptr, n_nodes, elem_size, new2old)

    // get rid of temporary arrays
    FREE(new2old, int, n_nodes);
    FREE(temp, unsigned char, n_nodes*elem_size);
}

