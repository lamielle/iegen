/**********************************************************************//*!
 \file      RectDomain.h

 \brief     Contains declaration of RectDomain data structure.

 \authors   Michelle Strout

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
    

 Copyright ((c)) 2008, Colorado State University
 All rights reserved.
 See COPYING for copyright details.
 
*//**********************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

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
void RD_dtor( RectDomain** self );

void RD_set_lb( RectDomain *rd, int k, int lb );
void RD_set_ub( RectDomain *rd, int k, int lb );


int RD_dim(RectDomain *rd );
int RD_lb(RectDomain *rd, int k);
int RD_ub(RectDomain *rd, int k);
int RD_size(RectDomain *rd, int k); 
int RD_size(RectDomain *rd); 

void RD_dump( RectDomain* self ); 

#endif

