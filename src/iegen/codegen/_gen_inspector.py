from iegen.codegen import Statement,calc_equality_value,calc_lower_bound_string,calc_upper_bound_string

#Generates code for the inspector
def gen_inspector(mapir):
	from iegen.codegen import Function
	from iegen.idg.visitor import ParamVisitor,DeclVisitor,CodegenVisitor

	#Create the inspector function with the necessary parameters
	inspector=Function('inspector','void',ParamVisitor().visit(mapir.idg).params)

	#Add the necessary variable declarations
	inspector.body.extend(DeclVisitor().visit(mapir.idg).decls.values())

	#Add the code for the body of the inspector
	inspector.body.extend(CodegenVisitor().visit(mapir.idg).stmts)

	#Add the code to free any necessary memory
	#TODO: Need to add a visitor that adds destructor calls for the necessary ERs
	#      Also need to add a node to the IDG that represents deallocation of an ER
	#      when it is no longer needed
	#inspector.body.extend(gen_destroy_index_array_wrappers(mapir))

	return inspector

def gen_rect_domain(name,set):
	from iegen.codegen import Statement,Comment

	if 1!=len(set.sets): raise ValueError("Set's relation has multiple terms in the disjunction")

	stmts=[]
	stmts.append(Comment('RectDomain for set %s'%(set)))

	stmts.append(Statement('RectDomain *%s=RD_ctor(%d);'%(name,set.arity())))

	for var in set.sets[0].tuple_set.vars:
		stmts.append(Statement('RD_set_lb(%s,0,%s);'%(name,calc_lower_bound_string(set.lower_bound(var.id)))))
		stmts.append(Statement('RD_set_ub(%s,0,%s);'%(name,calc_upper_bound_string(set.upper_bound(var.id)))))

	return stmts

#Generate code for a given ERSpec
def gen_er_spec(er_spec):
	import iegen.pycloog
	from iegen.pycloog import codegen
	from iegen.codegen import Statement,Comment

	if 0==len(er_spec.relation.relations): raise ValueError("ESpec's relation has no terms in the disjunction")
	if (1,1)!=er_spec.relation.arity(): raise ValueError("ESpec's relation must have arity (1,1)")

	var_in_name=er_spec.relation.relations[0].tuple_in.vars[0].id
	var_out_name=er_spec.relation.relations[0].tuple_out.vars[0].id

	#Generate the define/undefine statements
	cloog_stmts=[]
	define_stmts=[]
	undefine_stmts=[]
	for relation_index in xrange(len(er_spec.relation.relations)):
		relation=er_spec.relation.relations[relation_index]

		#Get the value to insert
		value=calc_equality_value(var_out_name,relation)

		define_stmts.append(Statement('#define S%d ER_in_ordered_insert(%s,Tuple_make(%s),Tuple_make(%s));'%(relation_index,er_spec.name,var_in_name,value)))

		cloog_stmts.append(iegen.pycloog.Statement(er_spec.input_bounds))
		undefine_stmts.append(Statement('#undef S%d'%(relation_index,)))

	#Generate the whole set of statements
	stmts=[]
	in_domain_name='in_domain_%s'%(er_spec.name)
	stmts.extend(gen_rect_domain(in_domain_name,er_spec.input_bounds))
	stmts.append(Statement())
	stmts.append(Comment('Creation of ExplicitRelation of the ARTT'))
	stmts.append(Comment(str(er_spec.relation)))
	stmts.append(Statement('ExplicitRelation* %s = ER_ctor(%d,%d,%s,%s,%s);'%(er_spec.name,er_spec.relation.arity_in(),er_spec.relation.arity_out(),in_domain_name,str(er_spec.is_function).lower(),str(er_spec.is_permutation).lower())))
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

def gen_output_er_spec(output_er_spec):
	from iegen.codegen import Statement,Comment

	stmts=[]

	#Create a rect domain for the ERSpec
	in_domain_name='in_domain_%s'%(output_er_spec.name)
	stmts.extend(gen_rect_domain(in_domain_name,output_er_spec.input_bounds))
	stmts.append(Statement('*%s=ER_ctor(%d,%d,%s,%s);'%(output_er_spec.name,output_er_spec.input_bounds.arity(),output_er_spec.output_bounds.arity(),in_domain_name,str(output_er_spec.is_permutation).lower())))
	stmts.append(Statement('%s_ER=*%s;'%(output_er_spec.name,output_er_spec.name)))

	return stmts

def gen_erg_spec(erg_spec,output_er_specs):
	stmts=[]

	#Generate the code to setup the output ERs before making the call
	for output_er_spec in output_er_specs:
		gen_output_er_spec(output_er_spec)

	#Generate the code to make the call to the ERG
	arg_list_template=','.join(['%s']*(len(erg_spec.inputs)+len(erg_spec.outputs)))
	call_template='%s('+arg_list_template+');'
	call_strings=tuple([erg_spec.erg_func_name]+[input.name for input in erg_spec.inputs]+[output.name+'_ER' for output in erg_spec.outputs])
	stmts.append(Statement(call_template%call_strings))

	return stmts

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
