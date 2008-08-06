#include <stdio.h>
#include <cloog/cloog.h>

void print_mat(int **mat,int num_rows,int num_cols)
{
   int row,col;
   printf("In C, whoo!\n");

   printf("mat: %p\n",mat);
   printf("mat is %d by %d\n",num_rows,num_cols);

   for(row=0;row<num_rows;row++)
   {
      for(col=0;col<num_cols;col++)
      {
//         printf("%d,%d: ",row,col);
//         printf("%p\n",mat[row]);
//         printf("(%d) %d ",row*num_cols+col,mat[row*num_cols+col]);
         printf("%d ",mat[row*num_cols+col]);
//         printf("%d ",mat[row][col]);
      }
      printf("\n");
   }
   printf("\n");
}
