/*! \file   RectUnionDomain.c

    Implements the RectUnionDomain data structure for use with the PIES project.
*/

#include "RectUnionDomain.h"


RectUnionDomain* RUD_ctor(int dim, int num_rects)
/*----------------------------------------------------------------*//*! 
  \short Construct RectUnionDomain structure and return a ptr to it.

  \return Returns a ptr to the constructed RectUnionDomain structure.

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
{
    RectUnionDomain* self = (RectUnionDomain*)malloc(sizeof(RectUnionDomain));
    
    self->dim = dim;
    self->num_rects = num_rects;
    self->rects = (RectDomain**)malloc(sizeof(RectDomain*));
    
    return self;
}


RectUnionDomain* RUD_ctor(RectDomain* rd)
/*----------------------------------------------------------------*//*! 
  \short Construct RectUnionDomain structure with only given rectangular 
         domain and return a ptr to it.

  \return Returns a ptr to the constructed RectUnionDomain structure.

  \author Michelle Strout 7/7/09
*//*----------------------------------------------------------------*/
{
    RectUnionDomain* self = RUD_ctor(RD_dim(rd), 1);
    RUD_insert(self,rd);
    return self;
}

/*----------------------------------------------------------------*//*! 
  \short Deallocate all memory for RectUnionDomain

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
void RUD_dtor( RectUnionDomain** self )
{
    if ((*self)->rects != NULL) {
        for (int i=0; i<(*self)->num_rects; i++) {
            RD_dtor(&((*self)->rects[0]));
        }
        free((*self)->rects); 
    }
    free(*self);
    *self = NULL;
}


void RUD_insert(RectUnionDomain *rud, RectDomain *rd)
/*----------------------------------------------------------------*//*! 
  \short There is only one rectangular domain in whole union.

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
{
    // make sure RectDomain has same dimensionality as RectUnionDomain
    assert(rd->dim == rud->dim);
    // make sure this RectUnionDomain was only supposed to have one rect
    assert(rud->num_rects == 1);

    // store copy of single rectangle    
    rud->rects[0] = RD_ctor(rd);
}

void RUD_insert(RectUnionDomain *rud, Tuple embed_tuple, RectDomain *rd)
/*----------------------------------------------------------------*//*! 
  \short Insert rectangular domain with given embedding tuple.

  Currently this routine assumes the embedding tuple is of arity 1.

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
{
    // make sure RectDomain has one less dimensionality than RectUnionDomain
    assert(rd->dim  == (rud->dim - 1));
    // make sure this RectUnionDomain was supposed to have >1 rect
    assert(rud->num_rects > 1);

    // store copy of rectangular domain   
    rud->rects[Tuple_val(embed_tuple,0)] = RD_ctor(rd);
}


int RUD_dim(RectUnionDomain *rud )
/*----------------------------------------------------------------*//*! 
  \short Returns dimensionality of the rectangular union domain.

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
{
    return rud->dim;
}

int RUD_size(RectUnionDomain *rud)
/*----------------------------------------------------------------*//*! 
  \short Returns size for full domain.
  
  Adds up sizes for all rectangular domains in union.

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
{
    int k;
    int retval = 0;
    for (k=0; k<rud->num_rects; k++) {
        retval += RD_size(rud->rects[k]);
    }
    return retval;
}

Tuple RUD_firstTuple( RectUnionDomain* rud)
/*----------------------------------------------------------------*//*! 
  \short Returns the lexicographically first tuple in domain.

  \author Michelle Strout 7/6/09
*//*----------------------------------------------------------------*/
{
    assert(rud->rects[0] != NULL );
    
    // If union only contains one RectDomain then call first
    // tuple on that.
    if (rud->num_rects==1) {
        return RD_firstTuple( rud->rects[0] );
    }
    
    // Otherwise have to create tuple in embedded union.
    else {
        Tuple t = RD_firstTuple( rud->rects[0] );
        Tuple retval = Tuple_make_with_arity( RUD_dim(rud) );
        for (int k=1; k<RUD_dim(rud); k++) {
            // breaking Tuple interface for efficiency
            retval.valptr[k] = t.valptr[k-1];   
        }
        return retval;
    }
    
}

Tuple RUD_nextTuple( RectUnionDomain* rud, Tuple tuple )
/*----------------------------------------------------------------*//*! 
  \short Given a tuple computes the lexicographically next point
         in the RectUnionDomain.

  Implementation notes:  Do not want to use RD_nextTuple for efficiency
  reasons, so duplicating much of the functionality in RD_nextTuple
  here.

  \author Michelle Strout 7/6/09
*//*----------------------------------------------------------------*/
{
    assert(RUD_dim(rud)==tuple.arity);
    
    // If union only contains one RectDomain then call next
    // tuple on that.
    if (rud->num_rects==1) {
        return RD_nextTuple(rud->rects[0], tuple);
    }
    
    // Otherwise have to duplicate much of RD_nextTuple functionality
    // but still take embedding into account.
    else {
        RectDomain * current_rd = rud->rects[Tuple_val(tuple, 0)];
        assert( current_rd != NULL );
    
        // in a loop check if the elements from innermost to outermost
        // have hit their upperbounds
        for (int d=tuple.arity-1; d>0; d--) {
    
            // if current element has not hit upper bound then just increment
            // shifting to d-1 ub because of embedding
            if ( tuple.valptr[d] < RD_ub( current_rd, d-1 ) ) {
                tuple.valptr[d] = tuple.valptr[d]+1;
                return tuple;
            
            // if current element has hit upperbound then set it
            // to lower bound so outer elements can increment
            // shifting to d-1 ub because of embedding
            } else {
                tuple.valptr[d] = RD_lb( current_rd, d-1 );
            }
        }
    
        // If get out of this loop then all of the elements in the current 
        // embedded rectangle were at their upper bound.  
        // Need to go to next rectangle.
        tuple.valptr[0]++;
        
        // Have to enable going one tuple over because the loops will be doing
        // this even though the last iteration won't pass bounds check.
        // Just return the same iter.
    
        return tuple;
    }
}    

bool RUD_in_domain(RectUnionDomain * rud, Tuple t)
/*----------------------------------------------------------------*//*! 
  \short Returns true if given tuple is in given domain.

    Implementation note: again copied much of the implementation
    from RD_in_domain.

  \author Michelle Strout 7/7/09
*//*----------------------------------------------------------------*/
{
    // check that the Tuple and RectUnionDomain have same dimensionality
    if (t.arity != RUD_dim(rud)) {
        return false;
    }

    if (rud->num_rects==1) {
        return RD_in_domain( rud->rects[0], t );
    }
    
    // Otherwise have to check if tuple is in embedded union.
    else {
        if (Tuple_val(t, 0) >= rud->num_rects) {
            return false;
        }
        
        // check that the tuple values lie within bounds.
        for (int i=1; i<t.arity; i++) {
            if ( t.valptr[i] < RD_lb(rud->rects[Tuple_val(t, 0)],i-1) 
                 || t.valptr[i] > RD_ub(rud->rects[Tuple_val(t, 0)],i-1) ) 
            {
                return false;
            }
        }
            
    }

    return true;
}

int RUD_calcIndex( RectUnionDomain* rud, Tuple t )
/*----------------------------------------------------------------*//*!
  \short Given an in tuple calculates an index.  The tuples could
         be lexicographically sorted using the computed index.

  \author Michelle Strout 7/7/09
*//*----------------------------------------------------------------*/
{
    assert(t.arity != RUD_dim(rud));

    int index;

    // If just have one rectangular domain then call calcIndex on it.
    if (rud->num_rects==1) {
        index = RD_calcIndex( rud->rects[0], t );
    }
    
    // Otherwise have to determine which rectangular domain to get
    // an initial index from and then offset based on the size of
    // the preceding rectangular domains.
    else {
        // create tuple with all elements but first
        Tuple truncated = Tuple_make_with_arity(RUD_dim(rud)-1);
        for (int i=1; i<RUD_dim(rud); i++) {
            truncated.valptr[i-1] = t.valptr[i];
        }
        
        // get index from appropriate rectangle
        assert( t.valptr[0] >=0 && t.valptr[0] < rud->num_rects );
        int rd_index = RD_calcIndex(rud->rects[t.valptr[0]], truncated);
        
        // Add index in particular RD to sizes of all previous RD.
        index = rd_index;
        for (int i=0; i<t.valptr[0]; i++) {
            index = index + RD_size(rud->rects[i]);
        }
    }
    
    return index;
}

int RUD_calcIndex( RectUnionDomain* rud, int val )
/*----------------------------------------------------------------*//*!
  \short Given an 1D in tuple (so just the single value)
         calculates the index into domain.  
         1D-to-1D arity specialization.

    <pre>
        in_tuple: <x_0>
        index: x_0-lb_0
    </pre>

  \author Michelle Strout 9/22/08, 7/7/09
*//*----------------------------------------------------------------*/
{
    assert(rud->dim==1);

    return (val-RD_lb(rud->rects[0],0) );
}

RectDomain* RUD_approx( RectUnionDomain* rud )
/*----------------------------------------------------------------*//*!
  \short Given a RectUnionDomain constructs and returns a pointer
         to an approximating RectDomain.
         
    The approximation is due to the lowest lower bound for a certain
    dim and the upper bound is the highest for certain dim.

  \author Michelle Strout 7/7/09
*//*----------------------------------------------------------------*/
{
    RectDomain* retval;
    
    // If just have one rectangular domain then return copy of it.
    if (rud->num_rects==1) {
        retval = RD_ctor( rud->rects[0] );
    }

    // Otherwise have to create a new RectDomain.
    else {
        retval = RD_ctor(rud->dim);
    
        // Set lower and upper bound of indices into rectangles.
        RD_set_lb( retval, 0, 0 );
        RD_set_ub( retval, 0, rud->num_rects-1 );
        
        // grab lower bounds and upper bounds from embedded rects
        for (int i=1; i<rud->dim; i++ ) {
            int lb = INT_MAX;
            int ub = 0;
            for (int r=0; r<rud->num_rects; r++) {
                if ( RD_lb( rud->rects[r], i-1 ) < lb ) {
                    lb = RD_lb( rud->rects[r], i-1 );
                }
                if ( RD_ub( rud->rects[r], i-1 ) > ub ) {
                    ub = RD_ub( rud->rects[r], i-1 );
                }
            
            }
            
            RD_set_lb( retval, i, lb );
            RD_set_ub( retval, i, ub );
        }
    }    
    
    return retval;
}

/*----------------------------------------------------------------*//*! 
  \short Output text representation of RectUnionDomain to standard out.

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
void RUD_dump( RectUnionDomain* self )
{
    int k;
    
    printf("RectUnionDomain\n");
    printf("\tdim = %d\n", self->dim);

    for (k=0; k<self->num_rects; k++) {
        RD_dump( self->rects[k] );
    }
}

