/* Hypergraph.c */
#include "Hypergraph.h"
/*! \file 
    Implements the Hypergraph data structure for use with the PIES project.
    
    The Hypergraph data structure is for creating an explicit representation
    of access relations at runtime.  The primary hypergraph will have
    iterations as hyperedges and the data locations being accessed as 
    nodes within individual hyperedges.
*/

#include "Hypergraph.h"

/*----------------------------------------------------------------*//*! 
  \short Construct Hypergraph structure and return a ptr to it.

  \return Returns a ptr to the constructed Hypergraph structure.

  \author Michelle Strout 5/30/08
*//*----------------------------------------------------------------*/
