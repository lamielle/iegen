#include <stdio.h>
#include <stdlib.h>

#include <iegen.h>

#define TETRA_COMMON_DECL /* Symbolic constants */\
	int N=10;\
\
	/* Data arrays */\
	double *data_orig,*res_orig,*data_notrans,*res_notrans,*data_trans,*res_trans;\
\
	/* Index arrays */\
	int *n1_orig,*n2_orig,*n3_orig,*n4_orig,*n1_notrans,*n2_notrans,*n3_notrans,*n4_notrans,*n1_trans,*n2_trans,*n3_trans,*n4_trans;

#define TETRA_COMMON_ALLOC printf("Allocating data/index arrays... ");\
	alloc_arrays(&data_orig,&res_orig,&n1_orig,&n2_orig,&n3_orig,&n4_orig,N);\
	alloc_arrays(&data_notrans,&res_notrans,&n1_notrans,&n2_notrans,&n3_notrans,&n4_notrans,N);\
	alloc_arrays(&data_trans,&res_trans,&n1_trans,&n2_trans,&n3_trans,&n4_trans,N);\
	printf("done\n");

#define TETRA_COMMON_INIT \
	printf("Initializing data/index arrays... ");\
	init_arrays(data_orig,res_orig,n1_orig,n2_orig,n3_orig,n4_orig,N);\
	init_arrays(data_notrans,res_notrans,n1_notrans,n2_notrans,n3_notrans,n4_notrans,N);\
	init_arrays(data_trans,res_trans,n1_trans,n2_trans,n3_trans,n4_trans,N);\
	printf("done\n");

#define TETRA_COMMON_ORIG /* Print data/index arrays before original computation */\
	printf("Before original computation: \n");\
	print_arrays(data_orig,res_orig,n1_orig,n2_orig,n3_orig,n4_orig,N);\
\
	/* Perform the original computation */\
	printf("Performing original computation... ");\
	executor_orig(data_orig,res_orig,n1_orig,n2_orig,n3_orig,n4_orig,N);\
	printf("done\n");\
\
	/* Print data/index arrays after original computation */\
	printf("After original computation: \n");\
	print_arrays(data_orig,res_orig,n1_orig,n2_orig,n3_orig,n4_orig,N);

#define TETRA_COMMON_COMPARE int *index_arrays[][3]={{n1_orig,n1_notrans,n1_trans},\
	                     {n2_orig,n2_notrans,n2_trans},\
	                     {n3_orig,n3_notrans,n3_trans},\
	                     {n4_orig,n4_notrans,n4_trans}};\
	double *data_arrays[][3]={{data_orig,data_notrans,data_trans},\
	                          {res_orig,res_notrans,res_trans}};\
	const char* row_labels[6]={"n1","n2","n3","n4","data","res"};\
	const char* col_labels[3]={"Orig-NoTrans","Orig-Trans","NoTrans-Trans"};\
	print_comparison(index_arrays,4,N,data_arrays,2,N,row_labels,col_labels);

#define TETRA_COMMON_FREE free_arrays(&data_orig,&res_orig,&n1_orig,&n2_orig,&n3_orig,&n4_orig);\
	free_arrays(&data_notrans,&res_notrans,&n1_notrans,&n2_notrans,&n3_notrans,&n4_notrans);\
	free_arrays(&data_trans,&res_trans,&n1_trans,&n2_trans,&n3_trans,&n4_trans);

void alloc_arrays(double **data,double **res,int **n1,int **n2,int **n3,int **n4,int N)
{
	alloc_double_array(data,N);
	alloc_double_array(res,N);
	alloc_int_array(n1,N);
	alloc_int_array(n2,N);
	alloc_int_array(n3,N);
	alloc_int_array(n4,N);
}

void free_arrays(double **data,double **res,int **n1,int **n2,int **n3,int **n4)
{
	free_double_array(data);
	free_double_array(res);
	free_int_array(n1);
	free_int_array(n2);
	free_int_array(n3);
	free_int_array(n4);
}

void init_arrays(double *data,double *res,int *n1,int *n2,int *n3,int *n4,int N)
{
	int i;

	/* Init data arrays and index arrays*/
	for(i=0;i<N;i++)
	{
		data[i]=3.0*i;
		res[i]=0.0;
		n1[i]=i;
		n2[i]=(i+1)%N;
		n3[i]=(i+2)%N;
		n4[i]=(i+3)%N;
	}
}

void print_arrays(double *data,double *res,int *n1,int *n2,int *n3,int *n4,int N)
{
	printf("data: "); print_double_array(data,N); printf("\n");
	printf("res:  "); print_double_array(res,N); printf("\n");
	printf("n1:   "); print_int_array(n1,N); printf("\n");
	printf("n2:   "); print_int_array(n2,N); printf("\n");
	printf("n3:   "); print_int_array(n3,N); printf("\n");
	printf("n4:   "); print_int_array(n4,N); printf("\n");
}

void executor_orig(double *data,double *res,int *n1,int *n2,int *n3,int *n4,int N)
{
	int i;

	for(int i=0; i<N; i++)
	{
		res[i]+=data[n1[i]];
		res[i]+=data[n2[i]];
		res[i]+=data[n3[i]];
		res[i]+=data[n4[i]];
	}
}

/* Include the untransformed code */
#include "tetra_notrans.c"

/* Include the transformed code */
#include "tetra_trans.c"
