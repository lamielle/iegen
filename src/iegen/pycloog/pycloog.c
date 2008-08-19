#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <cloog/cloog.h>
#include <iegen/pycloog/pycloog.h>

char* pycloog_codegen(pycloog_statement *pycloog_statements,int pycloog_num_statements,pycloog_names *pycloog_names,string_allocator_t string_allocator)
{
   CloogDomainList *cloog_scatter_list;
   CloogProgram *cloog_program;
   CloogOptions *cloog_options;
   FILE *temp;
   char *result;

   /* Make sure we were given at least one statement to work with */
   if(pycloog_num_statements<=0)
   {
      fprintf(stderr,"[pyCLooG] No statements given to generate code for!\n");
      result=pycloog_get_error_result();
   }
   else
   {
      /* Build the CLooG program structure for the given statments and names */
      cloog_program=pycloog_get_program(pycloog_statements,pycloog_num_statements,pycloog_names);

      /* Get a list of scattering functions */
      cloog_scatter_list=pycloog_get_scatter_list(pycloog_statements,pycloog_num_statements,pycloog_names);

      /* Apply the scattering functions */
      pycloog_scatter(cloog_program,cloog_scatter_list);

      /* Get an options object */
      cloog_options=pycloog_get_options();

      /* Ask CLooG to generate a program from the give domain specifications */
      cloog_program=cloog_program_generate(cloog_program,cloog_options);

      /* Get a temporary file for CLooG to write to */
      temp=NULL;
      temp=pycloog_get_temp_file();
      if(NULL==temp)
      {
         fprintf(stderr,"[pyCLooG] Unable to obtain a temporary file for writing.\n");
         result=pycloog_get_error_result();
      }
      else
      {
         /* Print the program that was generated */
         cloog_program_pprint(temp,cloog_program,cloog_options);

         /* Get a string (allocated from python) from the text file that CLooG wrote to */
         result=pycloog_get_pystring_from_file(temp,string_allocator);
      }

      /* Close the temporary file */
      pycloog_close_temp_file(temp);

      /*
       *  Set the iterator and parameter names to NULL as they were not
       *  dynamically allocated and we don't want cloog to unallocate them.
       */
      cloog_program->names->iterators=NULL;
      cloog_program->names->parameters=NULL;

      /* Free the allocated structures */
      cloog_options_free(cloog_options);
      cloog_program_free(cloog_program); /* This recursively deallocates all substructures as well */
      cloog_domain_list_free(cloog_scatter_list);
   }

   return result;
}

char* pycloog_get_error_result(void)
{
	return "";
}

CloogProgram* pycloog_get_program(
   pycloog_statement *pycloog_statements,
   int pycloog_num_statements,
   pycloog_names *pycloog_names)
{
   CloogNames *cloog_names;
   CloogDomain *cloog_context;
   CloogLoop *cloog_loops;
   CloogProgram *cloog_program;

   /* Define the names of the iterators and parameters */
   cloog_names=pycloog_get_names(pycloog_names);

   /* Define the context (the constraints on the parameters) */
   cloog_context=pycloog_get_context(pycloog_names);

   /* Get a CloogLoop for each statement */
   cloog_loops=pycloog_get_loops(pycloog_statements,pycloog_num_statements,pycloog_names);

   /* Get a CloogProgram structure */
   cloog_program=cloog_program_malloc();
   cloog_program->language='c';
   cloog_program->nb_scattdims=0;
   cloog_program->names=cloog_names;
   cloog_program->context=cloog_context;
   cloog_program->loop=cloog_loops;
   cloog_program->blocklist=NULL;

   return cloog_program;
}

CloogDomainList* pycloog_get_scatter_list(
   pycloog_statement *pycloog_statements,
   int pycloog_num_statements,
   pycloog_names *pycloog_names)
{
   int pycloog_statement_num;
   CloogDomainList *cloog_scatter_head,*cloog_scatter_curr;

   /* Get the first scattering function */
   cloog_scatter_head=pycloog_get_domain_list(&pycloog_statements[0]);
   cloog_scatter_curr=cloog_scatter_head;
   cloog_scatter_curr->next=NULL;

   /* Iterate over each statement and build the necessary CLooG structures */
   for(pycloog_statement_num=1;pycloog_statement_num<pycloog_num_statements;pycloog_statement_num++)
   {
      /* Get a domain for the current statement's scattering function */
      cloog_scatter_curr->next=pycloog_get_domain_list(&pycloog_statements[pycloog_statement_num]);
      cloog_scatter_curr=cloog_scatter_curr->next;
      cloog_scatter_curr->next=NULL;
   }

   return cloog_scatter_head;
}

CloogOptions* pycloog_get_options()
{
   CloogOptions *cloog_options;

   /* Allocate an options structure */
   cloog_options=cloog_options_malloc();

   /* Set the name as it doesn't get done when using CLooG through its C API */
   cloog_options->name="pyCLooG";

   return cloog_options;
}

FILE* pycloog_get_temp_file(void)
{
   return tmpfile();
}

char* pycloog_get_pystring_from_file(FILE *file,string_allocator_t string_allocator)
{
   char *result;
   off_t size;
   size_t num_read;

   if(NULL==file)
   {
      fprintf(stderr,"[pyCLooG] Unable to obtain a string from a NULL file.\n");
      result=pycloog_get_error_result();
   }
   else
   {
      /* Flush the file to make sure all of the pending data has been written to disk */
      fflush(file);

      /* Get the file size */
      size=pycloog_get_file_size(fileno(file));
      if(-1==size)
      {
         fprintf(stderr,"[pyCLooG] Unable to determine size of temporary file.\n");
         result=pycloog_get_error_result();
      }
      else
      {
         /* Allocate space for the text of the file */
         result=NULL;
         result=string_allocator(size+1);
         if(NULL==result)
         {
            fprintf(stderr,"[pyCLooG] Unable to allocate space for file text.\n");
            result=pycloog_get_error_result();
         }
         else
         {
            /* Seek to the beginning of the file */
            if(-1==fseek(file,0,SEEK_SET))
            {
               fprintf(stderr,"[pyCLooG] Unable to seek to beginning of temporary file.\n");
               result=pycloog_get_error_result();
            }
            else
            {
               num_read=fread(result,sizeof(char),size,file);
               if(size!=num_read)
               {
                  fprintf(stderr,"[pyCLooG] Did not read expected number of characters from temporary file.\n");
                  result=pycloog_get_error_result();
               }
            }
         }
      }
   }

   return result;
}

off_t pycloog_get_file_size(int fd)
{
	struct stat sb;

	if(-1==fstat(fd,&sb))
	{
		perror("stat");
		return -1;
	}

	return sb.st_size;
}

void pycloog_close_temp_file(FILE *file)
{
   fclose(file);
}

CloogNames* pycloog_get_names(pycloog_names *pycloog_names)
{
   CloogNames *cloog_names;

   cloog_names=cloog_names_malloc();
   cloog_names->nb_scattering=0;
   cloog_names->nb_iterators=pycloog_names->num_iters;
   cloog_names->nb_parameters=pycloog_names->num_params;
   cloog_names->scattering=NULL;
   cloog_names->iterators=pycloog_names->iters;
   cloog_names->parameters=pycloog_names->params;

   return cloog_names;
}

CloogDomain* pycloog_get_context(pycloog_names *pycloog_names)
{
   CloogMatrix *cloog_matrix;
   CloogDomain *cloog_context;
   Value **p;
   int col;

   /* Allocate a CloogMatrix object */
   cloog_matrix=cloog_matrix_alloc(1,pycloog_names->num_params+2);

   /* Get the pointer to the matricies' data */
   p=cloog_matrix->p;

   /* Set zeros at each position in the context matrix */
   for(col=0;col<pycloog_names->num_params+2;col++)
   {
      p[0][col]=0;
   }

   /* Convert the matrix to a CLooG domain structure */
   cloog_context=cloog_domain_matrix2domain(cloog_matrix);

   /* Free the allocated CLooG matrix structure */
   cloog_matrix_free(cloog_matrix);

   return cloog_context;
}

CloogLoop* pycloog_get_loops(
   pycloog_statement *pycloog_statements,
   int pycloog_num_statements,
   pycloog_names *pycloog_names)
{
   CloogLoop *cloog_loop_head,*cloog_loop_curr;
   int pycloog_statement_num;

   /* Get the first loop structure */
   cloog_loop_head=pycloog_get_loop_from_statement(&pycloog_statements[0],pycloog_names,0);
   cloog_loop_curr=cloog_loop_head;
   cloog_loop_curr->next=NULL;

   /* Iterate over each statement and build the necessary CLooG structures */
   for(pycloog_statement_num=1;pycloog_statement_num<pycloog_num_statements;pycloog_statement_num++)
   {
      /* Get a loop structure for the current statement */
      cloog_loop_curr->next=pycloog_get_loop_from_statement(&pycloog_statements[pycloog_statement_num],pycloog_names,pycloog_statement_num);
      cloog_loop_curr=cloog_loop_curr->next;
      cloog_loop_curr->next=NULL;
   }

   return cloog_loop_head;
}

CloogLoop* pycloog_get_loop_from_statement(
   pycloog_statement *pycloog_statement,
   pycloog_names *pycloog_names,
   int pycloog_statement_num)
{
   CloogStatement *cloog_statement;
   CloogBlock *cloog_block;
   CloogLoop *cloog_loop;

   /* Define the CLooG statement structure */
   cloog_statement=cloog_statement_malloc();
   cloog_statement->number=pycloog_statement_num;
   cloog_statement->usr=NULL;
   cloog_statement->next=NULL;

   /* Define the statement block */
   cloog_block=cloog_block_malloc();
   cloog_block->statement=cloog_statement;
   cloog_block->scattering=NULL;
   cloog_block->depth=0;

   /* Define this statement's loop structure */
   cloog_loop=cloog_loop_malloc();
   cloog_loop->domain=pycloog_get_unioned_domains(pycloog_statement->domains,pycloog_statement->num_domains);
   cloog_loop->stride=1;
   cloog_loop->block=cloog_block;
   cloog_loop->inner=NULL;
   cloog_loop->next=NULL;

   return cloog_loop;
}

CloogDomain* pycloog_get_unioned_domains(pycloog_domain *domains,int num_domains)
{
   CloogDomain *unioned_domains,*curr_domain,*temp_domain;
   int curr_domain_pos;

   unioned_domains=pycloog_get_domain(&domains[0]);
   if(num_domains>1)
   {
      for(curr_domain_pos=1;curr_domain_pos<num_domains;curr_domain_pos++)
      {
         curr_domain=pycloog_get_domain(&domains[curr_domain_pos]);
         temp_domain=unioned_domains;
         unioned_domains=cloog_domain_union(temp_domain,curr_domain);
         cloog_domain_free(curr_domain);
         cloog_domain_free(temp_domain);
      }
   }

   return unioned_domains;
}

CloogDomain* pycloog_get_domain(pycloog_domain *domain)
{
   CloogMatrix *cloog_matrix;
   CloogDomain *cloog_domain;
   Value **p;
   int row,col;

   /* Allocate a CLooG matrix structure */
   cloog_matrix=cloog_matrix_alloc(domain->num_rows,domain->num_cols);

   /* Get the pointer to the matricies' data */
   p=cloog_matrix->p;

   /*
    * Copy the data from the given two dimensional array to
    * the allocated matrix
    */
   for(row=0;row<domain->num_rows;row++)
   {
      for(col=0;col<domain->num_cols;col++)
      {
         p[row][col]=domain->domain[row][col];
      }
   }

   /* Convert the matrix to a CLooG domain structure */
   cloog_domain=cloog_domain_matrix2domain(cloog_matrix);

   /* Free the allocated CLooG matrix structure */
   cloog_matrix_free(cloog_matrix);

   return cloog_domain;
}

CloogDomainList* pycloog_get_domain_list(pycloog_statement *pycloog_statement)
{
   CloogDomainList *cloog_domain_list;

   /*
    * There is no function to allocate a CloogDomainList.
    * This method (malloc) is used in cloog_domain_list_read,
    * so it must be good enough to use here!
    */
   cloog_domain_list=(CloogDomainList*)malloc(sizeof(CloogDomainList));

   cloog_domain_list->domain=pycloog_get_domain(&pycloog_statement->scatter);
   cloog_domain_list->next=NULL;

   return cloog_domain_list;
}

void pycloog_scatter(CloogProgram *cloog_program,CloogDomainList *cloog_scatter_list)
{
   int i;
   char **scattering;

   if (cloog_scatter_list != NULL)
   {
      if(cloog_domain_list_lazy_same(cloog_scatter_list))
      {
         fprintf(stderr, "[CLooG]WARNING: some scattering functions are similar.\n");
      }

      cloog_program->nb_scattdims=cloog_domain_dimension(cloog_scatter_list->domain)-cloog_domain_dimension(cloog_program->loop->domain);

      scattering=cloog_names_generate_items(cloog_program->nb_scattdims,"c",'1');

      /* The boolean array for scalar dimensions is created and set to 0. */
      cloog_program->scaldims = (int *)malloc(cloog_program->nb_scattdims*(sizeof(int)));

      if (cloog_program->scaldims == NULL)
      {
         fprintf(stderr, "[CLooG]ERROR: memory overflow.\n");
         exit(1);
      }

      for(i=0;i<cloog_program->nb_scattdims;i++)
         cloog_program->scaldims[i]=0;

      /* We try to find blocks in the input problem to reduce complexity. */
      cloog_program_block(cloog_program,cloog_scatter_list);
      cloog_program_extract_scalars(cloog_program,cloog_scatter_list);
      cloog_program_scatter(cloog_program,cloog_scatter_list);
   }
   else
   {
      cloog_program->nb_scattdims=0;
      cloog_program->scaldims=NULL;
   }
}
