import iegen

#---------- Calculation Phase ----------
def do_calc(mapir):
	from iegen.codegen import calc_initial_idg,calc_full_iter_space,calc_update_access_relations,calc_unupdate_access_relations

	iegen.print_progress('Starting calculation phase...')

	#Update iteration spaces and access relations before we start calculations
	calc_update(mapir)

	#Calculate the initial IDG
	calc_initial_idg(mapir)

	iegen.print_progress('Calculating full iteration space...')

	#Calculate the full iteration space based on the current iteration spaces of the statements
	mapir.full_iter_space=calc_full_iter_space(mapir.get_statements())

	iegen.print_detail('----- Current full iteration space: -----')
	iegen.print_detail(mapir.full_iter_space)
	iegen.print_detail('-----------------------------------------')

	#Do calculations for each reordering
	for transformation in mapir.transformations:
		iegen.print_progress("Applying transformation '%s'..."%(transformation.name))

		iegen.print_detail('----- Transformation: -----')
		iegen.print_detail(transformation)
		iegen.print_detail('------------------------------------')

		#Determine if the current transformation is a transformation or an ITO
		is_transformation=False
		is_ito=False

		#Assume the current transformation is a transformation, not an ITO
		try:
			#Ensure the transformation has the four expected methods
			calc_input=transformation.calc_input
			calc_output=transformation.calc_output
			update_mapir=transformation.update_mapir
			update_idg=transformation.update_idg

			is_transformation=True
		except AttributeError as e1:
			#Try the current transformation as an ITO
			try:
				#Ensure the ito has the single 'apply' method
				apply=transformation.apply

				is_ito=True
			except AttributeError as e2:
				pass

		if is_transformation:
			iegen.print_progress('Calculating inputs to transformation...')
			#Tell the transformation to calculate the inputs that it will need at runtime
			transformation.calc_input(mapir)

			iegen.print_progress('Calculating outputs from transformation...')
			#Tell the transformation to calculate the outputs it will produce at runtime
			transformation.calc_output(mapir)

			iegen.print_progress('Updating the MapIR...')
			#Tell the transformation to update the access relations, scattering functions and other components of the MapIR
			transformation.update_mapir(mapir)

			iegen.print_progress('Updating the IDG...')
			#Tell the transformation to update the IDG
			transformation.update_idg(mapir)
		elif is_ito:
			iegen.print_progress("Applying intertransopt '%s'..."%(transformation.name))

			iegen.print_detail('----- InterTransOpt: -----')
			iegen.print_detail(transformation)
			iegen.print_detail('------------------------------------')

			transformation.apply(mapir)
		else:
			raise ValueError("Current transformation '%s' is neither a transformation nor an ITO"%(transformation.name))

		#Calculate IDG dependences
		calc_idg_deps(mapir)

		iegen.print_modified("----- Updated statements (after transformation '%s'): -----"%(transformation.name))
		for statement in mapir.get_statements():
			iegen.print_modified(statement)
			iegen.print_modified("\n")
		iegen.print_modified('-----------------------------------------')

		iegen.print_progress('Calculating full iteration space...')

		#Calculate the full iteration space based on the current iteration spaces of the statements
		mapir.full_iter_space=calc_full_iter_space(mapir.get_statements())

		iegen.print_detail('----- Current full iteration space: -----')
		iegen.print_detail(mapir.full_iter_space)
		iegen.print_detail('-----------------------------------------')

	#Un-update iteration spaces and access relations now that the calculation phase is over
	calc_unupdate(mapir)

	from iegen.idg.visitor import DotVisitor
	v=DotVisitor().visit(mapir.idg)
	v.write_dot('test.dot')

	iegen.print_progress('Calculation phase completed...')
#---------------------------------------

#---------- IDG related calculation functions ----------
#Creates an initial set of IDG nodes for Symbolics, Index Arrays, and Data Arrays
def calc_initial_idg(mapir):
	from iegen import VersionedDataArray
	from iegen.idg import IDGSymbolic,IDGDataArray,IDGIndexArray

	#Create the symbolic nodes
	for symbolic in mapir.get_symbolics():
		mapir.idg.get_node(IDGSymbolic,symbolic)

	#Create the data array nodes
	for data_array in mapir.get_data_arrays():
		mapir.idg.get_node(IDGDataArray,VersionedDataArray(data_array,0))

	#Create the index array nodes
	for index_array in mapir.get_index_arrays():
		mapir.idg.get_node(IDGIndexArray,index_array)

#Calculates general dependences between IDG nodes
def calc_idg_deps(mapir):
	#Setup symbolic dependences
	#Setup index array dependences
	#Setup ERSpec dependences
	for er_spec in mapir.get_er_specs():
		calc_er_spec_deps(er_spec,mapir)

#Adds any dependences the given ERSpec has to the IDG
def calc_er_spec_deps(er_spec,mapir):
	from iegen.idg import IDGSymbolic,IDGIndexArray,IDGERSpec
	#Ignore index arrays
	if er_spec.name not in mapir.index_arrays:
		#Get the IDG node for the given ERSpec
		er_spec_node=mapir.idg.get_node(IDGERSpec,er_spec)

		#Make sure this node is dependent on only one node
		if len(er_spec_node.deps)>1:
			raise ValueError("IDG node '%s' is dependent on more than one node"%(er_spec_node.name))

		#Get the node that produced this ERSpec
		parent_er_spec_node=er_spec_node.deps[er_spec_node.deps.keys()[0]]

		#Gather symbolic dependences
		for symbolic in er_spec.symbolics():
			symbolic_node=mapir.idg.get_node(IDGSymbolic,mapir.symbolics[symbolic])
			parent_er_spec_node.add_dep(symbolic_node)

		#Gather other ERSpec dependences
		for function in er_spec.functions():
			#Die if the function is referenced but no associated ERSpec exists in the MapIR
			if function not in mapir.er_specs:
				raise ValueError("Function '%s' referenced but no associated ERSpec exists"%function)

			#Ignore self references
			if function!=er_spec.name:
				#Get the IDG node for the ERSpec that represents this function
				#Check if the function is an index array
				if function in mapir.index_arrays:
					dep_node=mapir.idg.get_node(IDGIndexArray,mapir.index_arrays[function])
				else:
					dep_node=mapir.idg.get_node(IDGERSpec,mapir.er_specs[function])

				#Setup the dependence relationship
				parent_er_spec_node.add_dep(dep_node)

				#Recursively add dependences for the dependence node
				calc_er_spec_deps(dep_node.data,mapir)

#Adds any dependences the given DataDependence has to the IDG
def calc_data_dep_deps(data_dep,mapir):
	from iegen.idg import IDGSymbolic,IDGIndexArray,IDGERSpec,IDGDataDep
	#Get the IDG node for the given DataDependence
	data_dep_node=mapir.idg.get_node(IDGDataDep,data_dep)

	#Make sure this node is dependent on only one node
	if len(data_dep_node.deps)>1:
		raise ValueError("IDG node '%s' is dependent on more than one node"%(data_dep_node.name))

	#Get the node that produced this ERSpec
	parent_of_data_dep_node=data_dep_node.deps[data_dep_node.deps.keys()[0]]

	#Gather symbolic dependences
	for symbolic in data_dep.symbolics():
		symbolic_node=mapir.idg.get_node(IDGSymbolic,mapir.symbolics[symbolic])
		parent_of_data_dep_node.add_dep(symbolic_node)

	#Gather ERSpec dependences
	for function in data_dep.functions():
		#Die if the function is referenced but no associated ERSpec exists in the MapIR
		if function not in mapir.er_specs:
			raise ValueError("Function '%s' referenced but no associated ERSpec exists"%function)

		#Get the IDG node for the ERSpec that represents this function
		#Check if the function is an index array
		if function in mapir.index_arrays:
			dep_node=mapir.idg.get_node(IDGIndexArray,mapir.index_arrays[function])
		else:
			dep_node=mapir.idg.get_node(IDGERSpec,mapir.er_specs[function])

		#Setup the dependence relationship
		parent_of_data_dep_node.add_dep(dep_node)
#-------------------------------------------------------

#---------- Access Relation calculation functions ----------
#Updates the MapIR for the computation phase
def calc_update(mapir):
	calc_update_iter_spaces(mapir)
	calc_update_access_relations(mapir)

#Updates iteration spaces for the computation phase
def calc_update_iter_spaces(mapir):
	iegen.print_progress('Updating iteration spaces...')

	#Update each statement's iteration space to be within the context of the full iteration space
	#rather than just iterators
	for statement in mapir.get_statements():
		statement.iter_space=statement.iter_space.apply(statement.scatter)

#Updates access relations for the computation phase
def calc_update_access_relations(mapir):
	iegen.print_progress('Updating access relations...')

	#Update each access relation's iteration to data relation to
	# match its statement's scattering function
	for statement in mapir.get_statements():
		for access_relation in statement.get_access_relations():
			iegen.print_detail("Updating iter_to_data of access relation '%s'..."%(access_relation.name))

			before=str(access_relation.iter_to_data)

			#Compose the access relation to be in terms of the statement's scattering function
			access_relation.iter_to_data=access_relation.iter_to_data.compose(statement.scatter.inverse())

			iegen.print_modified("Updated iter_to_data of access relation '%s': %s -> %s"%(access_relation.name,before,access_relation.iter_to_data))

#Un-updates the MapIR following the computation phase
def calc_unupdate(mapir):
	full_to_iter=calc_unupdate_iter_spaces(mapir)
	calc_unupdate_access_relations(mapir,full_to_iter)
	calc_unupdate_scatter(mapir)

#Unupdates iteration spaces following the computation phase
def calc_unupdate_iter_spaces(mapir):
	from iegen import Relation
	iegen.print_progress('Un-updating iteration spaces...')

	full_to_iter={}

	#Update each statement's iteration space to be only iterators and no interleaved constants
	for statement in mapir.get_statements():
		#Extract the iterators and not the constant positions (iterators are the odd positions)
		iters=[tuple_var for pos,tuple_var in enumerate(statement.iter_space.tuple_set) if pos%2==1]

		#Create a new set with just the extracted iterators
		extract_iters_rel=Relation('{[%s]->[%s]}'%(','.join(statement.iter_space.tuple_set),','.join(iters)))
		temp_iter=statement.iter_space.apply(extract_iters_rel)

		#Determine the dimensions of the new iteration space that are not constant
		non_const_vars=[]
		for var in temp_iter.tuple_set:
			try:
				#Try to determine what the current variable is equal to
				val=calc_equality_value(var,temp_iter,mapir)
			except ValueError as e:
				#The current variable wasn't equal to a single value, i.e. not constant
				non_const_vars.append(var)
			else:
				try:
					#The current variable was equal to a single value, try to convert it to an integer
					val=int(val)
				except ValueError as e:
					#The current variable was equal to a single value but not an integer
					#TODO: This checking doesn't check for transitivity (i.e. a=b and b=0)
					non_const_vars.append(var)

		#Construct a relation for taking the full iteration space down to just the non-constant iterators
		full_to_iter_rel=Relation('{[%s]->[%s]}'%(','.join(iters[:len(non_const_vars)]),','.join(statement.iter_space.tuple_set))).inverse()
		full_to_iter[statement.name]=full_to_iter_rel

		#Un-update the statement's iteration space using the full_to_iter relation
		statement.iter_space=statement.iter_space.apply(full_to_iter_rel)

	return full_to_iter

#Un-updates access relations following the computation phase
def calc_unupdate_access_relations(mapir,full_to_iter):
	from iegen import Relation
	iegen.print_progress('Un-updating access relations...')

	#Update each access relation's iteration to data relation to
	# match its statement's iteration space
	for statement in mapir.get_statements():
		for access_relation in statement.get_access_relations():
			iegen.print_detail("Un-updating iter_to_data of access relation '%s'..."%(access_relation.name))

			before=str(access_relation.iter_to_data)

			#Compose the access relation to be in terms of the statement's iteration space
			access_relation.iter_to_data=full_to_iter[statement.name].compose(access_relation.iter_to_data.inverse()).inverse()

			iegen.print_modified("Un-updated iter_to_data of access relation '%s': %s -> %s"%(access_relation.name,before,access_relation.iter_to_data))

def calc_unupdate_scatter(mapir):
	from iegen import Relation

	iegen.print_progress("Un-updating scattering functions...")

	for statement in mapir.get_statements():
		#TODO: This approach is a HACK due to the lack of an intersect operation with set/relation
		#Get a string of the constraints for the statement's scattering function
		scatter_constrs=str(list(list(statement.scatter.range())[0].disjunction.conjunctions)[0])

		#Get the output tuple from the scattering function
		scatter_tuple_out=statement.scatter.tuple_out

		#Get just the iterators and not interleaved constants from the scattering function
		scatter_iters=[tuple_var for pos,tuple_var in enumerate(statement.scatter.tuple_out) if pos%2==1]

		#Get the statement's iteration space iterators
		iters=statement.iter_space.tuple_set

		#Get pairs of scatter iters/iteration space iters
		#If there are more scattering iters than in the iteration space, zip handles it
		iter_pairs=zip(iters,scatter_iters)

		#Create equality constraint strings for the pairs of iterators
		eq_constraints=[]
		for iter_space_iter,scatter_iter in iter_pairs:
			eq_constraints.append('%s=%s'%(iter_space_iter,scatter_iter))
		eq_constraints=' and '.join(eq_constraints)

		#Make comma separated lists
		iters=','.join(iters)
		scatter_tuple_out=','.join(scatter_tuple_out)

		new_scatter=Relation('{[%s]->[%s]: %s and %s}'%(iters,scatter_tuple_out,scatter_constrs,eq_constraints),symbolics=statement.scatter.symbolics)
		statement.scatter=new_scatter

def calc_access_relation_rename(access_relation,iter_space):
	#Make sure the input arity of the access relation matches
	# the arity of the iteration set
	if access_relation.arity_in()!=iter_space.arity():
		raise ValueError('Input arity of access relation (%d) is not equal to arity of iteration space (%d).'%(access_relation.arity_in(),iter_space.arity()))

	from_vars=access_relation.tuple_in
	to_vars=iter_space.tuple_set

	rename={}

	for i in xrange(len(from_vars)):
		rename[from_vars[i]]=to_vars[i]

	return rename
#-----------------------------------------------------------

#---------- IDG Node calculation functions ----------
def calc_reorder_call(trans_name,data_array,reordering_name,mapir):
	from iegen import FunctionCallSpec

	func_name='reorderArray'
	name=trans_name+'_'+func_name+'_'+data_array.name
	args=[
	      '(unsigned char*)%s'%(data_array.name),
	      data_array.elem_size,
	      calc_size_string(data_array.bounds,data_array.bounds.tuple_vars[0]),
	      mapir.er_specs[reordering_name].get_var_name()
	     ]

	return FunctionCallSpec(name,func_name,args)

def calc_erg_call(trans_name,erg_func_name,inputs,outputs):
	from iegen import FunctionCallSpec
	name=trans_name+'_'+erg_func_name

	args=[er for er in inputs+outputs]

	arg_strs=[]
	for er in inputs+outputs:
		if er.is_gen_output():
			arg_strs.append('&%s'%(er.get_var_name()))
		else:
			arg_strs.append(er.get_var_name())

	output_args=[arg for arg in args if arg.is_gen_output()]

	return FunctionCallSpec(name,erg_func_name,arg_strs,output_args)
#----------------------------------------------------

#---------- Utility calculation functions ----------
#Given a collection of Statement objects, calculates the combined iteration space of all statements
#Assumes that at least one statement is given
def calc_full_iter_space(statements):
	full_iter=statements[0].iter_space
	for statement in statements[1:]:
		full_iter=full_iter.union(statement.iter_space)
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
	return calc_bound_string(bounds,'max')

#Creates a string that is a C expression that will calculate the upper bound for a given collection of NormExps
def calc_upper_bound_string(bounds):
	return calc_bound_string(bounds,'min')

#Calculates the difference of the upper and lower bounds of the given variable in the given set
def calc_size_string(set,var_name):
	#Get the upper/lower bounds for the variable
	upper_bounds=set.upper_bounds(var_name,ignore_ufs=True)[0]
	lower_bounds=set.lower_bounds(var_name,ignore_ufs=True)[0]

	#Get the string that calculates the size of the ER at runtime
	return '%s-%s+1'%(calc_upper_bound_string(upper_bounds),calc_lower_bound_string(lower_bounds))

#Returns the value that the given variable is equal to in the given formula
#If raw_array is True, accesses to arrays (functions) will not be treated as explicit relation lookups
#If only_eqs is True, only equality constraints are considered (inequalities are ignored)
def calc_equality_value(var_name,formula,mapir,raw_array=False,only_eqs=False):
	import iegen

	iegen.print_detail("Calculating equality value for tuple variable '%s' in relation %s"%(var_name,formula))

	bounds=formula.bounds(var_name)

	if 0==len(bounds): raise ValueError("Tuple variable '%s' is not involved in any equality constraints in formula '%s'"%(var_name,formula))
	if len(bounds)>1: raise ValueError("Tuple variable '%s' is equal to multiple values in formula '%s'"%(var_name,formula))

	#Ignore inequality constraints?
	if only_eqs:
		lower_bounds=[]
		upper_bounds=[]

		#Remove any bounds that are only an upper or a lower bound (looking for equalities)
		for lb in bounds[0][0]:
			if lb in bounds[0][1]:
				lower_bounds.append(lb)
				upper_bounds.append(lb)
	else:
		lower_bounds,upper_bounds=bounds[0]

	if 1!=len(lower_bounds) or 1!=len(upper_bounds): raise ValueError("TupleVariable '%s' is not equal to exactly one value in formula '%s'"%(var_name,formula))
	if lower_bounds!=upper_bounds: raise ValueError("TupleVariable '%s' is not equal to one value in formula '%s'"%(var_name,formula))

	equal_value=list(lower_bounds)[0]

	ufs_name_map=mapir.ufs_name_map()

	iegen.print_detail("-->Equality value for tuple variable '%s' in relation %s: %s"%(var_name,formula,equal_value.value_string(function_name_map=ufs_name_map)))

	return equal_value.value_string(function_name_map=ufs_name_map)
#---------------------------------------------------
