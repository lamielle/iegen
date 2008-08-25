from iegen.ast.visitor import DFVisitor

class TransVisitor(DFVisitor):
	def __init__(self,params):
		self.params=params
		self.num_params=len(params)

	#Do nothing by default
	def defaultIn(self,node):
		pass
	def defaultOut(self,node):
		pass

	def inSet(self,node):
		self.mat=[]

	def inRelation(self,node):
		raise ValueError('This visitor only works on Sets.')

	def inVarTuple(self,node):
		self.vars=node.id_list
		self.num_vars=len(self.vars)
		self.num_cols=1+self.num_vars+self.num_params+1

	def inInequality(self,node):
		self.row=[0]*self.num_cols
		self.row[0]=1

	def outInequality(self,node):
		self.mat.append(self.row)

	def inEquality(self,node):
		self.row=[0]*self.num_cols
		self.row[0]=0

	def outEquality(self,node):
		self.mat.append(self.row)

	def inVarExp(self,node):
		#Calculate the position of this variable in the matrix
		if node.id in self.vars:
			pos=self.vars.index(node.id)+1
		elif node.id in self.params:
			pos=self.params.index(node.id)+self.num_vars+1
		else:
			raise ValueError('Existential variable in set.')

		#Assign this variable's coefficient to the matrix at the clculated position
		self.row[pos]=node.coeff

	#Cannot translate sets with functions
	def inFuncExp(self,node):
		raise ValueError('Translation of function expressions is not supported.')

	def inNormExp(self,node):
		#Set the last element in the row to the constant value of the expression
		self.row[-1]=node.const
