/* test_ExplicitRelation.c */
/*! \file

    Driver that unit tests the ExplicitRelation data structure.
*/

#include "ExplicitRelation.h"
#include "IAG.h"
#include "util.h"

#define NUM_IN 10
#define NUM_OUT 5

int main() 
{
    ExplicitRelation* relptr;
    RectDomain* in_domain;
    int in, out;

    // Test out explicit relations that are functions and where the
    // in_domain is provided.
    in_domain = RD_ctor(2);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, 4);
    RD_set_lb(in_domain, 1, 1);
    RD_set_ub(in_domain, 1, 5);
    relptr = ER_ctor(2,2, in_domain, true);
    
    ER_dump(relptr);
    
    ER_dtor(&relptr);
  
/*    relptr = ER_ctor(1,1);

    // then add [in]->[out] relationships 
    // for this example doing all combos of possible
    // in and out values
    for (in=0; in<NUM_IN; in++) {
      for (out=0; out<NUM_OUT; out++) {
            ER_in_ordered_insert( relptr, in, out );
        }
    }
    
    
    ER_dump(relptr);
    
    ER_dtor(&relptr);

    //------- testing code that will be used in IAG_cpack
    // first construct an explicit relation and fill it
    // the explicit relation will be passed to IAG_cpack
    relptr = ER_ctor(1,1);

    // add only some out vals for each in val
    for (in=0; in<NUM_IN; in++) {
      for (out=(in)%NUM_OUT; out<NUM_OUT; out+=2) {
            ER_in_ordered_insert( relptr, in, out );
        }
    }
    
    ER_dump(relptr);
    
    // Iterate over the integer tuple relations
    printf("\nTraversing in order of input tuples\n");
    FOREACH_in_tuple_1d1d(relptr, in) {
        FOREACH_out_given_in_1d1d(relptr, in, out) {
            printf("\t[%d] -> [%d]\n", in, out);
        }
    }
*/
/*
    //----- testing IAG_cpack itself
    int* new2old 
        = (int*)malloc(sizeof(int)*ER_getRangeCount(relptr));
    IAG_cpack(relptr,new2old);
    printf("\nnew2old = ");
    printArray(new2old,ER_getRangeCount(relptr));

    free(new2old);
    ER_dtor(&relptr);
*/

    // ok now do somewhat of a stress test of the memory management
    /* MMS, this takes a long time so only do it when MEM_ALLOC_INCREMENT
     * is set low
    hg = Hypergraph_ctor();
    for (he=0; he<MEM_ALLOC_INCREMENT*2+10; he++) {
      for (n=0; n<MEM_ALLOC_INCREMENT*2+5; n++) {
      
            Hypergraph_ordered_insert_node( hg, he, n );
        }
    }
    Hypergraph_finalize(hg);
    Hypergraph_dtor(&hg);
    
    //Hypergraph_dump(hg);
    */
    
    
    return 0;
}

