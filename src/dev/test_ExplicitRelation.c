/* test_ExplicitRelation.c */
/*! \file

    Driver that unit tests the ExplicitRelation data structure.
*/

#include "ExplicitRelation.h"
#include "IAG.h"
#include "util.h"

#define NUM_IN 10
#define NUM_OUT 5

int main() 
{
    ExplicitRelation* relptr;
    RectDomain* in_domain;
    int in, out;

    // Test out explicit relations that are functions and where the
    // in_domain is provided.
    in_domain = RD_ctor(2);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, 4);
    RD_set_lb(in_domain, 1, 1);
    RD_set_ub(in_domain, 1, 5);
    relptr = ER_ctor(2,2, in_domain, true);
    
    printf("==== Before inserting any relations into 2D -> 2D relation\n");
    ER_dump(relptr);
    
    ER_insert(relptr, Tuple_make(2,3), Tuple_make(3,4));
    ER_insert(relptr, Tuple_make(1,2), Tuple_make(2,3));
    
    // Checking with asserts.
    assert(Tuple_equal( ER_out_given_in(relptr,Tuple_make(2,3)), 
                        Tuple_make(3,4) ) );
    assert(Tuple_equal( ER_out_given_in(relptr,Tuple_make(1,2)), 
                        Tuple_make(2,3) ) );
    
    printf("==== After inserting some relations\n");
    ER_dump(relptr);    
    
    ER_dtor(&relptr);
  
    printf("==== Before inserting any relations into 1D -> 1D relation\n");
    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 3);
    RD_set_ub(in_domain, 0, 6);
    relptr = ER_ctor(1,1, in_domain, false);
    

    // then add [in]->[out] relationships 
    // for this example doing all combos of possible
    // in and out values
    int count=0;
    for (in=3; in<=6; in++) {
      for (out=0; out<=2; out++) {
            ER_in_ordered_insert( relptr, in, out );
            count++;
        }
    }
    
    ER_in_ordered_insert(relptr, 6, 3);
    count++;
    
    ER_dump(relptr);

    // Checking with asserts.
    int test_in = 3; int test_out;
    int test_count = 0;
    assert(RD_lb(in_domain, 0)==3);
    assert(RD_ub(in_domain, 0)==6);
    FOREACH_in_tuple_1d1d(relptr, in) {
        printf("\tin=%d\n", in);
        test_out = 0;
        FOREACH_out_given_in_1d1d(relptr, in, out) {
            printf("\t[%d] -> [%d]\n", in, out);
            assert( (in==test_in) && (out==test_out));
            test_out++;
            test_count++;
        }
        test_in++;
    }
    assert(test_count==count);
    
    ER_dtor(&relptr);

    //======= test creation and use of ER for access relation
    printf("==== test creation and use of ER for access relation\n");
    //------- testing code that will be used in IAG_cpack
    // first construct an explicit relation for the access
    // relation and fill it.
    // The explicit relation will be passed to IAG_cpack.
    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, (NUM_IN - 1));
    // We know in_domain for access relations, but they are not functions.
    // Notice also that this is a 1Dto1D relation example.
    relptr = ER_ctor(1,1, in_domain, false);

    // add only some out vals for each in val
    count = 0;
    for (in=0; in<NUM_IN; in++) {
      for (out=(in)%NUM_OUT; out<NUM_OUT; out+=2) {
            ER_in_ordered_insert( relptr, in, out );
            count++;
        }
    }
    
    ER_dump(relptr);
    
    // Iterate over the integer tuple relations
    printf("\nTraversing 1Dto1D relation in order of input tuples\n");
    ER_order_by_in(relptr);
    test_in=0;
    test_count=0;
    FOREACH_in_tuple_1d1d(relptr, in) {
        test_out=test_in % NUM_OUT;
        FOREACH_out_given_in_1d1d(relptr, in, out) {
            printf("\t[%d] -> [%d]\n", in, out);
            assert( (in==test_in) && (out==test_out));
            test_out+=2;
            test_count++;
        }
        test_in++;
    }
    assert(count==test_count);

    ER_dtor(&relptr);

    //======= test creation and use of ER for sigma and delta, 
    //======= which are permutations and 1D to 1D
    printf("==== test creation and use of ER for for sigma and delta\n");

    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, (NUM_IN - 1));
    // We know in_domain for permutations and a permutation is a function.
    relptr = ER_ctor(1,1, in_domain, true);

    // create a permutation that is just a modular shift
    count = 0;
    for (in=0; in<NUM_IN; in++) {
        ER_in_ordered_insert( relptr, in, (in+1) % NUM_IN);
        count++;
    }

    ER_dump(relptr);

    // Iterate over the integer tuple relations
    printf("\nTraversing sigma example\n");
    ER_order_by_in(relptr);
    test_count=0;
    test_in = 0;
    FOREACH_in_tuple_1d1d(relptr, in) {
        test_out = (in+1) % NUM_IN;
        printf("\t[%d] -> [%d]\n", in, ER_out_given_in(relptr,in));
        assert((in==test_in) && test_out==ER_out_given_in(relptr,in));
        test_count++;
        test_in++;
    }
    assert(count==test_count);

    ER_dtor(&relptr);

    //======= test creation and use of 2D-to-3D example
    // { [i,j] -> [i,j,k] : k=1 && 1 <= i,j <= 10}
    // union { [i,j] -> [i-1,j+1,k] : k=2 && 1 <= i,j <= 10}
    printf("==== test creation and use of 2D-to-3D example\n");
    printf("example: { [i,j] -> [i,j,k] : k=1 && 0 <= i,j <= 10}\n\tunion { [i,j] -> [i-1,j+1,k] : k=2 && 0 <= i,j <= 10}\n");
    
    in_domain = RD_ctor(2);
    // i
    RD_set_lb(in_domain, 0, 1); RD_set_ub(in_domain, 0, 10);
    // j
    RD_set_lb(in_domain, 1, 1); RD_set_ub(in_domain, 1, 10);
    
    // We know in_domain for data dependence, but it is not a function.
    relptr = ER_ctor(2,3, in_domain, false);
    
    // code for explicitly creating the relation
    // we should be able to automatically generate this loop from the
    // static specification of the relation
  {
    
    int i, j, k;
    count = 0;
    for (i=1; i<=10; i++) {
        for (j=1; j<=10; j++) {
            k=1;
            ER_in_ordered_insert( relptr, 
                Tuple_make(i,j), Tuple_make(i,j,k));
            printf("\tER_in_ordered_insert( (%d, %d), (%d, %d, %d) )\n", 
                   i, j, i, j, k);

            k=2;
            ER_in_ordered_insert( relptr, 
                Tuple_make(i,j), Tuple_make(i-1,j+1,k));
            printf("\tER_in_ordered_insert( (%d, %d), (%d, %d, %d) )\n", 
                   i, j, i-1, j+1, k);
                   
            count +=2;
        }
    }

    ER_dump(relptr);
    
    // Iterate over the integer tuple relations
    printf("\nTraversing 2D-to-3D example\n");
    ER_order_by_in(relptr);
    Tuple in_tuple, out_tuple;
    test_count = 0;
    FOREACH_in_tuple(relptr, in_tuple) {
       int out_count=0;
       FOREACH_out_given_in(relptr, in_tuple, out_tuple) {
            printf("\t");
            Tuple_print(in_tuple);
            printf(" -> ");
            Tuple_print(out_tuple);
            printf("\n");
            // testing the output tuples being retrieved
            if (out_count == 0) {
                assert( Tuple_val(out_tuple,0)==Tuple_val(in_tuple,0)
                        && Tuple_val(out_tuple,1)==Tuple_val(in_tuple,1)
                        && Tuple_val(out_tuple,2)==1 );
            } else { 
                assert( Tuple_val(out_tuple,0)==(Tuple_val(in_tuple,0)-1)
                        && Tuple_val(out_tuple,1)==(Tuple_val(in_tuple,1)+1)
                        && Tuple_val(out_tuple,2)==2 );
            }
            assert(out_count<=1);
            out_count++;
            test_count++;
        }
    }
    printf("\n");
    assert(count == test_count);

    ER_dtor(&relptr);
  }
    
    //======= test creation and use of ER for data dependences
    // { [s,z,i,j] -> [c] : z=1 && j=1 && i=inter1(c) && s=1 && 0 <= i <= 10}
    // union { [s,z,i,j] -> [c] : z=1 && j=1 && i=inter2(c) && s=1 && 0<=i<=10}
    printf("==== test creation and use of ER for for data dependences\n");
    printf("example: { [s,z,i,j] -> [c] : z=1 && j=1 && i=inter1(c) && s=1 && 0 <= i <= 10}\n\tunion { [s,z,i,j] -> [c] : z=1 && j=1 && i=inter2(c) && s=1 && 0<=i<=10}\n");
    
    in_domain = RD_ctor(4);
    // s
    RD_set_lb(in_domain, 0, 1); RD_set_ub(in_domain, 0, 1);
    // z
    RD_set_lb(in_domain, 1, 1); RD_set_ub(in_domain, 1, 1);
    // i
    RD_set_lb(in_domain, 2, 0); RD_set_ub(in_domain, 2, 10);
    // j
    RD_set_lb(in_domain, 3, 1); RD_set_ub(in_domain, 3, 1);
    
    // We know in_domain for data dependence, but it is not a function.
    relptr = ER_ctor(4,1, in_domain, false);
    
    // create fake index arrays inter1 and inter2
    int * inter1 = (int*)malloc(sizeof(int)*11);
    int * inter2 = (int*)malloc(sizeof(int)*11);
    int k;
    for (k=0; k<11; k++) {
        inter1[k] = k;
        inter2[k] = (k+3) % 11;
    }
    
    // convert those index arrays into explicit relations
    // FIXME: how will we automate this process?
    ExplicitRelation * inter1_ER = ER_ctor(inter1,11);
    ExplicitRelation * inter2_ER = ER_ctor(inter2,11);

    // code for explicitly creating the data dependences
    // loop would be generated by cloog
    int s, z, i, j;
    s = 1; z = 1;
    count = 0;
    for (i=0; i<=10; i++) {
        j=1;
        ER_in_ordered_insert( relptr, 
            Tuple_make(s,z,i,j), Tuple_make(ER_out_given_in(inter1_ER,i)));
        ER_in_ordered_insert( relptr, 
            Tuple_make(s,z,i,j), Tuple_make(ER_out_given_in(inter2_ER,i)));

        count += 2;
    }
    

    ER_dump(relptr);
    
    // Iterate over the integer tuple relations
    printf("\nTraversing access relation example\n");
    ER_order_by_in(relptr);
    Tuple in_tuple, out_tuple;
    test_count = 0;
    FOREACH_in_tuple(relptr, in_tuple) {
        int out_count = 0;
        FOREACH_out_given_in(relptr, in_tuple, out_tuple) {
            printf("\t");
            Tuple_print(in_tuple);
            printf(" -> ");
            Tuple_print(out_tuple);
            printf("\n");
            test_count++;
            
            // testing the output tuples being retrieved
            if (out_count == 0) {
                assert( Tuple_val(out_tuple,0)
                        ==ER_out_given_in(inter1_ER,Tuple_val(in_tuple,2)) );
            } else { 
                assert( Tuple_val(out_tuple,0)
                        ==ER_out_given_in(inter2_ER,Tuple_val(in_tuple,2)) );
            }

            out_count++;
        }
    }
    printf("\n");
    assert(test_count==count);

    // keeping this relptr as input to testing IAG_cpack
    //ER_dtor(&relptr);


    //----- testing IAG_cpack itself
    // constructing sigma
    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, 10);
    ExplicitRelation * sigma = ER_ctor(1,1,in_domain,true);
    
    // relptr is input to IAG_cpack and sigma is output
    IAG_cpack( relptr, sigma );    
    
    printf("==== dumping sigma after IAG_cpack call\n");
    ER_dump(sigma);
    assert(ER_verify_permutation(sigma));
    
    ER_dtor(&relptr);
    ER_dtor(&sigma);


    //======= test creation and use of ER for access relation
    // Recreating and then fixing BUG Alan found where 
    // ER_in_ordered_insert doesn't work when the in_domain is not
    // specified.
    printf("==== test creation and use of ER when in_domain not specified\n");

    // Notice also that this is a 1Dto1D relation example.
    relptr = ER_ctor(1,1);

    // add only some out vals for each in val
    count = 0;
    for (in=0; in<NUM_IN; in++) {
      for (out=(in)%NUM_OUT; out<NUM_OUT; out+=2) {
            ER_in_ordered_insert( relptr, in, out );
            count++;
        }
    }
    
    ER_dump(relptr);
    
    // Iterate over the integer tuple relations
    printf("\nTraversing 1Dto1D relation in order of input tuples\n");
    ER_order_by_in(relptr);
    test_in=0;
    test_count=0;
    FOREACH_in_tuple_1d1d(relptr, in) {
        test_out=test_in % NUM_OUT;
        FOREACH_out_given_in_1d1d(relptr, in, out) {
            printf("\t[%d] -> [%d]\n", in, out);
            assert( (in==test_in) && (out==test_out));
            test_out+=2;
            test_count++;
        }
        test_in++;
    }
    assert(count==test_count);

    ER_dtor(&relptr);


    //======= test ER_genInverse
    // Recreating and then fixing BUG Alan found where 
    // ER_in_ordered_insert doesn't work when the in_domain is not
    // specified.
    printf("==== test creation and use of ER when in_domain not specified\n");
    
    // create an input relation
    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, (NUM_IN - 1));
    // We know in_domain for permutations and a permutation is a function.
    relptr = ER_ctor(1,1, in_domain, true);

    // create a permutation that is just a modular shift
    count = 0;
    for (in=0; in<NUM_IN; in++) {
        ER_in_ordered_insert( relptr, in, (in+1) % NUM_IN);
        count++;
    }

    ER_dump(relptr);

    // Iterate over the integer tuple relations
    printf("\nTraversing relation we plan to invert\n");
    ER_order_by_in(relptr);
    test_count=0;
    test_in = 0;
    FOREACH_in_tuple_1d1d(relptr, in) {
        test_out = (in+1) % NUM_IN;
        printf("\t[%d] -> [%d]\n", in, ER_out_given_in(relptr,in));
        assert((in==test_in) && test_out==ER_out_given_in(relptr,in));
        test_count++;
        test_in++;
    }
    assert(count==test_count);
    
    // call routine that should generate the inverse
    ExplicitRelation* new_relptr = ER_genInverse(relptr);
    printf("Dumping inverse relation\n");
    ER_dump(new_relptr);


    // Iterate over the integer tuple relations
    printf("\nTraversing inverted relation\n");
    ER_order_by_in(relptr); // FIXME: want to remove these
    test_count=0;
    test_in = 0;
    FOREACH_in_tuple_1d1d(new_relptr, in) {
        test_out = (in-1);
        if (test_out == -1) { test_out = NUM_IN-1; }
        printf("\t[%d] -> [%d]\n", in, ER_out_given_in(new_relptr,in));
        assert((in==test_in) && (test_out==ER_out_given_in(new_relptr,in)));
        assert(in==ER_out_given_in(relptr,ER_out_given_in(new_relptr,in)));
        test_count++;
        test_in++;
    }
    assert(count==test_count);
    

    // ok now do somewhat of a stress test of the memory management
    /* MMS, this takes a long time so only do it when MEM_ALLOC_INCREMENT
     * is set low
    hg = Hypergraph_ctor();
    for (he=0; he<MEM_ALLOC_INCREMENT*2+10; he++) {
      for (n=0; n<MEM_ALLOC_INCREMENT*2+5; n++) {
      
            Hypergraph_ordered_insert_node( hg, he, n );
        }
    }
    Hypergraph_finalize(hg);
    Hypergraph_dtor(&hg);
    
    //Hypergraph_dump(hg);
    */
    
    //======= testing creation and iteration over a 2D-to-3D
    //======= explicit relation.
    //  - using unordered insert
    //  - using assert to check values returned by FOREACH loops
    //  - using a non-zero lower bound for some of the in domain dims
    

    
    return 0;
}

