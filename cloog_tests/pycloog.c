#include <stdio.h>
#include <cloog/cloog.h>

void print_mat(int **mat,int num_rows,int num_cols,char **iters,int num_iters,char **params,int num_params)
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

   for(row=0;row<num_iters;row++)
      printf("iter %d: %s\n",row,iters[row]);
   for(row=0;row<num_params;row++)
      printf("param %d: %s\n",row,params[row]);
}

void code_gen(int **dom,int num_rows,int num_cols,char **iters,int num_iters,char **params,int num_params)
{
   CloogProgram *program;

   CloogNames *names;

   CloogMatrix *context_matrix;
   CloogDomain *context_domain;

   CloogLoop *loop;

   CloogMatrix *domain_matrix;
   CloogDomain *domain;

   CloogBlock *block;
   CloogStatement *statement;

   CloogOptions *options;

   Value **p;
   int row,col;

   /* Define the single statement */
   statement=cloog_statement_malloc();
   statement->number=0;
   statement->usr=NULL;
   statement->next=NULL;

   /* Define the statement block */
   block=cloog_block_malloc();
   block->statement=statement;
   block->scattering=NULL;
   block->depth=0;

   /* Define the domain */
   domain_matrix=cloog_matrix_alloc(num_rows,num_cols);
   p=domain_matrix->p;
   for(row=0;row<num_rows;row++)
      for(col=0;col<num_cols;col++)
         p[row][col]=dom[row][col];

//   p[0][0]=1; p[0][1]=1;  p[0][2]=0;  p[0][3]=0; p[0][4]=0;  p[0][5]=-6;
//   p[1][0]=1; p[1][1]=-1; p[1][2]=0;  p[1][3]=1; p[1][4]=0;  p[1][5]=-1;
//   p[2][0]=1; p[2][1]=0;  p[2][2]=1;  p[2][3]=0; p[2][4]=0;  p[2][5]=9;
//   p[3][0]=1; p[3][1]=0;  p[3][2]=-1; p[3][3]=0; p[3][4]=-1; p[3][5]=-1;
   domain=cloog_domain_matrix2domain(domain_matrix);

   /* Define the loop */
   loop=cloog_loop_malloc();
   loop->domain=domain;
   loop->stride=1;
   loop->block=block;
   loop->inner=NULL;
   loop->next=NULL;

   /* Define the names of the iterators and parameters */
   names=cloog_names_malloc();
   names->nb_scattering=0;
   names->nb_iterators=num_iters;
   names->nb_parameters=num_params;
   names->scattering=NULL;
   names->iterators=iters;
   names->parameters=params;

   /* Define the context (the constraints on the parameters) */
   context_matrix=cloog_matrix_alloc(1,4);
   p=context_matrix->p;
   p[0][0]=0; p[0][1]=0; p[0][2]=0; p[0][3]=0;
   context_domain=cloog_domain_matrix2domain(context_matrix);

   /* Build the CLooG program structure for this example */
   program=cloog_program_malloc();
   program->language='c';
   program->nb_scattdims=0;
   program->names=names;
   program->context=context_domain;
   program->loop=loop;
   program->blocklist=NULL;

   /* Allocate an options object */
   options=cloog_options_malloc();

   /* Set the name as it doesn't get done when using CLooG through its C API */
   options->name="pyCLooG";

   /* Ask cloog to generate a program from the given domain */
   program=cloog_program_generate(program,options);

   /* Print the program that was generated */
   cloog_program_pprint(stdout,program,options);

   /*
    *  Set the iterator names to NULL as they were not dynamically
    *  allocated and we don't want cloog to do it
    */
   names->iterators=NULL;
   names->parameters=NULL;

   /* Free the allocated structures */
   cloog_options_free(options);
   cloog_program_free(program); //This recursively allocates all substructures as well
   cloog_matrix_free(context_matrix);
   cloog_matrix_free(domain_matrix);
}
