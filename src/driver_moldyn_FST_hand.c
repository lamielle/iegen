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

//=======================================================
// definitions that should be automatically generated

// this macro captures A_II0_to_X0, count, and data_index
#define s1(t1) data_index = inter1[t1]; \
                        Hypergraph_ordered_insert_node(A_II0_to_X0,count, \
                        data_index); \
                        data_index = inter2[t1]; \
                        Hypergraph_ordered_insert_node(A_II0_to_X0,count, \
                        data_index); \
                        count++
//=======================================================

int main() 
{
    // Create a fake interaction list.  Have node i and node (i+2)%NUM_NODES
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
        inter2[i] = (i+2)%NUM_NODES;
    }
 
    printf("inter1 = "); 
    printArray(inter1, NUM_NODES);
    printf("inter2 = "); 
    printArray(inter2, NUM_NODES);

    // set up data values
    for (i=0; i<NUM_NODES; i++) {
        fx[i] = 0.0;
        x[i] = i;
    }    
    
    //---------------- Original computation
    
    int ii;
    int n_inter = NUM_NODES;
    for (ii=0; ii<n_inter; ii++) {
        fx[inter1[ii]] += x[inter1[ii]] - x[inter2[ii]]; 
        fx[inter2[ii]] += x[inter1[ii]] - x[inter2[ii]]; 
    }

    // print fx values
    printf("fx = ");
    for (i=0; i<NUM_NODES; i++) {
        printf("%f ", fx[i]);
    }
    printf("\n");

    // save off values of fx to enable later comparisons
    // also reset fx values to 0
    double *original_fx;
    MALLOC(original_fx, double, NUM_NODES);
    for (i=0; i<NUM_NODES; i++) {
        original_fx[i] = fx[i];
        fx[i] = 0;
    }
    
//=======================================================
// Code that should be automatically generated

    //---------------- Data reordering inspector/executor

    // Inspector
    // initialize variables
    Hypergraph* A_II0_to_X0 = Hypergraph_ctor();
    int count=0;
    int data_index=0;
    int t1;
                    
    // build the hypergraph representing the access relation explicitly
    for(t1 = 0; t1 <= n_inter-1; t1++) {
        // see top of file for definition of s1 macro
        s1(t1);
    }

    Hypergraph_finalize(A_II0_to_X0);

    // call the index array generator to create reordering function
    int *sigma;
    MALLOC(sigma,int,NUM_NODES);
    CPackHyper( A_II0_to_X0, sigma );

    // FIXME: sigma is really new2old, inverse of what transformation
    // specifies

    // reorder two data array based on reordering function
    // FIXME: this interface is a bit confusing, might want to refactor
    int n = 2;          // reordering 2 arrays
    long (*repos)[2];   // pointer to reordering info
    repos = (long (*)[2]) malloc( sizeof(long)*2*n ); 
    repos[0][0] = (long) x; repos[0][1] = sizeof(*x);
    repos[0][0] = (long) fx; repos[0][1] = sizeof(*fx);
    reorderArrays(n,repos,sigma,NUM_NODES); 

    // update the index arrays
    pointerUpdate(inter1, n_inter, sigma, NUM_NODES);
    pointerUpdate(inter2, n_inter, sigma, NUM_NODES);

    // executor - execute the computation with modified arrays
    for (ii=0; ii<n_inter; ii++) {
        fx[inter1[ii]] += x[inter1[ii]] - x[inter2[ii]]; 
        fx[inter2[ii]] += x[inter1[ii]] - x[inter2[ii]]; 
    }

//=======================================================

    // testing the inspector/executor
    Hypergraph_dump(A_II0_to_X0);
    if (compareRealArrays(original_fx, fx, n_inter)) {
        printf("Same result\n");
    } else {
        printf("Different result\n");
    }

    return 0;
}

