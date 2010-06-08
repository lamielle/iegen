import iegen
from iegen import IEGenObject
from iegen.codegen import Statement,Comment,calc_equality_value,calc_lower_bound_string,calc_upper_bound_string,calc_size_string

#Generates code for the inspector
def gen_inspector(mapir):
	from iegen.codegen import Function
	from iegen.idg.visitor import ParamVisitor,DeclVisitor,CodegenVisitor

	#Create the inspector function with the necessary parameters
	inspector=Function(iegen.settings.inspector_name,'void',ParamVisitor().visit(mapir.idg).get_params())

	#If there are no transformations, don't bother doing any codegen
	if len(mapir.transformations)>0:
		#Add the necessary variable declarations
		inspector.body.extend(DeclVisitor(mapir).visit(mapir.idg).get_decls())
		inspector.newline()

		#Add the code for the body of the inspector
		inspector.body.extend(CodegenVisitor(mapir).visit(mapir.idg).stmts)

		#Add the code to free any necessary memory
		#TODO: Need to add a visitor that adds destructor calls for the necessary ERs
		#      Also need to add a node to the IDG that represents deallocation of an ER
		#      when it is no longer needed
		#inspector.body.extend(gen_destroy_index_array_wrappers(mapir))

	return inspector

# Right now generating a RectUnionDomain, but later might generate a more
# general data structure.
def gen_domain(name,set):
	from iegen.codegen import Statement,Comment

	iegen.print_detail("Generating RectUnionDomain for set %s"%set)

	stmts=[]
	stmts.append(Comment('RectUnionDomain for set %s'%(set)))

	if 1==len(set):
		conj_name = '%s_conj0'%(name)
		stmts.extend(gen_rect_domain(conj_name, list(set)[0]))
		stmts.append(Statement('RectUnionDomain *%s=RUD_ctor(%s);'%(name,conj_name)))
	else:
		stmts.append(Statement('RectUnionDomain *%s=RUD_ctor(%d);'%(name,set.arity())))
		count = 0
		for conjunct in set:
			conj_name = '%s_conj%d'%(name,count)
			stmts.extend(gen_rect_domain(conj_name,conjunct))
			stmts.append(Statement('RUD_insert(%s,%s);'%(name,conj_name)))
			count = count + 1

	return stmts

def gen_rect_domain(name,set):
	from iegen.codegen import Statement,Comment

	if 1!=len(set): raise ValueError("Set's relation has multiple terms in the disjunction: '%s'"%(set))

	stmts=[]
	stmts.append(Comment('RectDomain for set %s'%(set)))
	stmts.append(Statement('RectDomain *%s=RD_ctor(%d);'%(name,set.arity())))
	for var in set.tuple_set:
		stmts.append(Statement('RD_set_lb(%s,0,%s);'%(name,calc_lower_bound_string(set.lower_bounds(var)[0]))))
		stmts.append(Statement('RD_set_ub(%s,0,%s);'%(name,calc_upper_bound_string(set.upper_bounds(var)[0]))))

	return stmts

def calc_int_bounds_from_bounds(bounds):
	int_bounds=[]
	for bound in bounds:
		if len(bound)!=1:
			raise ValueError('Multiple bounds discovered')
		bound=str(list(bound)[0])
		try:
			bound=int(bound)
		except ValueError as e:
			raise ValueError('Non-integer bound discovered')
		int_bounds.append(bound)

	return int_bounds

def calc_single_bounds_from_bounds(bounds):
	res_bounds=[]
	for bound in bounds:
		if len(bound)!=1:
			raise ValueError('Multiple bounds discovered')
		bound=str(list(bound)[0])
		res_bounds.append(bound)

	return res_bounds

def gen_rect_union_domain_2d(name,set):
	from iegen.codegen import Statement,Comment

	if set.arity()!=2: raise ValueError("Set does not have arity 2 (%d)"%(set.arity()))

	stmts=[]

	#Determine the lower and upper bounds of the first dimension of each conjunction in the set
	lbs=calc_int_bounds_from_bounds(set.lower_bounds(set.tuple_vars[0]))
	ubs=calc_int_bounds_from_bounds(set.upper_bounds(set.tuple_vars[0]))

	#Make sure the integer bounds are pair-wise equal
	for i in xrange(len(set)):
		if lbs[i]!=ubs[i]:
			raise ValueError('Non-constant value for first dimension of given set: %s'%(set))

	#The list of constant values for each conjunction
	const_vals=lbs

	#Determine the lower and upper bounds of the second dimensions of each conjunction in the set
	lbs=calc_single_bounds_from_bounds(set.lower_bounds(set.tuple_vars[1]))
	ubs=calc_single_bounds_from_bounds(set.upper_bounds(set.tuple_vars[1]))

	#Calculate the static array for the bounds
	bounds_sub_arrays=['{%s,%s,%s}'%items for items in zip(const_vals,lbs,ubs)]
	bounds_array='{'+','.join(bounds_sub_arrays)+'}'

	#Declare the bounds for the dimensions
	stmts.append(Comment('RUD2D bounds for %s'%(name,)))
	stmts.append(Statement('int %s_bounds[][3] = %s;'%(name,bounds_array)))
	stmts.append(Statement('RectUnionDomain2D *%s_rud = RUD2D_ctor(%d,%d,%d,%s_bounds);'%(name,set.arity(),min(const_vals),max(const_vals),name)))

	return stmts

#---------- ERSpec code generation ----------
#Generate code for a given ERSpec
def gen_er_spec(er_spec,mapir):
	if er_spec.is_inverse:
		stmts=gen_inverse_er_spec(er_spec,mapir)
	else:
		if er_spec.is_union_1d():
			stmts=gen_explicit_er_union_1d(er_spec,mapir)
		elif er_spec.is_ef_2d():
			raise ValueError('Code generation of non-output EF_2D ERSpecs not yet implemented')
		else:
			stmts=gen_explicit_er_spec(er_spec,mapir)
	return stmts

#Generate an ERSpec that is the inverse of another
def gen_inverse_er_spec(er_spec,mapir):
	from iegen.codegen import Statement,Comment
	stmts=[]
	stmts.append(Comment("Create the inverse ER '%s' from the ER '%s'"%(er_spec.name,er_spec.inverse_of)))
	stmts.append(Statement('*%s=%s(%s);'%(er_spec.get_param_name(),er_spec.get_genInverse_str(),mapir.er_specs[er_spec.inverse_of].get_var_name())))
	stmts.append(Statement('%s=*%s;'%(er_spec.get_var_name(),er_spec.get_param_name())))
	return stmts

def gen_explicit_er_union_1d(er_spec,mapir):
	from iegen.codegen import Statement,Comment

	if 0==len(er_spec.relation): raise ValueError("ESpec's relation has no terms in the disjunction")
	if (1,1)!=er_spec.relation.arity(): raise ValueError("ESpec's relation must have arity (1,1)")

	iegen.print_progress("Generating code for ERSpec '%s'..."%(er_spec.name))
	iegen.print_detail(er_spec)

	var_in_name=er_spec.relation.tuple_in[0]
	var_out_name=er_spec.relation.tuple_out[0]

	stmts=[]
	stmts.append(Comment('Creation of ER_U1D for abstract relation:'))
	stmts.append(Comment(str(er_spec.relation)))
	stmts.append(Statement('%s = %s();'%(er_spec.get_var_name(),er_spec.get_ctor_str())))
	stmts.append(Statement())
	stmts.append(Comment('Insert relevant EFs into ER_U1D'))

	#TODO: This assumes the ERSpec we are creading has the form:
	# {[in]->[out]: out=f1(in)} union ... union {[in]->[out]: out=fn(in)}
	#Because we assume this here, we can just iterate over the functions
	# that the relation contains
	for function_name in er_spec.relation.function_names:
		#Get the er_spec for the current function
		function_er_spec=mapir.er_specs[function_name]

		#Add the function to the ER_U1D
		stmts.append(Statement('ER_U1D_insert(%s, %s);'%(er_spec.get_var_name(),function_er_spec.get_var_name())))

	stmts.append(Statement())

	return stmts

#Generate code for creating an ERSpec explicitly
def gen_explicit_er_spec(er_spec,mapir):
	import iegen.pycloog
	from iegen.pycloog import codegen
	from iegen.codegen import Statement,Comment

	if 0==len(er_spec.relation): raise ValueError("ESpec's relation has no terms in the disjunction")
	if (1,1)!=er_spec.relation.arity(): raise ValueError("ESpec's relation must have arity (1,1)")

	iegen.print_progress("Generating code for ERSpec '%s'..."%(er_spec.name))
	iegen.print_detail(er_spec)

	var_in_name=er_spec.relation.tuple_in[0]
	var_out_name=er_spec.relation.tuple_out[0]

	#Generate the define/undefine statements
	cloog_stmts=[]
	define_stmts=[]
	undefine_stmts=[]
	for relation_index,relation in enumerate(er_spec.relation):
		#Get the value to insert
		value=calc_equality_value(var_out_name,relation,mapir)

		define_stmts.append(Statement('#define S%d(%s) ER_in_ordered_insert(%s_ER,Tuple_make(%s),Tuple_make(%s));'%(relation_index,var_in_name,er_spec.name,var_in_name,value)))

		cloog_stmts.append(iegen.pycloog.Statement(er_spec.input_bounds))
		undefine_stmts.append(Statement('#undef S%d'%(relation_index,)))

	#Generate the whole set of statements
	stmts=[]
	in_domain_name='in_domain_%s'%(er_spec.name)
	stmts.extend(gen_domain(in_domain_name,er_spec.input_bounds))
	stmts.append(Statement())
	stmts.append(Comment('Creation of ExplicitRelation'))
	stmts.append(Comment(str(er_spec.relation)))
	stmts.append(Statement('%s_ER = %s(%d,%d,%s,%s,%s);'%(er_spec.name,er_spec.get_ctor_str(),er_spec.relation.arity_in(),er_spec.relation.arity_out(),in_domain_name,str(er_spec.is_function).lower(),str(er_spec.is_permutation).lower())))
	stmts.append(Statement())
	stmts.append(Comment('Define loop body statements'))
	stmts.extend(define_stmts)
	stmts.append(Statement())
	loop_stmts=codegen(cloog_stmts).split('\n')
	for loop_stmt in loop_stmts:
		stmts.append(Statement(loop_stmt))
	stmts.append(Statement())
	stmts.append(Comment('Undefine loop body statements'))
	stmts.extend(undefine_stmts)
	return stmts
#--------------------------------------------

#---------- Output ERSpec code generation ----------
def gen_output_er_spec(output_er_spec,is_call_input,mapir):
	if output_er_spec.is_union_1d():
		stmts=gen_output_er_spec_general(output_er_spec,is_call_input,mapir)
	elif output_er_spec.is_ef_2d():
		stmts=gen_output_ef_2d(output_er_spec,is_call_input,mapir)
	else:
		raise ValueError('Code generation for unsupported output ERSpec type')

	return stmts

def gen_output_ef_2d(output_er_spec,is_call_input,mapir):
	import iegen.pycloog
	from iegen.pycloog import codegen
	from iegen.codegen import Statement,Comment

	iegen.print_progress("Generating code for output ERSpec '%s'..."%(output_er_spec.name))
	iegen.print_detail(str(output_er_spec))

	stmts=[]

	stmts.extend(gen_rect_union_domain_2d(output_er_spec.name,output_er_spec.input_bounds))

	#Variable name of the RUD2D
	domain_name='%s_rud'%(output_er_spec.get_param_name(),)

	stmts.append(Comment('Creation of ExplicitFunction for abstract relation:'))
	stmts.append(Comment(str(output_er_spec.relation)))
	stmts.append(Comment('Bounds for set %s'%(output_er_spec.input_bounds)))

	stmts.append(Statement('*%s=%s(%s,%s,%s);'%(output_er_spec.get_param_name(),output_er_spec.get_ctor_str(),output_er_spec.relation.arity_in(),output_er_spec.relation.arity_out(),domain_name)))

	stmts.append(Statement('%s=*%s;'%(output_er_spec.get_var_name(),output_er_spec.get_param_name())))
	stmts.append(Statement())

	return stmts

def gen_output_er_spec_general(output_er_spec,is_call_input,mapir):
	import iegen.pycloog
	from iegen.pycloog import codegen
	from iegen.codegen import Statement,Comment

	iegen.print_progress("Generating code for output ERSpec '%s'..."%(output_er_spec.name))
	iegen.print_detail(str(output_er_spec))

	stmts=[]

	#TODO: Make this routine more general so it can handle generation for
	# general relations in addition to functions
	# Currently it just generates code for explicit functions
	#TODO: Generalize the bounds expression calculations to handle
	# more than a single expression (with min/max)
	var_name=output_er_spec.input_bounds.tuple_set[0]
	lower_bound=str(list(output_er_spec.input_bounds.lower_bounds(var_name)[0])[0])
	upper_bound=str(list(output_er_spec.input_bounds.upper_bounds(var_name)[0])[0])
	stmts.append(Comment('Creation of ExplicitFunction for abstract relation:'))
	stmts.append(Comment(str(output_er_spec.relation)))
	stmts.append(Comment('Bounds for set %s'%(output_er_spec.input_bounds)))
	stmts.append(Statement('*%s=%s(%s,%s,%s);'%(output_er_spec.get_param_name(),output_er_spec.get_ctor_str(),lower_bound,upper_bound,str(output_er_spec.is_permutation).lower())))
	stmts.append(Statement('%s=*%s;'%(output_er_spec.get_var_name(),output_er_spec.get_param_name())))
	stmts.append(Statement())

	if not is_call_input:
		#Generate the define/undefine statements
		cloog_stmts=[]
		define_stmts=[]
		undefine_stmts=[]

		var_in_name=output_er_spec.relation.tuple_in[0]
		var_out_name=output_er_spec.relation.tuple_out[0]

		for relation_index,single_relation in enumerate(output_er_spec.relation):
			#Get the value to insert
			value=calc_equality_value(var_out_name,single_relation,mapir)

			define_stmts.append(Statement('#define S%d(%s) %s(%s,%s,%s);'%(relation_index,var_in_name,output_er_spec.get_setter_str(),output_er_spec.get_var_name(),var_in_name,value)))

			cloog_stmts.append(iegen.pycloog.Statement(output_er_spec.input_bounds))
			undefine_stmts.append(Statement('#undef S%d'%(relation_index,)))

		#Generate the whole set of statements
		stmts.append(Comment('Define loop body statements'))
		stmts.extend(define_stmts)
		stmts.append(Statement())
		loop_stmts=codegen(cloog_stmts).split('\n')
		for loop_stmt in loop_stmts:
			stmts.append(Statement(loop_stmt))
		stmts.append(Statement())
		stmts.append(Comment('Undefine loop body statements'))
		stmts.extend(undefine_stmts)
		stmts.append(Statement())

	#TODO: This is the old code that generates an ER rather than an EF
	##Create a domain for the ERSpec
	#in_domain_name='in_domain_%s'%(output_er_spec.name)
	#stmts.extend(gen_domain(in_domain_name,output_er_spec.input_bounds))
	#stmts.append(Statement('*%s=ER_ctor(%d,%d,%s,%s,%s);'%(output_er_spec.name,output_er_spec.input_bounds.arity(),output_er_spec.output_bounds.arity(),in_domain_name,str(output_er_spec.is_function).lower(),str(output_er_spec.is_permutation).lower())))
	#stmts.append(Statement('%s_ER=*%s;'%(output_er_spec.name,output_er_spec.name)))

	return stmts
#---------------------------------------------------

def gen_data_dep(data_dep,mapir):
	stmts=[]

	stmts.append(Comment('Data dep code for %s goes here'%(data_dep.name)))

	return stmts

def gen_call(call_spec):
	iegen.print_progress("Generating code for call to '%s'..."%(call_spec.function_name))

	stmts=[]
	stmts.append(Comment('Call the %s routine'%(call_spec.function_name)))
	stmts.append(Statement(call_spec.function_name+'('+','.join(call_spec.arguments)+');'))
	stmts.append(Statement())

	return stmts
