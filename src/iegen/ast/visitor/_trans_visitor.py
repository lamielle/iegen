from iegen.ast.visitor import DFVisitor

#Translation Visitor:
#Only works on a Set, not a Relation
#Given a Set, produces a collection of domain matrices,
#one for each PresSet in the Set.
#The result is placed in the 'mats' attribute
class TransVisitor(DFVisitor):
	def __init__(self,params):
		self.params=params
		self.num_params=len(params)
		self.at_var_tuple=False

	#Do nothing by default
	def defaultIn(self,node): pass
	def defaultOut(self,node): pass

	def inSet(self,node):
		self.mats=[]

	def inPresSet(self,node):
		self._mat=[]

	def outPresSet(self,node):
		self.mats.append(self._mat)

	def inRelation(self,node):
		raise ValueError('This visitor only works on Sets.')

	def inVarTuple(self,node):
		self.vars=[var.id for var in node.vars]
		self.num_vars=len(self.vars)
		self.num_cols=1+self.num_vars+self.num_params+1
		self.at_var_tuple=True

	def outVarTuple(self,node):
		self.at_var_tuple=False

	def inInequality(self,node):
		self._row=[0]*self.num_cols
		self._row[0]=1

	def outInequality(self,node):
		self._mat.append(self._row)

	def inEquality(self,node):
		self._row=[0]*self.num_cols
		self._row[0]=0

	def outEquality(self,node):
		self._mat.append(self._row)

	def inVarExp(self,node):
		if not self.at_var_tuple:
			#Calculate the position of this variable in the matrix
			if node.id in self.vars:
				pos=self.vars.index(node.id)+1
			elif node.id in self.params:
				pos=self.params.index(node.id)+self.num_vars+1
			else:
				raise ValueError('Existential variable in set.')

			#Assign this variable's coefficient to the matrix at the clculated position
			self._row[pos]=node.coeff

	#Cannot translate sets with functions
	def inFuncExp(self,node):
		raise ValueError('Translation of function expressions is not supported.')

	def inNormExp(self,node):
		#Set the last element in the row to the constant value of the expression
		self._row[-1]=node.const
