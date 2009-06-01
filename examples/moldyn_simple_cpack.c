#include "moldyn_simple_common.c"

int main()
{
	MOLDYN_SIMPLE_COMMON_DECL

	/* Explicit relations */
	ExplicitRelation *sigma;

	MOLDYN_SIMPLE_COMMON_ALLOC

	MOLDYN_SIMPLE_COMMON_INIT

	MOLDYN_SIMPLE_COMMON_ORIG

	/* Print data/index arrays before untransformed computation */
	printf("Before untransformed computation: \n");
	print_arrays(x_notrans,fx_notrans,inter1_notrans,inter2_notrans,N,n_inter);

	/* Perform the untransformed computation */
	printf("Performing untransformed computation... ");
	executor_notrans(N,n_inter,fx_notrans,x_notrans,inter1_notrans,inter2_notrans);
	printf("done\n");

	/* Print data/index arrays after untransformed computation */
	printf("After untransformed computation: \n");
	print_arrays(x_notrans,fx_notrans,inter1_notrans,inter2_notrans,N,n_inter);


	/* Print data/index arrays before transformed computation */
	printf("Before transformed computation: \n");
	print_arrays(x_trans,fx_trans,inter1_trans,inter2_trans,N,n_inter);

	/* Perform the transformed computation */
	printf("Calling inspector for transformed computation... ");
	inspector_trans(N,n_inter,fx_trans,x_trans,inter1_trans,inter2_trans,&sigma);
	printf("done\n");
	printf("Performing transformed computation... ");
	executor_trans(N,n_inter,fx_trans,x_trans,inter1_trans,inter2_trans,&sigma);
	printf("done\n");

	/* Print data/index arrays after transformed computation */
	printf("After transformed computation: \n");
	print_arrays(x_trans,fx_trans,inter1_trans,inter2_trans,N,n_inter);

	MOLDYN_SIMPLE_COMMON_COMPARE

	MOLDYN_SIMPLE_COMMON_FREE
}
