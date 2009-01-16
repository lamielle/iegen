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

	def atIDGERSpec(self,node):
		print 'atIDGERSpec: %s'%node.key

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
