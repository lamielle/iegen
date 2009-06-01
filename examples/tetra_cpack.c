#include "tetra_common.c"

int main()
{
	/* Declare common variables */
	TETRA_COMMON_DECL

	/* Explicit relations */
	ExplicitRelation *sigma;

	/* Allocate data/index arrays */
	TETRA_COMMON_ALLOC

	/* Init data/index arrays */
	TETRA_COMMON_INIT

	/* Perform the original computation */
	TETRA_COMMON_ORIG

	/* Print data/index arrays before untransformed computation */
	printf("Before untransformed computation: \n");
	print_arrays(data_notrans,res_notrans,n1_notrans,n2_notrans,n3_notrans,n4_notrans,N);

	/* Perform the untransformed computation */
	printf("Performing untransformed computation... ");
	executor_notrans(N,data_notrans,res_notrans,n1_notrans,n2_notrans,n3_notrans,n4_notrans);
	printf("done\n");

	/* Print data/index arrays after untransformed computation */
	printf("After untransformed computation: \n");
	print_arrays(data_notrans,res_notrans,n1_notrans,n2_notrans,n3_notrans,n4_notrans,N);


	/* Print data/index arrays before transformed computation */
	printf("Before transformed computation: \n");
	print_arrays(data_trans,res_trans,n1_trans,n2_trans,n3_trans,n4_trans,N);

	/* Perform the transformed computation */
	printf("Calling inspector for transformed computation... ");
	inspector_trans(N,data_trans,res_trans,n1_trans,n2_trans,n3_trans,n4_trans,&sigma);
	printf("done\n");
	printf("Performing transformed computation... ");
	executor_trans(N,data_trans,res_trans,n1_trans,n2_trans,n3_trans,n4_trans,&sigma);
	printf("done\n");

	/* Print data/index arrays after transformed computation */
	printf("After transformed computation: \n");
	print_arrays(data_trans,res_trans,n1_trans,n2_trans,n3_trans,n4_trans,N);


	/* Compare data/index arrays to ensure they are the same */
	TETRA_COMMON_COMPARE

	/* Free space allocated for data/index arrays */
	TETRA_COMMON_FREE
}
