/*! \file       test_RectDomain.c

    Driver that unit tests the RectDomain data structure.
*/

#include "RectDomain.h"
#include <assert.h>

#define DIM 5


int main() 
{
    RectDomain* rd;
    int k;
    
    rd = RD_ctor(DIM);

    // then indicate bounds
    for (k=0; k<DIM; k++) {
        
        RD_set_lb( rd, k, k );
        RD_set_ub( rd, k, k + DIM );
        
    }
    
    // check that get expected dimensionality
    assert( RD_dim(rd) == DIM );
    
    // check that get expected values for bounds
    for (k=0; k<DIM; k++) {
        
        assert(RD_lb(rd,k) == k);
        assert(RD_ub(rd,k) == k + DIM);
        assert(RD_size(rd,k) == DIM+1 );
    }
    
    RD_dump(rd);
    
    RD_dtor(&rd);
    
    return 0;
}

