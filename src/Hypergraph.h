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
    

 Copyright ((c)) 2008, Colorado State University
 All rights reserved.
 See COPYING for copyright details.
 
*//**********************************************************************/

#ifndef _Hypergraph_H
#define _Hypergraph_H

/* ////////////////////////////////////////////////////////////////////
// Class Hypergraph Definition
// 
//////////////////////////////////////////////////////////////////// */
typedef struct {

    int      nv;		 // Number of vertices.
	int      ne;		 // Number of hyperedges.
	
	//----- primary hypergraph ---------------------------------------
	int      *from; 	 // Indices into the hgdata array that indicate
	                     // where the nodes for hyperedges start and finish.
	                     // hyperedge i will have its nodes stored at
	                     // hgdata[from[i]], hgdata[from[i]+1], ..., 
	                     // hgdata[from[i+1]-1]
	int      *hgdata;    // Stores nodes for each hyperedge.
	
	//----- dual hypergraph ------------------------------------------
	int      dual_built; // Keeps track of whether dual has been built.
	int		 *from2;  	 // Indices into dualdata for hyperedges in dual.
	int 	 *dualdata;  // Stores nodes for each hyperedge in dual.

} Hypergraph;

#endif