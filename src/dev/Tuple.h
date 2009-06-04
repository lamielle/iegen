/**********************************************************************//*!
 \file      Tuple.h

 \brief     Contains declaration of Tuple data structure.

 \authors   Michelle Strout
    
 Copyright ((c)) 2008, Colorado State University
 All rights reserved.
 See COPYING for copyright details.
 </pre>
 
*//**********************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#ifndef _Tuple_H
#define _Tuple_H

/* ////////////////////////////////////////////////////////////////////
// Tuple Definition
// 
//////////////////////////////////////////////////////////////////// */
typedef struct {
    int *valptr;    //! pts to flat 1D array of vals in tuple
    int arity;      //! indicates number of values in the tuple
} Tuple;

// function prototypes

//! Create a Tuple structure and return a copy of it.
//! Calling it _make because it is different from a constructor in
//! that it does not return a pointer to the object, but returns
//! the whole object.
Tuple Tuple_make(int x1);
Tuple Tuple_make(int x1, int x2);
Tuple Tuple_make(int x1, int x2, int x3);
Tuple Tuple_make(int x1, int x2, int x3, int x4);
Tuple Tuple_make_with_arity(int arity);


int Tuple_val(Tuple t, int k);
Tuple Tuple_set_val(Tuple t, int k, int value);
bool Tuple_equal(Tuple t1, Tuple t2);

void Tuple_print(Tuple t);

//! Returns the kth element value in the tuple.
int Tuple_val(Tuple t, int k);

//! Returns -1 if first tuple less, 0 if they are equal, 
//! and 1 if first is greater.
int Tuple_compare( Tuple t1, Tuple t2);


#endif

