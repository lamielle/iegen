/*! \file   RectDomain.c

    Implements the RectDomain data structure for use with the PIES project.
*/

#include "RectDomain.h"


/*
void RD_set_ub( RectDomain *rd, int k, int lb );


int RD_dim();
int RD_lb(int k);
int RD_ub(int k);
int RD_size(int k); 
*/

RectDomain* RD_ctor(int dim)
/*----------------------------------------------------------------*//*! 
  \short Construct RectDomain structure and return a ptr to it.

  \return Returns a ptr to the constructed RectDomain structure.

  \author Michelle Strout 8/26/08
*//*----------------------------------------------------------------*/
{
    RectDomain* self = (RectDomain*)malloc(sizeof(RectDomain));
    
    self->dim = dim;
    self->bounds = (int*)malloc(sizeof(int)*dim*2);
    
    return self;
}

RectDomain* RD_ctor(RectDomain *other)
/*----------------------------------------------------------------*//*! 
  \short Copy constructor for RectDomain.

  \return Returns a ptr to the constructed RectDomain structure.

  \author Michelle Strout 11/14/08
*//*----------------------------------------------------------------*/
{
    // Set up in domain for retval from input's output domain
    RectDomain* self = RD_ctor(other->dim);
    
    // Iterate over each dimension and copy lower and upper bounds.
    int i;
    for (i=0; i<other->dim; i++) {
        RD_set_lb(self, i, RD_lb(other, i));
        RD_set_ub(self, i, RD_ub(other, i));
    }

    return self;
}

/*----------------------------------------------------------------*//*! 
  \short Deallocate all memory for RectDomain

  \author Michelle Strout 8/26/08
*//*----------------------------------------------------------------*/
void RD_dtor( RectDomain** self )
{
    if ((*self)->bounds != NULL) { free((*self)->bounds); }
    free(*self);
    *self = NULL;
}


void RD_set_lb( RectDomain *rd, int k, int lb )
/*----------------------------------------------------------------*//*! 
  \short Set lower bound for dimension k.

  \author Michelle Strout 8/26/08
*//*----------------------------------------------------------------*/
{
    // make sure k is within dimensionality for this RectDomain
    assert(k<rd->dim);
    
    // bounds[k*2] contains lower bound for kth dim
    rd->bounds[k*2] = lb;
}

void RD_set_ub( RectDomain *rd, int k, int ub )
/*----------------------------------------------------------------*//*! 
  \short Set upper bound for dimension k.

  \author Michelle Strout 8/27/08
*//*----------------------------------------------------------------*/
{
    // make sure k is within dimensionality for this RectDomain
    assert(k<rd->dim);
    
    // bounds[k*2 + 1] contains upper bound for kth dim
    rd->bounds[k*2+1] = ub;
}

int RD_dim(RectDomain *rd )
/*----------------------------------------------------------------*//*! 
  \short Returns dimensionality of the rectangular domain.

  \author Michelle Strout 8/27/08
*//*----------------------------------------------------------------*/
{
    return rd->dim;
}

int RD_lb(RectDomain *rd, int k)
/*----------------------------------------------------------------*//*! 
  \short Returns lower bound for given dimension.

  \author Michelle Strout 8/27/08
*//*----------------------------------------------------------------*/
{
    // make sure k is within dimensionality for this RectDomain
    assert(k<rd->dim);
    
    // bounds[k*2] contains lower bound for kth dim
    return rd->bounds[k*2];
}

int RD_ub(RectDomain *rd, int k)
/*----------------------------------------------------------------*//*! 
  \short Returns upper bound for dimension k.

  \author Michelle Strout 8/27/08
*//*----------------------------------------------------------------*/
{
    // make sure k is within dimensionality for this RectDomain
    assert(k<rd->dim);
    
    // bounds[k*2 + 1] contains upper bound for kth dim
    return rd->bounds[k*2+1];
}

int RD_size(RectDomain *rd, int k)
/*----------------------------------------------------------------*//*! 
  \short Returns size for dimension k.

  \author Michelle Strout 8/27/08
*//*----------------------------------------------------------------*/
{
    // make sure k is within dimensionality for this RectDomain
    assert(k<rd->dim);

    return rd->bounds[k*2+1] - rd->bounds[k*2] + 1;
}

int RD_size(RectDomain *rd)
/*----------------------------------------------------------------*//*! 
  \short Returns size for full domain.

  \author Michelle Strout 9/2/08
*//*----------------------------------------------------------------*/
{
    int k;
    int retval = 1;
    for (k=0; k<rd->dim; k++) {
        retval = retval*RD_size(rd,k);
    }
    return retval;
}

Tuple RD_nextTuple( RectDomain* rd, Tuple t )
/*----------------------------------------------------------------*//*! 
  \short Given a tuple computes the lexicographically next point
         in the RectDomain.

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
{
    assert(RD_dim(rd)==t.arity);
    
    // in a loop check if the elements from innermost to outermost
    // have hit their upperbounds
    for (int d=t.arity-1; d>=0; d--) {
    
        // if current element has not hit upper bound then just increment
        if ( t.valptr[d] < RD_ub( rd, d ) ) {
            t.valptr[d] = t.valptr[d]+1;
            return t;
            
        // if current element has hit upperbound then set it
        // to lower bound so outer elements can increment
        } else {
            t.valptr[d] = RD_lb( rd, d );
        }
    }
    
    // If get out of this loop then all of the elements were at their
    // upper bound.
    // Have to enable going one tuple over because the loops will be doing
    // this even though the last iteration won't pass bounds check.
    // Just return the same iter.
    
    return t;
}    

bool RD_in_domain(RectDomain * rd, Tuple t)
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



/*----------------------------------------------------------------*//*! 
  \short Output text representation of RectDomain to standard out.

  \author Michelle Strout 8/27/08
*//*----------------------------------------------------------------*/
void RD_dump( RectDomain* self )
{
    int k;
    
    printf("RectDomain\n");
    printf("\tdim = %d\n", self->dim);

    for (k=0; k<self->dim; k++) {
        printf("\tdim %d: lb = %d, ub = %d\n", 
            k, self->bounds[k*2], self->bounds[k*2+1] );
    }
    printf("\n");

}

