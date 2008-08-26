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
    RD_dim()    
    
    // Returns lower bound for the kth dimension
    RD_lb(int k)
    // Returns upper bound for the kth dimension
    RD_ub(int k)
    
    // Returns size for the kth dimension.
    // RD_size(k) = RD_ub(k)-RD_lb(k)+1
    RD_size(int k)    
    

 Copyright ((c)) 2008, Colorado State University
 All rights reserved.
 See COPYING for copyright details.
 
*//**********************************************************************/

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

void RD_set_lb( RectDomain *rd, int k, int lb );
void RD_set_ub( RectDomain *rd, int k, int lb );


int RD_dim();
int RD_lb(int k);
int RD_ub(int k);
int RD_size(int k); 
 

#endif

