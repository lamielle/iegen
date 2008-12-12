from iegen.ast.visitor import DFVisitor

class CollectSymbolicsVisitor(DFVisitor):
	def __init__(self):
		self.symbolics=set()

	def _outFormula(self,node):
		self.symbolics=sorted(list(self.symbolics))

	def outSet(self,node):
		self._outFormula(node)
	def outRelation(self,node):
		self._outFormula(node)

	def _outPresFormula(self,node):
		self.symbolics=self.symbolics.union(set([sym.name for sym in node.symbolics]))

	def outPresSet(self,node):
		self._outPresFormula(node)
	def outPresRelation(self,node):
		self._outPresFormula(node)
