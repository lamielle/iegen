/*! \file

    IAG_lexmin.c

    A version of the lexmin reordering heuristic that operates on the
    ExplicitRelation datastructure version of the access relation.
    It iterates over the relation in order of the output tuples.

*/

#include "util.h"
#include "ExplicitRelation.h"

void IAG_lexmin(ExplicitRelation* relptr, ExplicitRelation*  old2new)
/*----------------------------------------------------------------*//*! 
    \short Creates permutation of input tuples based on order they 
           order they are seen with output tuples.

    \param relptr   Pointer to the explicit relation that represents
                    how the iterations of a loop map to a data space.
                    Assumed to be a 1D-to-1D relation.
                    
    \param old2new  Explicit relation that maps old iteration 
                    to new iteration.  Should be contructed but empty 
                    before entry to this function. 

    The mapping will be a permutation. 
    Another way of thinking about it is that at index 0 in old2new there
    will be the new id for what was previously output tuple value 0.  

    Lexmin is the dual to CPack.  Another way to implement Lexmin is
    to create the inverse explicit relation for relptr and pass that into CPack.  

    \author Michelle Strout 7/9/08, 11/11/08
*//*----------------------------------------------------------------*/
{
    assert(old2new!=NULL);
    assert(relptr!=NULL);
    assert(relptr->in_arity==1 && relptr->out_arity==1);

    int  in, out, count;
    bool *taken;

    // number of items we will be mapping from an old location
    // to a new location
    int out_count = RD_size(ER_in_domain(old2new));


        
    // allocate array that keeps track of what points in the
    // have been remapped
    MALLOC(taken, bool, out_count);
    int index;
    for (index = 0; index < count; index++) {
            taken[index] = false;
    }

    // reorder input tuples on a first-touch basis
    // based on order of output tuples
    // FIXME: switch the FOREACH
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
        
    // handle input tuples that are never touched, if any 
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

