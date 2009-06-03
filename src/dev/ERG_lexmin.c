/*! \file

    ERG_lexmin.c

    A version of the lexmin reordering heuristic that operates on the
    ExplicitRelation datastructure version of the access relation.
    It iterates over the relation in order of the output tuples.

*/

#include "util.h"
#include "ExplicitRelation.h"

void ERG_lexmin(ExplicitRelation* relptr, ExplicitRelation*  old2new)
/*----------------------------------------------------------------*//*! 
    \short Creates permutation of input tuples based on order they 
           order they are seen with output tuples.

    \param relptr   Pointer to the explicit relation that represents
                    how the iterations of a loop map to a data space.
                    Assumed to be a 1D-to-1D relation.
                    
    \param old2new  Explicit relation that maps old iteration 
                    to new iteration.  Should be contructed but empty 
                    before entry to this function.  old2new will
                    be a permutation.

    The old2new mapping will be a permutation. 
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

    bool *taken;

    // number of items we will be mapping from an old location
    // to a new location
    int in_count = RD_size(ER_in_domain(old2new));


        
    // allocate array that keeps track of what points in the
    // have been remapped
    MALLOC(taken, bool, in_count);
    int index;
    for (index = 0; index < in_count; index++) {
            taken[index] = false;
    }

    // Reorder input tuples on a first-touch basis
    // based on order of output tuples.
    // To iterate over relation in order of output tuples
    // creating the inverse of the relation.
    int  in=0, out=0, inv_in, inv_out, count;
    count = 0;
    
    // First create the inverse relation.
    ExplicitRelation *inv_relptr = ER_genInverse(relptr);

    // Then iterate over that inverse relation.
    FOREACH_in_tuple_1d1d(inv_relptr, inv_in) {        
        FOREACH_out_given_in_1d1d(inv_relptr, inv_in, inv_out) {
            // input and output tuples for original relation
            out = inv_in;
            in = inv_out;

            if (!taken[in]) {
                ER_insert(old2new, in, count);
                taken[in]   = true;
                count++;
            }
        }
    }
        
    // handle input tuples that are never touched, if any 
    if (count < in_count) {
        for (in = 0; out < in_count; in++) {
            if (taken[in] == false) {
                ER_insert(old2new, in, count);
                count++;
            }
        }
    }
        
    FREE(taken,bool,in_count);       
}

