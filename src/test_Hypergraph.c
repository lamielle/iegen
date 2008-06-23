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
    
    return 0;
}