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
    // and create last tuple
    Tuple last_tuple = Tuple_make_with_arity(DIM);
    for (k=0; k<DIM; k++) {
        assert(RD_lb(rd,k) == k);
        assert(RD_ub(rd,k) == k + DIM);
        assert(RD_size(rd,k) == DIM+1 );
        
        last_tuple = Tuple_set_val( last_tuple, k, k+DIM );
//        printf("last_tuple = "); Tuple_print(last_tuple); printf("\n");
    }
    
    RD_dump(rd);
    
    // Iterate over all of the tuples in the RectDomain.
    Tuple t; int i;
    printf("Iterating over RectDomain\n");
    for (t=RD_firstTuple(rd), i=0; i<RD_size(rd); i++, t=RD_nextTuple(rd,t) ) {
        //printf("\n\t");
        //Tuple_print(t);
        if (i==RD_size(rd)-1) {
            printf("t = "); Tuple_print(t); printf("\n");
            printf("last_tuple = "); Tuple_print(last_tuple); printf("\n");
            
            assert( Tuple_equal(t, last_tuple) );
        }
    }
    printf("\n");
    
    RD_dtor(&rd);
    
    return 0;
}

