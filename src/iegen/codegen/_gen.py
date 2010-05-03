#---------- Code Generation Phase ----------
def do_gen(mapir):
	import iegen
	from iegen.codegen import Program,gen_preamble,gen_inspector,gen_executor,gen_main

	iegen.print_progress('Starting the code generation phase...')

	program=Program()

	#Create the program
	if iegen.settings.gen_preamble:
		iegen.print_progress('Generating the preamble...')
		program.preamble.extend(gen_preamble())

	#Generate the inspector
	iegen.print_progress('Generating the inspector...')
	program.functions.append(gen_inspector(mapir))

	#Generate the executor
	iegen.print_progress('Generating the executor...')
	program.functions.append(gen_executor(mapir))

	#Generate the main code
	if iegen.settings.gen_main:
		iegen.print_progress('Generating main()...')
		program.functions.append(gen_main(mapir))

	iegen.print_progress('Code generation phase completed...')

	return program
#-------------------------------------------

#---------- Utility code generation functions ----------
def gen_preamble():
	from iegen.codegen import Statement,Comment
	stmts=[]
	stmts.append(Comment('To compile, run the following command from the root of the iegen source tree:'))
	stmts.append(Comment('g++ test.c -g src/dev/ExplicitRelation.c src/dev/RectDomain.c src/dev/util.c src/dev/ERG_cpack.c -o test -I./src/dev'))
	stmts.append(Statement('#include "ExplicitRelation.h"'))
	stmts.append(Statement('#include "ERG.h"'))
	stmts.append(Statement('#include "util.h"'))
	stmts.append(Statement())
	stmts.append(Statement("#define max(a,b) (((a)>(b))?(a):(b))"))
	stmts.append(Statement("#define min(a,b) (((a)<(b))?(a):(b))"))
	stmts.append(Statement())
	return stmts

#The raw data of an index array will be passed in to the inspector
#However, we need the index array to look like an Explicit Relation
#Therefore, for all index arrays, we create a wrapper ER
def gen_index_array(index_array):
	from iegen.codegen import Statement,Comment,calc_size_string

	input_bounds=index_array.input_bounds

	#Calculate the size of this index array
	#Assumes only one set in the union...
	if 1!=len(input_bounds): raise ValueError("IndexArray's input bounds have multiple terms in the disjunction")
	#Assumes the index array dataspace is 1D...
	if 1!=input_bounds.arity(): raise ValueError("IndexArray's dataspace does not have arity 1")

	#Get the single tuple variable's name
	var_name=input_bounds.tuple_set[0]

	#Get the string that calculates the size of the ER at runtime
	size_string=calc_size_string(input_bounds,var_name)

	stmts=[]
	stmts.append(Comment('Wrapping index array %s'%(index_array.name)))
	stmts.append(Statement('%s=%s(%s,%s);'%(index_array.get_var_name(),index_array.get_ctor_str(),index_array.get_param_name(),size_string)))
	stmts.append(Statement())

	return stmts

def gen_tuple_vars_decl(set):
	from iegen.codegen import VarDecl

	var_decl=VarDecl('int')
	var_decl.var_names.extend(set.tuple_set)

	return [var_decl]
#-------------------------------------------------------
