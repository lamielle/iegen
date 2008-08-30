/*! \file        ExplicitRelation.c
    Implements the ExplicitRelation data structure for use with the PIES project.
*/

#include "ExplicitRelation.h"

int ER_calcIndex( ExplicitRelation* relptr, Tuple in_tuple )
/*----------------------------------------------------------------*//*! 
  \short Given an in tuple calculate the index into out_vals array where
         the out tuple is stored.  

    <pre>
        in_tuple: <x_0, x_1, ..., x_k>
        out_tuple will be stored at 
            out_vals[ (x_0*(RD_size(1)*...*RD_size(k)) 
                      + x_1*(RD_size(2)* ... *LD_size(k))
                      + x_k) * out_arity ]
    </pre>
         
    Assumes we are dealing with a function.
    
    FIXME? Possible performance problem.

  \author Michelle Strout 8/30/08
*//*----------------------------------------------------------------*/
{
    int i, j, index;
    index = 0;
    RectDomain * in_domain = ER_in_domain(relptr);
    // add up all the terms for each dimension of the in_tuple
    for (i=0; i<relptr->in_arity; i++) {
        // get element value from Tuple
        int term = Tuple_val(in_tuple, i);
        for (j=i+1; j<relptr->in_arity; j++) {
            term *= RD_size( j );
        }
        index += term;
    }
    
    return index * relptr->out_arity;
}

int ER_calcIndex( ExplicitRelation* relptr, int in_val )
/*----------------------------------------------------------------*//*! 
  \short Given an 1D in tuple (so just the single value) 
         calculates the index into out_vals array where
         the out tuple value is stored.  1D-to-1D arity specialization.

    <pre>
        in_tuple: <x_0>
        out_tuple will be stored at 
            out_vals[ x_0 * out_arity ]
    </pre>
         
    Assumes we are dealing with a function.
    
    FIXME? Possible performance problem.

  \author Michelle Strout 8/30/08
*//*----------------------------------------------------------------*/
{
    return in_val*relptr->out_arity;
}


ExplicitRelation* ER_ctor(int in_tuple_arity, int out_tuple_arity,
                          RectDomain *in_domain=NULL, bool isFunction=false)
/*----------------------------------------------------------------*//*! 
  \short Construct ExplicitRelation structure and return a ptr to it.

  Initializes the explicit relation to empty.
  
  If isFunction and in_domain is provided then,
  <ul>
    <li> will not need out_index because each in_val only has one out_val
    <li> Going to use multi-dim array addressing arithmetic to index into out_vals.  Each point in the in_domain will need out_arity spaces to store the associated output_tuple.  See ER_calcIndex() for more details.
  </ul>
  
  If in_domain provided, but do not know if it is a function
  <ul>
    <li> disallow calls to ER_out_given_in
    <li> instead of using the multidim array equation to index into out_vals will use it to index into out_index instead.  Need out_index to keep track of all the out tuples for a given in_tuple.
    <li> This is great, but since don't know number of out_tuples per in_tuple can only insert directly into this format if doing an ordered insert on the in_tuple.
  </ul>
  
  If isFunction, but no in_domain is provided.
  <ul>
    <li>Without an in_domain specification, we can't sort until after everything is put in.  Therefore, I think that if no in_domain is provided, then we should have insert just put all of the relations into the raw data array.  Each entry will take in_arity+out_arity spots in the raw_data array.  Insert can then keep track of the in_domain.
    <li>The fact that it is a function just means that we don't need the out_index array.
  </ul>
  
  \param in_tuple_arity     Arity of the input tuples.
  \param out_tuple_arity    Arity of the output tuples.
  \param in_domain          Min and max values of all entries in in_tuples.
  \param isFunction         Indicates each input tuple has only one output.

  \return Returns a ptr to the constructed ExplicitRelation structure.

  \author Michelle Strout 8/29/08
*//*----------------------------------------------------------------*/
{
    ExplicitRelation* self 
        = (ExplicitRelation*)malloc(sizeof(ExplicitRelation));
    
    self->in_arity = in_tuple_arity;
    self->out_arity = out_tuple_arity;  
    self->isFunction = isFunction;
    self->in_domain = in_domain;
    
    // if in_domain was not provided then create one to keep track of 
    // values observed within insert.
    if (in_domain != NULL) {
        self->in_domain_given = true;
        assert(self->in_arity == RD_arity(self->in_domain));
        
    // set up an "undefined" rectangular domain where the starting
    // ub is 0 and the starting lb is maxint.  That way when
    // actual values are inserted, the ub and lb will be properly
    // updated.
    } else {
        self->in_domain_given = false;
        self->in_domain = RD_ctor(self->in_arity);
        int i;
        for (i=0; i<self->in_arity; i++ ) {
            RD_set_lb( self->in_domain, INT_MAX );
            RD_set_ub( self->in_domain, 0 );
        }
    }
    
    // set up out_domain
    self->out_domain = RD_ctor(self->out_arity);
    int i;
    for (i=0; i<self->out_arity; i++ ) {
        RD_set_lb( self->out_domain, INT_MAX );
        RD_set_ub( self->out_domain, 0 );
    }
    
    self->in_vals = NULL;
    self->out_index = NULL;
    self->out_vals = NULL; 
    self->raw_data = NULL;
    self->raw_num = 0;
    
    self->in_vals_size = 0;
    self->out_index_size = 0;
    self->out_vals_size = 0;
    self->raw_data_size = 0;

    // By default not ordered.
    self->ordered_by_in = false;
    self->ordered_by_out = false;

    // check for special conditions
    if ( isFunction && in_domain!=NULL ) {
        self->ordered_by_in = true;
    }   
    
    return self;
}


/*----------------------------------------------------------------*//*! 
  \short Deallocate all memory for ExplicitRelation.
  
  The ExplicitRelation deletes the RectDomain for the in_domain,
  which may cause problems if the RectDomain pointer is being used
  elsewhere.

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
void ER_dtor( ExplicitRelation** self )
{
    if ((*self)->in_vals != NULL) { free((*self)->in_vals); }
    if ((*self)->out_index != NULL) { free((*self)->out_index); }
    if ((*self)->out_vals != NULL) { free((*self)->out_vals); }
    if ((*self)->raw_data != NULL) { free((*self)->raw_data); }
    if ((*self)->in_domain != NULL) { free((*self)->in_domain); }
    free(*self);
    *self = NULL;
}

Tuple Tuple_make(int x1)
/*----------------------------------------------------------------*//*! 
  \short Creates a 1D Tuple and returns a copy of it.

  \author Michelle Strout 8/23/08
*//*----------------------------------------------------------------*/
{
    // first create array to store single value
    // FIXME: pretty inefficient for 1D
    int * valptr = (int*)malloc(sizeof(int));
    
    // put values in array
    valptr[0] = x1;
    
    Tuple retval = { valptr, 1 };
    return retval;
}

Tuple Tuple_make(int x1, int x2)
/*----------------------------------------------------------------*//*! 
  \short Creates a 2D Tuple and returns a copy of it.

  \author Michelle Strout 8/23/08
*//*----------------------------------------------------------------*/
{
    // first create array to store both values
    int * valptr = (int*)malloc(sizeof(int)*2);
    
    // put values in array
    valptr[0] = x1;
    valptr[1] = x2;
    
    Tuple retval = { valptr, 2 };
    return retval;
}

Tuple Tuple_make(int x1, int x2, int x3)
/*----------------------------------------------------------------*//*! 
  \short Creates a 3D Tuple and returns a copy of it.

  \author Michelle Strout 8/23/08
*//*----------------------------------------------------------------*/
{
    // first create array to store both values
    int * valptr = (int*)malloc(sizeof(int)*3);
    
    // put values in array
    valptr[0] = x1;
    valptr[1] = x2;
    valptr[2] = x3;
    
    Tuple retval = { valptr, 3 };
    return retval;
}


int Tuple_val(Tuple t, int k)
/*----------------------------------------------------------------*//*! 
  \short Returns the value of the kth element in the tuple.

  \author Michelle Strout 8/30/08
*//*----------------------------------------------------------------*/
{
    // check that not attempting to index outside of the tuple
    assert(k >= 0  && k<t.arity );
    
    return t.valptr[k];
}

//! Helper routine for expanding an arrays data allocation.
static void expand_array( int** array_handle, int* array_size )
{
    // save old info
//    int* temp = *array_handle;
//    int old_size = *array_size;
//    int i;
            
    // create new array that is bigger
    *array_size += MEM_ALLOC_INCREMENT;
    *array_handle = (int*)realloc(*array_handle, (*array_size)*sizeof(int));
            
/*    // copy data from old array
    for (i=0; i<old_size; i++) {
        (*array_handle)[i] = temp[i];
    }

    // delete old array
    free(temp);
*/
}

/*----------------------------------------------------------------*//*! 
  \short Insert a relation, [in]->[out], into the explicit relation.  
  
  This function assumes that the relation has 1D-to-1D arity.

  Handles some memory management wrt the from and hgdata arrays.

  \author Michelle Strout 8/29/08
*//*----------------------------------------------------------------*/
void ER_insert(ExplicitRelation* self, int in_int, int out_int)
{    
    // assuming non-negative in and out values
    assert(in_int>=0 && out_int>=0);

    // if the relation is not a function
    // indicate that this relation is no longer ordered
    if (!self->isFunction) { self->ordered_by_in = false; }

    // if isFunction and know in_domain then 
    if (self->isFunction  && self->in_domain_given) {
        // check that in int is within bounds
        assert(in_int>=RD_lb(self->in_domain) 
               && in_int<=RD_ub(self->in_domain));  
               
        self->out_vals[ER_calcIndex(self, in_int)] = out_int;    
    
    // else must put all relations in raw_data array, set ordered_by_in = false
    } else {
        self->raw_data[self->raw_num ++ ] = out_int;

        // keep track of domain as things are being inserted
        if (in_int < RD_lb(self->in_domain, 0) ) {
            RD_set_lb( self->in_domain, 0, in_int );
        }
        if (in_int > RD_ub(self->in_domain, 0) ) {
            RD_set_ub( self->in_domain, 0, in_int );
        }
        
    }
                          
    // keep track of out tuple ub and lb whether the in_domain is
    // already known or not
    if (out_int < RD_lb(self->out_domain, 0) ) {
        RD_set_lb( self->out_domain, 0, out_int );
    }
    if (out_int > RD_ub(self->out_domain, 0) ) {
        RD_set_ub( self->out_domain, 0, out_int );
    }
    
    
    
    // since not inserting ordered by in, must keep track of
    // all the in_vals and will just assume that each in val
    // is unique to make things easier.
    // FIXME: does this mess up some assumptions made about the
    //      data structure elsewhere?
    self->in_count++;
        
    // if we are on the next unique in_tuple then check if we need to 
    // expand the array.
    if  (self->in_count + 1 > self->out_index_size) {
        expand_array( &(self->out_index), &(self->out_index_size) );
    }
    if  (self->in_count + 1 > self->in_vals_size) {
        expand_array( &(self->in_vals), &(self->in_vals_size) );
    }
    
    FIXME: LEFTOFF: This is going to be horribly inefficient.  I know how big this is going to be and I know that it is a function, I really want to take advantage of that information.  Not just because it would be more efficient, also because it would be easier to implement.  Do I need the more general case for dependences?
    
    
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
    // FIXME: not sure if this will be correct in all cases
    if (out_int > (self->out_count -1) ) {
        self->out_count = out_int+1;
    }

}


/*----------------------------------------------------------------*//*! 
  \short Insert a relation, [in]->[out], into the explicit relation.  
  
  This function assumes that the relation has 1D-to-1D arity and that
  the relations will be inserted in order based on the in integer.

  Handles some memory management wrt the from and hgdata arrays.

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
void ER_in_ordered_insert(ExplicitRelation* self, 
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
    
    // assuming non-negative in and out values
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

/*----------------------------------------------------------------*//*! 
  \short 1D-to-1D version. Given in val return single associated out val.

  \author Michelle Strout 8/23/08
*//*----------------------------------------------------------------*/
int ER_out_given_in( ExplicitRelation* relptr, int in_val)
{
    assert(in_val < relptr->in_count);
    return relptr->out_vals[in_val];
}

/*----------------------------------------------------------------*//*! 
  \short General version.  Given in_tuple return single associated out_tuple.

    FIXME: this is going to cause serious performance problems because
    it is doing a linear search through input tuples.

  \author Michelle Strout 8/23/08
*//*----------------------------------------------------------------*/
Tuple ER_out_given_in( ExplicitRelation* relptr, Tuple in_tuple)
{
    assert(0);  // not implemented yet
}


//! Returns the number of unique 1D output tuples seen
// FIXME: how could we generalize this?
int ER_getRangeCount( ExplicitRelation* self)
    { return self->out_count; }

//! Returns number of unique 1D input tuples seen
// FIXME: again specific to 1D
int ER_getDomainCount( ExplicitRelation* self)
    { return self->in_count; }


/*----------------------------------------------------------------*//*! 
  \short Ensure that the given explicit relation is ordered by in tuples.

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
void ER_order_by_in( ExplicitRelation* self )
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
void ER_dump( ExplicitRelation* self )
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