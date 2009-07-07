/* trudt_RectUnionDomain.c */
/*! \file

    Driver that unit tests the RectUnionDomain data structure.
*/

#include "RectUnionDomain.h"
#include "util.h"

#define NUM_IN 10
#define NUM_OUT 5

//static int debug = false;

int main() 
{
  
  // scoping so that each trudt case can use the same variable namrud
  
  //-----------------------------------------------------------------
  // set1 = {[t,x] : 0 <= t < nt && 0 <= x <=1 }
  //-----------------------------------------------------------------
  {
    int nt = 3048;
    
    int dim = 2; 
    int num_rects = 1;
    RectUnionDomain* rud = RUD_ctor( dim, num_rects );
    RectDomain* rd;
    // first conjunction
    rd = RD_ctor(2);
    RD_set_lb(rd, 0, 0);
    RD_set_ub(rd, 0, nt-1);
    RD_set_lb(rd, 1, 0);
    RD_set_ub(rd, 1, 1);
    RUD_insert(rud, rd);
    
    RUD_dump(rud);
  }

  //-----------------------------------------------------------------
  // set2 = {[0,i] : 0 <= i < natom } union {[1,i] : 0 <= i < ninter }
  //-----------------------------------------------------------------
  {
    int natom = 189;
    int ninter = 1056;
    //int natom = 3;
    //int ninter = 5;

    int dim = 2; 
    int num_rects = 2;

    RectUnionDomain* rud = RUD_ctor( dim, num_rects );
    RectDomain* rd;
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
  
    RUD_dump(rud);
    
    // check the size of the explicit set
    assert(RUD_size(rud)==(natom+ninter));

    // checking the tuple traversal
    Tuple tuple = RUD_firstTuple(rud);
    printf("natom = %d, ninter = %d\n", natom, ninter);
    for (int i=0; i<RUD_size(rud); i++, tuple = RUD_nextTuple( rud, tuple )) 
    {
        //printf("tuple = "); Tuple_print(tuple); printf("\n");
    
        int x0 = Tuple_val(tuple, 0);
        int x1 = Tuple_val(tuple, 1);
        
        //printf("x0 = %d, x1 = %d\n", x0, x1);
        
        if (x0==0) {
            assert((0<=x1) && (x1<natom));
        } else if (x0==1) {
            assert((0<=x1) && (x1<ninter));
        } else {
            assert(0);
        }
    }
  }
    
  return 0;
}

