import iegen
from iegen.codegen import calc_equality_value

#Generates code for the executor
def gen_executor(mapir):
	from iegen.codegen import Function,gen_index_array
	from iegen.idg.visitor import ParamVisitor,DeclVisitor

	#Create the executor function with the necessary parameters
	executor=Function(iegen.settings.executor_name,'void',ParamVisitor().visit(mapir.idg).params)

	#Add the necessary variable declarations
	executor.body.extend(DeclVisitor(mapir).visit(mapir.idg).get_decls())

	#Generate wrappers for the index arrays
	for index_array in mapir.get_index_arrays():
		executor.body.extend(gen_index_array(index_array))

	#Generate the loop statement definitions
	executor.body.extend(gen_executor_loop_stmts(mapir))
	executor.newline()

	#Generate the loop body using CLooG
	executor.body.extend(gen_executor_loop(mapir))
	executor.newline()

	return executor

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
			ar_dict[access_relation.name]=calc_equality_value(access_relation.iter_to_data.relations[0].tuple_out.vars[0].id,access_relation.iter_to_data)

		#Gather the loop iterators
		iterators=','.join([var.id for var in statement.iter_space.sets[0].tuple_set.vars])

		stmt_string='#define S%d(%s) %s'%(i,iterators,statement.text)
		stmts.append(Statement(stmt_string%ar_dict))

	return stmts

#Generates the executor main loop
def gen_executor_loop(mapir):
	from iegen.codegen import Statement,Comment
	import iegen.pycloog as pycloog
	from iegen.pycloog import codegen

	stmts=[]
	stmts.append(Comment('The executor main loop'))

	cloog_stmts=[]
	for statement in mapir.get_statements():
		cloog_stmts.append(pycloog.Statement(statement.iter_space))
	cloog_stmts=codegen(cloog_stmts).split('\n')
	for cloog_stmt in cloog_stmts:
		stmts.append(Statement(cloog_stmt))

	return stmts
