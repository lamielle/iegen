/* test_Hypergraph.c */
/*! \file

    Driver that unit tests the Hypergraph data structure.
*/

#include <iegen/hypergraph/Hypergraph.h>
#include <iegen/iag/IAG.h>
#include <iegen/util/iegen_util.h>

#define NUM_HE 10
#define NUM_NODES 5

int main() 
{
    Hypergraph* hg;
    int he, n;
    
    hg = Hypergraph_ctor();

    // then add (hyperedge,node) relationships by calling
    // for this example putting all nodes in all hyperedges
    for (he=0; he<NUM_HE; he++) {
      for (n=0; n<NUM_NODES; n++) {
      
            Hypergraph_ordered_insert_node( hg, he, n );
        }
    }
    
    // indicate we are done constructing the hypergraph
    Hypergraph_finalize(hg);
    
    Hypergraph_dump(hg);
    
    Hypergraph_dtor(&hg);

    // testing IAG_cpack
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

