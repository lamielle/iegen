/* This is a very simple example of how to use the CLooGLib inside your
 * programs. You should compile it by typing 'make' (after edition of the
 * makefile)
 *
 * This program generates loops to iterate over the set { [i,j] : 5<i<N and -10<j<-M }
 * and prints them to stdout.
 *
 * 5<i<N --> 5<i and i<N --> i>5 and -i>-N --> i-6>=0 and -i+N-1>=0
 *
 * -10<j<-M --> -10<j and j<-M --> j>-10 and -j>M --> j+9>=0 and -j-M-1>=0
 *
 * Thus the four constraints are:
 *  i-6>=0
 *  -i+N-1>=0
 *  j+9>=0
 *  -j-M-1>=0
 *
 * The cloog matrix should then be:
 * eq/in  i  j  n  m const
 *   1    1  0  0  0  -6
 *   1   -1  0  1  0  -1
 *   1    0  1  0  0   9
 *   1    0 -1  0 -1  -1

 */

#include <stdio.h>
#include <cloog/cloog.h>

int main()
{
   CloogProgram *program;

   CloogNames *names;
   char *iterator_names[]={"i","j"};
   char *parameter_names[]={"n","m"};

   CloogMatrix *context_matrix;
   CloogDomain *context_domain;

   CloogLoop *loop;

   CloogMatrix *domain_matrix;
   CloogDomain *domain;

   CloogBlock *block;
   CloogStatement *statement;

   CloogOptions *options;

   Value **p;

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
   domain_matrix=cloog_matrix_alloc(4,6);
   p=domain_matrix->p;
   p[0][0]=1; p[0][1]=1;  p[0][2]=0;  p[0][3]=0; p[0][4]=0;  p[0][5]=-6;
   p[1][0]=1; p[1][1]=-1; p[1][2]=0;  p[1][3]=1; p[1][4]=0;  p[1][5]=-1;
   p[2][0]=1; p[2][1]=0;  p[2][2]=1;  p[2][3]=0; p[2][4]=0;  p[2][5]=9;
   p[3][0]=1; p[3][1]=0;  p[3][2]=-1; p[3][3]=0; p[3][4]=-1; p[3][5]=-1;
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
   names->nb_iterators=2;
   names->nb_parameters=2;
   names->scattering=NULL;
   names->iterators=iterator_names;
   names->parameters=parameter_names;

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
   options = cloog_options_malloc();

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

   return 0;
}
