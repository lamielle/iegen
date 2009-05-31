from iegen.ast.visitor import DFVisitor

#Translation Visitor: Translate the visited Set or Relation into
# a matrix representing a domain or scattering function in
# CLooG format.
#
#Briefly, this format is a matrix that represents a polyhedron.
#Each row of the matrix is one constraint, either equality or inequality.
#
#For domain constraint matrices, the columns are ordered as follows:
#eq/in iterators parameters constant
#Col 1: {0,1} 0=equality 1=inequality
#Col 2-num iterators+1: coefficients on the iterators in this constraint
#Col num iterators+2-num iterators+num parameters+1: coefficients on the
# parameters (symbolics)
#Col num iterators+num parameters+2: constraint constant
#
#For scattering function constraint matrices, the columns are ordered as follows:
#eq/in out-vars in-vars parameters constant
#Col 1: {0,1} 0=equality 1=inequality
#Col 2-num out-vars+1: identity row (1 for associated out var, 0s elsewhere)
#Col num out-vars+2-num out-vars num in-vars+1: input var coefficients
#Col num out-vars+num in-vars+2-num out-vars+num in-vars+num params+1: parameter coefficients
#Col num out-vars+num in-vars+num params+2: constraint constant
#
#Multiple conjunctions of PresSet objects in the Set (for a domain)
# will be translated to a collection of constraint matrices
# (a union of polyhedra).
#Multiple conjunctions of PresRelation objects in the Relation
# are not supported, a ValueError will be raised if this is detected.
#
#This visitor requires as input a collection of names of parameters.
#This is needed so that multiple uses of this visitor have the same parameter
# columns in common.
#
#The result of this visitor is placed in the mats attribute.
#In the case of a domain (Set) this may have multiple matrices.
#In the case of a scattering function (Relation) this will have a single matrix.
class TransVisitor(DFVisitor):
	def __init__(self,params):
		self.params=params

		self.at_var_tuple=False

		#---------- Visiting state variables ----------
		#Are we within a Set?
		self.in_set=False

		#Are we within a Relation?
		self.in_relation=False

		#Dictionary of name -> column position mappings
		self.name_dict=None
		#----------------------------------------------

	def calc_name_dict(self,var_names):
		names=var_names+self.params
		name_dict={}

		for pos,name in enumerate(names):
			name_dict[name]=pos+1

		return name_dict

	#Calculates the number of columns in the matrix we are creating
	def calc_num_cols(self):
		#1 column for the eq/in column
		#len(self.name_dict) columns
		#1 column for the constant column
		return 1+len(self.name_dict)+1

	def inSet(self,node):
		#Starting to visit a Set, init the result list
		self.mats=[]

	def inPresSet(self,node):
		#Starting to translate a PresSet to a matrix, init the result matrix
		self._mat=[]

		#Build mappings for tuple variables and symbolics to column index
		self.name_dict=self.calc_name_dict([var.id for var in node.tuple_set.vars])

	def outPresSet(self,node):
		#Append the current result matrix to the result matrix collection
		self.mats.append(self._mat)

	def inRelation(self,node):
		#Make sure this Relation has only a single conjunction
		if len(node.relations)!=1:
			raise ValueError('Translation of multiple Relation conjunctions is not supported')

	def inPresRelation(self,node):
		#Starting to translate a PresRelation to a matrix, init the result matrix
		self._mat=[]

		#Build mappings for tuple variables and symbolics to column index
		self.name_dict=self.calc_name_dict([var.id for var in node.tuple_out.vars+node.tuple_in.vars])

	def outPresRelation(self,node):
		self.mat=self._mat

	def inVarTuple(self,node):
		self.at_var_tuple=True

	def outVarTuple(self,node):
		self.at_var_tuple=False

	def inInequality(self,node):
		#Create a new row for an inequality constraint
		self._row=[0]*self.calc_num_cols()
		self._row[0]=1

	def outInequality(self,node):
		self._mat.append(self._row)

	def inEquality(self,node):
		#Create a new row for an equality constraint
		self._row=[0]*self.calc_num_cols()
		self._row[0]=0

	def outEquality(self,node):
		self._mat.append(self._row)

	def inVarExp(self,node):
		if not self.at_var_tuple:
			#Get the column of this variable in the matrix
			try:
				pos=self.name_dict[node.id]

				#Assign this variable's coefficient to the matrix in the proper column
				self._row[pos]=node.coeff
			except KeyError,e:
				raise ValueError("Variable '%s' is either a free variable or was not specified as a parameter"%(node.id))

	#Cannot translate formulas with functions
	def inFuncExp(self,node):
		raise ValueError('Translation of function expressions is not supported.')

	def inNormExp(self,node):
		#Set the last element in the row to the constant value of the expression
		self._row[-1]=node.const
