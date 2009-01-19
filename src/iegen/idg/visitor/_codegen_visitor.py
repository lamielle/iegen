from iegen.idg.visitor import TopoVisitor
from iegen.codegen import Statement,calc_size_string

class CodegenVisitor(TopoVisitor):

	def __init__(self):
		TopoVisitor.__init__(self)
		self.stmts=[]

	def atIDGSymbolic(self,node):
		print 'atIDGSymbolic'

	def atIDGDataArray(self,node):
		print 'atIDGDataArray'

	def atIDGERSpec(self,node): pass
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
	def atIDGIndexArray(self,node):
		index_array=node.data
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
		self.stmts.append(Statement('%s_ER=ER_ctor(%s,%s);'%(index_array.name,index_array.name,size_string)))

	def atIDGOutputERSpec(self,node): pass
#def gen_create_sigma(mapir):
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

	def atIDGERGCall(self,node): pass
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
