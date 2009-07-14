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

Tuple RD_firstTuple( RectDomain* rd)
/*----------------------------------------------------------------*//*! 
  \short Given a tuple returns the lexicographically first point
         in the RectDomain.

  \author Michelle Strout 7/6/09
*//*----------------------------------------------------------------*/
{
    Tuple retval = Tuple_make_with_arity(RD_dim(rd));
    
    // Fill the tuple will all of the lower bounds.
    for (int d=0; d<RD_dim(rd); d++) {
        // probably faster than using Tuple_set_val, but does
        // break data abstraction for Tuple
        retval.valptr[d] = RD_lb(rd,d); 
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

int RD_calcIndex( RectDomain* rd, Tuple t )
/*----------------------------------------------------------------*//*!
  \short Given an in tuple calculates an index.  The tuples could
         be lexicographically sorted using the computed index.

    <pre>
        in_tuple: <x_0, x_1, ..., x_k>
        index: ((x_0-lb_0)*(RD_size(1)*...*RD_size(k))
               + (x_1-lb_0)*(RD_size(2)* ... *RD_size(k))
               + (x_k-lb_k)) ]
    </pre>

  \author Michelle Strout 8/30/08, 7/7/09
*//*----------------------------------------------------------------*/
{
    assert(t.arity == RD_dim(rd));

    int i, j, index;
    index = 0;
    // add up all the terms for each dimension of the domain
    for (i=0; i<rd->dim; i++) {
        // get element value from Tuple
        int term = Tuple_val(t, i) - RD_lb(rd, i);
        for (j=i+1; j<rd->dim; j++) {
            term *= RD_size( rd, j );
        }
        index += term;
    }

    return index;
}

int RD_calcIndex( RectDomain* rd, int val )
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
    assert(rd->dim==1);

    return (val-RD_lb(rd,0) );
}

//Tuple RD_calcTuple( RectDomain* rd, int index )
/*----------------------------------------------------------------*//*!
  \short This function is the inverse function of RD_calcIndex.


  Given an index into out_index, or out_vals/out_arity, calculates the
  input tuple based on information about the domain.  
  
  If the index is a raw index into out_vals of the ExplicitRelation data
  structure, then it must be divided by out_arity before being passed to
  this function.

  This function is currently being used in the FOREACH macros to iterate
  over input tuples with arity greater than 1.



    <pre>
        Size terms for each dim and then calculate tuple values.
            in_tuple: <x_0, x_1, ..., x_k>
            t0 = (RD_size(1)*...*RD_size(k))
            t1 = (RD_size(2)* ... *RD_size(k))
            ...
            tk = 1

        We need to solve the following equation for x values:
            index = (x_0-lb0)*t0 + (x_1-lb1)*t1 ... + (x_k-lbk)*tk

            x_0 = index/t0 + lb0
            index = (x_1-lb1)*t1 + (x_2-lb2)*t2 ... + (x_k-lbk)*tk
                  = index % t0

            x_1 = index/t1 + lb1
            index = (x_2-lb2)*t2 ... + (x_k-lbk)*tk
                  = index % t1

            ...
    </pre>

  \author Michelle Strout 9/22/08
*//*----------------------------------------------------------------*/
/*{
    int i;
    RectUnionDomain * in_domain = ER_in_domain(relptr);

    // allocate an array to hold size for each
    // tuple element in array index computation.
    int *t = (int*)malloc(sizeof(int)*relptr->in_arity);

    // calculate those sizes
    // tk = 1
    t[relptr->in_arity - 1] = 1;
    for (i=relptr->in_arity - 2; i>=0; i--) {
        // ti = (RD_size(i+1)* ... *RD_size(k))
        t[i] = t[i+1] * RD_size(in_domain, i+1);
    }

    // Solve for the tuple entries based on the sizes and given index.
    Tuple retval;
    retval.valptr = (int*)malloc(sizeof(int)*relptr->in_arity);
    retval.arity = relptr->in_arity;
    for (i=0; i<relptr->in_arity; i++) {
        // x_i = index/ti + lbi
        retval.valptr[i] = index / t[i] + RD_lb(in_domain,i);
        // index = x_{i+1} * t_{i+1} ... x_k * tk = index % ti
        index = index % t[i];
    }

    return retval;
}*/

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

