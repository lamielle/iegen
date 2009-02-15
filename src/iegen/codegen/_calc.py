#---------- Calculation Phase ----------
def do_calc(mapir):

	from iegen.codegen import calc_full_iter_space

	#Do calculations for each reordering
	for transformation in mapir.transformations:
		print '----- Applying transformation: -----'
		print transformation
		print '------------------------------------'
		print

		print 'Calculating full iteration space...'

		#Calculate the full iteration space based on the current iteration spaces of the statements
		mapir.full_iter_space=calc_full_iter_space(mapir.get_statements())

		print '----- Current full iteration space: -----'
		print mapir.full_iter_space
		print '-----------------------------------------'
		print

		print 'Calculating inputs to transformation...'
		#Tell the transformation to calculate the inputs that it will need at runtime
		transformation.calc_input(mapir)

		print 'Calculating outputs from transformation...'
		#Tell the transformation to calculate the outputs it will produce at runtime
		transformation.calc_output(mapir)

		print 'Updating the MapIR...'
		#Tell the transformation to update the access relations, scattering functions and other components of the MapIR
		transformation.update_mapir(mapir)

		print 'Updating the MapIR...'
		#Tell the transformation to update the IDG
		transformation.update_idg(mapir)

		print '----- Updated statements: -----'
		for statement in mapir.get_statements():
			print statement
		print '-----------------------------------------'
		print

	from iegen.idg.visitor import DotVisitor
	v=DotVisitor().visit(mapir.idg)
	v.write_dot('test.dot')
#---------------------------------------

#---------- Utility calculation functions ----------
#Given a collection of Statement objects, calculates the combined iteration space of all statements
#Assumes that at least one statement is given
def calc_full_iter_space(statements):
	full_iter=statements[0].iter_space.apply(statements[0].scatter)
	for statement in statements[1:]:
		full_iter=full_iter.union(statement.iter_space.apply(statement.scatter))
	return full_iter

#Creates a string that is a C expression that will combine the given bounds using the given function name
def calc_bound_string(bounds,func):
	from cStringIO import StringIO

	bound_string=StringIO()
	for i in xrange(len(bounds)):
		if len(bounds)-1==i:
			bound_string.write('%s'+')'*(len(bounds)-1))
		else:
			bound_string.write('%s(%s,',func)
	return bound_string.getvalue()%tuple(bounds)

#Creates a string that is a C expression that will calculate the lower bound for a given collection of NormExps
def calc_lower_bound_string(bounds):
	return calc_bound_string(bounds,'min')

#Creates a string that is a C expression that will calculate the upper bound for a given collection of NormExps
def calc_upper_bound_string(bounds):
	return calc_bound_string(bounds,'max')

#Calculates the difference of the upper and lower bounds of the given variable in the given set
def calc_size_string(set,var_name):
	#Get the upper/lower bounds for the variable
	upper_bounds=set.upper_bound(var_name)
	lower_bounds=set.lower_bound(var_name)

	#Get the string that calculates the size of the ER at runtime
	return '%s-%s'%(calc_upper_bound_string(upper_bounds),calc_lower_bound_string(lower_bounds))

def calc_equality_value(var_name,formula):
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
#---------------------------------------------------
