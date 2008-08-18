/*! \file

    IAG_cpack.c

    A version of the cpack reordering heuristic that operates on the
    Hypergraph datastructure version of the access relation.

*/

#include "util.h"
#include "Hypergraph.h"

/*----------------------------------------------------------------*//*! 
    \short Creates permutation of nodes in hypergraph based on hyperedge order.

    \param hg       Pointer to the hypergraph.
    \param old2new  Maps old index to new index.

    It is assumed that old2new points to an array of integers with
    one integer per node in the hypergraph.  This function will fill
    the old2new array with a mapping of old node to new node.  The mapping
    will be a permutation. 
    Another way of thinking about it is that at index 0 in old2new there
    will be the new id for what was previously node 0.  

    \author Kevin Depue, edited significantly by Michelle Strout 6/2008
*//*----------------------------------------------------------------*/
void CPackHyper(Hypergraph* hg, int* old2new)
{
    assert(old2new!=NULL);
    assert(hg!=NULL);

    int  hedge, count, index;
    bool *taken;

    // number of nodes in the hypergraph
    int nnodes = hg->nv;
        
    MALLOC(taken, bool, nnodes);
    
    for (index = 0; index < nnodes; index++) {
            taken[index] = false;
    }
            
    // reorder nodes on a first-touch basis
    count = 0;
    FOREACH_hyperedge(hg,hedge) {
        FOREACH_node_in_hyperedge(hg,hedge,index) {
            if (!taken[index]) {
                old2new[index] = count;
                taken[index]   = true;
                count++;
            }
        }
    }
        
    // handle nodes that are never touched, if any 
    if (count < nnodes) {
        for (index = 0; index < nnodes; index++) {
            if (taken[index] == false) {
                old2new[index] = count;
                count++;
            }
        }
    }
        
    FREE(taken,bool,nnodes);
}

