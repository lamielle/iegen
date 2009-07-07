/*! \file   Tuple.c

    Implements the Tuple data structure for use with the PIES project.
*/

#include "Tuple.h"

Tuple Tuple_make(int x1)
/*----------------------------------------------------------------*//*!
  \short Creates a 1D Tuple and returns a copy of it.

  \author Michelle Strout 8/23/08
*//*----------------------------------------------------------------*/
{
    // first create array to store single value
    // FIXME: pretty inefficient for 1D
    int * valptr = (int*)malloc(sizeof(int));

    // put values in array
    valptr[0] = x1;

    Tuple retval = { valptr, 1 };
    return retval;
}

Tuple Tuple_make(int x1, int x2)
/*----------------------------------------------------------------*//*!
  \short Creates a 2D Tuple and returns a copy of it.

  \author Michelle Strout 8/23/08
*//*----------------------------------------------------------------*/
{
    // first create array to store both values
    int * valptr = (int*)malloc(sizeof(int)*2);

    // put values in array
    valptr[0] = x1;
    valptr[1] = x2;

    Tuple retval = { valptr, 2 };
    return retval;
}

Tuple Tuple_make(int x1, int x2, int x3)
/*----------------------------------------------------------------*//*!
  \short Creates a 3D Tuple and returns a copy of it.

  \author Michelle Strout 8/23/08
*//*----------------------------------------------------------------*/
{
    // first create array to store both values
    int * valptr = (int*)malloc(sizeof(int)*3);

    // put values in array
    valptr[0] = x1;
    valptr[1] = x2;
    valptr[2] = x3;

    Tuple retval = { valptr, 3 };
    return retval;
}

Tuple Tuple_make(int x1, int x2, int x3, int x4)
/*----------------------------------------------------------------*//*!
  \short Creates a 4D Tuple and returns a copy of it.

  \author Michelle Strout 9/10/08
*//*----------------------------------------------------------------*/
{
    // first create array to store both values
    int * valptr = (int*)malloc(sizeof(int)*4);

    // put values in array
    valptr[0] = x1;
    valptr[1] = x2;
    valptr[2] = x3;
    valptr[3] = x4;

    Tuple retval = { valptr, 4 };
    return retval;
}

Tuple Tuple_make_with_arity(int arity)
/*----------------------------------------------------------------*//*!
  \short Creates an Tuple with given arity and returns a copy of it.

  \author Michelle Strout 6/3/09
*//*----------------------------------------------------------------*/
{
    assert(arity>=1);
    
    // first create array to store arity values
    int * valptr = (int*)malloc(sizeof(int)*arity);

    // put 0 values in array
    int i;
    for (i=0; i<arity; i++) {
        valptr[i] = 0;
    }
    
    Tuple retval = { valptr, arity };
    return retval;
}


int Tuple_val(Tuple t, int k)
/*----------------------------------------------------------------*//*!
  \short Returns the value of the kth element in the tuple.

  \author Michelle Strout 8/30/08
*//*----------------------------------------------------------------*/
{
    // check that not attempting to index outside of the tuple
    assert(k >= 0  && k<t.arity );

    return t.valptr[k];
}

Tuple Tuple_set_val(Tuple t, int k, int value)
/*----------------------------------------------------------------*//*!
  \short Returns a Tuple where the value of the kth element in the 
         tuple is set to value.

  \author Michelle Strout 9/3/09
*//*----------------------------------------------------------------*/
{
    // check that not attempting to index outside of the tuple
    assert(k >= 0  && k<t.arity );
    t.valptr[k] = value;
    return t;
}


bool Tuple_equal(Tuple t1, Tuple t2)
/*----------------------------------------------------------------*//*!
  \short Returns true if given tuples are equal.

  \author Michelle Strout 9/2/08
*//*----------------------------------------------------------------*/
{
    if (t1.arity != t2.arity) {
        return false;
    }
    int k;
    for (k=0; k<t1.arity; k++) {
        if ( t1.valptr[k] != t2.valptr[k] ) {
            return false;
        }
    }
    return true;
}

int Tuple_compare( Tuple t1, Tuple t2)
/*----------------------------------------------------------------*//*!
  \short Returns -1, 0, or 1 depending on whether t1 is <, =, or > than t2.

  FIXME: should probably replace Tuple_equal calls to calls to this?
  This is less lenient though.  It assumes both tuples have the same
  arity.

  \author Michelle Strout 9/4/08
*//*----------------------------------------------------------------*/
{
    if (t1.arity != t2.arity) {
        assert(0);
    }
    int k;
    for (k=0; k<t1.arity; k++) {
        if ( t1.valptr[k] < t2.valptr[k] ) {
            return -1;
        } else if ( t1.valptr[k] < t2.valptr[k] ) {
            return 1;
        }
    }
    // All elements in tuples were equal.
    return 0;
}



void Tuple_print(Tuple t)
/*----------------------------------------------------------------*//*!
  \short Prints tuple value to standard out.

  Format of output will be (x_1, x_2, ..., x_d) where d is arity
  of tuple.

  \author Michelle Strout 9/18/08
*//*----------------------------------------------------------------*/
{
    int k;
    printf("[");
    printf("%d", t.valptr[0]);
    for (k=1; k<t.arity; k++) {
        printf(",%d", t.valptr[k]);
    }
    printf("]");
}


