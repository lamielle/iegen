from iegen.ast.visitor import DFVisitor

#Sparse Translation Visitor: Translate the visited Set or Relation into
# a SparseSet or SparseRelation.
class SparseTransVisitor(DFVisitor):
	def __init__(self,sparse_formula):

		#---------- Visiting state variables ----------
		#Are we within a variable tuple?
		self.at_var_tuple=False
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
		self.at_var_tuple=True

	def outVarTuple(self,node):
		self.at_var_tuple=False

	def inInequality(self,node): pass

	def outInequality(self,node): pass

	def inEquality(self,node): pass

	def outEquality(self,node): pass

	def inVarExp(self,node):
		if self.at_var_tuple: pass
		else: pass

	def inFuncExp(self,node): pass

	def inNormExp(self,node): pass
