#---------- Utility functions ----------
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

def get_ie_arg_names_string(mapir):
	from cStringIO import StringIO

	arg_names_string=StringIO()
	for arg in mapir.ie_args:
		for var_name in arg.var_names:
			if '**'==arg.type[-2:]:
				arg_names_string.write('&%s,'%(var_name))
			else:
				arg_names_string.write('%s,'%(var_name))
	return arg_names_string.getvalue()[:-1]
#---------------------------------------

#---------- Calculation Phase Functions ----------
#Given a collection of Statement objects, calculates the combined iteration space of all statements
def calc_full_iter_space(statements):
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

def calc_ie_args(mapir):
	from iegen.codegen import VarDecl
	args=[]

	#Data spaces
	data_space_vars=VarDecl('double *')
	for data_space in mapir.pure_data_spaces():
		data_space_vars.var_names.append(data_space.name)
	args.append(data_space_vars)

	#Index arrays
	index_array_vars=VarDecl('int *')
	for index_array in mapir.index_arrays:
		index_array_vars.var_names.append(index_array.data_space.name)
	args.append(index_array_vars)

	#Symbolics
	symbolic_vars=VarDecl('int ')
	for symbolic in mapir.symbolics():
		symbolic_vars.var_names.append(symbolic.name)
	args.append(symbolic_vars)

	#Sigma/delta
	args.append(VarDecl('ExplicitRelation **',['delta','sigma']))

	return args
#-------------------------------------------------

#---------- Code Generation Phase Functions ----------
def gen_symbolics_decl(mapir):
	from iegen.codegen import VarDecl

	var_decl=VarDecl('int')
	for sym in mapir.symbolics():
		var_decl.var_names.append(sym)
		var_decl.values.append('10')
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
	from iegen.codegen import Function,Statement,VarDecl,Comment

	#Create the main function
	main=Function('main','int',[])

	#Add a declaration of the symbolic variables
	main.body.append(Comment('Declare the symbolics'))
	main.body.extend(gen_symbolics_decl(mapir))
	main.body.append(Statement())

	#Add declarations for the non-index array data spaces
	main.body.append(Comment('Declare the data spaces'))
	data_space_vars=VarDecl('double');
	for data_space in mapir.pure_data_spaces():
		data_space_vars.var_names.append('*'+data_space.name)
		data_space_vars.values.append('NULL');
	main.body.append(data_space_vars);
	main.body.append(Statement())

	#Add declarations of the index arrays
	main.body.append(Comment('Declare the index arrays'))
	index_array_vars=VarDecl('int')
	for index_array in mapir.index_arrays:
		index_array_vars.var_names.append('*'+index_array.data_space.name)
		index_array_vars.values.append('NULL')
	main.body.append(index_array_vars)
	main.body.append(Statement())

	#Add declarations of sigma and delta
	main.body.append(Comment('Declare pointers for sigma and delta'))
	er_vars=VarDecl('ExplicitRelation')
	er_vars.var_names.append('*sigma')
	er_vars.values.append('NULL')
	er_vars.var_names.append('*delta')
	er_vars.values.append('NULL')
	main.body.append(er_vars)
	main.body.append(Statement())

	#Allocate memory for the data spaces
	main.body.append(Comment('Allocate memory for the data spaces'))
	for data_space in mapir.pure_data_spaces():
		main.body.append(Statement('%s=(double*)malloc(sizeof(double)*10);'%data_space.name))
	main.body.append(Statement())

	#Allocate memory for the index arrays
	main.body.append(Comment('Allocate memory for the index arrays'))
	for index_array in mapir.index_arrays:
		main.body.append(Statement('%s=(int*)malloc(sizeof(int)*10);'%(index_array.data_space.name)))
	main.body.append(Statement())

	#Set index arrays to be 'identity' index arrays
	main.body.append(Comment("Set index arrays to be 'identity' index arrays"))
	for index_array in mapir.index_arrays:
		main.body.append(Statement('for(int i=0;i<10;i++) %s[i]=i;'%(index_array.data_space.name)))
	main.body.append(Statement())

	#Call the inspector
	main.body.append(Comment('Call the inspector'))
	main.body.append(Statement('inspector(%s);'%(get_ie_arg_names_string(mapir))))
	main.body.append(Statement())

	#Call the executor
	main.body.append(Comment('Call the executor'))
	main.body.append(Statement('executor(%s);'%(get_ie_arg_names_string(mapir))))
	main.body.append(Statement())

	#Free the data space memory
	main.body.append(Comment('Free the data space memory'))
	for data_space in mapir.pure_data_spaces():
		main.body.append(Statement('free(%s);'%data_space.name))
	main.body.append(Statement())

	#Free the data space memory
	main.body.append(Comment('Free the index array memory'))
	for index_array in mapir.index_arrays:
		main.body.append(Statement('free(%s);'%index_array.data_space.name))
	main.body.append(Statement())

	main.body.append(Statement('return 0;'))

	return main

def gen_create_artt(mapir):
	from cStringIO import StringIO
	import iegen.pycloog as pycloog
	from iegen.pycloog import codegen
	from iegen.codegen import Statement,Comment

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
	stmts.append(Comment('Creation of ExplicitRelation of the ARTT'))
	stmts.append(Comment(str(mapir.artt.iter_to_data)))
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
	                     #TODO: FIX this so 'x' is not hardcoded
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

#Generates code for the inspector
def gen_inspector(mapir):
	from iegen.codegen import Function,VarDecl

	inspector=Function('inspector','void',mapir.ie_args)

	#Add declarations of the index array wrappers
	er_vars=VarDecl('ExplicitRelation')
	for index_array in mapir.index_arrays:
		er_vars.var_names.append('*'+index_array.data_space.name+'_ER')
	inspector.body.append(er_vars)

	#Step 1a) generate code that creates an explicit representation of the access relation artt at runtime
	inspector.body.extend(gen_create_artt(mapir))

	#Step 1b) Generate code that passes explicit relation to IAG
	inspector.body.extend(gen_create_sigma(mapir))
	return inspector
	return arg_names_string.getvalue()[:-1]

#Generates code for the executor
def gen_executor(mapir):
	from iegen.codegen import Function

	executor=Function('executor','void',mapir.ie_args)
	return executor
#-----------------------------------------------------

#---------- Public Interface Function ----------
def codegen(mapir,data_permute,iter_permute,code):
	from iegen.codegen import Program
	from iegen.codegen.visitor import CPrintVisitor

	#---------- Calculation Phase ----------
	#Step 1) Calculate the full iteration space based on the iteration spaces of the statements
	mapir.full_iter_space=calc_full_iter_space(mapir.statements)

	#Step 2) generate an AccessRelation specification that will be the input for data reordering
	mapir.artt=calc_artt(mapir,data_permute)

	#Step 3) Generate the IAG and Index Array for sigma
	mapir.sigma=calc_sigma(mapir,data_permute)

	#Step 4) Modify data dependences, scattering functions, and access functions based on previous transformation.
	#TODO: Do this step

	#Step 5) Determine the parameters for the inspector and executor functions
	mapir.ie_args=calc_ie_args(mapir)

	#Put the full iteration space in the iter permute rtrt
#	iter_permute.iter_space=mapir.full_iter_space
	#---------------------------------------

	#---------- Code Generation Phase ----------
	#Create the program
	program=Program()
	program.preamble.extend(gen_preamble())

	#Generate the inspector
	program.functions.append(gen_inspector(mapir))

	#Generate the executor
	program.functions.append(gen_executor(mapir))

	#Generate the main driver code
	program.functions.append(gen_main_driver(mapir))

	#Pretty print the generated program structure
	CPrintVisitor(code,'  ').visit(program)
	#-------------------------------------------
#-----------------------------------------------
