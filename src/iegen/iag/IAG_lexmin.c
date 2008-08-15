/*! \file

    IAG_lexmin.c

    A version of the lexmin reordering heuristic that operates on the
    Hypergraph datastructure version of the access relation.
    It iterates over the nodes in the hypergraph in order, thus
    requiring the hypergraph dual.

*/

#include <iegen/util/iegen_util.h>
#include <iegen/hypergraph/Hypergraph.h>

/*----------------------------------------------------------------*//*! 
    \short Creates permutation of hyperedges based on the node order.

    \param hg       Pointer to the hypergraph.
    \param old2new  Maps old edge id to new edge id.

    It is assumed that old2new points to an array of integers with
    one integer per hyperedge in the hypergraph.  This function will fill
    the old2new array with a mapping of old edge to new edge.  The mapping
    will be a permutation. 
    Another way of thinking about it is that at index 0 in old2new there
    will be the new id for what was previously hyperedge 0.  

    Lexmin is the dual to CPack.  Another way to implement Lexmin is
    to create the dual hypergraph and pass that into CPack.  
    However, since the Hypergraph abstraction contains the primary
    and dual (and currently no way to swap the too) this implementation
    is a nice test of whether the dual is correctly constructed when
    we want to iterate over the hypergraph nodes in order.

    \author Michelle Strout 7/9/08
*//*----------------------------------------------------------------*/
void IAG_lexmin(Hypergraph* hg, int* old2new)
{
    assert(old2new!=NULL);
    assert(hg!=NULL);

    int  node, count, hedge;
    bool *taken;

    // number of nodes in the hypergraph
    //int nnodes = hg->nv;
    // number of edges in the hypergraph
    int nedges = hg->ne;
        
    MALLOC(taken, bool, nedges);
    
    fprintf(stderr,"WARNING: variable 'index' changed to 'i' here to make this code compile.\n");
    int i;
    for (i = 0; i < nedges; i++) {
            taken[i] = false;
    }
            
    // reorder nodes on a first-touch basis
    count = 0;
    FOREACH_node(hg,node) {
        FOREACH_hyperedge_for_node(hg,node,hedge) {
            if (!taken[hedge]) {
                old2new[hedge] = count;
                taken[hedge]   = true;
                count++;
            }
        }
    }
        
    // handle nodes that are never touched, if any 
    if (count < nedges) {
        for (hedge = 0; hedge < nedges; hedge++) {
            if (taken[hedge] == false) {
                old2new[hedge] = count;
                count++;
            }
        }
    }
        
    FREE(taken,bool,nedges);
}

