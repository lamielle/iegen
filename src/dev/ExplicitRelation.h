/* ExplicitRelation.h */
/**********************************************************************//*!
 \file

 \authors Michelle Strout

 The ExplicitRelation data structure is for creating an explicit representation
 of integer tuple relations at runtime.
 
 To create a ExplicitRelation, call the constructor
 
    relptr = ExplicitRelation_ctor(in_tuple_arity, out_tuple_arity);

 and then add tuple relations by calling one of the following:
 
    // insert entries into a relation
    ExplicitRelation_insert(relptr, in_tuple, out_tuple); 
    // insertions are ordered lexicographically by in_tuple
    ExplicitRelation_in_ordered_insert(relptr, in_tuple, out_tuple); 
    // insertions are ordered lexicographically by in_tuple concat out_tuple
    ExplicitRelation_ordered_insert(relptr, in_tuple, out_tuple); 
        
 If the in and out tuple arities are both one, then the in and out tuples can just be single integers.  Otherwise, the in and out tuples can be created with a call to the tuple function.
 
    // constructing a tuple
    Tuple mytuple;
    mytuple = Tuple(x_1, x_2, ..., x_n);
    
    // accessing entry k in a tuple
    // these should be macros
    ... = Tuple_val(mytuple, k) ;
    Tuple_val(mytuple, k) = ... ;

 Before accessing the values in a relation, it is possible to indicate how
 the entries should be ordered.
    ExplicitRelation_order_by_in(relptr);
    ExplicitRelation_order_by_out(relptr);   // is this possible?
    ExplicitRelation_order_by_in_out(relptr);
    ExplicitRelation_order_by_out_in(relptr);
   
 The following macros enable iteration over the relation.  Because
 these are implemented as macros (for efficiency) instead of functions, 
 the special treatment of 1D-to-1D arity relations is exposed.
 
    // iterate over an already constructed explicit relation
    FOREACH_in_tuple(relptr, in_tuple) {
        FOREACH_out_given_in(relptr, in_tuple, out_tuple) {

    FOREACH_out_tuple(relation, out_tuple) {
        FOREACH_in_given_out(relptr, out_tuple, in_tuple) {

    // special version of iterators for 1D-to-1D relations
    FOREACH_in_tuple_1d1d(relptr, in_int) {
        FOREACH_out_given_in_1d1d(reptr, in_int, out_int) {
        
    FOREACH_out_tuple_1d1d(relptr, out_int) {
        FOREACH_in_given_out_1d1d(relptr, out_int, in_int) {
     

 Copyright ((c)) 2008, Colorado State University
 All rights reserved.
 See COPYING for copyright details.
 
*//**********************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "util.h"

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
typedef struct {

    int     in_arity;   // arity of input tuple
    int     out_arity;  // arity of output tuple
    
	//----- relation representation ---------------------------------------
    // WARNING: Do not access these fields directly, use interface.
    
    int     in_count;   // Keeps track of how many "unique" input 
                        // tuples have been inserted.  If the same 
                        // input tuple shows up more than once, but
                        // adjacent in the insertion order, then 
                        // that input tuple will only be counted once.
                        // If the same tuple shows up separated in the
                        // insertion order, then it will be counted for 
                        // the number of separations.

    int     out_count;  // Keeps track of how many "unique" output 
                        // tuples have been inserted.  
                        // FIXME: this currently works for output_arity=1 only.
    
    int*    in_vals;    // Every in_arity entries represent the values
                        // for an input tuple instance.
                        // The given input tuple values starting at
                        // in_vals[i*in_arity] are valid
                        // for all of the output tuples stored from
                        // out_vals[out_index[i]] through 
                        // out_vals[out_index[i+1]] non-inclusive.
                        
                        
    int*    out_index;  // Indices into the out_vals array.
    int*    out_vals;   // Output tuple values.
    
    //----- order management -----------------------------------------
    // Keeps track of how the integer tuples have been inserted.
    bool    ordered_by_in;
    bool    ordered_by_out; // FIXME: possible?
    bool    ordered_by_in_out;
    
    //----- memory management -----------------------------------------
	// Need to keep track of the number of entries in each of the current
	// array allocations.
	// Needed because size of hypergraph is not known apriori.
    int     in_vals_size;     // number of entries in current allocation
    int     out_index_size;   // number of entries in current allocation
    int     out_vals_size;    // number of entries in current allocation
    
} ExplicitRelation;

// function prototypes

//! Construct an empty ExplicitRelation by specifying arity for in and out tuples.
ExplicitRelation* ExplicitRelation_ctor(int in_tuple_arity, 
                                        int out_tuple_arity);

//! Deallocate all of the memory for the ExplicitRelation.
void ExplicitRelation_dtor(ExplicitRelation**);

//----------------------- Routines for inserting relations

//! Insertions are ordered lexicographically by in_tuple.
// FIXME: put this in once have Tuple

//! Insertion for special 1D-to-1D arity relations.  Ordered by in_int.
void ExplicitRelation_in_ordered_insert(ExplicitRelation* relptr, 
                                        int in_int, 
                                        int out_int); 

//----------------------- Informational routines

//! Returns the number of unique 1D output tuples seen
// FIXME: how could we generalize this?
int ExplicitRelation_getRangeCount( ExplicitRelation* self);

//! Returns number of unique 1D input tuples seen
// FIXME: again specific to 1D
int ExplicitRelation_getDomainCount( ExplicitRelation* self); 

//! Output debug text representation of ExplicitRelation to standard out.
void ExplicitRelation_dump( ExplicitRelation* self );

//----------------------- Setting up ExplicitRelation for iteration

//! Insure that the integer tuple relations are sorted by the input tuples.
void ExplicitRelation_order_by_in(ExplicitRelation* relptr);

//----------------------- Macros for iterating over relations

//! Iterate over the special 1D-to-1D arity relations.
//! \param relptr   Pointer to a ExplicitRelation.
//! \param in_int   Variable in which to store the input tuple single entry.
#define FOREACH_in_tuple_1d1d(relptr, in_int) \
    for ((in_int)=0; (in_int)<(relptr)->in_count; (in_int)++) 

//! Iterate over output ints given input ints for 1D-to-1D arity relations.
//! \param relptr   Pointer to a ExplicitRelation.
//! \param in_int   input tuple value
//! \param out_int  Variable in which to store the output tuple value.
#define FOREACH_out_given_in_1d1d(relptr, in_int, out_int) \
    int _FE_iter;  \
    for (_FE_iter=(relptr)->out_index[(in_int)],    \
            out_int=(relptr)->out_vals[_FE_iter];      \
         _FE_iter<(relptr)->out_index[(in_int)+1];  \
         _FE_iter++,out_int=(relptr)->out_vals[_FE_iter]) 
        
#endif

