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
    \param new2old  Array containing permutation of hypergraph nodes.

    It is assumed that new2old points to an array of integers with
    one integer per node in the hypergraph.  This function will fill
    the new2old array with a permutation of the hypergraph nodes.
    Another way of thinking about it is that at index 0 in new2old there
    will be the old id for a node.  Its new id will be 0 once
    this reordering is used.

    \author Kevin Depue, edited by Michelle Strout 6/2008
*//*----------------------------------------------------------------*/
void CPackHyper(Hypergraph* hg, int* new2old)
{
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
                new2old[count] = index;
                taken[index]   = true;
                count++;
            }
        }
    }
        
    // handle nodes that are never touched, if any 
    if (count < nnodes) {
        for (index = 0; index < nnodes; index++) {
            if (taken[index] == false) {
                new2old[count] = index;
                count++;
            }
        }
    }
        
    FREE(taken,bool,nnodes);
}

