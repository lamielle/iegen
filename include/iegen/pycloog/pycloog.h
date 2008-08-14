#ifndef _PYCLOOG_H_
#define _PYCLOOG_H_

#include <cloog/cloog.h>

/*
 * Contains all data for a single statement:
 *   -Domain of the statement
 *   -Number of rows/cols for the domain
 *   -Scattering function for the statement
 *   -Number of rows/cols for the scattering function
 */
struct pycloog_statement
{
   int **domain;
   int domain_num_rows;
   int domain_num_cols;
   int **scatter;
   int scatter_num_rows;
   int scatter_num_cols;
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

/* PUBLIC INTERFACE: */

/*
 * Generates code using CLooG using the data
 * for the given statements and iterator/parameter names
 */
void pycloog_codegen(pycloog_statement *pycloog_statements,int pycloog_num_statements,pycloog_names *pycloog_names);

/* PRIVATE INTERFACE: */

/*
 * Gets a CloogProgram structure filled with data from
 * the given statements and names.
 */
CloogProgram* pycloog_get_program(
   pycloog_statement *pycloog_statements,
   int pycloog_num_statements,
   pycloog_names *pycloog_names);

/*
 * Gets a linked list of CloogDomainList structures,
 * one per statement, where the domain of each is the
 * scattering function for the statement.
 */
CloogDomainList* pycloog_get_scatter_list(
   pycloog_statement *pycloog_statements,
   int pycloog_num_statements,
   pycloog_names *pycloog_names);

/*
 * Gets a CloogOptions object
 */
CloogOptions* pycloog_get_options();

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
 * Gets a CloogDomain structure
 * with data from the given two dimensional array.
 */
CloogDomain* pycloog_get_domain(int **domain,int num_rows,int num_cols);

/*
 * Gets a CloogDomainList with the domain
 * set to the scattering function of the given statement.
 */
CloogDomainList* pycloog_get_domain_list(pycloog_statement *pycloog_statement);

/*
 * Applies the given scattering functions to the given program.
 *
 * NOTE: This code was originally taken from the CLooG code base: source/cloog.c
 * Many useful things are done here that are not exposed through the C API.
 */
void pycloog_scatter(CloogProgram *cloog_program,CloogDomainList *cloog_scatter_list);

#endif
