/*! \file

    IAG_cpack.c

    A version of the cpack reordering heuristic that operates on the
    explicit relation datastructure version of the access relation.

*/

#include "IAG.h"

void IAG_cpack(ExplicitRelation* relptr, ExplicitRelation* old2new)
/*----------------------------------------------------------------*//*! 
    \brief Creates permutation of explicit relation's range 
           (set of output tuple values) based on the order they appear
           with the sorted input tuple values.

    \param relptr   Pointer to the explicit relation that represents
                    how the iterations of a loop map to a data space.
    \param old2new  Explicit relation that maps old data index 
                    to new data index.  Should be contructed but empty 
                    before entry to this function. 

    The mapping will be a permutation. 
    Another way of thinking about it is that at index 0 in old2new there
    will be the new id for what was previously output tuple value 0.  

    \author Michelle Strout 8/19/08, 8/23/08
*//*----------------------------------------------------------------*/
{
    assert(relptr!=NULL);
    assert(old2new!=NULL);
    // FIXME? don't have anyway to check that old2new is empty

    int  in, count, out;
    bool *taken;

    // number of items we will be mapping from an old location
    // to a new location
    int out_count = RD_size(ER_in_domain(old2new));

    // allocate array that keeps track of what points in the
    // have been remapped
    MALLOC(taken, bool, out_count);
    for (out = 0; out < out_count; out++) {
            taken[out] = false;
    }
    
    
    // reorder data indices (out vals) on a first-touch basis
    count = 0;
    FOREACH_in_tuple_1d1d(relptr, in) {
        FOREACH_out_given_in_1d1d(relptr, in, out) {
            if (!taken[out]) {
                ER_insert(old2new, out, count);
                taken[out]   = true;
                count++;
            }
        }
    }
        
    // handle nodes that are never touched, if any 
    if (count < out_count) {
        for (out = 0; out < out_count; out++) {
            if (taken[out] == false) {
                ER_insert(old2new, out, count);
                count++;
            }
        }
    }
        
    FREE(taken,bool,out_count);
}

