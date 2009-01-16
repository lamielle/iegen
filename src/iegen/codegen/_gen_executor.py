#Generates code for the executor
def gen_executor(mapir):
	from iegen.codegen import Function
	from iegen.idg.visitor import ParamVisitor

	#Create the executor function with the necessary parameters
	executor=Function('executor','void',ParamVisitor().visit(mapir.idg).params)

#	#Create the declare/create the index array wrappers
#	executor.body.extend(gen_declare_index_array_wrappers(mapir))
#	executor.newline()
#	executor.body.extend(gen_create_index_array_wrappers(mapir))
#	executor.newline()
#
#	#Create a sigma_ER variable
#	executor.body.extend(gen_declare_sigma_er())
#	executor.newline()
#
#	#Generate the loop statement definitions
#	executor.body.extend(gen_executor_loop_stmts(mapir))
#	executor.newline()
#
#	#Generate the loop body using CLooG
#	executor.body.extend(gen_executor_loop(mapir))
#	executor.newline()
#
#	#Destroy the index array wrappers
#	executor.body.extend(gen_destroy_index_array_wrappers(mapir))
#
	return executor

##Generates the executor main loop statements
#def gen_executor_loop_stmts(mapir):
#	from iegen.codegen import Statement,Comment
#
#	stmts=[]
#	stmts.append(Comment('Define the executor main loop body statments'))
#	for i in xrange(len(mapir.get_statements())):
#		statement=mapir.get_statements()[i]
#		stmts.append(Comment('%s'%(statement.text)))
#		ar_dict={}
#		for access_relation in statement.get_access_relations():
#			stmts.append(Comment('%s: %s'%(access_relation.name,access_relation.iter_to_data)))
#			ar_dict[access_relation.name]=calc_equality_value(access_relation.iter_to_data.relations[0].tuple_out.vars[0].id,access_relation.iter_to_data)
#
#		stmt_string='#define S%d %s'%(i+1,statement.text)
#		stmts.append(Statement(stmt_string%ar_dict))
#
#	return stmts
#
##Generates the executor main loop
#def gen_executor_loop(mapir):
#	from iegen.codegen import Statement,Comment
#	import iegen.pycloog as pycloog
#	from iegen.pycloog import codegen
#
#	stmts=[]
#	stmts.append(Comment('The executor main loop'))
#
#	#Assumes that all statements have the same iterator variables
#	stmts.extend(gen_tuple_vars_decl(mapir.get_statements()[0].iter_space));
#
#	cloog_stmts=[]
#	for statement in mapir.get_statements():
#		cloog_stmts.append(pycloog.Statement(statement.iter_space))
#	cloog_stmts=codegen(cloog_stmts).split('\n')
#	for cloog_stmt in cloog_stmts:
#		stmts.append(Statement(cloog_stmt))
#
#	return stmts
