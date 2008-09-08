/*! \file        ExplicitRelation.c
    Implements the ExplicitRelation data structure for use with the PIES project.
*/

#include "ExplicitRelation.h"

int ER_calcIndex( ExplicitRelation* relptr, Tuple in_tuple )
/*----------------------------------------------------------------*//*! 
  \short Given an in tuple calculate the index into out_vals array where
         the out tuple is stored.  If relptr is not storing a function
         then calculates index into out_index.

    <pre>
        in_tuple: <x_0, x_1, ..., x_k>
        out_tuple will be stored at 
            out_vals[ ((x_0-lb_0)*(RD_size(1)*...*RD_size(k)) 
                      + (x_1-lb_0)*(RD_size(2)* ... *RD_size(k))
                      + (x_k-lb_k)) * out_arity ]
    </pre>
         
    Or for a non function:
    <pre>
        in_tuple: <x_0, x_1, ..., x_k>
        index into out_vals will be stored at 
            out_index[ ((x_0-lb_0)*(RD_size(1)*...*RD_size(k)) 
                      + (x_1-lb_0)*(RD_size(2)* ... *RD_size(k))
                      + (x_k-lb_k)) * out_arity ]
    </pre>
    
    
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
        int term = Tuple_val(in_tuple, i) - RD_lb(in_domain,i);
        for (j=i+1; j<relptr->in_arity; j++) {
            term *= RD_size( in_domain, j );
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
            out_vals[ (x_0-lb_0) * out_arity ]
    </pre>
         
    Assumes we are dealing with a function.
    
    FIXME? Possible performance problem.

  \author Michelle Strout 8/30/08
*//*----------------------------------------------------------------*/
{
    assert(relptr->isFunction);
    
    return (in_val-RD_lb(relptr->in_domain,0) )*relptr->out_arity;
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

    self->in_vals = NULL;
    self->unique_in_count = 0;
    self->out_index = NULL;
    self->out_vals = NULL; 
    self->raw_data = NULL;
    self->raw_num = 0;
    
    self->in_vals_size = 0;
    self->out_index_size = 0;
    self->out_vals_size = 0;
    self->raw_data_size = 0;
    
    // if in_domain was not provided then create one to keep track of 
    // values observed within insert.
    if (in_domain != NULL) {
        self->in_domain_given = true;
        assert(self->in_arity == RD_dim(self->in_domain));
        
        // with a known in_domain, we know how big out_vals array must be
        self->out_vals_size 
            = self->out_arity *  RD_size(self->in_domain);
        self->out_vals = (int*)malloc(self->out_vals_size*sizeof(int));
        
    // set up an "undefined" rectangular domain where the starting
    // ub is 0 and the starting lb is maxint.  That way when
    // actual values are inserted, the ub and lb will be properly
    // updated.
    } else {
        self->in_domain_given = false;
        self->in_domain = RD_ctor(self->in_arity);
        int i;
        for (i=0; i<self->in_arity; i++ ) {
            RD_set_lb( self->in_domain, i, INT_MAX );
            RD_set_ub( self->in_domain, i, 0 );
        }
    }
    
    // set up out_range
    self->out_range = RD_ctor(self->out_arity);
    int i;
    for (i=0; i<self->out_arity; i++ ) {
        RD_set_lb( self->out_range, i, INT_MAX );
        RD_set_ub( self->out_range, i, 0 );
    }

    // By default ordered by in tuples.  Will change if generic insert is
    // used.
    self->ordered_by_in = true;
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

bool Tuple_in_domain(Tuple t, RectDomain * rd)
/*----------------------------------------------------------------*//*! 
  \short Indicates with Tuple t is inside domain rd.

  \author Michelle Strout 9/2/08
*//*----------------------------------------------------------------*/
{
    // check that the Tuple and RectDomain have same dimensionality
    if (t.arity != RD_dim(rd)) {
        return false;
    }
    
    // check that the tuple values lie within bounds.
    int i;
    for (i=0; i<t.arity; i++) {
        if ( t.valptr[i] < RD_lb(rd,i) || t.valptr[i] > RD_ub(rd,i) ) {
            return false;
        }
    }
    
    return true;
}

bool Tuple_equal(Tuple t1, Tuple t2)
/*----------------------------------------------------------------*//*! 
  \short Returns true if given tuples are equal.

  \author Michelle Strout 9/2/08
*//*----------------------------------------------------------------*/
{
    if (t1.arity != t2.arity) {
        return false;
    }
    int k;
    for (k=0; k<t1.arity; k++) {
        if ( t1.valptr[k] != t2.valptr[k] ) {
            return false;
        }
    }
    return true;
}

int Tuple_compare( Tuple t1, Tuple t2)
/*----------------------------------------------------------------*//*! 
  \short Returns -1, 0, or 1 depending on whether t1 is <, =, or > than t2.
  
  FIXME: should probably replace Tuple_equal calls to calls to this?
  This is less lenient though.  It assumes both tuples have the same
  arity.

  \author Michelle Strout 9/4/08
*//*----------------------------------------------------------------*/
{
    if (t1.arity != t2.arity) {
        assert(0);
    }
    int k;
    for (k=0; k<t1.arity; k++) {
        if ( t1.valptr[k] < t2.valptr[k] ) {
            return -1;
        } else if ( t1.valptr[k] < t2.valptr[k] ) {
            return 1;
        }
    }
    // All elements in tuples were equal.
    return 0;
}


//! Helper routine for expanding an arrays data allocation.
//! Guarantees that the newly expanded part of the array is 
//! set to zero.
static void expand_array( int** array_handle, int* array_size )
{
    // save old info
//    int* temp = *array_handle;
    int old_size = *array_size;
    int i;
            
    // create new array that is bigger
    *array_size += MEM_ALLOC_INCREMENT;
    *array_handle = (int*)realloc(*array_handle, (*array_size)*sizeof(int));
    
    // Want to make sure that the newly allocated spaces at the 
    // end of the array are all set to zero.  realloc does not guarantee that.
    for (i=old_size; i<*array_size; i++) {
        (*array_handle)[i] = 0;
    }
    
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

    // For now just use the more general insert.
    ER_insert(self, Tuple_make(in_int), Tuple_make(out_int));
    
/*  Might use this code if we decide to specialize for 1Dto1D arity.
    // assuming non-negative in and out values
    assert(in_int>=0 && out_int>=0);

    // if the relation is not a function
    // indicate that this relation is no longer ordered
    if (!self->isFunction) { self->ordered_by_in = false; }

    // if isFunction and know in_domain then 
    if (self->isFunction  && self->in_domain_given) {
        // check that in int is within bounds
        assert(in_int>=RD_lb(self->in_domain, 0) 
               && in_int<=RD_ub(self->in_domain, 0));  
               
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
    if (out_int < RD_lb(self->out_range, 0) ) {
        RD_set_lb( self->out_range, 0, out_int );
    }
    if (out_int > RD_ub(self->out_range, 0) ) {
        RD_set_ub( self->out_range, 0, out_int );
    }
*/    
    

}


/*----------------------------------------------------------------*//*! 
  \short Insert a relation, [in]->[out], into the explicit relation.  
  
  This function handles general in and out arity.

  Handles some memory management wrt to the raw_data, out_vals, etc arrays.

  \author Michelle Strout 9/2/08
*//*----------------------------------------------------------------*/
void ER_insert(ExplicitRelation* self, Tuple in_tuple, Tuple out_tuple)
{    
    int k;

    // if the relation is not a function
    // indicate that this relation is no longer ordered
    if (!self->isFunction) { self->ordered_by_in = false; }

    // if isFunction and know in_domain then 
    if (self->isFunction  && self->in_domain_given) {
        // check that in Tuple is within bounds
        assert(Tuple_in_domain(in_tuple , self->in_domain) );  
               
        // insert output tuple values into locations in out_vals
        // associated with this input tuple
        assert( self->out_arity == out_tuple.arity );
        
        // do actual insertion of output tuple
        int start_index = ER_calcIndex(self, in_tuple);
        for (k=0; k< self->out_arity; k++) {        
            self->out_vals[start_index+k] = out_tuple.valptr[k];
        }
    
    // else must put all relations in raw_data array, set ordered_by_in = false
    } else {
        // Check tuple arities.
        assert( self->out_arity == out_tuple.arity
                && self->in_arity == in_tuple.arity );

        // indicate not doing ordered insert.
        self->ordered_by_in = false;
        
        // make sure there is enough room in the array
        if  (self->raw_num + self->in_arity + self->out_arity 
             > self->raw_data_size) 
        {
            expand_array( &(self->raw_data), &(self->raw_data_size) );
        }

        // Insert in_tuple and out_tuple into the raw_data array.
        for (k=0; k<self->in_arity; k++) {
            self->raw_data[self->raw_num ++ ] = in_tuple.valptr[k];

            // keep track of domain as things are being inserted
            if (in_tuple.valptr[k] < RD_lb(self->in_domain, k) ) {
                RD_set_lb( self->in_domain, k, in_tuple.valptr[k] );
            }
            if (in_tuple.valptr[k] > RD_ub(self->in_domain, k) ) {
                RD_set_ub( self->in_domain, k, in_tuple.valptr[k] );
            }
        }
        for (k=0; k<self->out_arity; k++) {
            self->raw_data[self->raw_num ++ ] = out_tuple.valptr[k];
            
            // see below for keeping track of out_tuple bounds
        }
        
    }
                          
    // keep track of out tuple ub and lb whether the in_domain is
    // already known or not
    for (k=0; k<self->out_arity; k++) {
        if (out_tuple.valptr[k] < RD_lb(self->out_range, k) ) {
            RD_set_lb( self->out_range, k, out_tuple.valptr[k] );
        }
        if (out_tuple.valptr[k] > RD_ub(self->out_range, k) ) {
            RD_set_ub( self->out_range, k, out_tuple.valptr[k] );
        }
    }
    
}

/*----------------------------------------------------------------*//*! 
  \short Insert a relation, [in]->[out], into the explicit relation.  
  
  This function handles general in and out arity.  It uses the assumption
  that the relations are provided in lexigraphical order wrt the input
  tuple values.

  Handles some memory management wrt to the raw_data, out_vals, etc arrays.

  \author Michelle Strout 9/4/08
*//*----------------------------------------------------------------*/
void ER_in_ordered_insert(ExplicitRelation* self, 
                          Tuple in_tuple, Tuple out_tuple)
{    
    int k;

    // If inserting into a relation that implements a function,
    // then just use the regular ER_insert.
    if (self->isFunction) { 
        ER_insert(self, in_tuple, out_tuple);
    
    // If we know the in_domain, then the calculated index
    // into the out_index array should match our unique input
    // tuple count, which we keep even if we don't know they
    // in_domain.  Therefore, can handle both cases the same,
    // with an extra assertion for the case where we know the
    // in_domain.  Also, when know in_domain do not need to store
    // input tuple into in_vals.
    } else  {

        // check that out_arity is correct
        assert( self->out_arity == out_tuple.arity );

        // determine if the input tuple is a new unique
        // input tuple or the same as previously seen
        if (self->in_domain_given) {
            // check that indexing matches unique_in_count-1
            // or is greater
            assert((self->unique_in_count-1) <= ER_calcIndex(self, in_tuple));
            if ((self->unique_in_count - 1) < ER_calcIndex(self, in_tuple)) {
                // doing assignment because could be skipping something
                // in the in_domain
                self->unique_in_count = ER_calcIndex(self, in_tuple)+1;
            }
            
        // otherwise we need to look at previous input
        // tuple value in in_vals and see if this tuple
        // is lexicographically greater than or equal
        } else {
            // previous Tuple
            Tuple prev;
            prev.arity = self->in_arity;
            prev.valptr = &(self->in_vals[self->unique_in_count]);
            
            // make sure the in_tuple is the same or ordered after
            // previous tuple
            assert( Tuple_compare(prev, in_tuple) >= 0 );
        
            // if have a new unique in_tuple then increment unique count
            // and store in_tuple into in_vals
            if (Tuple_compare(prev,in_tuple) == 1) {
                self->unique_in_count ++;
                for (k=0; k<self->in_arity; k++) {
                    int i = (self->unique_in_count - 1) * self->in_arity + k;
                    self->in_vals[ i ] = Tuple_val(in_tuple,k);
                    
                    // keep track of domain as things are being inserted
                    if (in_tuple.valptr[k] < RD_lb(self->in_domain, k) ) {
                        RD_set_lb( self->in_domain, k, in_tuple.valptr[k] );
                    }
                    if (in_tuple.valptr[k] > RD_ub(self->in_domain, k) ) {
                        RD_set_ub( self->in_domain, k, in_tuple.valptr[k] );
                    }      
                }
            }
            
            
        }

        //=========================================================
        // At this point the self->unique_in_count is set properly
        // to index into self->out_vals.  Now we just need to insert
        // the out tuple.
        
        // check that out_index is big enough
        if ( self->unique_in_count >= self->out_index_size ) {
            expand_array( &(self->out_index), &(self->out_index_size) );
        }
        
        // If this is the first time we are inserting output tuples
        // for the specific input tuple then we will need to set up
        // the out_indices.
        // Indices into out_vals, 
        // out_index[unique_in_count-1] to out_index[unique_in_count]
        if (self->out_index[self->unique_in_count]==0) {
            self->out_index[self->unique_in_count] 
                = self->out_index[self->unique_in_count-1];
        }
        
        // check that out_vals is big enough
        if ( self->out_index[self->unique_in_count] + self->out_arity >     
             self->out_vals_size ) 
        {
            expand_array( &(self->out_vals), &(self->out_vals_size) );
        }

        // do actual insertion of output tuple
        for (k=0; k<self->out_arity; k++) {        
            self->out_vals[self->out_index[self->unique_in_count]+k] 
                = out_tuple.valptr[k];
                
            // keep track of out tuple ub and lb 
            if (out_tuple.valptr[k] < RD_lb(self->out_range, k) ) {
                RD_set_lb( self->out_range, k, out_tuple.valptr[k] );
            }
            if (out_tuple.valptr[k] > RD_ub(self->out_range, k) ) {
                RD_set_ub( self->out_range, k, out_tuple.valptr[k] );
            }
        }                
        
        // increment last out_index value to point after out_tuple
        // just inserted
        self->out_index[self->unique_in_count] += self->out_arity;
        
    }
        
}


/*----------------------------------------------------------------*//*! 
  \short Insert a relation, [in]->[out], into the explicit relation.  
  
  This function assumes that the relation has 1D-to-1D arity and that
  the relations will be inserted in order based on the in integer.

  Handles some memory management wrt the from and hgdata arrays.

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
void ER_in_ordered_insert(ExplicitRelation* self, int in_int, int out_int)
{   

    // For now just use the more general insert.
    ER_in_ordered_insert(self, Tuple_make(in_int), Tuple_make(out_int));

/*    // cannot insert an in tuple less than our current in tuple
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
*/
}

/*----------------------------------------------------------------*//*! 
  \short 1D-to-1D version. Given in val return single associated out val.

  \author Michelle Strout 8/23/08
*//*----------------------------------------------------------------*/
int ER_out_given_in( ExplicitRelation* relptr, int in_val)
{
    // For now just use more general implementation.
    return Tuple_val(ER_out_given_in( relptr, Tuple_make(in_val)),0);
}

/*----------------------------------------------------------------*//*! 
  \short General version.  Given in_tuple return single associated out_tuple.

    Assumes that explicit relation is representing a function.

  \author Michelle Strout 9/2/08
*//*----------------------------------------------------------------*/
Tuple ER_out_given_in( ExplicitRelation* relptr, Tuple in_tuple)
{
    assert(relptr->isFunction);
    
    // Find index of beginning of output tuple and use address of 
    // that to create tuple.
    Tuple retval;
    retval.arity = relptr->out_arity;
    retval.valptr = & (relptr->out_vals[ER_calcIndex(relptr, in_tuple)]);
    return retval;
}


RectDomain* ER_in_domain( ExplicitRelation * relptr)
{ return relptr->in_domain; }

RectDomain* ER_out_range( ExplicitRelation * relptr)
{ return relptr->out_range; }


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

void ER_dump( ExplicitRelation* self )
/*----------------------------------------------------------------*//*! 
  \short Output text representation of relation to standard out.

  Format of output is one tuple pair per line.
  
    [in_tuple] -> [out_tuple]
    ...
    
  The values of other fields are also printed.

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
{
//    int in, p;
    
    printf("ExplicitRelation\n");
    printf("\tin_arity = %d\n", self->in_arity);
    printf("\tout_arity = %d\n", self->out_arity);
    printf("\tisFunction = %d\n", self->isFunction);
    printf("\tin_domain = ");
    RD_dump(self->in_domain);
    printf("\tout_range = ");
    RD_dump(self->out_range);
    printf("\tin_vals_size = %d\n", self->in_vals_size);
    printf("\tout_index_size = %d\n", self->out_index_size);
    printf("\tout_vals_size = %d\n", self->out_vals_size);
    printf("\traw_data_size = %d\n", self->raw_data_size);
    printf("\traw_num = %d\n", self->raw_num);
    
    // nicely formated list of integer tuple pairs in the relation
/*    if (self->in_arity==1 && self->out_arity==1) {
    
        for (in=0; in<self->in_count; in++) {
            for (p=self->out_index[in]; p<self->out_index[in+1]; p++) {
                printf("[%d] -> [%d]\n", in, self->out_vals[p]);
            }
        }
        
    } else {
        assert(0);  // needs implemented for more general arities
    }
*/

    // rest of the raw data
    // FIXME: not keeping track of in_vals yet
    //printf("in_vals = "); 
    //printArray(self->in_vals, self->in_vals_size);
    printf("\nout_index = "); 
    printArray(self->out_index, self->out_index_size);
    printf("\nout_vals = ");
    printArray(self->out_vals, self->out_vals_size);
}