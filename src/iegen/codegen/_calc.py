#---------- Calculation Phase ----------
def do_calc(mapir):

	from iegen.codegen import calc_full_iter_space,calc_inspector_params,calc_executor_params

	#Do calculations for each reordering
	for transformation in mapir.transformations:
		#Calculate the full iteration space based on the current iteration spaces of the statements
		mapir.full_iter_space=calc_full_iter_space(mapir.get_statements())

		print '----- Current full iteration space: -----'
		print mapir.full_iter_space
		print '-----------------------------------------'
		print

		#Tell the RTRT to calculate the inputs that it will need at runtime
		transformation.calc_input(mapir)

		#Tell the RTRT to calculate the outputs it will produce at runtime
		transformation.calc_output(mapir)

		print '----- Applying transformation: -----'
		print transformation
		print '------------------------------------'
		print

		#Tell the RTRT to update the access relations and scattering functions
		transformation.calc_apply(mapir)

		#transformation.calc_data_remaps()

	#Calculate the parameters for the inspector and executor functions
	mapir.inspector_params=calc_inspector_params(mapir)
	mapir.executor_params=calc_executor_params(mapir)
#---------------------------------------

#---------- Utility calculation functions ----------
#Given a collection of Statement objects, calculates the combined iteration space of all statements
#Assumes that at least one statement is given
def calc_full_iter_space(statements):
	full_iter=statements[0].iter_space.apply(statements[0].scatter)
	for statement in statements[1:]:
		full_iter=full_iter.union(statement.iter_space.apply(statement.scatter))
	return full_iter

#Calculates the parameters needed for the inspector function
def calc_inspector_params(mapir):
	from iegen.codegen import Parameter

	params=[]

	#Data Arrays (assumed to contain double data)
	for data_array in mapir.get_data_arrays():
		params.append(Parameter('double *',data_array.name))

	#Index arrays (assumed to contain integers)
	for index_array in mapir.get_index_arrays():
		params.append(Parameter('int *',index_array.name))

	#Symbolic variables (assumed to be integers)
	for symbolic in mapir.get_symbolics():
		params.append(Parameter('int',symbolic.name))

	#Transformation outputs
	for transformation in mapir.transformations:
		for output in transformation.outputs:
			params.append(Parameter('ExplicitRelation *',output.name))

	return params

#Calculates the parameters needed for the executor function
def calc_executor_params(mapir):
	return calc_inspector_params(mapir)

#def calc_ie_args(mapir):
#	from iegen.codegen import VarDecl
#	args=[]
#
#	#Data spaces
#	data_array_vars=VarDecl('double *')
#	for data_array in mapir.get_data_arrays():
#		data_array_vars.var_names.append(data_array.name)
#	args.append(data_array_vars)
#
#	#Index arrays
#	index_array_vars=VarDecl('int *')
#	for index_array in mapir.get_index_arrays():
#		index_array_vars.var_names.append(index_array.name)
#	args.append(index_array_vars)
#
#	#Symbolics
#	symbolic_vars=VarDecl('int ')
#	for symbolic in mapir.get_symbolics():
#		symbolic_vars.var_names.append(symbolic.name)
#	args.append(symbolic_vars)
#
#	#Sigma/delta
#	args.append(VarDecl('ExplicitRelation **',['delta','sigma']))
#
#	return args
#
##Creates a string that is a C expression that will combine the given bounds using the given function name
#def calc_bound_string(bounds,func):
#	from cStringIO import StringIO
#
#	bound_string=StringIO()
#	for i in xrange(len(bounds)):
#		if len(bounds)-1==i:
#			bound_string.write('%s'+')'*(len(bounds)-1))
#		else:
#			bound_string.write('%s(%s,',func)
#	return bound_string.getvalue()%tuple(bounds)
#
##Creates a string that is a C expression that will calculate the lower bound for a given collection of NormExps
#def calc_lower_bound_string(bounds):
#	return calc_bound_string(bounds,'min')
#
##Creates a string that is a C expression that will calculate the upper bound for a given collection of NormExps
#def calc_upper_bound_string(bounds):
#	return calc_bound_string(bounds,'max')
#
##Calculates the difference of the upper and lower bounds of the given variable in the given set
#def calc_size_string(set,var_name):
#	#Get the upper/lower bounds for the variable
#	upper_bounds=set.upper_bound(var_name)
#	lower_bounds=set.lower_bound(var_name)
#
#	#Get the string that calculates the size of the ER at runtime
#	return '%s-%s'%(calc_upper_bound_string(upper_bounds),calc_lower_bound_string(lower_bounds))
#
#def calc_ie_arg_names_string(mapir):
#	from cStringIO import StringIO
#
#	arg_names_string=StringIO()
#	for arg in mapir.ie_args:
#		for var_name in arg.var_names:
#			if '**'==arg.type[-2:]:
#				arg_names_string.write('&%s,'%(var_name))
#			else:
#				arg_names_string.write('%s,'%(var_name))
#	return arg_names_string.getvalue()[:-1]
#
#def calc_equality_value(var_name,formula):
#	from iegen.ast.visitor import FindConstraintVisitor,ValueStringVisitor
#	from iegen.ast import Equality,NormExp
#
#	values=FindConstraintVisitor(Equality,var_name).visit(formula).var_constraints
#
#	if 0==len(values): raise ValueError("Tuple variable '%s' is not involved in any equality constraints"%(var_name))
#	if len(values)>1: raise ValueError("Tuple variable '%s' is equal to multiple values"%(var_name))
#
#	value=values[0]
#
#	var=value[0]
#	exp=value[1].exp
#
#	if var.coeff>0:
#		var=NormExp([],-1)*NormExp([var],0)
#		exp=NormExp([],-1)*exp
#	else:
#		var=NormExp([var],0)
#
#	value=exp-var
#
#	return ValueStringVisitor().visit(value).value
#---------------------------------------------------
