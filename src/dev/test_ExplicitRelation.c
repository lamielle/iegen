/* test_ExplicitRelation.c */
/*! \file

    Driver that unit tests the ExplicitRelation data structure.
*/

#include "ExplicitRelation.h"
#include "ERG.h"
#include "util.h"

#define NUM_IN 10
#define NUM_OUT 5

static int debug = false;

int main() 
{
  
  // scoping so that each test case can use the same variable names
  
  //-----------------------------------------------------------------
  // 2D to 2D relation that is a function, but not a permutation.
  // input domain is specified.
  //-----------------------------------------------------------------
  {
    ExplicitRelation* relptr;
    RectDomain* in_domain;
    bool isFunction, isPermutation;

    // Test out explicit relations that are functions and where the
    // in_domain is provided.
    in_domain = RD_ctor(2);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, 4);
    RD_set_lb(in_domain, 1, 1);
    RD_set_ub(in_domain, 1, 5);
    isFunction = true; isPermutation = false;
    relptr = ER_ctor(2,2, in_domain, isFunction, isPermutation);
    
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
  }

  //-----------------------------------------------------------------
  // 1D to 1D relation that is neither a function, nor a permutation
  // input domain is specified.
  //-----------------------------------------------------------------  
  {
    ExplicitRelation* relptr;
    RectDomain* in_domain;
    int in, out;
    bool isFunction, isPermutation;

    printf("\n==== Before inserting any relations into 1D -> 1D relation\n");
    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 3);
    RD_set_ub(in_domain, 0, 6);
    isFunction = false; isPermutation = false;
    relptr = ER_ctor(1,1, in_domain, isFunction, isPermutation);
    

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
  }

  //-----------------------------------------------------------------
  // Testing ER_genInverse on a 1D to 1D function, which is also a 
  // permutation.  The input domain is provided.
  //-----------------------------------------------------------------    
  {
    ExplicitRelation* relptr;
    RectDomain* in_domain;
    int in, count, test_count, test_in, test_out;
    bool isFunction, isPermutation;
  
    //======= test ER_genInverse
    printf("\n==== test ER_genInverse\n");
    
    // create an input relation
    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, (NUM_IN - 1));
    isFunction = true;
    isPermutation = true;
    relptr = ER_ctor(1,1, in_domain, isFunction, isPermutation);

    // create a permutation that is just a modular shift
    count = 0;
    for (in=0; in<NUM_IN; in++) {
        ER_in_ordered_insert( relptr, in, (in+1) % NUM_IN);
        count++;
    }

    ER_dump(relptr);

    // Iterate over the integer tuple relations
    printf("\nTraversing relation we plan to invert\n");
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
    
    ER_dtor(&relptr);
    ER_dtor(&new_relptr);

  }    
    

  //-----------------------------------------------------------------
  // 1D to 1D relation that is neither a function nor a permutation. 
  // Similar to the kind of access relation that we might feed to 
  // ERG_CPack and ERG_lexmin, which are also tested here.
  //-----------------------------------------------------------------    
  {
    ExplicitRelation* relptr;
    RectDomain* in_domain;
    int in, out, count, test_count, test_in, test_out;
    bool isFunction, isPermutation;

    //======= test creation and use of ER for access relation
    printf("==== test creation and use of ER for access relation\n");
    //------- testing code that will be used in ERG_cpack
    // first construct an explicit relation for the access
    // relation and fill it.
    // The explicit relation will be passed to ERG_cpack.
    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, (NUM_IN - 1));
    // We know in_domain for access relations, 
    // but they are not functions or permutations.
    // Notice also that this is a 1Dto1D relation example.
    isFunction = false;
    isPermutation = false;
    relptr = ER_ctor(1,1, in_domain, isFunction, isPermutation);

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
    
    // Testing ER_genInverse
    printf("\nTesting ER_genInverse on something other than permutation\n");
    ExplicitRelation *inverse = ER_genInverse(relptr);

    // assert if the number of relations are incorrect
    test_count=0;
    FOREACH_in_tuple_1d1d(inverse, in) {
        FOREACH_out_given_in_1d1d(inverse, in, out) {
            printf("\t[%d] -> [%d]\n", in, out);
            test_count++;
        }
    }
    assert(count==test_count);
    

    ER_dtor(&inverse);

    //----- testing ERG_cpack itself takes 1D-to-1D relation as input
    // constructing sigma
    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, (NUM_OUT - 1));
    isFunction = true;
    isPermutation = true;
    ExplicitRelation * sigma = ER_ctor(1,1,in_domain,isFunction,isPermutation);
    
    // relptr is input to ERG_cpack and sigma is output
    ERG_cpack( relptr, sigma );    
    
    printf("==== dumping sigma after ERG_cpack call\n");
    ER_dump(sigma);
    assert(ER_verify_permutation(sigma));
    
    //ER_dtor(&relptr);
    ER_dtor(&sigma);

    //----- testing ERG_lexmin itself
    // Assume that passing same relptr into ERG_lexmin that we passed 
    // into ERG_cpack.
    // constructing delta, which will map old iteration points to new
    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, NUM_IN-1);
    isFunction = true;
    isPermutation = true;
    ExplicitRelation * delta = ER_ctor(1,1,in_domain,isFunction,isPermutation); 
    
    // relptr is input to ERG_cpack and sigma is output
    ERG_lexmin( relptr, delta );    
    
    printf("==== dumping delta after ERG_lexmin call\n");
    ER_dump(delta);
    assert(ER_verify_permutation(delta));
    
    ER_dtor(&relptr);
    ER_dtor(&delta);

  }

  //-----------------------------------------------------------------
  // 1D to 1D permutation.
  //-----------------------------------------------------------------    
  {
    ExplicitRelation* relptr;
    RectDomain* in_domain;
    int in, test_in, test_out, count, test_count;
    bool isFunction, isPermutation;


    //======= test creation and use of ER for sigma and delta, 
    //======= which are permutations and 1D to 1D
    printf("==== test creation and use of ER for for sigma and delta\n");

    in_domain = RD_ctor(1);
    RD_set_lb(in_domain, 0, 0);
    RD_set_ub(in_domain, 0, (NUM_IN - 1));
    // We know in_domain for permutations and a permutation is a function.
    isFunction = true;
    isPermutation = true;
    relptr = ER_ctor(1,1, in_domain, isFunction, isPermutation);

    // create a permutation that is just a modular shift
    count = 0;
    for (in=0; in<NUM_IN; in++) {
        ER_in_ordered_insert( relptr, in, (in+1) % NUM_IN);
        count++;
    }

    ER_dump(relptr);

    // Iterate over the integer tuple relations
    printf("\nTraversing sigma example\n");
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
  }
  
  //-----------------------------------------------------------------
  // 2D to 3D relation.
  // Also testing the size of its inverse.
  //-----------------------------------------------------------------    
  {
    ExplicitRelation* relptr, *inverse;
    RectDomain* in_domain;
    int count, test_count;
    bool isFunction, isPermutation;

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
    isFunction = false;
    isPermutation = false;
    relptr = ER_ctor(2,3, in_domain, isFunction, isPermutation);
    
    // code for explicitly creating the relation
    // we should be able to automatically generate this loop from the
    // static specification of the relation
    int i, j, k;
    count = 0;
    for (i=1; i<=10; i++) {
        for (j=1; j<=10; j++) {
            k=1;
            ER_in_ordered_insert( relptr, 
                Tuple_make(i,j), Tuple_make(i,j,k));
            if (debug) {
                printf("\tER_in_ordered_insert( (%d, %d), (%d, %d, %d) )\n", 
                   i, j, i, j, k);
            }

            k=2;
            ER_in_ordered_insert( relptr, 
                Tuple_make(i,j), Tuple_make(i-1,j+1,k));
            if (debug) {
                printf("\tER_in_ordered_insert( (%d, %d), (%d, %d, %d) )\n", 
                   i, j, i-1, j+1, k);
            }
                   
            count +=2;
        }
    }

    ER_dump(relptr);
    
    // Iterate over the integer tuple relations
    printf("\nTraversing 2D-to-3D example\n");
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

    // Testing ER_genInverse on something that is not 1D to 1D
    printf("\nInverse for 2D to 3D example\n");
    inverse = ER_genInverse(relptr);
    test_count = 0;
    FOREACH_in_tuple(inverse, in_tuple) {
        FOREACH_out_given_in(inverse, in_tuple, out_tuple) {
            printf("\t");
            Tuple_print(in_tuple);
            printf(" -> ");
            Tuple_print(out_tuple);
            printf("\n");
            test_count++;
        }
    }
    printf("\n");
    assert(test_count==count);

    ER_dtor(&relptr);
    ER_dtor(&inverse);

  }

  //-----------------------------------------------------------------
  // 4D to 1D relation.  Similar to data dependences we will have in 
  // moldyn.
  // Also testing the size of its inverse.
  //-----------------------------------------------------------------    
  {
    ExplicitRelation* relptr, *inverse;
    RectDomain* in_domain;
    int count, test_count;
    bool isFunction, isPermutation;
    
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
    isFunction = false;
    isPermutation = false;
    relptr = ER_ctor(4,1, in_domain, isFunction, isPermutation);
    
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
    printf("\nTraversing data dependence example\n");
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
    
    
    // Testing ER_genInverse on something that is not 1D to 1D
    printf("\nInverse for data dependence example\n");
    inverse = ER_genInverse(relptr);
    test_count = 0;
    FOREACH_in_tuple(inverse, in_tuple) {
        FOREACH_out_given_in(inverse, in_tuple, out_tuple) {
            printf("\t");
            Tuple_print(in_tuple);
            printf(" -> ");
            Tuple_print(out_tuple);
            printf("\n");
            test_count++;
        }
    }
    printf("\n");
    assert(test_count==count);

    ER_dtor(&relptr);
    ER_dtor(&inverse);

  }
  
  //-----------------------------------------------------------------
  // 1D to 1D relation with no in domain specification.
  //-----------------------------------------------------------------    
  {
    ExplicitRelation* relptr;
    int in, out, count, test_count, test_in, test_out;

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
  }

  //-----------------------------------------------------------------
  // Testing ERG_blockpart1D
  //-----------------------------------------------------------------    
  {
    ExplicitRelation* relptr;
    RectDomain* in_domain;
    int in, test_count;
    bool isFunction, isPermutation;


    printf("==== test usage of ERG_blockpart to create part ER\n");
    // ERG_blockpart assumes partitioning 1D iteration space for now
    in_domain = RD_ctor(1);
    int lb = 0; int ub = NUM_IN-1;
    RD_set_lb(in_domain, 0, lb);
    RD_set_ub(in_domain, 0, ub);
    isFunction = true;
    isPermutation = false;
    relptr = ER_ctor(1,1, in_domain, isFunction, isPermutation);

    // have ERG fill in ER
    int numpart = 4;
    ERG_blockpart1D(numpart, relptr);

    ER_dump(relptr);

    // Iterate over the integer tuple relations
    printf("\nTraversing part example\n");
    test_count=0;
    FOREACH_in_tuple_1d1d(relptr, in) {
        int out = ER_out_given_in(relptr,in);
        printf("\t[%d] -> [%d]\n", in, ER_out_given_in(relptr,in));
        assert(0<=out && out<numpart);
        test_count++;
    }
    assert((ub-lb+1)==test_count);

    ER_dtor(&relptr);
  }

  //-----------------------------------------------------------------
  // Testing ERG_blockpart1D
  //-----------------------------------------------------------------    
  {
    ExplicitRelation* relptr;
    RectDomain* in_domain;
    int in, test_count;
    bool isFunction, isPermutation;


    printf("==== test usage of ERG_blockpart to create part ER\n");
    // 1D iteration space 
    in_domain = RD_ctor(1);
    int lb = 0; int ub = NUM_IN-1;
    RD_set_lb(in_domain, 0, lb);
    RD_set_ub(in_domain, 0, ub);
    isFunction = true;
    isPermutation = false;
    relptr = ER_ctor(1,1, in_domain, isFunction, isPermutation);

    // have ERG fill in ER
    int numpart = 4;
    ERG_blockpart1D(numpart, relptr);

    ER_dump(relptr);

    // Iterate over the integer tuple relations
    printf("\nTraversing part example\n");
    test_count=0;
    FOREACH_in_tuple_1d1d(relptr, in) {
        int out = ER_out_given_in(relptr,in);
        printf("\t[%d] -> [%d]\n", in, ER_out_given_in(relptr,in));
        assert(0<=out && out<numpart);
        test_count++;
    }
    assert((ub-lb+1)==test_count);

    ER_dtor(&relptr);
  }

  //-----------------------------------------------------------------
  // Testing ERG_blockpart1D with multidim input
  //-----------------------------------------------------------------    
  {
    ExplicitRelation* relptr;
    RectDomain* in_domain;
    int test_count;
    Tuple in_tuple;
    bool isFunction, isPermutation;


    printf("==== test usage of ERG_blockpart1D with multidim in domain\n");
    // 2D iteration space with lb==ub in first dim
    in_domain = RD_ctor(2);
    int lb = 0; int ub = 0;
    RD_set_lb(in_domain, 0, lb);
    RD_set_ub(in_domain, 0, ub);
    lb = 0; ub = NUM_IN-1;
    RD_set_lb(in_domain, 1, lb);
    RD_set_ub(in_domain, 1, ub);
    isFunction = true;
    isPermutation = false;
    relptr = ER_ctor(2, 1, in_domain, isFunction, isPermutation);

    // have ERG fill in ER
    int numpart = 4;
    ERG_blockpart1D(numpart, relptr);

    ER_dump(relptr);

    // Iterate over the integer tuple relations
    printf("\nTraversing part example\n");
    test_count=0;
    FOREACH_in_tuple(relptr, in_tuple) {
        Tuple out_tuple = ER_out_given_in(relptr,in_tuple);
        printf("\t");
        Tuple_print(in_tuple);
        printf(" -> ");
        Tuple_print(out_tuple);
        printf("\n");

        assert(0<=Tuple_val(out_tuple,0) && Tuple_val(out_tuple,0)<numpart);
        test_count++;
    }
    assert((ub-lb+1)==test_count);

    ER_dtor(&relptr);
  }


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

