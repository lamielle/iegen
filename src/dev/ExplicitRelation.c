/*! \file        ExplicitRelation.c
    Implements the ExplicitRelation data structure for use with the PIES 
    project.

    See the notes in the ER_ctor function to see how implementation
    of the data structure will vary based on its characteristics.

    If the relation is a function, then the out_index array is not needed and 
    the input tuple can index directly into the out_vals array with 
    RUD_calcIndex(in_domain, in_tuple)*out_arity.

    If each input tuple has a varying number of output tuples or more than one 
    output tuples associated with it, then the input tuple indexes into 
    out_index with RUD_calcIndex(in_domain, in_tuple) and the out_index indexes 
    into out_vals, pointing at the first output relation for the input_tuple.
*/

#include "ExplicitRelation.h"

static bool debug = false;


ExplicitRelation* ER_ctor(int in_tuple_arity, int out_tuple_arity,
                          RectUnionDomain *in_domain,
                          bool isFunction, bool isPermutation)
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

  If no in_domain is provided.
  <ul>
    <li>Without an in_domain specification, we can't sort by the input tuples until after all the tuple pairs have been inserted into the relation.  Therefore, if no in_domain is provided, then we should have insert just put all of the relations into the raw data array.  Each entry will take in_arity+out_arity spots in the raw_data array.  Insert can then keep track of the in_domain lower and upper bounds.
  </ul>

  \param in_tuple_arity     Arity of the input tuples.
  \param out_tuple_arity    Arity of the output tuples.
  \param in_domain          Min and max values of all entries in in_tuples.
  \param isFunction         Indicates each input tuple has only one output.
  \param isPermutation      Indicates that in domain and out range are the same
                            and the relation is one-to-one and onto.

  \return Returns a ptr to the constructed ExplicitRelation structure.

  \author Michelle Strout 8/29/08
*//*----------------------------------------------------------------*/
{
    ExplicitRelation* self
        = (ExplicitRelation*)malloc(sizeof(ExplicitRelation));

    self->in_arity = in_tuple_arity;
    self->out_arity = out_tuple_arity;
    self->isFunction = isFunction;
    self->isPermutation = isPermutation;
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

    self->external_out_vals=false;

    // if in_domain was provided.
    if (in_domain != NULL) {
        self->in_domain_given = true;
        assert(self->in_arity == RUD_dim(self->in_domain));

        // With a known in_domain and if we have a function,
        // we know how big out_vals array must be.
        if (self->isFunction) {
            self->out_vals_size
                = self->out_arity *  RUD_size(self->in_domain);
            // want all out_vals to be initialized to zero
            self->out_vals = (int*)calloc(self->out_vals_size,sizeof(int));

        // If we don't have a function then we don't know how many
        // output tuples are associated with each input tuple, but
        // we do know how big the out_index array must be.
        } else {
            self->out_index_size = RUD_size(self->in_domain) + 1;
            self->out_index = (int*)calloc(self->out_index_size,sizeof(int));
        }


    // The in_domain is not defined.
    // set up an "undefined" rectangular domain where the starting
    // ub is 0 and the starting lb is maxint.  That way when
    // actual values are inserted, the ub and lb will be properly
    // updated.
    } else {
        self->in_domain_given = false;
        RectDomain *rd = RD_ctor(self->in_arity);
        int i;
        for (i=0; i<self->in_arity; i++ ) {
            RD_set_lb( rd, i, INT_MAX );
            RD_set_ub( rd, i, 0 );
        }
        self->in_domain = RUD_ctor(rd);
    }

    // set up out_range
    self->out_range = RD_ctor(self->out_arity);
    int i;
    // first set up default values
    for (i=0; i<self->out_arity; i++ ) {
        RD_set_lb( self->out_range, i, INT_MAX );
        RD_set_ub( self->out_range, i, 0 );
    }

    // By default ordered by in tuples.  Will change if generic insert is
    // used.
    self->ordered_by_in = true;

    return self;
}

ExplicitRelation* ER_ctor(int * index_array, int size)
/*----------------------------------------------------------------*//*!
  \short Construct ExplicitRelation structure based on given index array
         and returns a pointer to it.

  Assumes the explicit relation should be a function and has 1D-to-1D
  arity.  Also assumes that the input domain is 0 <= i < size.

  Keeps a pointer to index_array, so index_array should not be externally
  deallocated.
  FIXME: We could copy the output values to another array since we are
  traversing them anyway to determine the output value range.

  \param index_array        Flat index array.
  \param size               Number of entries in flat index array.

  \return Returns a ptr to the constructed ExplicitRelation structure.

  \author Michelle Strout 9/10/08
*//*----------------------------------------------------------------*/
{
    ExplicitRelation* self
        = (ExplicitRelation*)malloc(sizeof(ExplicitRelation));

    self->in_arity = 1;
    self->out_arity = 1;
    self->isFunction = true;

    RectDomain *rd = RD_ctor(1);
    RD_set_lb(rd, 0, 0); RD_set_ub(rd, 0, size-1);
    self->in_domain = RUD_ctor(rd);

    self->in_vals = NULL;
    self->unique_in_count = size;
    self->out_index = NULL;
    self->out_vals = index_array;
    self->raw_data = NULL;
    self->raw_num = 0;

    self->in_vals_size = 0;
    self->out_index_size = 0;
    self->out_vals_size = size;
    self->raw_data_size = 0;

    self->external_out_vals=true;

    // Determine domain for out values.
    // set up out_range
    self->out_range = RD_ctor(self->out_arity);
    int i;
    // first set up default values
    for (i=0; i<self->out_arity; i++ ) {
        RD_set_lb( self->out_range, i, INT_MAX );
        RD_set_ub( self->out_range, i, 0 );
    }
    // then iterate through actual out values and determine range
    for (i=0; i<size; i++) {
        if (index_array[i] < RD_lb(self->out_range, 0) ) {
            RD_set_lb( self->out_range, 0, index_array[i] );
        }
        if (index_array[i] > RD_ub(self->out_range, 0) ) {
            RD_set_ub( self->out_range, 0, index_array[i] );
        }
    }

    // By default ordered by in tuples.  Will change if generic insert is
    // used.
    self->ordered_by_in = true;

    return self;
}

ExplicitRelation* ER_genInverse(ExplicitRelation * input)
/*----------------------------------------------------------------*//*!
  \short Create the inverse of the input ER.

  Allocates a new ER data structure and populates it with inverse
  of given relation.
  Has one version of the code for relations that are 1D-to-1D
  and permutations and then a more general version for other relations.

  The more general version is probably an algorithm that should be
  used when converting an unordered ER to one that is ordered by
  input tuples.

  \author Michelle Strout 11/4/08, 11/14/08
*//*----------------------------------------------------------------*/
{
    // As input has been constructed, we have been keeping track
    // of its in domain and out range.  Therefore, we can us
    // the out range as the input range for the inverse ER.
    RectUnionDomain* in_domain = RUD_ctor(input->out_range);

    ExplicitRelation* retval;

    // If the ER is a permutation and has in and out arity of 1,
    // then can easily invert.
    if (input->isPermutation
        && (input->in_arity == 1) && (input->out_arity == 1))
    {
        // have constructor create new ER
        retval = ER_ctor(input->out_arity,input->in_arity, in_domain,
                         true, true);
        retval->out_range = RUD_approx(input->in_domain);

        // Fill the inverted ER by iterating over input ER.
        int in;
        FOREACH_in_tuple_1d1d(input, in) {
            ER_insert( retval, ER_out_given_in(input, in), in);
        }


    // more general inverse of relation
    } else {
        // have constructor create new ER, false indicates we do not know
        // if it is a function or not
        retval = ER_ctor(input->out_arity, input->in_arity, in_domain, false);
        retval->out_range = RD_ctor(RUD_approx(input->in_domain));

        // Count number of input tuples associated with each
        // output tuple and store count in retval's out_index array.
        Tuple in_tuple, out_tuple;
        int count = 0;
  
        FOREACH_in_tuple(input, in_tuple) {
            FOREACH_out_given_in(input, in_tuple, out_tuple) {
                // Calculate index into out_index array.
                int idx = RUD_calcIndex(retval->in_domain, out_tuple);
                retval->out_index[idx] += retval->out_arity;
                count++;

                if (debug) {
                    printf("ER_genInverse\n");
                    printf("\tin_tuple = ");
                    Tuple_print(in_tuple); printf("\n");
                    printf("\tout_tuple = ");
                    Tuple_print(out_tuple); printf("\n");
                }

            }
        }

        // Modify out_index array so that it now points correctly
        // into the out_vals array for inverse.
        int i;
        retval->out_index[RUD_size(retval->in_domain)] 
            = count*retval->out_arity;
        for (i=RUD_size(retval->in_domain); i>0; i--) {
            retval->out_index[i-1]
                = retval->out_index[i] - retval->out_index[i-1];
        }
        retval->out_index[0] = 0;

        // Allocate the out_vals array.
        // (count entries) * (retval->out_arity)
        retval->out_vals = (int*)malloc(sizeof(int)*count*retval->out_arity);
        retval->out_vals_size = count*retval->out_arity;

        // Do another pass over input ER and populate out_vals
        // for inverse.
        FOREACH_in_tuple(input, in_tuple) {
            FOREACH_out_given_in(input, in_tuple, out_tuple) {
                // Calculate index into out_index array.
                int idx = RUD_calcIndex(retval->in_domain, out_tuple);
                // do actual insertion of output tuple
                for (int k=0; k<retval->out_arity; k++) {
                    retval->out_vals[retval->out_index[idx]+k]
                        = Tuple_val(in_tuple, k);
                }
                retval->out_index[idx] += retval->out_arity;
            }
        }

        // Readjust the out_index array for inverse.
        for (i=RUD_size(retval->in_domain); i>0; i--) {
            retval->out_index[i] = retval->out_index[i-1];
        }
        retval->out_index[0] = 0;

    }

    // FIXME:
    // The input ER will "own" the inverse ER.  Actually do they own each
    // other?  This might cause memory management issues.
    input->inverse = retval;
    retval->inverse = input;

    return retval;
}


/*----------------------------------------------------------------*//*!
  \short Deallocate all memory for ExplicitRelation.

  The ExplicitRelation deletes the RectUnionDomain for the in_domain,
  which may cause problems if the RectUnionDomain pointer is being used
  elsewhere.

  \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
void ER_dtor( ExplicitRelation** self )
{
    if ((*self)->in_vals != NULL) { free((*self)->in_vals); }
    if ((*self)->out_index != NULL) { free((*self)->out_index); }
    if ((*self)->out_vals != NULL && !(*self)->external_out_vals) { free((*self)->out_vals); }
    if ((*self)->raw_data != NULL) { free((*self)->raw_data); }
    if ((*self)->in_domain != NULL) { free((*self)->in_domain); }
    free(*self);
    *self = NULL;
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
    // realloc does guarantee that old data is copied over to new allocation.
    for (i=old_size; i<*array_size; i++) {
        (*array_handle)[i] = 0;
    }

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

    // if isFunction and know in_domain then
    if (self->isFunction  && self->in_domain_given) {
        // check that in Tuple is within bounds
        assert(RUD_in_domain(self->in_domain, in_tuple) );

        // insert output tuple values into locations in out_vals
        // associated with this input tuple
        assert( self->out_arity == out_tuple.arity );

        // do actual insertion of output tuple
        int start_index 
            = RUD_calcIndex(self->in_domain, in_tuple)*self->out_arity;
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
            // FIXME: is it ok to assume that in domain is only going
            // to have one rect if it is not given.
            // FIXME: Refactor this code that keeps modifying the RD approx.
            if (in_tuple.valptr[k] < RD_lb(self->in_domain->rects[0], k) ) {
                RD_set_lb( self->in_domain->rects[0], k, in_tuple.valptr[k] );
            }
            if (in_tuple.valptr[k] > RD_ub(self->in_domain->rects[0], k) ) {
                RD_set_ub( self->in_domain->rects[0], k, in_tuple.valptr[k] );
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

    if (debug) {
        printf("ER_in_ordered_insert\n");
        printf("\tin_tuple = "); Tuple_print(in_tuple); printf("\n");
        printf("\tout_tuple = "); Tuple_print(out_tuple); printf("\n");
    }

    // If inserting into a relation that implements a function,
    // then just use the regular ER_insert.
    if (self->isFunction  && self->in_domain_given) {
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
            assert((self->unique_in_count-1) 
                   <= RUD_calcIndex(self->in_domain, in_tuple));
            if ((self->unique_in_count - 1) 
                < RUD_calcIndex(self->in_domain, in_tuple)) 
            {
                // doing assignment because could be skipping something
                // in the in_domain
                self->unique_in_count 
                    = RUD_calcIndex(self->in_domain, in_tuple)+1;
            }

        // otherwise we need to look at previous input
        // tuple value in in_vals and see if this tuple
        // is lexicographically greater than or equal
        } else {

            // if there is a previous tuple then check if the current
            // tuple is lexicographically greater and therefore
            // means we need to insert a new input tuple.
            bool insert_flag = false;
            if (self->unique_in_count > 0) {
                // previous Tuple
                Tuple prev;
                prev.arity = self->in_arity;
                assert(self->in_vals != NULL);
                prev.valptr =
                  &(self->in_vals[(self->unique_in_count-1)*self->in_arity]);

                // make sure the in_tuple is the same or ordered after
                // previous tuple
                assert( Tuple_compare(prev, in_tuple) <= 0 );

                // if have a new unique in_tuple then increment unique count
                // and indicate need to store in_tuple into in_vals
                if (Tuple_compare(prev,in_tuple) == -1) {
                    insert_flag = true;
                }

            // otherwise this is the first input tuple and
            // we definitely need to do an insert
            } else {
                insert_flag = true;
            }

            // if have a new unique in_tuple then increment unique count
            // and store in_tuple into in_vals
            if (insert_flag) {
                self->unique_in_count ++;

                // check that in_vals is big enough
                // For each input tuple need space for all elements
                // of the tuple.
                if ( self->unique_in_count*self->in_arity
                     >= self->in_vals_size )
                {
                    expand_array( &(self->in_vals), &(self->in_vals_size) );
                }

                // insert all elements in the tuple
                for (k=0; k<self->in_arity; k++) {
                    int i = (self->unique_in_count - 1) * self->in_arity + k;
                    self->in_vals[ i ] = Tuple_val(in_tuple,k);

                    // keep track of domain as things are being inserted
                    // FIXME: Rect approx refactor.
                    if (in_tuple.valptr[k] < RD_lb(self->in_domain->rects[0], k) ) {
                        RD_set_lb( self->in_domain->rects[0], k, in_tuple.valptr[k] );
                    }
                    if (in_tuple.valptr[k] > RD_ub(self->in_domain->rects[0], k) ) {
                        RD_set_ub( self->in_domain->rects[0], k, in_tuple.valptr[k] );
                    }
                }
            }


        }

        //=========================================================
        // At this point the self->unique_in_count is set properly
        // to index into self->out_index.
        // Now we just need to insert the out tuple.

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
    retval.valptr = & (relptr->out_vals[
            RUD_calcIndex(relptr->in_domain, in_tuple) * relptr->out_arity ]);
    return retval;
}


RectUnionDomain* ER_in_domain( ExplicitRelation * relptr)
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

bool ER_verify_permutation(ExplicitRelation* relptr)
/*------------------------------------------------------------*//*!
  \short Verifies that the given ER is a permutation.

  For now only handling 1D-to-1D explicit relations.

  \param  relptr    pointer to an explicit relation

  \author Michelle Strout 10/10/08
*//*--------------------------------------------------------------*/
{
    assert(relptr->in_arity==1 && relptr->out_arity==1);

    // If it is a permutation then it has to be a function.
    if (!relptr->isFunction) { return false; }

    bool * val_seen = (bool*)calloc(RD_size(relptr->out_range), sizeof(bool));

    int i;
    for (i=0; i<RD_size(relptr->out_range); i++) {
        val_seen[relptr->out_vals[i]] = true;
    }
    for (i=0; i<RD_size(relptr->out_range); i++) {
        if (val_seen[i] == false) { return false; }
    }
    return true;
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
    RUD_dump(self->in_domain);
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
    if (self->in_vals != NULL) {
        printf("in_vals = ");
        print_int_array(self->in_vals, self->in_vals_size);
    }
    printf("\nout_index = ");
    print_int_array(self->out_index, self->out_index_size);
    printf("\nout_vals = ");
    print_int_array(self->out_vals, self->out_vals_size);
}

