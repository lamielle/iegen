/* test_ExplicitRelation.c */
/*! \file

    Driver that unit tests the ExplicitRelation data structure.
*/

#include "ExplicitRelation.h"
//#include "IAG.h"
#include "util.h"

#define NUM_IN 10
#define NUM_OUT 5

int main() 
{
    ExplicitRelation* relptr;
    int in, out;
    
    relptr = ExplicitRelation_ctor(1,1);

    // then add [in]->[out] relationships 
    // for this example doing all combos of possible
    // in and out values
    for (in=0; in<NUM_IN; in++) {
      for (out=0; out<NUM_OUT; out++) {
            ExplicitRelation_in_ordered_insert( relptr, in, out );
        }
    }
    
    
    ExplicitRelation_dump(relptr);
    
    ExplicitRelation_dtor(&relptr);

/*    // testing IAG_cpack
    hg = Hypergraph_ctor();

    // add only some nodes to each hyperedge
    for (he=0; he<NUM_HE; he++) {
      for (n=(he)%NUM_NODES; n<NUM_NODES; n+=2) {
      
            Hypergraph_ordered_insert_node( hg, he, n );
        }
    }
    
    // indicate we are done constructing the hypergraph
    Hypergraph_finalize(hg);
    
    Hypergraph_dump(hg);

    int* new2old = (int*)malloc(sizeof(int)*hg->nv);
    CPackHyper(hg,new2old);
    printf("\nnew2old = ");
    printArray(new2old,hg->nv);
    
    // Iterate over the hyperedges and nodes in each hyperedge
    int hedge, node;
    printf("\nTraversing in order of hyperedges\n");
    FOREACH_hyperedge(hg,hedge) {
        FOREACH_node_in_hyperedge(hg,hedge,node) {
            printf("\thedge = %d, node = %d\n", hedge, node);
        }
    }

    printf("\nTraversing in order of nodes\n");
    FOREACH_node(hg,node) {
        FOREACH_hyperedge_for_node(hg,node,hedge) {
            printf("\tnode = %d, hedge = %d\n", node, hedge);
        }
    }

    Hypergraph_dump(hg);

    free(new2old);
    Hypergraph_dtor(&hg);
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

