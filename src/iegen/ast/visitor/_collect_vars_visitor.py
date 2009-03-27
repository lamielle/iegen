from iegen.ast.visitor import DFVisitor

#Collects all tuple variables in a Set or Relation
#Places the list of sorted tuple variable strings in the vars field
class CollectVarsVisitor(DFVisitor):
	def __init__(self):
		self.vars=set()

		self.in_var_tuple=False

	def inVarTuple(self,node):
		self.in_var_tuple=True
	def outVarTuple(self,node):
		self.in_var_tuple=False

	def inVarExp(self,node):
		if self.in_var_tuple:
			self.vars.add(node.id)

	def _outFormula(self,node):
		self.vars=sorted(list(self.vars))

	def outSet(self,node):
		self._outFormula(node)
	def outRelation(self,node):
		self._outFormula(node)
