#include <stdio.h>

#include <isl/isl_ctx.h>
#include <isl/isl_set.h>
#include <isl/isl_constraint.h>

int main(int ac,char** av)
{
	struct isl_ctx *ctx;

	const char *str = "{[x,y]: x=6 && y>=10}";
	struct isl_basic_set *bset_parsed,*bset_man;
	struct isl_set *set_parsed,*set_man;
	struct isl_constraint *eq,*ineq;
	isl_int temp;

	/* Init the temporary integer we'll be using */
	isl_int_init(temp);

	/* Allocate a context object */
	ctx = isl_ctx_alloc();

	/* Create an isl_set from the set string */
	bset_parsed=isl_basic_set_read_from_str(ctx, str, 0, ISL_FORMAT_OMEGA);
	set_parsed=isl_set_from_basic_set(bset_parsed);

	/* Create the same isl_set manually */
	bset_man=isl_basic_set_alloc(ctx,0,2,0,1,1);
	eq=isl_equality_alloc(isl_dim_copy(bset_man->dim));
	ineq=isl_inequality_alloc(isl_dim_copy(bset_man->dim));

	isl_int_set_si(temp,1);
	isl_constraint_set_coefficient(eq,isl_dim_set,0,temp);
	isl_int_set_si(temp,-6);
	isl_constraint_set_constant(eq,temp);
	bset_man=isl_basic_set_add_constraint(bset_man,eq);

	isl_int_set_si(temp,1);
	isl_constraint_set_coefficient(ineq,isl_dim_set,1,temp);
	isl_int_set_si(temp,-10);
	isl_constraint_set_constant(ineq,temp);
	bset_man=isl_basic_set_add_constraint(bset_man,ineq);

	set_man=isl_set_from_basic_set(bset_man);

	/* Print the two sets */
	printf("Parsed set:\n");
	isl_set_print(set_parsed,stdout,0,ISL_FORMAT_POLYLIB);

	printf("\nConstructed set:\n");
	isl_set_print(set_man,stdout,0,ISL_FORMAT_POLYLIB);

	isl_set_free(set_parsed);
	isl_set_free(set_man);

	isl_ctx_free(ctx);

	isl_int_clear(temp);

	//isl_set_eliminate_dims
	//isl_set_free
	//isl_basic_set_print
	//isl_set_print
	return 0;
}
