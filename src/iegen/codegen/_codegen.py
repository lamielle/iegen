#Given a collection of Statement objects, calculates the combined iteration space of all statements
def calc_full_iter_space(statements):
	#Get the iteration space of the first statement
	statement=statements[0]
	full_iter=statement.iter_space.apply(statement.scatter)

	#Now union this with the rest of the statement's iteration spaces
	for statement in statements[1:]:
		full_iter=full_iter.union(statement.iter_space.apply(statement.scatter))

	return full_iter

def get_bound_string(bounds,func):
	from cStringIO import StringIO

	bound_string=StringIO()
	for i in range(len(bounds)):
		if len(bounds)-1==i:
			bound_string.write('%s'+')'*(len(bounds)-1))
		else:
			bound_string.write('max(%s,')
	return bound_string.getvalue()%tuple(bounds)

#Creates a string that is a C expression that will calculate the lower bound for a given collection of NormExps
def get_lower_bound_string(bounds):
	return get_bound_string(bounds,'min')

#Creates a string that is a C expression that will calculate the upper bound for a given collection of NormExps
def get_upper_bound_string(bounds):
	return get_bound_string(bounds,'max')

def gen_symbolics_decl(mapir):
	from iegen.codegen import VarDecl

	var_decl=VarDecl('int')
	for sym in mapir.symbolics():
		var_decl.var_names.append(sym)
	return [var_decl]

def gen_tuple_vars_decl(set):
	from iegen.codegen import VarDecl

	var_decl=VarDecl('int')
	for set in set.sets:
		for var in set.tuple_set.vars:
			var_decl.var_names.append(var.id)
	return [var_decl]

def gen_preamble():
	from iegen.codegen import Statement
	stmts=[]
	stmts.append(Statement('#include "ExplicitRelation.h"'))
	stmts.append(Statement())
	stmts.append(Statement("#define max(a,b) (((a)>(b))?(a):(b))"))
	stmts.append(Statement("#define min(a,b) (((a)<(b))?(a):(b))"))
	stmts.append(Statement())
	return stmts

def gen_main_driver(mapir):
	from iegen.codegen import Function,VarDecl
	main=Function('main','int',[])
	main.body.extend(gen_symbolics_decl(mapir))
	index_array_vars=VarDecl('int')
	for index_array in mapir.index_arrays:
		index_array_vars.var_names.append('*'+index_array.data_space.name)
	main.body.append(index_array_vars)
	er_vars=VarDecl('ExplicitRelation')
	for index_array in mapir.index_arrays:
		er_vars.var_names.append('*'+index_array.data_space.name+'_ER')
	er_vars.var_names.append('*sigma')
	er_vars.var_names.append('*delta')
	main.body.append(er_vars)
	return main

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

def calc_ie_args(mapir):
	args=[]
	for data_space in mapir.data_spaces.values():
		if not data_space.is_index_array:
			args.append('double *'+data_space.name)
	for index_array in mapir.index_arrays:
		args.append('ExplicitRelation *'+index_array.data_space.name)
	for symbolic in mapir.symbolics():
		args.append('int '+symbolic.name)
	args.append('ExplicitRelation **sigma')
	args.append('ExplicitRelation **delta')
	return args

def gen_create_artt(mapir):
	from cStringIO import StringIO
	import iegen.pycloog as pycloog
	from iegen.pycloog import codegen
	from iegen.codegen import Statement

	iterator_name=mapir.artt.iter_space.sets[0].tuple_set.vars[0]

	#Generate the define/undefine statements
	cloog_stmts=[]
	define_stmts=[]
	undefine_stmts=[]
	for relation_index in xrange(1,len(mapir.artt.iter_to_data.relations)+1):
		relation=mapir.artt.iter_to_data.relations[relation_index-1]

		define_stmts.append(Statement('#define S%d ER_in_ordered_insert(%s,Tuple_make(%s),ER_out_given_in(%s, Tuple_make(%s)));'%(relation_index,mapir.artt.name,iterator_name,mapir.artt.name,iterator_name)))

		cloog_stmts.append(pycloog.Statement(mapir.artt.iter_space)) 
		undefine_stmts.append(Statement('#undef S%d'%(relation_index,)))

	#Generate the whole set of statements
	stmts=[]
	stmts.append(Statement('//Creation of ExplicitRelation of the ARTT'))
	stmts.append(Statement('//'+str(mapir.artt.iter_to_data)))
	stmts.append(Statement('ExplicitRelation* %s = ER_ctor(%d,%d,NULL,false);'%(mapir.artt.name,mapir.artt.iter_to_data.arity_in(),mapir.artt.iter_to_data.arity_out())))
	stmts.append(Statement())
	stmts.extend(define_stmts)
	stmts.extend(gen_tuple_vars_decl(mapir.artt.iter_space))
	loop_stmts=codegen(cloog_stmts).split('\n')
	for loop_stmt in loop_stmts:
		stmts.append(Statement(loop_stmt))
	stmts.append(Statement())
	stmts.extend(undefine_stmts)
	stmts.append(Statement())
	return stmts

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
	                  input_bounds=Set('{[k]:0<=k and k<=(N-1)}',syms),
	                  output_bounds=Set('{[k]:0<=k and k<=(N-1)}',syms))
	return IAGPermute(name='IAG_cpack',
	                   input=mapir.artt,
	                   result=result)

def gen_create_sigma(mapir):
	from iegen.codegen import Statement
	iag=mapir.sigma.result

	stmts=[]
	stmts.append(Statement('RectDomain *in_domain=RD_ctor(%d);'%(iag.input_bounds.arity())))

	for var in iag.input_bounds.sets[0].tuple_set.vars:
		stmts.append(Statement('RD_set_lb(in_domain,0,%s);'%get_lower_bound_string(iag.input_bounds.lower_bound(var.id))))
		stmts.append(Statement('RD_set_ub(in_domain,0,%s);'%get_upper_bound_string(iag.input_bounds.upper_bound(var.id))))
	return stmts

#---------- Public Interface Function ----------
def codegen(mapir,data_permute,iter_permute,code):
	from iegen.codegen import Program,Function
	from iegen.codegen.visitor import CPrintVisitor

	#Step 0) Calculate the full iteration space based on the iteration spaces of the statements
	mapir.full_iter_space=calc_full_iter_space(mapir.statements)

	#Put the full iteration space in the iter permute rtrt
#	iter_permute.iter_space=mapir.full_iter_space

	program=Program()
	program.preamble.extend(gen_preamble())
	program.functions.append(gen_main_driver(mapir))

	#Step 1a) generate an AccessRelation specification that will be the input for data reordering
	mapir.artt=calc_artt(mapir,data_permute)

	#Step 1b) generate code that creates an explicit representation of the access relation artt at runtime
	ie_args=calc_ie_args(mapir)
	inspector=Function('inspector','void',ie_args)

	inspector.body.extend(gen_create_artt(mapir))

	#Step 1c) Generate the IAG and Index Array for sigma
	mapir.sigma=calc_sigma(mapir,data_permute)

	#Step 1d) Generate code that passes explicit relation to IAG
	inspector.body.extend(gen_create_sigma(mapir))

	executor=Function('executor','void',ie_args)

	program.functions.append(inspector)
	program.functions.append(executor)

	CPrintVisitor(code,'  ').visit(program)
#-----------------------------------------------
