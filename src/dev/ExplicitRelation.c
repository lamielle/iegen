/* ExplicitRelation.c */
#include "ExplicitRelation.h"
/*! \file 
    Implements the ExplicitRelation data structure for use with the PIES project.
*/

#include "ExplicitRelation.h"


ExplicitRelation* ExplicitRelation_ctor(int in_tuple_arity, 
                                        int out_tuple_arity) 
/*----------------------------------------------------------------*//*! 
  \short Construct ExplicitRelation structure and return a ptr to it.

  Initializes the explicit relation to empty.
  
  \param in_tuple_arity     Arity of the input tuples.
  \param out_tuple_arity    Arity of the output tuples.

  \return Returns a ptr to the constructed ExplicitRelation structure.

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
{
    ExplicitRelation* self 
        = (ExplicitRelation*)malloc(sizeof(ExplicitRelation));
    
    self->in_arity = in_tuple_arity;
    self->out_arity = out_tuple_arity;  
    
    self->in_count = 0;
    self->out_count = 0;
    
    self->in_vals = NULL;
    self->out_index = NULL;
    self->out_vals = NULL;  
    
    self->in_vals_size = 0;
    self->out_index_size = 0;
    self->out_vals_size = 0;

    // Default values.  The insertion routines should maintain these.
    // Do not change these lightly, it will cause problems.
    self->ordered_by_in = true;
    self->ordered_by_out = false;
    self->ordered_by_in_out = false;
    
    return self;
}

/*----------------------------------------------------------------*//*! 
  \short Deallocate all memory for ExplicitRelation

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
void ExplicitRelation_dtor( ExplicitRelation** self )
{
    if ((*self)->in_vals != NULL) { free((*self)->in_vals); }
    if ((*self)->out_index != NULL) { free((*self)->out_index); }
    if ((*self)->out_vals != NULL) { free((*self)->out_vals); }
    free(*self);
    *self = NULL;
}


//! Helper routine for expanding an arrays data allocation.
static void expand_array( int** array_handle, int* array_size )
{
    // save old info
    int* temp = *array_handle;
    int old_size = *array_size;
    int i;
            
    // create new array that is bigger
    *array_size += MEM_ALLOC_INCREMENT;
    *array_handle = (int*)calloc((*array_size),sizeof(int));
            
    // copy data from old array
    for (i=0; i<old_size; i++) {
        (*array_handle)[i] = temp[i];
    }

    // delete old array
    free(temp);
}


/*----------------------------------------------------------------*//*! 
  \short Insert a relation, [in]->[out], into the explicit relation.  
  
  This function assumes that the relation has 1D-to-1D arity and that
  the relations will be inserted in order based on the in integer.

  Handles some memory management wrt the from and hgdata arrays.

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
void ExplicitRelation_in_ordered_insert(ExplicitRelation* self, 
                                        int in_int, 
                                        int out_int)
{    
    // cannot insert an in tuple less than our current in tuple
    // due to ordered assumption
    assert(in_int+1 >= self->in_count);
    
    // we initially assume that things are inserted ordered
    // by the in tuple, so make sure that assumption has not
    // changed.
    assert(self->ordered_by_in);
    
    // assuming positive in and out values
    assert(in_int>=0 && out_int>=0);

    // first check whether inserting a new in_int
    // adding one to in_int because they are zero indexed
    if (self->in_count < (in_int+1)) {
        // number of unique input tuples is going to go up
        self->in_count += 1;
    
        // if we are on the next unique in_tuple then check if we need to 
        // expand the array.
        if  (self->in_count + 1 > self->out_index_size) {
            expand_array( &(self->out_index), &(self->out_index_size) );
        }
        
        // Set the end of the indices to nodes for this new in tuple to 
        // the same as the beginning, since currently haven't inserted any
        // relations for this in tuple.
        self->out_index[in_int+1] = self->out_index[in_int];
        
    }
    
    // Check that there is enough room to insert the relation's out tuple,
    // and if not then expand allocation for out_vals array.
    if (self->out_index[in_int+1] + 1 > self->out_vals_size) {
        expand_array( &(self->out_vals), &(self->out_vals_size) );
    }
    
    // insert [in_int] -> [out_int]
    self->out_vals[ self->out_index[in_int+1] ] = out_int;
    self->out_index[in_int+1]++;
    
    // if this output tuple numbers id is higher than any we have seen 
    // then increase the number out
    if (out_int > (self->out_count -1) ) {
        self->out_count = out_int+1;
    }

}

//! Returns the number of unique 1D output tuples seen
// FIXME: how could we generalize this?
int ExplicitRelation_getRangeCount( ExplicitRelation* self)
    { return self->out_count; }

//! Returns number of unique 1D input tuples seen
// FIXME: again specific to 1D
int ExplicitRelation_getDomainCount( ExplicitRelation* self)
    { return self->in_count; }


/*----------------------------------------------------------------*//*! 
  \short Ensure that the given explicit relation is ordered by in tuples.

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
void ExplicitRelation_order_by_in( ExplicitRelation* self )
{
    // for now just assert if this is not true
    // FIXME: eventually need to implement code that orders
    // all the data by the input tuple if the data is not already
    // ordered as such.
    assert(self->ordered_by_in);
}

/*----------------------------------------------------------------*//*! 
  \short Output text representation of relation to standard out.

  Format of output is one tuple pair per line.
  
    [in_tuple] -> [out_tuple]
    ...
    
  The values of other fields are also printed.

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
void ExplicitRelation_dump( ExplicitRelation* self )
{
    int in, p;
    
    printf("ExplicitRelation\n");
    printf("\tin_arity = %d\n", self->in_arity);
    printf("\tout_arity = %d\n", self->out_arity);
    printf("\tin_count = %d\n", self->in_count);
    printf("\tin_vals_size = %d\n", self->in_vals_size);
    printf("\tout_index_size = %d\n", self->out_index_size);
    printf("\tout_vals_size = %d\n", self->out_vals_size);
    
    // nicely formated list of integer tuple pairs in the relation
    if (self->in_arity==1 && self->out_arity==1) {
    
        for (in=0; in<self->in_count; in++) {
            for (p=self->out_index[in]; p<self->out_index[in+1]; p++) {
                printf("[%d] -> [%d]\n", in, self->out_vals[p]);
            }
        }
        
    } else {
        assert(0);  // needs implemented for more general arities
    }

    // rest of the raw data
    // FIXME: not keeping track of in_vals yet
    //printf("in_vals = "); 
    //printArray(self->in_vals, self->in_vals_size);
    printf("out_index = "); 
    printArray(self->out_index, self->in_count+1);
    printf("out_vals = "); 
    printArray(self->out_vals, self->out_index[self->in_count]);
}