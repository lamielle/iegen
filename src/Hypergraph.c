/* Hypergraph.c */
#include "Hypergraph.h"
/*! \file 
    Implements the Hypergraph data structure for use with the PIES project.
    

*/

#include "Hypergraph.h"

/*----------------------------------------------------------------*//*! 
  \short Construct Hypergraph structure and return a ptr to it.

  Initializes the hypergraph to empty.

  \return Returns a ptr to the constructed Hypergraph structure.

  \author Michelle Strout 6/23/08
*//*----------------------------------------------------------------*/
Hypergraph* Hypergraph_ctor() 
{
    Hypergraph* this = (Hypergraph*)malloc(sizeof(Hypergraph));
    
    this->nv = 0;
    this->ne = -1;  // this is so that when start inserting
                    // hyperedge 0, we can actually notice
    
    this->from = (int*)malloc(sizeof(int)*MEM_ALLOC_INCREMENT);
    this->hgdata = (int*)malloc(sizeof(int)*MEM_ALLOC_INCREMENT);
    
    this->dual_built = 0;
    this->from2 = NULL;
    this->dualdata = NULL;
    
    this->final = 0;
    this->from_size = MEM_ALLOC_INCREMENT;
    this->hgdata_size = MEM_ALLOC_INCREMENT;
    
    return this;
}


//! Helper routine for expanding an arrays data allocation.
// FIXME: How do I make this routine visible only in this C file?
void expand_array( int** array_handle, int* array_size )
{
    // save old info
    int* temp = *array_handle;
    int old_size = *array_size;
    int i;
            
    // create new array that is bigger
    *array_size += MEM_ALLOC_INCREMENT;
    *array_handle = (int*)malloc(sizeof(int)*(*array_size));
            
    // copy data from old array
    for (i=0; i<old_size; i++) {
        (*array_handle)[i] = temp[i];
    }
}


/*----------------------------------------------------------------*//*! 
  \short Insert a node into a hyperedge.  Insert in order of the hyperedges.

  Handles some memory management wrt the from and hgdata arrays.

  \author Michelle Strout 6/23/08
*//*----------------------------------------------------------------*/
void Hypergraph_ordered_insert_node(Hypergraph* this, int hyperedge, int node)
{
    // cannot insert new data into a finalized graph
    assert(this->final==0);
    
    // first check whether this is a new hyperedge
    if (this->ne < hyperedge) {
        // number of hyperedges is going to go up
        this->ne += 1;
    
        // if we are on the next hyperedge then check if we need to 
        // expand the array.
        if  (this->ne + 1 > this->from_size) {
            expand_array( &(this->from), &(this->from_size) );
        }
        
        // set the end of the indices to nodes for this new hyperedge to 
        // the same as the beginning, since currently haven't inserted any
        // nodes for the hyperedge.
        //this->from[(this->ne)] = this->from[(this->ne)-1];
        this->from[hyperedge+1] = this->from[hyperedge];
        
    }
    
    // check that there is enough room to insert a node into this hyperedge,
    // and if not then expand allocation for hgdata array.
    if (this->from[hyperedge+1] + 1 > this->hgdata_size) {
        expand_array( &(this->hgdata), &(this->hgdata_size) );
    }
    
    // insert the node into the hyperedge
    this->hgdata[ this->from[hyperedge+1]++ ] = node;
    
    // if this node id is higher than any we have seen then increase the number
    // of nodes.
    if (node > (this->nv -1) ) {
        this->nv = node+1;
    }
}

/*----------------------------------------------------------------*//*! 
  \short Indicate that all nodes and hyperedges have been added to the hypergraph.

  Right now just setting the final flag.  Later might do more work.

  \author Michelle Strout 6/23/08
*//*----------------------------------------------------------------*/
void Hypergraph_finalize( Hypergraph* this ) {
    this->final = 1;
}

/*----------------------------------------------------------------*//*! 
  \short Output text representation of hypergraph to standard out.

  Format of output is one hyperedge per line.
  
    0: 3 5 6
    1: 2 8 5
    ...
    
  Where the first number is the hyperedge number and the nodes in that hyperedge
  are listed after it.
  The values of other fields are also printed.

  \author Michelle Strout 6/23/08
*//*----------------------------------------------------------------*/
void Hypergraph_dump( Hypergraph* this )
{
    int he, p;
    
    printf("Hypergraph\n");
    printf("\tnv = %d\n", this->nv);
    printf("\tne = %d\n", this->ne);
    printf("\tdual_built = %d\n", this->dual_built);
    printf("\tfinal = %d\n", this->final);
    printf("\tfrom_size = %d\n", this->from_size);
    printf("\thgdata_size = %d\n", this->hgdata_size);
    
    for (he=0; he<this->ne; he++) {
        printf("\t%d: ", he);
        for (p=this->from[he]; p<this->from[he+1]; p++) {
            printf("%d ", this->hgdata[p]);
        }
        printf("\n");
    }
}

