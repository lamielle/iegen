#Given a collection of Statement objects, calculates the combined iteration space of all statements
def calc_full_iter_space(statements):
	#Get the iteration space of the first statement
	statement=statements[0]
	full_iter=statement.iter_space.apply(statement.scatter)

	#Now union this with the rest of the statement's iteration spaces
	for statement in statements[1:]:
		full_iter=full_iter.union(statement.iter_space.apply(statement.scatter))

	return full_iter

def write_symbolics_decl(mapir,code):
	from cStringIO import StringIO
	if len(mapir.symbolics())>0:
		decl=StringIO()
		print >>decl,"int",
		for sym in mapir.symbolics():
			print >>decl,'%s=10,'%(sym.name),
		print >>code,decl.getvalue()[:-1]+';'

def write_tuple_vars_decl(set,code):
	from cStringIO import StringIO
	decl=StringIO()
	print >>decl,"int",
	for set in set.sets:
		for var in set.tuple_set.vars:
			print >>decl,var.id+',',
	print >>code,decl.getvalue()[:-1]+';'

def write_preamble(code):
	print >>code,'#include "ExplicitRelation.h"'
	print >>code
	print >>code,'int main()'
	print >>code,'{'

def write_closing(code):
	print >>code,'}'

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
	from cStringIO import StringIO
	from iegen.pycloog import Statement,codegen

	print
	print mapir.artt
	print

	iterator_name=mapir.artt.iter_space.sets[0].tuple_set.vars[0]
	print 'iterator_name=%s'%iterator_name

	#Generate the define/undefine code
	define_code=StringIO()
	statements=[]
	undefine_code=StringIO()
	for relation_index in xrange(1,len(mapir.artt.iter_to_data.relations)+1):
		relation=mapir.artt.iter_to_data.relations[relation_index-1]

		print 'artt iter_to_data relation: %s'%(str(relation))

		print >>define_code,'#define S%d ER_in_ordered_insert(%s,Tuple_make(%s),ER_out_given_in(%s, Tuple_make(%s)));'%(relation_index,mapir.artt.name,iterator_name,mapir.artt.name,iterator_name)

		statements.append(Statement(mapir.artt.iter_space))

		print >>undefine_code,'#undef S2'

	#Actually write out the code
	print >>code,'//Creation of ExplicitRelation of the ARTT'
	print >>code,'ExplicitRelation* %s = ER_ctor(%d,%d,NULL,false);'%(mapir.artt.name,mapir.artt.iter_to_data.arity_in(),mapir.artt.iter_to_data.arity_out())
	print >>code
	print >>code,define_code.getvalue()
	write_tuple_vars_decl(mapir.artt.iter_space,code)
	print >>code,codegen(statements)
	print >>code
	print >>code,undefine_code.getvalue()

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
	print >>code,'RectDomain *in_domain=RD_ctor(%d);'%(sigma.result.input_bounds[0].arity())
#	print >>code,'RD_set_lb(in_domain,0,

#---------- Public Interface Function ----------
def codegen(mapir,data_permute,iter_permute,code):
	#Step 0) Calculate the full iteration space based on the iteration spaces of the statements
	mapir.full_iter_space=calc_full_iter_space(mapir.statements)

	#Put the full iteration space in the iter permute rtrt
#	iter_permute.iter_space=mapir.full_iter_space

	print 'Full iteration space for all statements: %s'%mapir.full_iter_space

	write_preamble(code)
	write_symbolics_decl(mapir,code)

	#Step 1a) generate an AccessRelation specification that will be the input for data reordering
	mapir.artt=calc_artt(mapir,data_permute)

	#Step 1b) generate code that creates an explicit representation of the access relation artt at runtime
	write_create_artt(mapir,code)

	#Step 1c) Generate the IAG and Index Array for sigma
	mapir.sigma=calc_sigma(mapir,data_permute)

	#Step 1d) Generate code that passes explicit relation to IAG
	write_create_sigma(mapir,code)

	write_closing(code)
#-----------------------------------------------
