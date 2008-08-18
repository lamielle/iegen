/* Hypergraph.c */
#include "Hypergraph.h"
/*! \file 
    Implements the Hypergraph data structure for use with the PIES project.
    

*/

#include "Hypergraph.h"

//----------------------- Helper routines for internal use

static void transpose_hypergraph(int hg_n, int *hg_idx, int *hg_list,
                                 int dual_n, int *dual_idx, int *dual_list);

Hypergraph* Hypergraph_ctor() 
/*----------------------------------------------------------------*//*! 
  \short Construct Hypergraph structure and return a ptr to it.

  Initializes the hypergraph to empty.

  \return Returns a ptr to the constructed Hypergraph structure.

  \author Michelle Strout 6/23/08
*//*----------------------------------------------------------------*/
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
    
    // nicely formated by hyperedge
    printf("\thedge: nodes in hedge\n");
    for (he=0; he<self->ne; he++) {
        printf("\t%d: ", he);
        for (p=self->from[he]; p<self->from[he+1]; p++) {
            printf("%d ", self->hgdata[p]);
        }
        printf("\n");
    }

    // rest of the raw data
    printf("from = "); 
    printArray(self->from, self->ne+1);
    printf("hgdata = "); 
    printArray(self->hgdata, self->from[self->ne]);
    if (self->dual_built) {
        printf("from2 = "); 
        printArray(self->from2, self->nv+1);
        printf("dualdata = "); 
        printArray(self->dualdata, self->from2[self->nv]);
    }

}

void construct_dual(Hypergraph* hg)
/*------------------------------------------------------------*//*!
  If the dual has not been constructed for this hypergraph,
  then construct it.

  \param  hg        Hypergraph pointer

  \author Michelle Strout 7/9/08
*//*--------------------------------------------------------------*/
{
    if (hg->dual_built==false) {
        MALLOC(hg->from2,int,hg->nv+1); 

        // the dualdata array will be the same size as the hgdata array
        MALLOC(hg->dualdata,int,hg->from[hg->ne]); 

        transpose_hypergraph(hg->ne, hg->from, hg->hgdata,
                             hg->nv, hg->from2, hg->dualdata);
        hg->dual_built=true;
    }

}

static void transpose_hypergraph(int hg_n, int *hg_idx, int *hg_list, 
                                 int dual_n, int *dual_idx, int *dual_list)
/*------------------------------------------------------------*//*!
  Forms the dual of a hypergraph.  Should only be used internal
  to Hypergraph abstraction.

  \param  hg_n      number of hyperedges in hypergraph
  \param  hg_idx    indices into linearized hypergraph
  \param  hg_list   linearized hypergraph
                    hg_list[hg_idx[i]]->hg_list[hg_idx[i+1]]-1 lists 
                    vertices in hyperedge i 
  \param  dual_n    number of hyperedges in dual hypergraph
  \param  dual_idx  indices into linearized dual hypergraph
  \param  dual_list linearized dual hypergraph (same size as hg_list)

  \author Paul Hovland 3/17/04
*//*--------------------------------------------------------------*/
{
        int i,j;

        for(i=0;i<=dual_n;i++)
                dual_idx[i] = 0;

        for(i=0;i<hg_idx[hg_n];i++)
                dual_idx[hg_list[i]]++;

        dual_idx[dual_n] = hg_idx[hg_n];
        for(i = dual_n; i>0; i--)
            dual_idx[i-1] = dual_idx[i] - dual_idx[i-1];

        for(i=0;i<hg_n;i++)
            for(j=hg_idx[i];j<hg_idx[i+1];j++)
                      dual_list[dual_idx[hg_list[j]]++] = i;

        for (i = dual_n; i > 0; i--)
            dual_idx[i] = dual_idx[i-1];

        dual_idx[0] = 0;
}

