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

