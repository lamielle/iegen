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

static bool debug = true;

//=======================================================
// definitions that should be automatically generated

// data reordering inspector hypergraph gen
// this macro captures A_I0_to_X0, count, and data_index
#define s1(t1) data_index = inter1[t1]; \
                        Hypergraph_ordered_insert_node(A_I0_to_X0,count, \
                        data_index); \
                        data_index = inter2[t1]; \
                        Hypergraph_ordered_insert_node(A_I0_to_X0,count, \
                        data_index); \
                        count++

// executor after data reordering
// this macro captures reordered x and fx, the index arrays inter1 and inter2,
// and the newly generated index array sigma.
#define e1(ii,g)    if ((g)==1) { \
    fx[sigma[inter1[ii]]] += x[sigma[inter1[ii]]]*0.1 \
                             + x[sigma[inter2[ii]]]*0.3; \
  } else { \
    fx[sigma[inter2[ii]]] += x[sigma[inter1[ii]]]*0.2  \
                             + x[sigma[inter2[ii]]]*0.4; \
  }

// iteration reordering inspector hypergraph gen
// this macro captures A_I1_to_X1, count, and data_index
#define s2(t1) data_index = sigma[inter1[t1]]; \
                        Hypergraph_ordered_insert_node(A_I1_to_X1,count, \
                        data_index); \
                        data_index = sigma[inter2[t1]]; \
                        Hypergraph_ordered_insert_node(A_I1_to_X1,count, \
                        data_index); \
                        count++ 

// executor after data reordering and iteration reordering
// this macro captures reordered x and fx, the index arrays inter1 and inter2,
// and the newly generated index array sigma.
#define e2(ii,g)    if ((g)==1) { \
    fx[sigma[inter1[ii]]] += x[sigma[inter1[ii]]]*0.1 \
                             + x[sigma[inter2[ii]]]*0.3; \
  } else { \
    fx[sigma[inter2[ii]]] += x[sigma[inter1[ii]]]*0.2  \
                             + x[sigma[inter2[ii]]]*0.4; \
  }


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
        inter2[i] = (i+3)%NUM_NODES;
    }
 
    if (debug) {
        printf("inter1 = "); 
        printArray(inter1, NUM_NODES);
        printf("inter2 = "); 
        printArray(inter2, NUM_NODES);
    }

    // set up data values
    for (i=0; i<NUM_NODES; i++) {
        fx[i] = 0.0;
        x[i] = i;
    }    
    if (debug) {
        printf("before original computation\n");
        printf("x = "); printRealArray(x, NUM_NODES);
        printf("fx = "); printRealArray(x, NUM_NODES);
    }
    
    //---------------- Original computation
    
    int ii;
    int n_inter = NUM_NODES;
    for (ii=0; ii<n_inter; ii++) {
        fx[inter1[ii]] += x[inter1[ii]]*0.1 + x[inter2[ii]]*0.3; 
        fx[inter2[ii]] += x[inter1[ii]]*0.2 + x[inter2[ii]]*0.4; 
    }

    // print fx values
    if (debug) {
        printf("after original computation, fx = ");
        printRealArray(fx, NUM_NODES);
    }

    // save off values of fx to enable later comparisons
    // also reset fx values to 0
    double *original_fx;
    MALLOC(original_fx, double, NUM_NODES);
    for (i=0; i<NUM_NODES; i++) {
        original_fx[i] = fx[i];
        fx[i] = 0;
    }
    
//=======================================================
// data reordering
// Code that should be automatically generated

    if (debug) {
        printf("\n===== Data Reordering =====\n");
        printf("\nbefore inspector/executor computation\n");
        printf("x = "); printRealArray(x, NUM_NODES);
        printf("fx = "); printRealArray(fx, NUM_NODES);
    }

    //---------------- Data reordering inspector/executor

    // Inspector
    // initialize variables
    Hypergraph* A_I0_to_X0 = Hypergraph_ctor();
    int count=0;
    int data_index=0;
    int t1;
                    
    // build the hypergraph representing the access relation explicitly
    for(t1 = 0; t1 <= n_inter-1; t1++) {
        // see top of file for definition of s1 macro
        s1(t1);
    }

    Hypergraph_finalize(A_I0_to_X0);

    // call the index array generator to create reordering function
    int *sigma;
    MALLOC(sigma,int,NUM_NODES);
    IAG_cpack( A_I0_to_X0, sigma );

    if (debug) {
        printf("\nAfter call to CPackHyper, sigma = ");
        printArray(sigma, NUM_NODES);
    }


    // reorder two data array based on reordering function
    reorderArray((unsigned char *)x, sizeof(double), NUM_NODES, sigma); 
    reorderArray((unsigned char *)fx, sizeof(double), NUM_NODES, sigma); 

    if (debug) {
        printf("\nafter reordering arrays\n");
        printf("x = "); printRealArray(x, NUM_NODES);
        printf("fx = "); printRealArray(fx, NUM_NODES);
    }

    // update the index arrays
    // MMS, 7/2/08, not for first time because this is really
    // a performance optimization.
    /*
    pointerUpdate(inter1, n_inter, sigma, NUM_NODES);
    pointerUpdate(inter2, n_inter, sigma, NUM_NODES);

    if (debug) {
        printf("\nafter pointer update\n");
        printf("inter1 = "); printArray(inter1, NUM_NODES);
        printf("inter2 = "); printArray(inter2, NUM_NODES);
    }
    */

    // executor - execute the computation with modified arrays
    for(t1 = 0; t1 <= n_inter-1; t1++) {
        e1(t1,1);
        e1(t1,2);
    }

//=======================================================

    // debug output
    if (debug) {
        Hypergraph_dump(A_I0_to_X0);
    
        printf("sigma = ");
        printArray(sigma, NUM_NODES);

        printf("inter1 = ");
        printArray(inter1, NUM_NODES);

        printf("inter2 = ");
        printArray(inter2, NUM_NODES);

        printf("fx = ");
        printRealArray(fx, NUM_NODES);
    }

    // testing the inspector/executor
    // first reorder the original results using the same sigma
    reorderArray((unsigned char *)original_fx, sizeof(double), NUM_NODES, sigma); 
    if (compareRealArrays(original_fx, fx, n_inter)) {
        printf("\nSame result\n");
    } else {
        printf("\nDifferent result\n");
    }

//=======================================================
// iteration reordering
// Code that should be automatically generated

    if (debug) {
        printf("\nbefore inspector/executor computation\n");
        printf("inter1 = "); printArray(inter1, NUM_NODES);
        printf("inter2 = "); printArray(inter2, NUM_NODES);
    }

    //---------------- Iteration reordering inspector/executor

    // Inspector
    // initialize variables
    {  // put in a block to simplify code between inspectors
        Hypergraph* A_I1_to_X1 = Hypergraph_ctor();
        int count=0;
        int data_index=0;
        int t1;
                    
        // build the hypergraph representing the access relation explicitly
        for(t1 = 0; t1 <= n_inter-1; t1++) {
            // see top of file for definition of s1 macro
            s2(t1);
        }

        Hypergraph_finalize(A_I1_to_X1);

        // call the index array generator to create reordering function
        int *delta;
        MALLOC(delta,int,NUM_NODES);
        IAG_lexmin( A_I1_to_X1, delta );

        if (debug) {
            printf("\nAfter call to IAG_lexmin, delta = ");
            printArray(delta, NUM_NODES);
        }

        // reorder two index arrays based on reordering function
        reorderArray((unsigned char *)inter1, sizeof(int), NUM_NODES, delta); 
        reorderArray((unsigned char *)inter2, sizeof(int), NUM_NODES, delta); 

        if (debug) {
            printf("\nafter reordering arrays\n");
            printf("inter1 = "); printArray(inter1, NUM_NODES);
            printf("inter2 = "); printArray(inter2, NUM_NODES);
        }

// Haven't figured this out yet for iteration reordering
        // executor - execute the computation with modified arrays
//        for(t1 = 0; t1 <= n_inter-1; t1++) {
//            e2(t1,1);
//            e2(t1,2);
//        }

        Hypergraph_dtor(&A_I1_to_X1);
        FREE(delta,int,NUM_NODES);

    }

//=======================================================


    // cleanup
    Hypergraph_dtor(&A_I0_to_X0);
    FREE(sigma,int,NUM_NODES);
    FREE(original_fx, double, NUM_NODES);
    FREE(fx,double,NUM_NODES);
    FREE(x,double,NUM_NODES);
    FREE(inter1,int,NUM_NODES);
    FREE(inter2,int,NUM_NODES);

    return 0;
}

