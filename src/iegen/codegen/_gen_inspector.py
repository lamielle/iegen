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

	if 1==len(set.sets):
		conj_name = '%s_conj0'%(name)
		stmts.extend(gen_rect_domain(conj_name, iegen.Set(sets=[set.sets[0]])))
		stmts.append(Statement('RectUnionDomain *%s=RUD_ctor(%s);'%(name,conj_name)))
	else:
		stmts.append(Statement('RectUnionDomain *%s=RUD_ctor(%d);'%(name,set.arity())))
		count = 0
		for conjunct in set.sets:
			conj_name = '%s_conj%d'%(name,count)
			stmts.extend(gen_rect_domain(conj_name, iegen.Set(sets=[conjunct])))
			stmts.append(Statement('RUD_insert(%s,%s);'%(name,conj_name)))
			count = count + 1

	return stmts

def gen_rect_domain(name,set):
	from iegen.codegen import Statement,Comment

	if 1!=len(set.sets): raise ValueError("Set's relation has multiple terms in the disjunction: '%s'"%(set))

	stmts=[]
	stmts.append(Comment('RectDomain for set %s'%(set)))
	stmts.append(Statement('RectDomain *%s=RD_ctor(%d);'%(name,set.arity())))
	for var in set.sets[0].tuple_set.vars:
		stmts.append(Statement('RD_set_lb(%s,0,%s);'%(name,calc_lower_bound_string(set.lower_bound(var.id)))))
		stmts.append(Statement('RD_set_ub(%s,0,%s);'%(name,calc_upper_bound_string(set.upper_bound(var.id)))))

	return stmts


#Generate code for a given ERSpec
def gen_er_spec(er_spec,mapir):
	if er_spec.is_inverse:
		stmts=gen_inverse_er_spec(er_spec)
	else:
		if er_spec.is_union_1d():
			stmts=gen_explicit_er_union_1d(er_spec,mapir)
		else:
			stmts=gen_explicit_er_spec(er_spec,mapir)
	return stmts

#Generate an ERSpec that is the inverse of another
def gen_inverse_er_spec(er_spec):
	from iegen.codegen import Statement,Comment
	stmts=[]
	stmts.append(Comment("Create the inverse ER '%s' from the ER '%s'"%(er_spec.name,er_spec.inverse_of)))
	stmts.append(Statement('*%s=EF_genInverse(%s);'%(er_spec.get_param_name(),er_spec.inverse_of)))
	stmts.append(Statement('%s=*%s;'%(er_spec.get_var_name(),er_spec.get_param_name())))
	return stmts

def gen_explicit_er_union_1d(er_spec,mapir):
	from iegen.codegen import Statement,Comment

	if 0==len(er_spec.relation.relations): raise ValueError("ESpec's relation has no terms in the disjunction")
	if (1,1)!=er_spec.relation.arity(): raise ValueError("ESpec's relation must have arity (1,1)")

	iegen.print_progress("Generating code for ERSpec '%s'..."%(er_spec.name))
	iegen.print_detail(er_spec)

	var_in_name=er_spec.relation.relations[0].tuple_in.vars[0].id
	var_out_name=er_spec.relation.relations[0].tuple_out.vars[0].id

	stmts=[]
	stmts.append(Comment('Creation of ER_U1D for abstract relation:'))
	stmts.append(Comment(str(er_spec.relation)))
	stmts.append(Statement('%s = ER_U1D_ctor();'%(er_spec.get_var_name())))
	stmts.append(Statement())
	stmts.append(Comment('Insert relevant EFs into ER_U1D'))

	#TODO: This assumes the ERSpec we are creading has the form:
	# {[in]->[out]: out=f1(in)} union ... union {[in]->[out]: out=fn(in)}
	#Because we assume this here, we can just iterate over the functions
	# that the relation contains
	for function_name in er_spec.relation.functions():
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

	if 0==len(er_spec.relation.relations): raise ValueError("ESpec's relation has no terms in the disjunction")
	if (1,1)!=er_spec.relation.arity(): raise ValueError("ESpec's relation must have arity (1,1)")

	iegen.print_progress("Generating code for ERSpec '%s'..."%(er_spec.name))
	iegen.print_detail(er_spec)

	var_in_name=er_spec.relation.relations[0].tuple_in.vars[0].id
	var_out_name=er_spec.relation.relations[0].tuple_out.vars[0].id

	#Generate the define/undefine statements
	cloog_stmts=[]
	define_stmts=[]
	undefine_stmts=[]
	for relation_index in xrange(len(er_spec.relation.relations)):
		relation=er_spec.relation.relations[relation_index]

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
	stmts.append(Statement('%s_ER = ER_ctor(%d,%d,%s,%s,%s);'%(er_spec.name,er_spec.relation.arity_in(),er_spec.relation.arity_out(),in_domain_name,str(er_spec.is_function).lower(),str(er_spec.is_permutation).lower())))
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

def gen_output_er_spec(output_er_spec,is_call_input,mapir):
	import iegen.pycloog
	from iegen.pycloog import codegen
	from iegen.codegen import Statement,Comment

	iegen.print_progress("Generating code for output ERSpec '%s'..."%(output_er_spec.name))

	stmts=[]

	#TODO: Make this routine more general so it can handle generation for
	# general relations in addition to functions
	# Currently it just generates code for explicit functions
	#TODO: Generalize the bounds expression calculations to handle
	# more than a single expression (with min/max)
	var_name=output_er_spec.input_bounds.sets[0].tuple_set.vars[0].id
	lower_bound=str(output_er_spec.input_bounds.lower_bound(var_name)[0])
	upper_bound=str(output_er_spec.input_bounds.upper_bound(var_name)[0])
	stmts.append(Comment('Creation of ExplicitFunction for abstract relation:'))
	stmts.append(Comment(str(output_er_spec.relation)))
	stmts.append(Comment('Bounds for set %s'%(output_er_spec.input_bounds)))
	stmts.append(Statement('*%s=EF_ctor(%s,%s,%s);'%(output_er_spec.get_param_name(),lower_bound,upper_bound,str(output_er_spec.is_permutation).lower())))
	stmts.append(Statement('%s=*%s;'%(output_er_spec.get_var_name(),output_er_spec.get_param_name())))
	stmts.append(Statement())

	if not is_call_input:
		#Generate the define/undefine statements
		cloog_stmts=[]
		define_stmts=[]
		undefine_stmts=[]

		var_in_name=output_er_spec.relation.relations[0].tuple_in.vars[0].id
		var_out_name=output_er_spec.relation.relations[0].tuple_out.vars[0].id

		for relation_index in xrange(len(output_er_spec.relation.relations)):
			relation=output_er_spec.relation.relations[relation_index]

			#Get the value to insert
			value=calc_equality_value(var_out_name,relation,mapir)

			define_stmts.append(Statement('#define S%d(%s) EF_set(%s,%s,%s);'%(relation_index,var_in_name,output_er_spec.get_var_name(),var_in_name,value)))

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

def gen_call(call_spec):
	iegen.print_progress("Generating code for call to '%s'..."%(call_spec.function_name))

	stmts=[]
	stmts.append(Comment('Call %s routine'%(call_spec.function_name)))
	stmts.append(Statement(call_spec.function_name+'('+','.join(call_spec.arguments)+');'))
	stmts.append(Statement())

	return stmts
