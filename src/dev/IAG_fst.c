/*! \file

    IAG_fst.c

    A version of the full sparse tiling inspector that uses
    the explicit relation data structure.

*/

#include "IAG.h"

ExplicitRelation* 
IAG_fst(ExplicitRelation* todeps, ExplicitRelation* fromdeps, 
        ExplicitRelation* seedpart)
/*----------------------------------------------------------------*//*! 
    \brief 

    \param todeps   Pointer to the explicit relation that represents
                    dependences going to the seed subspace.
                    
    \param fromdeps Pointer to the explicit relation that represents
                    dependences coming from the seed subspace.
                    
    \param seedpart Seed partition relation, which maps each point in
                    the seed subspace to a seed partition.
                    
    \return theta    Result of this function.  An explicit relation 
                    that maps points in the iteration space being
                    tiled to tiles.  The points in the seed subspace
                    will be mapped to a tile with the same number as
                    their seed partition.  

    \author Michelle Strout 8/25/08
*//*----------------------------------------------------------------*/
{
    // make sure we don't get any null input information
    assert(todeps!=NULL && fromdeps!=NULL && seedpart!=NULL);
    
    // We assume that the seed space arity is the same in its mapping to 
    // seed partitions as it is in the dependences.
    assert(ER_in_arity(seedpart)==ER_in_arity(fromdeps));
    assert(ER_in_arity(seedpart)==ER_out_arity(todeps));

    // construct an explicit relation to store theta
    // theta is a function, each iteration point only mapped to one tile
    // FIXME: need to get domain space as an input to function so can
    // pass into constructor
    // FIXME: how can we indicate that default out value should be 0?
    theta = ER_ctor( ER_in_arity(seedpart), 1, domain_space, function);
    
    // set all of the seed subspace theta values to the same
    // as their seed partition values.
    // IOW, each seed space iteration point is in the same named
    // tile as seed partition.
    // No order required on seedpart relation.
    FOREACH_in_tuple(seedpart, in_tuple) {
        // seed partition is a function
        out_tuple = ER_out_given_in(seedpart, in_tuple)
     
        ER_insert( theta, in_tuple, out_tuple);
        
        // iterate over todeps and set input tuple of
        // dependence to largest possible tile
        
        // iterate over fromdeps and set output tuple of
        // dependence to smallest possible tile
        
    }
    
    
    
    // iterate over the seed partitions in order
    FOREACH_out_tuple(seedpart, out_tuple) {
        FOREACH_in_given_out(seedpart, out_tuple, seed_space_point) {
        
            // iterate over the data dependences coming into this 
            // seed space iteration point.  Growing the tiles backwards.
            FOREACH_in_given_out(todeps, seed_space_point, in_dep) {
                ER_insert(theta, in_dep, 
                          MIN( ER_out_given_in(theta, in_dep),
                               ER_out_given_in(seedpart, seed_space_point));
            }
            
            // grow forwards will be similar except with MAX and fromdeps
                

    }
    
    
}

