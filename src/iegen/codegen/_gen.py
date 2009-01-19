#---------- Code Generation Phase ----------
def do_gen(mapir):
	from iegen.codegen import Program,gen_preamble,gen_inspector,gen_executor,gen_main

	#Create the program
	program=Program()
	program.preamble.extend(gen_preamble())

	#Generate the inspector
	program.functions.append(gen_inspector(mapir))

	#Generate the executor
	program.functions.append(gen_executor(mapir))

	#Generate the main code
	program.functions.append(gen_main(mapir))

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

#def gen_destroy_index_array_wrappers(mapir):
#	from iegen.codegen import Comment,Statement
#
#	#Destroy the index array wrappers
#	stmts=[]
#	stmts.append(Comment('Destroy the index array wrappers'))
#	for index_array in mapir.get_index_arrays():
#		stmts.append(Statement('ER_dtor(&%s_ER);'%(index_array.name)))
#
#	return stmts
#-------------------------------------------------------
