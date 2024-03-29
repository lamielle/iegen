/*! \file

    util.c

    Implementations for various utility functions such as reordering
    data arrays.
*/

#include "util.h"

static bool debug = true;

void null_int_array(int **array)
{
    *array=NULL;
}

void null_double_array(double **array)
{
    *array=NULL;
}

void alloc_int_array(int **array,int len)
{
    null_int_array(array);
    *array=(int*)malloc(sizeof(int)*len);
}

void alloc_double_array(double **array,int len)
{
    null_double_array(array);
    *array=(double*)malloc(sizeof(double)*len);
}

void free_int_array(int **array)
{
    free(*array);
    null_int_array(array);
}

void free_double_array(double **array)
{
    free(*array);
    null_double_array(array);
}

void print_int_array(int *array, int len)
/*------------------------------------------------------------*//*!
  The given array of integers are printed space delimited.

  \param  array     pointer to integer array
  \param  len       number of integers in the array

  \author Michelle Strout 6/30/08, Alan LaMielle 5/13/09
*//*--------------------------------------------------------------*/
{
    int i;
    assert((NULL==array)?(len==0):(len>=0));
    for(i=0;i<len;i++)
    {
        printf("%d ",array[i]);
    }
}

void print_double_array(double *array, int len)
/*------------------------------------------------------------*//*!
  The given array of doubles are printed space delimited.

  \param  array     pointer to double array
  \param  len       number of doubles in the array

  \author Michelle Strout 6/30/08, Alan LaMielle 5/13/09
*//*--------------------------------------------------------------*/
{
    int i;
    assert((NULL==array)?(len==0):(len>=0));
    for (i=0;i<len;i++)
    {
        printf("%g ", array[i]);
    }
}

bool int_arrays_equal(int *a1, int *a2, int len)
/*------------------------------------------------------------*//*!
  Do an element-wise comparison of two int arrays.
  Both should have len items.
  Returns true if all elements are equal and false otherwise.

  \param  a1        pointer to int array 1
  \param  a2        pointer to int array 2
  \param  len       number of ints in each array

  \author Michelle Strout 6/30/08, Alan LaMielle 5/13/09
*//*--------------------------------------------------------------*/
{
    bool retval = true;
    int i;
    assert((NULL==a1)?(len==0):(len>=0));
    assert((NULL==a2)?(len==0):(len>=0));
    for (i=0; i<len; i++) {
        if (a1[i]!=a2[i]) { retval = false; break;}
    }
    return retval;
}

bool double_arrays_equal(double *a1, double *a2, int len)
/*------------------------------------------------------------*//*!
  Do an element-wise comparison of two double arrays.
  Both should have len items.
  Returns true if all elements are equal and false otherwise.

  \param  a1        pointer to double array 1
  \param  a2        pointer to double array 2
  \param  len       number of doubles in each array

  \author Michelle Strout 6/30/08, Alan LaMielle 5/13/09
*//*--------------------------------------------------------------*/
{
    bool retval = true;
    int i;
    assert((NULL==a1)?(len==0):(len>=0));
    assert((NULL==a2)?(len==0):(len>=0));
    for (i=0; i<len; i++) {
        if (a1[i]!=a2[i]) { retval = false; break;}
    }
    return retval;
}

void print_comparison(int *index_arrays[][3],int num_index_arrays,int index_array_len,double *data_arrays[][3],int num_data_arrays,int data_array_len,const char *row_labels[],const char *col_labels[3])
{
	bool compare[num_index_arrays+num_data_arrays][3];
	int i,num_rows;

	num_rows=num_index_arrays+num_data_arrays;

	/* Compare the given index and data arrays */
	for(i=0;i<num_index_arrays;i++)
	{
		compare[i][0]=int_arrays_equal(index_arrays[i][0],index_arrays[i][1],index_array_len);
		compare[i][1]=int_arrays_equal(index_arrays[i][0],index_arrays[i][2],index_array_len);
		compare[i][2]=int_arrays_equal(index_arrays[i][1],index_arrays[i][2],index_array_len);
	}
	for(i=0;i<num_data_arrays;i++)
	{
		compare[i+num_index_arrays][0]=double_arrays_equal(data_arrays[i][0],data_arrays[i][1],data_array_len);
		compare[i+num_index_arrays][1]=double_arrays_equal(data_arrays[i][0],data_arrays[i][2],data_array_len);
		compare[i+num_index_arrays][2]=double_arrays_equal(data_arrays[i][1],data_arrays[i][2],data_array_len);
	}

	/* Determine the maximum string length of the row and column labels */
	int max_row_len=0,curr_row_len;
	for(i=0;i<num_rows;i++)
	{
		curr_row_len=strlen(row_labels[i]);
		if(curr_row_len>max_row_len)
		{
			max_row_len=curr_row_len;
		}
	}
	int max_col_len=0,curr_col_len;
	for(i=0;i<3;i++)
	{
		curr_col_len=strlen(col_labels[i]);
		if(curr_col_len>max_col_len)
		{
			max_col_len=curr_col_len;
		}
	}

	/* Print the comparison results */
	char header_format[255],row_format[255];
	assert(max_col_len<255);
	assert(max_row_len<255);
	sprintf(header_format,"%%%ds %%%ds %%%ds %%%ds\n",max_row_len,max_col_len,max_col_len,max_col_len);
	sprintf(row_format,"%%%ds %%%dd %%%dd %%%dd\n",max_row_len,max_col_len,max_col_len,max_col_len);
	printf(header_format,"",col_labels[0],col_labels[1],col_labels[2]);
	for(i=0;i<num_rows;i++)
	{
		printf(row_format,row_labels[i],compare[i][0],compare[i][1],compare[i][2]);
	}
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
        print_int_array(old2new, ia_size);
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
        print_int_array(temp, ia_size);
    }

    // do pointer update for original array
    for (i=0; i<ia_size; i++) {
        index_array[i] = old2new[temp[i]];
    }

    FREE(temp, int, ia_size);
}

void reorderArray(unsigned char *ptr, int elem_size, int num_elem,
                  ExplicitRelation *old2new)
/*------------------------------------------------------------*//*!
  Takes the mapping specified by the reordering function old2new, which
  maps old data positions
  to new positions, and remaps the arrays pointed to by ptr.

  \param  ptr           pointer to array
  \param  elem_size     size of each element in array
  \param  num_elem      number of entries in array
  \param  old2new       mapping from old data position to new data position

  \author Michelle Strout 6/30/08
*//*--------------------------------------------------------------*/
{
    assert(elem_size>0);
    assert(ptr!=NULL);
    assert(old2new!=NULL);
    assert(num_elem>0);

    // create a temporary array
    unsigned char * temp;
    MALLOC (temp, unsigned char, num_elem*elem_size)

    // call macro that does reordering.  It uses temp.
    int * new2old;
    MALLOC(new2old, int, num_elem);
    int i;
    for (i=0; i<num_elem; i++) {
        new2old[ER_out_given_in(old2new,i)] = i;
    }
    REPOSITION(temp, ptr, num_elem, elem_size, new2old)

    // get rid of temporary arrays
    FREE(new2old, int, num_elem);
    FREE(temp, unsigned char, num_elem*elem_size);
}

