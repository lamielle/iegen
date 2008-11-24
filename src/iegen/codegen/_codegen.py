#---------- Utility functions ----------
def get_bound_string(bounds,func):
	from cStringIO import StringIO

	bound_string=StringIO()
	for i in xrange(len(bounds)):
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

#Calculates the difference of the upper and lower bounds of the given variable in the given set
def get_size_string(set,var_name):
	#Get the upper/lower bounds for the variable
	upper_bounds=set.upper_bound(var_name)
	lower_bounds=set.lower_bound(var_name)

	#Get the string that calculates the size of the ER at runtime
	return '%s-%s'%(get_upper_bound_string(upper_bounds),get_lower_bound_string(lower_bounds))

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

def get_equality_value(var_name,formula):
	from iegen.ast.visitor import FindConstraintVisitor,ValueStringVisitor
	from iegen.ast import Equality,NormExp

	values=FindConstraintVisitor(Equality,var_name).visit(formula).var_constraints

	if 0==len(values): raise ValueError("Tuple variable '%s' is not involved in any equality constraints"%(var_name))
	if len(values)>1: raise ValueError("Tuple variable '%s' is equal to multiple values"%(var_name))

	value=values[0]

	var=value[0]
	exp=value[1].exp

	if var.coeff>0:
		var=NormExp([],-1)*NormExp([var],0)
		exp=NormExp([],-1)*exp
	else:
		var=NormExp([var],0)

	value=exp-var

	return ValueStringVisitor().visit(value).value
#---------------------------------------

#---------- Calculation Phase Functions ----------
#Given a collection of Statement objects, calculates the combined iteration space of all statements
def calc_full_iter_space(statements):
	full_iter=None
	for statement in statements:
		if None is full_iter:
			full_iter=statement.iter_space.apply(statement.scatter)
		else:
			full_iter=full_iter.union(statement.iter_space.apply(statement.scatter))

	return full_iter

def calc_ie_args(mapir):
	from iegen.codegen import VarDecl
	args=[]

	#Data spaces
	data_array_vars=VarDecl('double *')
	for data_array in mapir.get_data_arrays():
		data_array_vars.var_names.append(data_array.name)
	args.append(data_array_vars)

	#Index arrays
	index_array_vars=VarDecl('int *')
	for index_array in mapir.get_index_arrays():
		index_array_vars.var_names.append(index_array.name)
	args.append(index_array_vars)

	#Symbolics
	symbolic_vars=VarDecl('int ')
	for symbolic in mapir.get_symbolics():
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
	for sym in mapir.get_symbolics():
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
	from iegen.codegen import Statement,Comment
	stmts=[]
	stmts.append(Comment('To compile, run the following command from the root of the iegen source tree:'))
	stmts.append(Comment('g++ test.c -g src/dev/ExplicitRelation.c src/dev/RectDomain.c src/dev/util.c src/dev/IAG_cpack.c -o test -I./src/dev'))
	stmts.append(Statement('#include "ExplicitRelation.h"'))
	stmts.append(Statement('#include "IAG.h"'))
	stmts.append(Statement('#include "util.h"'))
	stmts.append(Statement())
	stmts.append(Statement("#define max(a,b) (((a)>(b))?(a):(b))"))
	stmts.append(Statement("#define min(a,b) (((a)<(b))?(a):(b))"))
	stmts.append(Statement())
	return stmts

def gen_declare_index_array_wrappers(mapir):
	from iegen.codegen import Comment,VarDecl

	#Declare the index array wrappers
	decls=[]
	decls.append(Comment('Declare the index array wrappers'))
	er_vars=VarDecl('ExplicitRelation')
	for index_array in mapir.get_index_arrays():
		er_vars.var_names.append('*%s_ER'%(index_array.name))
	decls.append(er_vars)

	return decls

def gen_create_index_array_wrappers(mapir):
	from iegen.codegen import Comment,Statement

	#Create the index array wrappers
	stmts=[]
	stmts.append(Comment('Create the index array wrappers'))
	for index_array in mapir.get_index_arrays():
		data_array_set=index_array.input_bounds
		#Calculate the size of this index array
		#Assumes only one set in the union...
		if 1!=len(data_array_set.sets): raise ValueError("IndexArray's dataspace has multiple terms in the disjunction")
		#Assumes the index array dataspace is 1D...
		if 1!=data_array_set.sets[0].arity(): raise ValueError("IndexArray's dataspace does not have arity 1")

		#Get the single tuple variable
		var=data_array_set.sets[0].tuple_set.vars[0]

		#Get the string that calculates the size of the ER at runtime
		size_string=get_size_string(data_array_set,var.id)

		#Append the construction of the wrapper the the collection of statements
		stmts.append(Statement('%s_ER=ER_ctor(%s,%s);'%(index_array.name,index_array.name,size_string)))

		#TODO: What was this for?
		#get_lower_bound_string

	return stmts

def gen_destroy_index_array_wrappers(mapir):
	from iegen.codegen import Comment,Statement

	#Destroy the index array wrappers
	stmts=[]
	stmts.append(Comment('Destroy the index array wrappers'))
	for index_array in mapir.get_index_arrays():
		stmts.append(Statement('ER_dtor(&%s_ER);'%(index_array.name)))

	return stmts

def gen_declare_sigma_er():
	from iegen.codegen import Comment,VarDecl

	#Declare a sigma_ER variable
	stmts=[]
	stmts.append(Comment('Declare sigma_ER'))
	stmts.append(VarDecl('ExplicitRelation',['*sigma_ER'],['*sigma']))

	return stmts

def gen_main_driver(mapir):
	from iegen.codegen import Function,Statement,VarDecl,Comment

	#Create the main function
	main=Function('main','int',[])

	#Add a declaration of the symbolic variables
	main.body.append(Comment('Declare the symbolics'))
	main.body.extend(gen_symbolics_decl(mapir))
	main.newline()

	#Add declarations for the non-index array data spaces
	main.body.append(Comment('Declare the data spaces'))
	data_array_vars=VarDecl('double');
	for data_array in mapir.get_data_arrays():
		data_array_vars.var_names.append('*'+data_array.name)
		data_array_vars.values.append('NULL');
	main.body.append(data_array_vars);
	main.newline()

	#Add declarations of the index arrays
	main.body.append(Comment('Declare the index arrays'))
	index_array_vars=VarDecl('int')
	for index_array in mapir.get_index_arrays():
		index_array_vars.var_names.append('*'+index_array.name)
		index_array_vars.values.append('NULL')
	main.body.append(index_array_vars)
	main.newline()

	#Add declarations of sigma and delta
	main.body.append(Comment('Declare pointers for sigma and delta'))
	er_vars=VarDecl('ExplicitRelation')
	er_vars.var_names.append('*sigma')
	er_vars.values.append('NULL')
	er_vars.var_names.append('*delta')
	er_vars.values.append('NULL')
	main.body.append(er_vars)
	main.newline()

	#Allocate memory for the data spaces
	main.body.append(Comment('Allocate memory for the data spaces'))
	for data_array in mapir.get_data_arrays():
		main.body.append(Statement('%s=(double*)malloc(sizeof(double)*10);'%data_array.name))
	main.newline()

	#Allocate memory for the index arrays
	main.body.append(Comment('Allocate memory for the index arrays'))
	for index_array in mapir.get_index_arrays():
		main.body.append(Statement('%s=(int*)malloc(sizeof(int)*10);'%(index_array.name)))
	main.newline()

	#Set index arrays to be 'identity' index arrays
	main.body.append(Comment("Set index arrays to be 'identity' index arrays"))
	for index_array in mapir.get_index_arrays():
		main.body.append(Statement('for(int i=0;i<10;i++) %s[i]=i;'%(index_array.name)))
	main.newline()

	#Call the inspector
	main.body.append(Comment('Call the inspector'))
	main.body.append(Statement('inspector(%s);'%(get_ie_arg_names_string(mapir))))
	main.newline()

	#Call the executor
	main.body.append(Comment('Call the executor'))
	main.body.append(Statement('executor(%s);'%(get_ie_arg_names_string(mapir))))
	main.newline()

	#Debug printing of the data spaces
	main.body.append(Comment('Debug printing of the data arrays'))
	main.body.append(Statement('for(int i=0;i<10;i++)'))
	main.body.append(Statement('{'))
	main.body.append(Statement('  printf("inter1[%d]=%d\\n",i,inter1[1]);'))
	main.body.append(Statement('  printf("inter2[%d]=%d\\n",i,inter1[1]);'))
	main.body.append(Statement('  printf("x[%d]=%d\\n",i,inter1[1]);'))
	main.body.append(Statement('  printf("fx[%d]=%d\\n",i,inter1[1]);'))

	main.body.append(Statement('}'))
	main.body.append(Statement(''))

	#Free the data space memory
	main.body.append(Comment('Free the data space memory'))
	for data_array in mapir.get_data_arrays():
		main.body.append(Statement('free(%s);'%data_array.name))
	main.newline()

	#Free the data space memory
	main.body.append(Comment('Free the index array memory'))
	for index_array in mapir.get_index_arrays():
		main.body.append(Statement('free(%s);'%index_array.name))
	main.newline()

	main.body.append(Statement('return 0;'))

	return main

def gen_rect_domain(name,set):
	from iegen.codegen import Statement,Comment

	stmts=[]
	stmts.append(Comment('RectDomain for set %s'%(set)))

	stmts.append(Statement('RectDomain *%s=RD_ctor(%d);'%(name,set.arity())))

	for var in set.sets[0].tuple_set.vars:
		stmts.append(Statement('RD_set_lb(%s,0,%s);'%(name,get_lower_bound_string(set.lower_bound(var.id)))))
		stmts.append(Statement('RD_set_ub(%s,0,%s);'%(name,get_upper_bound_string(set.upper_bound(var.id)))))

	return stmts

def gen_create_artt(mapir):
	import iegen.pycloog as pycloog
	from iegen.pycloog import codegen
	from iegen.codegen import Statement,Comment

	var_in_name=mapir.artt.iter_to_data.relations[0].tuple_in.vars[0].id
	var_out_name=mapir.artt.iter_to_data.relations[0].tuple_out.vars[0].id

	#Generate the define/undefine statements
	cloog_stmts=[]
	define_stmts=[]
	undefine_stmts=[]
	for relation_index in xrange(1,len(mapir.artt.iter_to_data.relations)+1):
		relation=mapir.artt.iter_to_data.relations[relation_index-1]

		#Get the value to insert
		value=get_equality_value(var_out_name,relation)

		define_stmts.append(Statement('#define S%d ER_in_ordered_insert(%s,Tuple_make(%s),Tuple_make(%s));'%(relation_index,mapir.artt.name,var_in_name,value)))

		cloog_stmts.append(pycloog.Statement(mapir.artt.iter_space))
		undefine_stmts.append(Statement('#undef S%d'%(relation_index,)))

	#Generate the whole set of statements
	stmts=[]
	in_domain_name='in_domain_%s'%(mapir.artt.name)
	stmts.extend(gen_rect_domain(in_domain_name,mapir.artt.data_array.bounds))
	stmts.append(Statement())
	stmts.append(Comment('Creation of ExplicitRelation of the ARTT'))
	stmts.append(Comment(str(mapir.artt.iter_to_data)))
	stmts.append(Statement('ExplicitRelation* %s = ER_ctor(%d,%d,%s,false);'%(mapir.artt.name,mapir.artt.iter_to_data.arity_in(),mapir.artt.iter_to_data.arity_out(),in_domain_name)))
	stmts.append(Statement())
	stmts.append(Comment('Define loop body statements'))
	stmts.extend(define_stmts)
	stmts.append(Statement())
	stmts.extend(gen_tuple_vars_decl(mapir.artt.iter_space))
	loop_stmts=codegen(cloog_stmts).split('\n')
	for loop_stmt in loop_stmts:
		stmts.append(Statement(loop_stmt))
	stmts.append(Statement())
	stmts.append(Comment('Undefine loop body statements'))
	stmts.extend(undefine_stmts)
	return stmts

def gen_create_sigma(mapir):
	from iegen.codegen import Statement,Comment
	iag=mapir.sigma.result

	stmts=[]

	#Create a rect domain for sigma
	in_domain_name='in_domain_%s'%(iag.name)
	stmts.extend(gen_rect_domain(in_domain_name,iag.input_bounds))
	stmts.append(Statement())

	stmts.append(Comment('Create sigma'))
	stmts.append(Statement('*sigma=ER_ctor(%d,%d,%s,%s);'%(iag.input_bounds.arity(),iag.output_bounds.arity(),in_domain_name,str(iag.is_permutation).lower())))
	stmts.append(Statement('%s=*sigma;'%(iag.name)))

	stmts.append(Statement('%s(%s,%s);'%(mapir.sigma.name,mapir.sigma.input.name,iag.name)))

	return stmts

#Generates code that does the data reordering
def gen_reorder_data(mapir,data_reordering):
	from iegen.codegen import Statement,Comment
	
	stmts=[]
	stmts.append(Comment('Reorder the data arrays'))

	for data_array in data_reordering.data_arrays:
		stmts.append(Statement('reorderArray((unsigned char*)%s,sizeof(double),%s,%s);'%(data_array.name,get_size_string(data_array.bounds,data_array.bounds.sets[0].tuple_set.vars[0].id),mapir.sigma.result.name)))

	return stmts

#Generates code for the inspector
def gen_inspector(mapir,data_reordering):
	from iegen.codegen import Function,VarDecl,Comment,Statement

	inspector=Function('inspector','void',mapir.ie_args)

	#Create the declare/create the index array wrappers
	inspector.body.extend(gen_declare_index_array_wrappers(mapir))
	inspector.newline()
	inspector.body.extend(gen_create_index_array_wrappers(mapir))
	inspector.newline()

	#Create a sigma_ER variable
	inspector.body.extend(gen_declare_sigma_er())
	inspector.newline()

	#Step 1a) generate code that creates an explicit representation of the access relation artt at runtime
	inspector.body.extend(gen_create_artt(mapir))
	inspector.newline()

	#Step 1b) Generate code that passes explicit relation to IAG
	inspector.body.extend(gen_create_sigma(mapir))
	inspector.newline()

	#Step 1c) Generate code that does data reordering
	inspector.body.extend(gen_reorder_data(mapir,data_reordering))
	inspector.newline()

	#Destroy the index array wrappers
	inspector.body.extend(gen_destroy_index_array_wrappers(mapir))

	return inspector

#Generates the executor main loop statements
def gen_executor_loop_stmts(mapir):
	from iegen.codegen import Statement,Comment

	stmts=[]
	stmts.append(Comment('Define the executor main loop body statments'))
	for i in xrange(len(mapir.get_statements())):
		statement=mapir.get_statements()[i]
		stmts.append(Comment('%s'%(statement.text)))
		ar_dict={}
		for access_relation in statement.get_access_relations():
			stmts.append(Comment('%s: %s'%(access_relation.name,access_relation.iter_to_data)))
			ar_dict[access_relation.name]=get_equality_value(access_relation.iter_to_data.relations[0].tuple_out.vars[0].id,access_relation.iter_to_data)

		stmt_string='#define S%d %s'%(i+1,statement.text)
		stmts.append(Statement(stmt_string%ar_dict))

	return stmts

#Generates the executor main loop
def gen_executor_loop(mapir):
	from iegen.codegen import Statement,Comment
	import iegen.pycloog as pycloog
	from iegen.pycloog import codegen

	stmts=[]
	stmts.append(Comment('The executor main loop'))

	#Assumes that all statements have the same iterator variables
	stmts.extend(gen_tuple_vars_decl(mapir.get_statements()[0].iter_space));

	cloog_stmts=[]
	for statement in mapir.get_statements():
		cloog_stmts.append(pycloog.Statement(statement.iter_space))
	cloog_stmts=codegen(cloog_stmts).split('\n')
	for cloog_stmt in cloog_stmts:
		stmts.append(Statement(cloog_stmt))

	return stmts

#Generates code for the executor
def gen_executor(mapir):
	from iegen.codegen import Function

	executor=Function('executor','void',mapir.ie_args)

	#Create the declare/create the index array wrappers
	executor.body.extend(gen_declare_index_array_wrappers(mapir))
	executor.newline()
	executor.body.extend(gen_create_index_array_wrappers(mapir))
	executor.newline()

	#Create a sigma_ER variable
	executor.body.extend(gen_declare_sigma_er())
	executor.newline()

	#Generate the loop statement definitions
	executor.body.extend(gen_executor_loop_stmts(mapir))
	executor.newline()

	#Generate the loop body using CLooG
	executor.body.extend(gen_executor_loop(mapir))
	executor.newline()

	#Destroy the index array wrappers
	executor.body.extend(gen_destroy_index_array_wrappers(mapir))

	return executor
#-----------------------------------------------------

#---------- Public Interface Function ----------
def codegen(mapir,code):
	from iegen.codegen import Program
	from iegen.codegen.visitor import CPrintVisitor

	#---------- Calculation Phase ----------
	for rtrt in mapir.rtrts:
		#Calculate the full iteration space based on the current iteration spaces of the statements
		mapir.full_iter_space=calc_full_iter_space(mapir.get_statements())

		print '----- Current full iteration space: -----'
		print mapir.full_iter_space
		print '-----------------------------------------'
		print

		#Tell the RTRT to calculate the inputs that it will need at runtime
		rtrt.calc_input(mapir)

		#Tell the RTRT to calculate the outputs it will produce at runtime
		rtrt.calc_output(mapir)

		print '----- Applying transformation: -----'
		print rtrt
		print '------------------------------------'
		print

		#Tell the RTRT to update the access relations and scattering functions
		rtrt.calc_apply(mapir)

		#rtrt.calc_data_remaps()
	#---------------------------------------

	#---------- Calculation Phase ----------
	#Step 5) Determine the parameters for the inspector and executor functions
#	mapir.ie_args=calc_ie_args(mapir)
	#---------------------------------------

	#---------- Code Generation Phase ----------
	#Create the program
#	program=Program()
#	program.preamble.extend(gen_preamble())

	#Generate the inspector
#	program.functions.append(gen_inspector(mapir,mapir.rtrts[0]))

	#Generate the executor
#	program.functions.append(gen_executor(mapir))

	#Generate the main driver code
#	program.functions.append(gen_main_driver(mapir))

	#Pretty print the generated program structure
#	CPrintVisitor(code,'  ').visit(program)
	#-------------------------------------------
#-----------------------------------------------
