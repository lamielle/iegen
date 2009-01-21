from iegen.codegen import Statement,calc_size_string

#Generates code for the inspector
def gen_inspector(mapir):
	from iegen.codegen import Function
	from iegen.idg.visitor import ParamVisitor,DeclVisitor,CodegenVisitor

	#Create the inspector function with the necessary parameters
	inspector=Function('inspector','void',ParamVisitor().visit(mapir.idg).params)

	#Add the necessary variable declarations
	inspector.body.extend(DeclVisitor().visit(mapir.idg).decls)

	#Add the code for the body of the inspector
	inspector.body.extend(CodegenVisitor().visit(mapir.idg).stmts)

	#Add the code to free any necessary memory
	#TODO: Need to add a visitor that adds destructor calls for the necessary ERs
	#      Also need to add a node to the IDG that represents deallocation of an ER
	#      when it is no longer needed
	#inspector.body.extend(gen_destroy_index_array_wrappers(mapir))

	return inspector

def gen_er_spec(er_spec): return []
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

#def gen_tuple_vars_decl(set):
#	from iegen.codegen import VarDecl
#
#	var_decl=VarDecl('int')
#	for set in set.sets:
#		for var in set.tuple_set.vars:
#			var_decl.var_names.append(var.id)
#	return [var_decl]

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

#The raw data of an index array will be passed in to the inspector
#However, we need the index array to look like an Explicit Relation
#Therefore, for all index arrays, we create a wrapper ER
def gen_index_array(index_array):
	input_bounds=index_array.input_bounds

	#Calculate the size of this index array
	#Assumes only one set in the union...
	if 1!=len(input_bounds.sets): raise ValueError("IndexArray's input bounds have multiple terms in the disjunction")
	#Assumes the index array dataspace is 1D...
	if 1!=input_bounds.sets[0].arity(): raise ValueError("IndexArray's dataspace does not have arity 1")

	#Get the single tuple variable's name
	var_name=input_bounds.sets[0].tuple_set.vars[0].id

	#Get the string that calculates the size of the ER at runtime
	size_string=calc_size_string(input_bounds,var_name)

	#Append the construction of the wrapper the the collection of statements
	return [Statement('%s_ER=ER_ctor(%s,%s);'%(index_array.name,index_array.name,size_string))]

def gen_output_er_spec(output_er_spec): return []
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

def gen_erg_call(erg_call): return []
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
