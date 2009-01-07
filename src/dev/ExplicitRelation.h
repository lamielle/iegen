/**********************************************************************//*!
 \file      ExplicitRelation.h

 \authors Michelle Strout   8/27/08

<pre>
 The ExplicitRelation data structure is for creating an explicit representation
 of integer tuple relations at runtime.
 
 To create a ExplicitRelation call the constructor, which returns a pointer
 
    relptr = ER_ctor(in_tuple_arity, out_tuple_arity );
    
        or

    relptr = ER_ctor(in_tuple_arity, out_tuple_arity,
                     in_domain, isFunction, isPermutation );
    // see RectDomain.h for instructions on creating an in_domain
                     
                     
 and then add tuple relations by calling one of the following:
 
    // insert entries into a relation
    ER_insert(relptr, in_tuple, out_tuple); 
    
    // insertions are ordered lexicographically by in_tuple
    ER_in_ordered_insert(relptr, in_tuple, out_tuple); 
        
 If the in and out tuple arities are both one, then the in and out tuples can just be single integers.  Otherwise, the in and out tuples can be created with a call to the tuple function.
 
    // constructing a tuple
    Tuple mytuple;
    mytuple = Tuple_make(x_1, x_2, ..., x_n);
    
 If the explicit relation is representing a function, then can get
 the single output tuple associated with each input_tuple.
 
    out_tuple = ER_out_given_in(relptr, in_tuple)
        
 Can request the domain for the input tuples or range for the output tuples.
 
    in_domain = ER_in_domain(relptr);
    out_range = ER_in_range(relptr);

 The assumption is that the relation will always be traversed in 
 lexicographical order of its input tuples.  If an ordering over output
 tuples is needed, then generate the inverse explicit relation with
 ER_genInverse.
 

 The following macros enable iteration over the relation.  Because
 these are implemented as macros (for efficiency) instead of functions, 
 the special treatment of 1D-to-1D arity relations is exposed.
 
    // iterate over an already constructed explicit relation
    FOREACH_in_tuple(relptr, in_tuple) {
        FOREACH_out_given_in(relptr, in_tuple, out_tuple) {

    // special version of iterators for 1D-to-1D relations
    FOREACH_in_tuple_1d1d(relptr, in_int) {
        FOREACH_out_given_in_1d1d(reptr, in_int, out_int) {


 Iterating over an ER in order of the output tuples.
    
 To avoid having another set of iterators for this purpose,
 the following code pattern will provide equivalent functionality.
    
 Assume that you have an ExplicitRelation* called relptr and you
 want to iterate over that relation in order of its ouput tuples.
    
        // First create the inverse relation.
        ExplicitRelation *inv_relptr = ER_genInverse(relptr);

        // Then iterate over that inverse relation.
        FOREACH_in_tuple_1d1d(inv_relptr, inv_in) {        
            FOREACH_out_given_in_1d1d(inv_relptr, inv_in, inv_out) {
                // input and output tuples for original relation.
                out = inv_in;
                in = inv_out;



 Copyright ((c)) 2008, Colorado State University
 All rights reserved.
 See COPYING for copyright details.

</pre>
 
*//**********************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <limits.h>
#include "util.h"
#include "RectDomain.h"

#ifndef _ExplicitRelation_H
#define _ExplicitRelation_H

// assuming one page is 4K or less, going to create more space for array
// in increments of 4K, which is 1024 integers.
// Will probably need to experiment with this number for performance reasons.
#define MEM_ALLOC_INCREMENT 1024
//#define MEM_ALLOC_INCREMENT 120

/* ////////////////////////////////////////////////////////////////////
// ExplicitRelation Definition
// 
//////////////////////////////////////////////////////////////////// */
typedef struct ER {

    int         in_arity;   //! arity of input tuple
    int         out_arity;  //! arity of output tuple

    bool        isFunction; //! If true indicates that each input tuple will map 
                            //! to only one output tuple.
                            
    bool        isPermutation;  //! If true indicates in domain and out range
                                //! are the same and the relation is one-to-one
                                //! and onto.
                    
    RectDomain* in_domain;  //! Domain for the input tuples.  If known at
                            //! construction time, then it is not necessary to 
                            //! finalize data structure for efficient access.

    bool        in_domain_given;    //! Keeps track of whether the domain was
                                    //! given or was dynamically built.
                                    
    RectDomain* out_range;  //! Range for the output tuples.                                 
    
    //----- relation representation ---------------------------------------
    // WARNING: Do not access these fields directly, use interface.
    
    
    int*        in_vals;    //! Every in_arity entries represent the values
                            //! for an input tuple instance.
                            //! The given input tuple values starting at
                            //! in_vals[i*in_arity] are valid
                            //! for all of the output tuples stored from
                            //! out_vals[out_index[i]] through 
                            //! out_vals[out_index[i+1]] non-inclusive.

    int         unique_in_count;    //! Number of unique input tuples that
                                    //! have been inserted.

    int*        out_index;  //! Indices into the out_vals array.

    int*        out_vals;   //! Output tuple values.

    int*        raw_data;   //! Holds raw relations as input tuple followed
                            //! by output tuple.  Used if do not know
                            //! in domain.
    int         raw_num;    //! Number of relations in raw_data array.

    //----- order management -----------------------------------------
    // Keeps track of how the integer tuples have been inserted.
    bool    ordered_by_in;

    struct ER * inverse; //! Result of ER_genInverse call.

    //----- memory management -----------------------------------------
    // Need to keep track of the number of entries in each of the current
    // array allocations.
    // Needed because size of hypergraph is not known apriori.
    int     in_vals_size;     // num entries in current in_vals allocation
    int     out_index_size;   // num entries in current out_index allocation
    int     out_vals_size;    // num entries in current out_vals allocation
    int     raw_data_size;    // num entries in current raw_data allocation

    bool    external_out_vals; // is the 'out_vals' field allocated locally 
                               // or passed in to the constructor?
    
} ExplicitRelation;

/* ////////////////////////////////////////////////////////////////////
// Tuple Definition
// 
//////////////////////////////////////////////////////////////////// */
typedef struct {
    int *valptr;    //! pts to flat 1D array of vals in tuple
    int arity;      //! indicates number of values in the tuple
} Tuple;

/* ////////////////////////////////////////////////////////////////////
// function prototypes
// 
//////////////////////////////////////////////////////////////////// */

//! Construct an empty ExplicitRelation by specifying arity 
//! for in and out tuples.
ExplicitRelation* ER_ctor(int in_tuple_arity, int out_tuple_arity,
                          RectDomain *in_domain=NULL, 
                          bool isFunction=false,
                          bool isPermutation=false);

//! Construct an empty ExplicitRelation by passing in a 1D array.
//! Assumes isFunction and has 1D-to-1D arity for now.
ExplicitRelation* ER_ctor(int * index_array, int size);

//! Construct a new ExplicitRelation that is the inverse of
//! the given relation.
ExplicitRelation* ER_genInverse(ExplicitRelation * input);


//! Deallocate all of the memory for the ExplicitRelation.
void ER_dtor(ExplicitRelation**);

//! Create a Tuple structure and return a copy of it.
//! Calling it _make because it is different from a constructor in
//! that it does not return a pointer to the object, but returns
//! the whole object.
Tuple Tuple_make(int x1);
Tuple Tuple_make(int x1, int x2);
Tuple Tuple_make(int x1, int x2, int x3);
Tuple Tuple_make(int x1, int x2, int x3, int x4);


int Tuple_val(Tuple t, int k);
bool Tuple_in_domain(Tuple t, RectDomain * rd);
bool Tuple_equal(Tuple t1, Tuple t2);

void Tuple_print(Tuple t);

//----------------------- Routines for inserting relations

//! Insert relation into given explicit relation.
void ER_insert(ExplicitRelation* relptr, Tuple in_int, Tuple out_int); 

//! Insertion for special 1D-to-1D arity relations.
void ER_insert(ExplicitRelation* relptr, int in_int, int out_int); 

//! Insertions are ordered lexicographically by in_tuple.
void ER_in_ordered_insert(ExplicitRelation* relptr, 
                          Tuple in_int, Tuple out_int); 

//! Insertion for special 1D-to-1D arity relations.  Ordered by in_int.
void ER_in_ordered_insert(ExplicitRelation* relptr, 
                          int in_int, int out_int); 

//----------------------- Informational routines

//! If the explicit relation is storing a function,
//! return the single output tuple for the given input tuple.
Tuple ER_out_given_in( ExplicitRelation* relptr, Tuple in_tuple);

//! If the explicit relation is storing a function and is 1D-to-1D,
//! return the single output integer for the given input integer.
int ER_out_given_in( ExplicitRelation* relptr, int in_int);


//! Returns the kth element value in the tuple.
int Tuple_val(Tuple t, int k);

//! Returns true if the given tuple is within the bounds specified in
//! given RectDomain.
bool Tuple_in_domain(Tuple t, RectDomain * rd);

//! Returns -1 if first tuple less, 0 if they are equal, 
//! and 1 if first is greater.
int Tuple_compare( Tuple t1, Tuple t2);

//! Returns the in domain.  Min and Max vals for each element in tuples.
RectDomain* ER_in_domain( ExplicitRelation * relptr);

//! Returns the out domain.  Min and Max vals for each element out tuples.
RectDomain* ER_out_range( ExplicitRelation * relptr);

//! Returns an index into the out_vals for the first out tuple element
//! associated with the given in tuple.  Assumes we know the in_domain for
//! the explicit relation.
int ER_calcIndex( ExplicitRelation* relptr, Tuple in_tuple );

int ER_calcIndex( ExplicitRelation* relptr, int in_val );

//! Inverse of calcIndex.
Tuple ER_calcTuple( ExplicitRelation* relptr, int index );

//! Verifies that the given explicit relation is a permutation.
bool ER_verify_permutation(ExplicitRelation* relptr);

//! Output debug text representation of ExplicitRelation to standard out.
void ER_dump( ExplicitRelation* self );

//----------------------- Setting up ExplicitRelation for iteration

//! Ensure that the integer tuple relations are sorted by the input tuples.
void ER_order_by_in(ExplicitRelation* relptr);

// Do not have an ER_order_by_out.  Instead see the comments below about
// iterating over an inverse of the relation.

//----------------------- Macros for iterating over relations

//! Iterate over general explicit relations.
//! \param relptr   Pointer to a ExplicitRelation.
//! \param in_tuple   Variable in which to store the input tuple.
//! For now assuming that the ER is constructed with the in_domain or
//! the in_domain is calculated when things are ordered by in tuples.
#define FOREACH_in_tuple(relptr, in_tuple)                  \
    ER_order_by_in(relptr);                                 \
    in_tuple=ER_calcTuple(relptr, 0);                       \
    for (int _FE_i=0;                                       \
         (_FE_i)<RD_size((relptr)->in_domain);              \
         (_FE_i)++, in_tuple=ER_calcTuple(relptr, _FE_i))

//! Iterate over output tuples given input tuple.
//! \param relptr       Pointer to a ExplicitRelation.
//! \param in_tuple     input tuple
//! \param out_tuple    Variable in which to store the output tuple
//! The out_tuple will be set to point into the actual explicit
//! relation data structure.
//! Only works for non function explicit relations.
#define FOREACH_out_given_in(relptr, int_tuple, out_tuple)                  \
    assert(! relptr->isFunction );                                          \
    int _FE_iter;                                                           \
    out_tuple.arity = relptr->out_arity;                                    \
    for (_FE_iter=(relptr)->out_index[ER_calcIndex(relptr,(in_tuple))],     \
            out_tuple.valptr=&((relptr)->out_vals[_FE_iter]);               \
         _FE_iter<(relptr)->out_index[ER_calcIndex(relptr,(in_tuple))+1];   \
         _FE_iter+=relptr->out_arity,                                       \
           out_tuple.valptr=&((relptr)->out_vals[_FE_iter]) )
        

//! Iterate over the special 1D-to-1D arity relations.
//! \param relptr   Pointer to a ExplicitRelation.
//! \param in_int   Variable in which to store the input tuple single entry.
#define FOREACH_in_tuple_1d1d(relptr, in_int)               \
    assert(relptr->in_arity==1);  assert(relptr->out_arity==1); \
    ER_order_by_in(relptr);                                 \
    for ((in_int)=RD_lb((relptr)->in_domain,0);             \
         (in_int)<=RD_ub((relptr)->in_domain,0); (in_int)++) 

//! Iterate over output ints given input ints for 1D-to-1D arity relations.
//! \param relptr   Pointer to a ExplicitRelation.
//! \param in_int   input tuple value
//! \param out_int  Variable in which to store the output tuple value.
//! Only works for non function explicit relations.
#define FOREACH_out_given_in_1d1d(relptr, in_int, out_int)  \
    assert(! relptr->isFunction );                          \
    int _lb_adjust = (in_int)-RD_lb((relptr)->in_domain,0); \
    int _FE_iter;                                           \
    for (_FE_iter=(relptr)->out_index[_lb_adjust],          \
            out_int=(relptr)->out_vals[_FE_iter];           \
         _FE_iter<(relptr)->out_index[_lb_adjust+1];        \
         _FE_iter++,out_int=(relptr)->out_vals[_FE_iter]) 



#endif

