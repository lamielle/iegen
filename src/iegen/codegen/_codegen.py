#Given a collection of Statement objects, calculates the combined iteration space of all statements
def full_iter_space(statements):
	#Get the iteration space of the first statement
	statement=statements[0]
	full_iter=statement.iter_space.apply(statement.scatter)

	#Now union this with the rest of the statement's iteration spaces
	for statement in statements[1:]:
		full_iter=full_iter.union(statement.iter_space.apply(statement.scatter))

	return full_iter

def calc_artt(mapir,data_permute):
	from iegen import AccessRelation
	#Iteration Sub Space Relation
	issr=data_permute.iter_sub_space_relation

	#Calculate the iteration space to data space relation
	iter_to_data=None
	for stmt in mapir.statements:
		if not iter_to_data:
			iter_to_data=issr.compose(stmt.scatter.compose(stmt.access_relations[0].iter_to_data.inverse())).inverse()
		else:
			iter_to_data=iter_to_data.union(issr.compose(stmt.scatter.compose(stmt.access_relations[0].iter_to_data.inverse())).inverse())

		for ar in stmt.access_relations[1:]:
			iter_to_data=iter_to_data.union(issr.compose(stmt.scatter.compose(ar.iter_to_data.inverse())).inverse())

	artt=AccessRelation(
              name='A_I_sub_to_%s'%(data_permute.target_data_space.name),
              iter_space=mapir.full_iter_space.apply(data_permute.iter_sub_space_relation),
              data_space=data_permute.target_data_space,
              iter_to_data=iter_to_data)
	return artt

def write_create_artt(mapir,code):
	from iegen.pycloog import Statement,codegen
	print mapir.artt.iter_space

	s1=Statement(mapir.artt.iter_space)
	s2=Statement(mapir.artt.iter_space)

	print >>code,'ExplicitRelation* A_I_0_sub_to_X_0 = ExplicitRelation_ctor(1,1);'
	print >>code
	print >>code,'#define S1 ExplicitRelation_in_ordered_insert(A_I_0_sub_to_X_0,Tuple_make(t1),ER_out_given_in(inter1_ER, Tuple_make(t1)));'
	print >>code,'#define S2 ExplicitRelation_in_ordered_insert(A_I_0_sub_to_X_0,Tuple_make(t1),ER_out_given_in(inter1_ER, Tuple_make(t1)));'
	print >>code
	print >>code,codegen([s1,s2])
	print >>code
	print >>code,'#undef S1'
	print >>code,'#undef S2'
	print >>code

def calc_sigma(mapir,data_permute):
	from copy import deepcopy
	from iegen import DataSpace,IndexArray,Set,IAGPermute

	#Hard coded to return an IAG_Permute, however, other IAGs will be possible later (IAG_Group,IAG_Part,IAG_Wavefront)
	syms=mapir.symbolics()
	data_space=DataSpace(name='sigma',
	                     set=deepcopy(mapir.data_spaces['x'].set),
	                     is_index_array=True)
	result=IndexArray(data_space=data_space,
	                  is_permutation=True,
	                  input_bounds=[Set('{[k]:0<=k and k<=(N-1)}',syms)],
	                  output_bounds=Set('{[k]:0<=k and k<=(N-1)}',syms))
	return IAGPermute(name='IAG_cpack',
	                   input=mapir.artt,
	                   result=result)

def write_create_sigma(mapir,code):
	sigma=mapir.sigma
	print >>code,'RectDomain *in_domain=RD_ctor(%d,%d)'%(sigma.result.input_bounds[0].arity(),sigma.result.input_bounds[0].arity())
#	print >>code,'RD_set_lb(in_domain,0,

#---------- Public Interface Function ----------
def codegen(mapir,data_permute,iter_permute,code):
	#Step 0) Calculate the full iteration space based on the iteration spaces of the statements
	mapir.full_iter_space=full_iter_space(mapir.statements)

	#Put the full iteration space in the iter permute rtrt
#	iter_permute.iter_space=mapir.full_iter_space

	print 'Full iteration space for all statements: %s'%mapir.full_iter_space

	#Step 1a) generate an AccessRelation specification that will be the input for data reordering
	mapir.artt=calc_artt(mapir,data_permute)

	#Step 1b) generate code that creates an explicit representation of the access relation artt at runtime
	write_create_artt(mapir,code)

	#Step 1c) Generate the IAG and Index Array for sigma
	mapir.sigma=calc_sigma(mapir,data_permute)

	#Step 1d) Generate code that passes explicit relation to IAG
	write_create_sigma(mapir,code)
#-----------------------------------------------
