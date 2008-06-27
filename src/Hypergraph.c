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
    Hypergraph* self = (Hypergraph*)malloc(sizeof(Hypergraph));
    
    self->nv = 0;
    self->ne = 0;  
    
    self->from = NULL;
    self->hgdata = NULL;
    
    self->dual_built = 0;
    self->from2 = NULL;
    self->dualdata = NULL;
    
    self->final = 0;
    self->from_size = 0;
    self->hgdata_size = 0;
    
    return self;
}

/*----------------------------------------------------------------*//*! 
  \short Deallocate all memory for Hypergraph

  \author Michelle Strout 6/24/08
*//*----------------------------------------------------------------*/
void Hypergraph_dtor( Hypergraph** self )
{
    if ((*self)->from != NULL) { free((*self)->from); }
    if ((*self)->hgdata != NULL) { free((*self)->hgdata); }
    if ((*self)->from2 != NULL) { free((*self)->from2); }
    if ((*self)->dualdata != NULL) { free((*self)->dualdata); }
    free(*self);
    *self = NULL;
}


//! Helper routine for expanding an arrays data allocation.
static void expand_array( int** array_handle, int* array_size )
{
    // save old info
    int* temp = *array_handle;
    int old_size = *array_size;
    int i;
            
    // create new array that is bigger
    *array_size += MEM_ALLOC_INCREMENT;
    *array_handle = (int*)calloc((*array_size),sizeof(int));
            
    // copy data from old array
    for (i=0; i<old_size; i++) {
        (*array_handle)[i] = temp[i];
    }

    // delete old array
    free(temp);
}


/*----------------------------------------------------------------*//*! 
  \short Insert a node into a hyperedge.  Insert in order of the hyperedges.

  Handles some memory management wrt the from and hgdata arrays.

  \author Michelle Strout 6/23/08
*//*----------------------------------------------------------------*/
void Hypergraph_ordered_insert_node(Hypergraph* self, int hyperedge, int node)
{
    // cannot insert new data into a finalized graph
    assert(self->final==0);
    
    // first check whether self is a new hyperedge
    // adding one to hyperedge because they are zero indexed
    if (self->ne < (hyperedge+1)) {
        // number of hyperedges is going to go up
        self->ne += 1;
    
        // if we are on the next hyperedge then check if we need to 
        // expand the array.
        if  (self->ne + 1 > self->from_size) {
            expand_array( &(self->from), &(self->from_size) );
        }
        
        // set the end of the indices to nodes for this new hyperedge to 
        // the same as the beginning, since currently haven't inserted any
        // nodes for the hyperedge.
        self->from[hyperedge+1] = self->from[hyperedge];
        
    }
    
    // check that there is enough room to insert a node into this hyperedge,
    // and if not then expand allocation for hgdata array.
    if (self->from[hyperedge+1] + 1 > self->hgdata_size) {
        expand_array( &(self->hgdata), &(self->hgdata_size) );
    }
    
    // insert the node into the hyperedge
    self->hgdata[ self->from[hyperedge+1] ] = node;
    self->from[hyperedge+1]++;

    // if this node id is higher than any we have seen then increase the number
    // of nodes.
    if (node > (self->nv -1) ) {
        self->nv = node+1;
    }
}

/*----------------------------------------------------------------*//*! 
  \short Indicate that all nodes and hyperedges have been added to the hypergraph.

  Right now just setting the final flag.  Later might do more work.

  \author Michelle Strout 6/23/08
*//*----------------------------------------------------------------*/
void Hypergraph_finalize( Hypergraph* self ) {
    self->final = 1;
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
void Hypergraph_dump( Hypergraph* self )
{
    int he, p;
    
    printf("Hypergraph\n");
    printf("\tnv = %d\n", self->nv);
    printf("\tne = %d\n", self->ne);
    printf("\tdual_built = %d\n", self->dual_built);
    printf("\tfinal = %d\n", self->final);
    printf("\tfrom_size = %d\n", self->from_size);
    printf("\thgdata_size = %d\n", self->hgdata_size);
    
    for (he=0; he<self->ne; he++) {
        printf("\t%d: ", he);
        for (p=self->from[he]; p<self->from[he+1]; p++) {
            printf("%d ", self->hgdata[p]);
        }
        printf("\n");
    }
}


