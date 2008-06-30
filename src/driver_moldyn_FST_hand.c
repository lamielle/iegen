/* driver_moldyn_FST_hand.c */
/*! \file
    Driver that was written by hand to test various composed inspectors for 
    a much simplified moldyn.

    See iegen/docs/moldyn-FST.txt for more notes.
*/

#include "Hypergraph.h"
#include "IAG.h"
#include "util.h"

#define NUM_NODES 5

int main() 
{
    // Create a fake interaction list.  Have node i and node (i+1)%NUM_NODES
    // interact.

    // data arrays
    double *fx, *x;
    MALLOC(fx,double,NUM_NODES);
    MALLOC(x,double,NUM_NODES);

    // index arrays
    int *inter1, *inter2;
    MALLOC(inter1,int,NUM_NODES);
    MALLOC(inter2,int,NUM_NODES);
    
    // set up the interactions
    int i;
    for (i=0; i<NUM_NODES; i++) {
        inter1[i] = i;
        inter2[i] = (i+1)%NUM_NODES;
    }
 
    printf("inter1 = "); 
    printArray(inter1, NUM_NODES);
    printf("inter2 = "); 
    printArray(inter2, NUM_NODES);
    
    
    return 0;
}

