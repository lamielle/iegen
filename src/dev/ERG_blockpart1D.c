/*! \file

    ERG_blockpart.c
    
    A block partitioner that generates an explicit relation as output.
    It would be more efficient to compute a block partitioning on the fly
    but it doesn't enable using the ER interface consistently just yet.
    Eventually I think we could create ERs that use closed form functions
    to return their values.


*/

#include "ERG.h"

void ERG_blockpart1D(int numpart, ExplicitRelation* part)
/*----------------------------------------------------------------*//*! 
    \brief This explicit relation generator creates an explicit relation that maps points in the in domain for part to partitions numbers 
    0 through numpart-1.

    The partitioning done is a simple block parititioning along each
    dimension (i.e. lb through lb+(loopsize/numpart) 
    are in the zeroth partition, lb+(loopsize/numpart)+1 through
    lb+2*(loopsize/numpart) are in the first partition, etc.).


    \param domain   Rectangular domain specified as lower and upper bounds.
                    
    \param numpart  Number of partitions.
                    
    \param part     Result of this function.  This function assumes that
                    part is an empty ExplicitRelation with its in
                    domain specified.
                    

    \author Michelle Strout 5/20/09
*//*----------------------------------------------------------------*/
{
    // check inputs
    assert(numpart > 0);
    assert(part!=NULL);
    
    // determine the partition size by computing the size of the last
    // dimension in the in domain and dividing it by numpart
    // FIXME: this definitely needs refactored.  The ERGs should
    // not be exposed to what data structures are being used for the
    // in domain and out range of the ER.
    int last_elem = RD_dim(RUD_approx(ER_in_domain(part)))-1;
    int lb = RD_lb(RUD_approx(ER_in_domain(part)), last_elem);
    int ub = RD_ub(RUD_approx(ER_in_domain(part)), last_elem);
    int partsize = ((ub-lb+1) / numpart) + 1;

    // Loop through points in in domain and assign them to partitions.
    Tuple in_tuple;
    FOREACH_in_tuple(part, in_tuple) {
        ER_insert(part, in_tuple, 
            Tuple_make( Tuple_val(in_tuple,last_elem)/partsize ) );
    }
        
}

