/**********************************************************************//*!
 \file

 \authors Michelle Strout

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