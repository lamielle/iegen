import iegen
from iegen.codegen import calc_equality_value

#Generates code for the executor
def gen_executor(mapir):
	from iegen.codegen import Function,gen_index_array
	from iegen.idg.visitor import ParamVisitor,DeclVisitor,OutputERVisitor

	#Create the executor function with the necessary parameters
	executor=Function(iegen.settings.executor_name,'void',ParamVisitor().visit(mapir.idg).get_params())

	#Add the necessary variable declarations
	executor.body.extend(DeclVisitor(mapir).visit(mapir.idg).get_decls())

	#Generate wrappers for the index arrays
	for index_array in mapir.get_index_arrays():
		executor.body.extend(gen_index_array(index_array))

	#Generate assignment statements for the output ERs
	executor.body.extend(OutputERVisitor(mapir).visit(mapir.idg).get_assigns())

	#Generate the loop statement definitions
	executor.body.extend(gen_executor_loop_stmts(mapir))
	executor.newline()

	#Generate the loop body using CLooG
	executor.body.extend(gen_executor_loop(mapir))
	executor.newline()

	#Generate the loop statement undefines
	executor.body.extend(gen_executor_undefs(mapir))
	executor.newline()

	return executor

#Generates the executor main loop statements
def gen_executor_loop_stmts(mapir):
	from iegen.codegen import Statement,Comment
	from iegen.util import trans_equals

	stmts=[]
	stmts.append(Comment('Define the executor main loop body statments'))
	statement_names=mapir.statements.keys()
	statement_names.sort()
	for i,statement_name in enumerate(statement_names):
		statement=mapir.statements[statement_name]
		for comment_line in statement.text.split('\n'):
			stmts.append(Comment(comment_line))
		ar_dict={}
		for access_relation in statement.get_access_relations():
			iegen.print_detail('Generating code for access relation %s'%(access_relation.name))
			stmts.append(Comment('%s: %s'%(access_relation.name,access_relation.iter_to_data)))
			ar_dict[access_relation.name]=calc_equality_value(access_relation.iter_to_data.tuple_out[0],access_relation.iter_to_data,mapir)

		#Gather the loop iterators
		if statement.sparse_sched is None:
			iterators=','.join(statement.iter_space.tuple_set)
		else:
			iterators=','.join(statement.iter_space.tuple_set[:-1])

		#If there are any UFS constraints, wrap the statement text in a guard
		statement_text=statement.text
		ufs_constraints=statement.iter_space.ufs_constraints()

		#Make sure there is only a single conjunction in the iteration space
		if len(ufs_constraints)!=1:
			raise ValueError('Iteration space has multiple conjunctions')

		#Check if we need to generate a sparse loop
		if statement.sparse_sched is not None:
			sparse_sched_name=statement.sparse_sched
			sparse_sched_er=mapir.er_specs[sparse_sched_name]

			iter_name=statement.iter_space.tuple_set[-1]
			outer_iter_name=statement.iter_space.tuple_set[-2]

			sparse_loop='''for(%s=%s(*%s,%s);\
    %s!=%s(*%s,%s);\
    %s=%s(*%s,%s))'''%(iter_name,sparse_sched_er.get_begin_iter(),sparse_sched_name,outer_iter_name,iter_name,sparse_sched_er.get_end_iter(),sparse_sched_name,outer_iter_name,iter_name,sparse_sched_er.get_next_iter(),sparse_sched_name,outer_iter_name)

			statement_text='''%s{\
%s\
}'''%(sparse_loop,statement_text)

		#Check if there are any UFS constraints that we need to generate guards for
		elif len(ufs_constraints[0])>0:
			ufs_constraints_strs=[trans_equals(str(constraint.value_string(function_name_map=mapir.ufs_name_map()))) for constraint in ufs_constraints[0]]
			statement_text='if(%s){%s}'%(' && '.join(ufs_constraints_strs),statement_text)

		stmt_string='#define S%d(%s) %s'%(i,iterators,statement_text)
		stmt_string=stmt_string.replace('\n','\\\n')
		stmts.append(Statement(stmt_string%ar_dict))

		stmts.append(Statement())

	return stmts

#Generates the executor main loop
def gen_executor_loop(mapir):
	from iegen import Set,Relation
	from iegen.codegen import Statement,Comment
	import iegen.pycloog as pycloog
	from iegen.pycloog import codegen

	stmts=[]
	stmts.append(Comment('The executor main loop'))

	statement_names=mapir.statements.keys()
	statement_names.sort()

	#True if any statement has a sparse schedule
	sparse_loop=any((mapir.statements[statement_name].sparse_sched is not None for statement_name in statement_names))

	cloog_stmts=[]
	for statement_name in statement_names:
		statement=mapir.statements[statement_name]

		#Approximate any iterators that are equal to a UFS using know range bounds
		cloog_iter_space=statement.iter_space.approximate(mapir.ufs_range_dict())

		#Use approximate with empty sets to remove any UFS equalities in the scattering function
		scatter_fnames=statement.scatter.function_names
		empty_sets=[Set('{[a]}')]*len(scatter_fnames)
		empty_sets_ufs_map=dict(zip(scatter_fnames,empty_sets))
		cloog_scatter=statement.scatter.approximate(empty_sets_ufs_map)

		#Calculate iteration space reduction relations
		orig_iters=','.join(cloog_iter_space.tuple_set)
		reduce_iters=','.join(cloog_iter_space.tuple_set[:-1])
		reduce_iter_space=Relation('{[%s]->[%s]}'%(reduce_iters,orig_iters)).inverse()

		orig_full_iters=','.join(cloog_scatter.tuple_out)
		reduce_full_iters=','.join(cloog_scatter.tuple_out[:-2])
		reduce_full_iter_space=Relation('{[%s]->[%s]}'%(reduce_full_iters,orig_full_iters)).inverse()

		#If the statement has a sparse schedule, reduce the dimensionality of the iteration space and scattering function
		if statement.sparse_sched is not None:
			cloog_iter_space=cloog_iter_space.apply(reduce_iter_space)
			cloog_scatter=reduce_full_iter_space.compose(cloog_scatter)
			cloog_scatter=reduce_iter_space.compose(cloog_scatter.inverse()).inverse()
		elif statement.sparse_sched is None and sparse_loop:
			cloog_scatter=reduce_full_iter_space.compose(cloog_scatter)

		#Create the statement to pass to CLooG using the modified iteration space and scattering function
		cloog_stmts.append(pycloog.Statement(cloog_iter_space,cloog_scatter))

	#Run CLooG, get the result string from CLooG's codegen
	cloog_gen_str=codegen(cloog_stmts)

	#Split the generated code at newlines
	cloog_stmts=cloog_gen_str.split('\n')

	#Create Statement objects for each line of the code generated by CLooG
	for cloog_stmt in cloog_stmts:
		stmts.append(Statement(cloog_stmt))

	return stmts

#Generates the loop statement undefines
def gen_executor_undefs(mapir):
	from iegen.codegen import Statement,Comment

	stmts=[]

	stmts.append(Comment('Undefine the executor main loop body statments'))

	for i in xrange(len(mapir.get_statements())):
		stmts.append(Statement('#undef S%d'%(i,)))

	return stmts
