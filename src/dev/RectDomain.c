/*! \file   RectDomain.c

    Implements the RectDomain data structure for use with the PIES project.
*/

#include "RectDomain.h"



void RD_set_ub( RectDomain *rd, int k, int lb );


int RD_dim();
int RD_lb(int k);
int RD_ub(int k);
int RD_size(int k); 


RectDomain* RD_ctor(int dim)
/*----------------------------------------------------------------*//*! 
  \short Construct RectDomain structure and return a ptr to it.

  Initializes the hypergraph to empty.

  \return Returns a ptr to the constructed RectDomain structure.

  \author Michelle Strout 8/26/08
*//*----------------------------------------------------------------*/
{
    RectDomain* self = (RectDomain*)malloc(sizeof(RectDomain));
    
    self->dim = dim;
    self->bounds = (int*)malloc(sizeof(int)*dim*2);
    
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

