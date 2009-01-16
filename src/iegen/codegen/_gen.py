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

#def gen_symbolics_decl(mapir):
#	from iegen.codegen import VarDecl
#
#	var_decl=VarDecl('int')
#	for sym in mapir.get_symbolics():
#		var_decl.var_names.append(sym)
#		var_decl.values.append('10')
#	return [var_decl]
#
#def gen_tuple_vars_decl(set):
#	from iegen.codegen import VarDecl
#
#	var_decl=VarDecl('int')
#	for set in set.sets:
#		for var in set.tuple_set.vars:
#			var_decl.var_names.append(var.id)
#	return [var_decl]
#
#def gen_declare_index_array_wrappers(mapir):
#	from iegen.codegen import Comment,VarDecl
#
#	#Declare the index array wrappers
#	decls=[]
#	decls.append(Comment('Declare the index array wrappers'))
#	er_vars=VarDecl('ExplicitRelation')
#	for index_array in mapir.get_index_arrays():
#		er_vars.var_names.append('*%s_ER'%(index_array.name))
#	decls.append(er_vars)
#
#	return decls
#
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
#
#def gen_declare_sigma_er():
#	from iegen.codegen import Comment,VarDecl
#
#	#Declare a sigma_ER variable
#	stmts=[]
#	stmts.append(Comment('Declare sigma_ER'))
#	stmts.append(VarDecl('ExplicitRelation',['*sigma_ER'],['*sigma']))
#
#	return stmts
#
#def gen_rect_domain(name,set):
#	from iegen.codegen import Statement,Comment
#
#	stmts=[]
#	stmts.append(Comment('RectDomain for set %s'%(set)))
#
#	stmts.append(Statement('RectDomain *%s=RD_ctor(%d);'%(name,set.arity())))
#
#	for var in set.sets[0].tuple_set.vars:
#		stmts.append(Statement('RD_set_lb(%s,0,%s);'%(name,calc_lower_bound_string(set.lower_bound(var.id)))))
#		stmts.append(Statement('RD_set_ub(%s,0,%s);'%(name,calc_upper_bound_string(set.upper_bound(var.id)))))
#
#	return stmts
#
#def gen_create_artt(mapir):
#	import iegen.pycloog as pycloog
#	from iegen.pycloog import codegen
#	from iegen.codegen import Statement,Comment
#
#	var_in_name=mapir.artt.iter_to_data.relations[0].tuple_in.vars[0].id
#	var_out_name=mapir.artt.iter_to_data.relations[0].tuple_out.vars[0].id
#
#	#Generate the define/undefine statements
#	cloog_stmts=[]
#	define_stmts=[]
#	undefine_stmts=[]
#	for relation_index in xrange(1,len(mapir.artt.iter_to_data.relations)+1):
#		relation=mapir.artt.iter_to_data.relations[relation_index-1]
#
#		#Get the value to insert
#		value=calc_equality_value(var_out_name,relation)
#
#		define_stmts.append(Statement('#define S%d ER_in_ordered_insert(%s,Tuple_make(%s),Tuple_make(%s));'%(relation_index,mapir.artt.name,var_in_name,value)))
#
#		cloog_stmts.append(pycloog.Statement(mapir.artt.iter_space))
#		undefine_stmts.append(Statement('#undef S%d'%(relation_index,)))
#
#	#Generate the whole set of statements
#	stmts=[]
#	in_domain_name='in_domain_%s'%(mapir.artt.name)
#	stmts.extend(gen_rect_domain(in_domain_name,mapir.artt.data_array.bounds))
#	stmts.append(Statement())
#	stmts.append(Comment('Creation of ExplicitRelation of the ARTT'))
#	stmts.append(Comment(str(mapir.artt.iter_to_data)))
#	stmts.append(Statement('ExplicitRelation* %s = ER_ctor(%d,%d,%s,false);'%(mapir.artt.name,mapir.artt.iter_to_data.arity_in(),mapir.artt.iter_to_data.arity_out(),in_domain_name)))
#	stmts.append(Statement())
#	stmts.append(Comment('Define loop body statements'))
#	stmts.extend(define_stmts)
#	stmts.append(Statement())
#	stmts.extend(gen_tuple_vars_decl(mapir.artt.iter_space))
#	loop_stmts=codegen(cloog_stmts).split('\n')
#	for loop_stmt in loop_stmts:
#		stmts.append(Statement(loop_stmt))
#	stmts.append(Statement())
#	stmts.append(Comment('Undefine loop body statements'))
#	stmts.extend(undefine_stmts)
#	return stmts
#
#def gen_create_sigma(mapir):
#	from iegen.codegen import Statement,Comment
#	erg=mapir.sigma.result
#
#	stmts=[]
#
#	#Create a rect domain for sigma
#	in_domain_name='in_domain_%s'%(erg.name)
#	stmts.extend(gen_rect_domain(in_domain_name,erg.input_bounds))
#	stmts.append(Statement())
#
#	stmts.append(Comment('Create sigma'))
#	stmts.append(Statement('*sigma=ER_ctor(%d,%d,%s,%s);'%(erg.input_bounds.arity(),erg.output_bounds.arity(),in_domain_name,str(erg.is_permutation).lower())))
#	stmts.append(Statement('%s=*sigma;'%(erg.name)))
#
#	stmts.append(Statement('%s(%s,%s);'%(mapir.sigma.name,mapir.sigma.input.name,erg.name)))
#
#	return stmts
#
##Generates code that does the data reordering
#def gen_reorder_data(mapir,data_reordering):
#	from iegen.codegen import Statement,Comment
#	
#	stmts=[]
#	stmts.append(Comment('Reorder the data arrays'))
#
#	for data_array in data_reordering.data_arrays:
#		stmts.append(Statement('reorderArray((unsigned char*)%s,sizeof(double),%s,%s);'%(data_array.name,calc_size_string(data_array.bounds,data_array.bounds.sets[0].tuple_set.vars[0].id),mapir.sigma.result.name)))
#
#	return stmts
#-------------------------------------------------------
