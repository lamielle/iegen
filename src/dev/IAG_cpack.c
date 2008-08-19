/*! \file

    IAG_cpack.c

    A version of the cpack reordering heuristic that operates on the
    Hypergraph datastructure version of the access relation.

*/

#include "IAG.h"

void IAG_cpack(ExplicitRelation* relptr, int* old2new)
/*----------------------------------------------------------------*//*! 
    \brief Creates permutation of explicit relation's range 
           (set of output tuple values) based on the order they appear
           with the sorted input tuple values.

    \param relptr   Pointer to the explicit relation.
    \param old2new  Maps old index to new index.

    It is assumed that old2new points to an array of integers with
    one integer per unique output tuple in the explicit relation.  
    This function will fill the old2new array with a mapping of old 
    output tuple to new output tuple. 
    // FIXME: old2new needs to be generalized to an explicit relation?
    // or we need to assert if the explicit relation does not have 1D-to-1D
    // arity.  How will the results of this function be used?
    // We might be able to make the 1D-to-1D assertion, but still 
    // represent old2new with an ExplicitRelation.
    The mapping will be a permutation. 
    Another way of thinking about it is that at index 0 in old2new there
    will be the new id for what was previously output tuple value 0.  

    \author Michelle Strout 8/19/08
*//*----------------------------------------------------------------*/
{
    assert(old2new!=NULL);
    assert(relptr!=NULL);

    int  in, count, out;
    bool *taken;

    // number of unique output tuples in relation
    int out_count = ExplicitRelation_getRangeCount(relptr);
        
    MALLOC(taken, bool, out_count);
    
    for (out = 0; out < out_count; out++) {
            taken[out] = false;
    }
            
    // reorder out tuples on a first-touch basis
    count = 0;
    FOREACH_in_tuple_1d1d(relptr, in) {
        FOREACH_out_given_in_1d1d(relptr, in, out) {
            if (!taken[out]) {
                old2new[out] = count;
                taken[out]   = true;
                count++;
            }
        }
    }
        
    // handle nodes that are never touched, if any 
    if (count < out_count) {
        for (out = 0; out < out_count; out++) {
            if (taken[out] == false) {
                old2new[out] = count;
                count++;
            }
        }
    }
        
    FREE(taken,bool,out_count);
}

