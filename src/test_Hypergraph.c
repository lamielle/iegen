/* test_Hypergraph.c */
/*! \file

    Driver that unit tests the Hypergraph data structure.
*/

#include "Hypergraph.h"

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
    
    // ok now do somewhat of a stress test of the memory management
    hg = Hypergraph_ctor();
    for (he=0; he<MEM_ALLOC_INCREMENT*2+10; he++) {
      for (n=0; n<MEM_ALLOC_INCREMENT*2+5; n++) {
      
            Hypergraph_ordered_insert_node( hg, he, n );
        }
    }
    Hypergraph_finalize(hg);
    Hypergraph_dtor(&hg);
    
    //Hypergraph_dump(hg);
    
    
    return 0;
}

