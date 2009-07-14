/**********************************************************************//*!
 \file      RectDomain.h

 \brief     Contains declaration of RectDomain data structure.

 \authors   Michelle Strout

 <pre>
 The RectDomain data structure is for storing the rectangular dynamic
 domain for an integer tuple space.
 
 To create a RectDomain, call the constructor
 
    rd = RD_ctor(dim);

 and then indicate lower and upper bounds for each dimension k:
 
    RD_set_lb( rd, k, lb );
    RD_set_ub( rd, k, lb );
    
 The RectDomain can then be queried about its dimensionality,
 the bounds for each dimension and the size of each dimension.

    // Returns dimensionality of the rectangular domain.
    RD_dim(rd)    
    
    // Returns lower bound for the kth dimension.
    RD_lb(rd, int k)
    // Returns upper bound for the kth dimension.
    RD_ub(rd, int k)
    
    // Returns size for the kth dimension.
    // RD_size(rd,k) = RD_ub(rd,k)-RD_lb(rd,k)+1
    RD_size(RectDomain*,int k)
    
    // Returns size for full domain.
    RD_size(rd)

 The following function enables lexicographical iteration over 
 the tuples in the domain.
 
    for (int i=0; i<RD_size(rd); i++) {
        Tuple next = RD_nextTuple( rd, tuple );
    }
    
 Copyright ((c)) 2008, Colorado State University
 All rights reserved.
 See COPYING for copyright details.
 </pre>
 
*//**********************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "Tuple.h"

#ifndef _RectDomain_H
#define _RectDomain_H


/* ////////////////////////////////////////////////////////////////////
// RectDomain Definition
// 
//////////////////////////////////////////////////////////////////// */
typedef struct {

    int *bounds;    // bounds[i*2] and bounds[i*2+1] respectively
                    // contain the lower and upper
                    // bounds for the ith dimension
                    
    int dim;        // dimensionality


} RectDomain;

// function prototypes

RectDomain* RD_ctor(int dim);
RectDomain* RD_ctor(RectDomain *other);
void RD_dtor( RectDomain** self );

void RD_set_lb( RectDomain *rd, int k, int lb );
void RD_set_ub( RectDomain *rd, int k, int lb );


int RD_dim(RectDomain *rd );
int RD_lb(RectDomain *rd, int k);
int RD_ub(RectDomain *rd, int k);
int RD_size(RectDomain *rd, int k); 
int RD_size(RectDomain *rd); 

//! Returns first tuple in domain in terms of lexicographical order.
Tuple RD_firstTuple( RectDomain* rud);

//! Returns lexicographically next tuple after given tuple.
Tuple RD_nextTuple( RectDomain* rd, Tuple t );

//! Returns true if the given tuple is within the bounds specified in
//! given RectDomain.
bool RD_in_domain(RectDomain * rd, Tuple t);

int RD_calcIndex( RectDomain* rd, Tuple t );
int RD_calcIndex( RectDomain* rd, int val );

void RD_dump( RectDomain* self ); 

#endif

