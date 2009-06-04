/**********************************************************************//*!
 \file      RectUnionDomain.h

 \authors Michelle Strout   6/3/09

<pre>
 The RectUnionDomain data structure is for storing the union of
 rectangular dynamic domains for an integer tuple space.
 For example,
    {[0,i] : 0 <= i < natom } union {[1,i] : 0 <= i < ninter }
 is the union of two 1D rectangular domains embedded in a 2D
 iteration space.
 
 To create a RectUnionDomain, call the constructor
 
    rud = RUD_ctor(dim);

 and then start inserting rectangular domains:
 
    // first conjunction
    rd = RD_ctor(1);
    RD_set_lb(rd, 0, 0);
    RD_set_ub(rd, 0, natom-1);
    RUD_insert(rud, Tuple_make(0), rd);
    
    // second conjunction
    rd = RD_ctor(1);
    RD_set_lb(rd, 0, 0);
    RD_set_ub(rd, 0, ninter-1);
    RUD_insert(rud, Tuple_make(1), rd);
 
 Note that you can also insert a single rectangular domain for the
 full union.
 
 LIMITATIONS: At this point this data structure can only handle
 a single level of rectangular unions.  Therefore, the tuple passed
 to RUD_insert can only be 1D and this data structure can only
 represent a single rectangular domain or a set of rectangular
 domains all embedded by using the constants 0 through num_rect-1
 in the Tuple.  This also means that the embedding has to start at 0.
 
    
 The RectUnionDomain can then be queried about its dimensionality
 and its size.

    // Returns dimensionality of the rectangular union domain.
    RUD_dim(rud)    
        
    // Returns size for full domain.
    RUD_size(rud)

 The following function enables lexicographical iteration over 
 the tuples in the domain.
 
    Tuple tuple = RUD_firstTuple(rud);
    for (int i=0; i<RUD_size(rud); i++, tuple = RUD_nextTuple( rud, tuple )) 
    {
        ...
    }
    
 Copyright ((c)) 2008, Colorado State University
 All rights reserved.
 See COPYING for copyright details.
</pre>
 
*//**********************************************************************/


#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "RectDomain.h"

#ifndef _RectUnionDomain_H
#define _RectUnionDomain_H


/* ////////////////////////////////////////////////////////////////////
// RectUnionDomain Definition
// 
//////////////////////////////////////////////////////////////////// */
typedef struct {

    RectDomain **rects; // Array of embedded rectangular domains.
    int num_rects;      // number of rectangular domains                
    int dim;            // dimensionality

} RectUnionDomain;

// function prototypes

RectUnionDomain* RUD_ctor(int dim, int num_rects);
void RUD_dtor( RectUnionDomain** self );

void RUD_insert(RectUnionDomain *rud, RectDomain *rd);
void RUD_insert(RectUnionDomain *rud, Tuple embed_tuple, RectDomain *rd);

int RUD_dim(RectUnionDomain *rud);
int RUD_size(RectUnionDomain *rud); 

Tuple RUD_firstTuple( RectUnionDomain* rud);
Tuple RUD_nextTuple( RectUnionDomain* rud, Tuple tuple );

void RUD_dump( RectUnionDomain* self ); 

#endif
