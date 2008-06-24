/**********************************************************************//*!
 \file

 \authors Michelle Strout

 The Hypergraph data structure is for creating an explicit representation
 of access relations at runtime.  The primary hypergraph will have
 iterations as hyperedges and the data locations being accessed as 
 nodes within individual hyperedges.
 
 To create a Hypergraph, call the constructor
 
    hg = Hypergraph_ctor();

 and then add (hyperedge,node) relationships by calling
 
    Hypergraph_ordered_insert_node( hg, hyperedge, node );
    
 Note that the ordered word indicates that the hyperedges will be inserted
 starting at 0 and monotonically increasing until the finalization call is 
 made.
 
    Hypergraph_finalize( hg );
    
 Assumptions
    - the number of nodes and/or iterations are not known before the hypergraph is being constructed
    - nodes have ids going from 0 to nv-1
    

 Copyright ((c)) 2008, Colorado State University
 All rights reserved.
 See COPYING for copyright details.
 
*//**********************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#ifndef _Hypergraph_H
#define _Hypergraph_H

// assuming one page is 4K or less, going to create more space for array
// in increments of 4K, which is 1024 integers.
// Will probably need to experiment with this number for performance reasons.
//#define MEM_ALLOC_INCREMENT 1024
#define MEM_ALLOC_INCREMENT 120

/* ////////////////////////////////////////////////////////////////////
// Hypergraph Definition
// 
//////////////////////////////////////////////////////////////////// */
typedef struct {

    int      nv;		 // Number of vertices.  
                         // Really indicates that range of vertex ids
                         // goes from 0 through nv-1.
	int      ne;		 // Number of hyperedges.
	
	//----- primary hypergraph ---------------------------------------
	int*     from; 	 // Indices into the hgdata array that indicate
	                     // where the nodes for hyperedges start and finish.
	                     // hyperedge i will have its nodes stored at
	                     // hgdata[from[i]], hgdata[from[i]+1], ..., 
	                     // hgdata[from[i+1]-1]
	int*     hgdata;    // Stores nodes for each hyperedge.
	
	//----- dual hypergraph ------------------------------------------
	int      dual_built; // Keeps track of whether dual has been built.
	int*     from2;  	 // Indices into dualdata for hyperedges in dual.
	int*     dualdata;   // Stores nodes for each hyperedge in dual.

	//----- memory management -----------------------------------------
	// Need to keep track of the number of entries in each of the current
	// array allocations.
	// Needed because size of hypergraph is not known apriori.
	int     final;       // flag indicating whether done building hg
    int     from_size;   // number of entries in current allocation
    int     hgdata_size; // number of entries in current allocation

} Hypergraph;

// function prototypes

//! construct an empty hypergraph
Hypergraph* Hypergraph_ctor();

//! deallocate all of the memory for the Hypergraph
void Hypergraph_dtor(Hypergraph**);

//! Insert a node into a hyperedge.  Insert in order of the hyperedges.
void Hypergraph_ordered_insert_node(Hypergraph* this, int hyperedge, int node);
//! Indicate that all nodes and hyperedges have been added to the hypergraph.
void Hypergraph_finalize( Hypergraph* this );

//! Output text representation of hypergraph to standard out.
void Hypergraph_dump( Hypergraph* this );

#endif

