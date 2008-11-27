#ifndef _PYCLOOG_H_
#define _PYCLOOG_H_

#include <stdio.h>
#include <cloog/cloog.h>

/*
 * Contains data for a two-dimensional domain:
 *  -The domain data itself
 *  -Number of rows for the domain
 *  -Number of cols for the domain
 */
struct pycloog_domain
{
   int **domain;
   int num_rows;
   int num_cols;
};
typedef struct pycloog_domain pycloog_domain;

/*
 * Contains all data for a single statement:
 *  -Collection of domains for the statement
 *  -Number of domains for the statement
 *  -Scattering function for the statement
 */
struct pycloog_statement
{
   pycloog_domain *domains;
   int num_domains;
   pycloog_domain *scatter;
};
typedef struct pycloog_statement pycloog_statement;

/* Iterator and parameter names */
struct pycloog_names
{
   char **iters;
   int num_iters;
   char **params;
   int num_params;
};
typedef struct pycloog_names pycloog_names;

typedef char*(*string_allocator_t)(int);

/* PUBLIC INTERFACE: */

/*
 * Generates code using CLooG using the data
 * for the given statements and iterator/parameter names
 * Returns a string with the code that CLooG generated
 * A note on scattering functions:
 * If the first statement's scattering function is NULL,
 * it is assumed that no scattering is desired.
 * If the first statement's scattering function is not NULL,
 * it is assumed that each statement will have one.
 * You can either provide a scattering function for each statement,
 * or not provide any at all.
 */
char* pycloog_codegen(pycloog_statement *pycloog_statements,int pycloog_num_statements,pycloog_names *pycloog_names,string_allocator_t string_allocator);

/* PRIVATE INTERFACE: */

/* Returns an empty string */
char* pycloog_get_error_result(void);

/*
 * Gets a CloogProgram structure filled with data from
 * the given statements and names.
 */
CloogProgram* pycloog_get_program(
   pycloog_statement *pycloog_statements,
   int pycloog_num_statements,
   pycloog_names *pycloog_names);

/*
 * Gets a linked list of CloogScatteringList structures,
 * one per statement, where the domain of each is the
 * scattering function for the statement.
 */
CloogScatteringList* pycloog_get_scatter_list(
   pycloog_statement *pycloog_statements,
   int pycloog_num_statements,
   pycloog_names *pycloog_names);

/*
 * Gets a CloogOptions object
 */
CloogOptions* pycloog_get_options();

/*
 * Gets a temporary stdio FILE* object
 */
FILE* pycloog_get_temp_file(void);

/*
 * Reads the text from the given file and returns
 * a string of that text
 */
char* pycloog_get_pystring_from_file(FILE *file,string_allocator_t string_allocator);

/*
 * Returns the file size of the file associated with the given file descriptor.
 * Returns -1 if a failure occurs.
 */
off_t pycloog_get_file_size(int fd);

/*
 * Closes the given file
 */
void pycloog_close_temp_file(FILE *file);

/*
 * Gets a CloogNames structure filled with the given
 * iterator and parameter names
 */
CloogNames* pycloog_get_names(pycloog_names *pycloog_names);

/*
 * Gets a CloogDomain representing the
 * constraints on the parameters.
 * For now, no constraints are set.
 */
CloogDomain* pycloog_get_context(pycloog_names *pycloog_names);

/*
 * Gets a linked list of CloogLoop structures,
 * one per statement, where the domain of each loop
 * is the domain of the corresponding statement.
 */
CloogLoop* pycloog_get_loops(
   pycloog_statement *pycloog_statements,
   int pycloog_num_statements,
   pycloog_names *pycloog_names);

/*
 * Gets a CloogLoop structure filled
 * with data from the given statement and names
 */
CloogLoop* pycloog_get_loop_from_statement(
   pycloog_statement *pycloog_statement,
   pycloog_names *pycloog_names,
   int pycloog_statement_num);

/*
 * Gets a CloogDomain structure that is the union of
 * the given collection of domains
 */
CloogDomain* pycloog_get_unioned_domains(pycloog_domain *domains,int num_domains);

/*
 * Gets a CloogDomain structure
 * with data from the given two dimensional array.
 */
CloogDomain* pycloog_get_domain(pycloog_domain *domain);

/*
 * Gets a CloogScatteringList with the domain
 * set to the scattering function of the given statement.
 */
CloogScatteringList* pycloog_get_domain_list(pycloog_statement *pycloog_statement);

/*
 * Applies the given scattering functions to the given program.
 *
 * NOTE: This code was originally taken from the CLooG code base: source/cloog.c
 * Many useful things are done here that are not exposed through the C API.
 */
void pycloog_scatter(CloogProgram *cloog_program,CloogScatteringList *cloog_scatter_list,CloogOptions *cloog_options);

#endif
