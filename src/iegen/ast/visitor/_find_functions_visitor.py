from iegen.ast.visitor import DFVisitor

class FindFunctionsVisitor(DFVisitor):
	def __init__(self):
		self.functions=set()

	def _outFormula(self,node):
		self.functions=sorted(list(self.functions))

	def outSet(self,node):
		self._outFormula(node)
	def outRelation(self,node):
		self._outFormula(node)

	def inFuncExp(self,node):
		self.functions.add(node.name)
