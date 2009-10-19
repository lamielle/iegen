from iegen.ast.visitor import DFVisitor

#Sparse Translation Visitor: Translate the visited Set or Relation into
# a SparseSet or SparseRelation.
class SparseTransVisitor(DFVisitor):
	def __init__(self,sparse_formula):

		self.sparse_formula=sparse_formula

		#---------- Visiting state variables ----------
		#Are we within a variable tuple?
		self.in_var_tuple=False

		#Are we within a constraint?
		self.in_constraint=False
		#----------------------------------------------

	def inSet(self,node):
		raise ValueError('Translation of a Set not supported')

	def inRelation(self,node):
		raise ValueError('Translation of a Relation not supported')

	def inPresSet(self,node): pass

	def outPresSet(self,node): pass


	def inPresRelation(self,node): pass

	def outPresRelation(self,node): pass

	def inVarTuple(self,node):
		self.in_var_tuple=True

	def outVarTuple(self,node):
		self.in_var_tuple=False

	def _inConstraint(self,node):
		self.in_constraint=True
		self.constraint_coeff=[0]*self.sparse_formula.num_columns()

	def _outConstraint(self,node):
		self.in_constraint=False

	def inEquality(self,node):
		self._inConstraint(node)

	def outEquality(self,node):
		self._outConstraint(node)
		self.sparse_formula.add_equality(self.constraint_coeff)

	def inInequality(self,node):
		self._inConstraint(node)

	def outInequality(self,node):
		self._outConstraint(node)
		self.sparse_formula.add_inequality(self.constraint_coeff)

	def inVarExp(self,node):
		if self.in_constraint:
			self.constraint_coeff[self.sparse_formula.get_column(node.id)]=node.coeff

	def inFuncExp(self,node):
		raise ValueError('Translation of function expressions not implemented yet!')

	def outNormExp(self,node):
		self.constraint_coeff[self.sparse_formula.get_constant_column()]=node.const
