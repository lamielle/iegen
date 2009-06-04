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

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
{
    assert(0);  // not implemented yet
    return Tuple_make(0,0);
}

Tuple RUD_nextTuple( RectUnionDomain* rud, Tuple tuple )
/*----------------------------------------------------------------*//*! 
  \short Given a tuple computes the lexicographically next point
         in the RectUnionDomain.

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
{
    assert(RUD_dim(rud)==tuple.arity);
    
    assert(0); // not implemented yet
    return Tuple_make(0,0);

/*    
    // in a loop check if the elements from innermost to outermost
    // have hit their upperbounds
    for (int d=tuple.arity-1; d>=0; d--) {
    
        // if current element has not hit upper bound then just increment
        if ( tuple.valptr[d] < RD_ub( rd, d ) ) {
            tuple.valptr[d] = tuple.valptr[d]+1;
            return in_tuple;
            
        // if current element has hit upperbound then set it
        // to lower bound so outer elements can increment
        } else {
            tuple.valptr[d] = RD_lb( rd, d );
        }
    }
    
    // If get out of this loop then all of the elements were at their
    // upper bound.
    // Have to enable going one tuple over because the loops will be doing
    // this even though the last iteration won't pass bounds check.
    // Just return the same iter.
    
    return tuple;
*/
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

