#include "moldyn_fst_common.c"

int main()
{
	MOLDYN_FST_COMMON_DECLS

	/* Explicit relations */
	ExplicitRelation *sigma;

	MOLDYN_FST_COMMON_ALLOC

	MOLDYN_FST_COMMON_INIT

	MOLDYN_FST_COMMON_ORIG

	/* Print data/index arrays before untransformed computation */
	printf("Before untransformed computation: \n");
	print_arrays(x_notrans,fx_notrans,inter1_notrans,inter2_notrans,N,n_inter);

	/* Perform the untransformed computation */
	printf("Performing untransformed computation... ");
	executor_notrans(N,fx_notrans,inter1_notrans,inter2_notrans,T,x_notrans,n_inter);
	printf("done\n");

	/* Print data/index arrays after untransformed computation */
	printf("After untransformed computation: \n");
	print_arrays(x_notrans,fx_notrans,inter1_notrans,inter2_notrans,N,n_inter);


	/* Print data/index arrays before transformed computation */
	printf("Before transformed computation: \n");
	print_arrays(x_trans,fx_trans,inter1_trans,inter2_trans,N,n_inter);

	/* Perform the transformed computation */
	printf("Calling inspector for transformed computation... ");
	inspector_trans(N,fx_trans,inter1_trans,inter2_trans,T,x_trans,n_inter,&sigma);
	printf("done\n");
	printf("Performing transformed computation... ");
	executor_trans(N,fx_trans,inter1_trans,inter2_trans,T,x_trans,n_inter,&sigma);
	printf("done\n");

	/* Print data/index arrays after transformed computation */
	printf("After transformed computation: \n");
	print_arrays(x_trans,fx_trans,inter1_trans,inter2_trans,N,n_inter);

	MOLDYN_FST_COMMON_COMPARE

	MOLDYN_FST_COMMON_FREE
}
