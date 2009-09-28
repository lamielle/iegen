from iegen.ast.visitor import DFVisitor

#Collects variable names in a Set or Relation
#If all_vars is True, all variable names (free, tuple, and symbolic) are collected
#If all_vars if False, Collects all tuple variables
#Places the list of sorted variable name strings in the vars field
class CollectVarsVisitor(DFVisitor):
	def __init__(self,all_vars=False):
		self.all_vars=all_vars

		self.vars=set()

		self.in_var_tuple=False

	def inVarTuple(self,node):
		self.in_var_tuple=True
	def outVarTuple(self,node):
		self.in_var_tuple=False

	def inVarExp(self,node):
		if self.in_var_tuple or self.all_vars:
			self.vars.add(node.id)

	def _inFormula(self,node):
		self.vars=set(self.vars)

	def inSet(self,node):
		self._inFormula(node)
	def inRelation(self,node):
		self._inFormula(node)

	def _outFormula(self,node):
		self.vars=sorted(list(self.vars))

	def outSet(self,node):
		self._outFormula(node)
	def outRelation(self,node):
		self._outFormula(node)
