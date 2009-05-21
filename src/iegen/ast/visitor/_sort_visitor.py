from iegen.ast.visitor import DFVisitor

class SortVisitor(DFVisitor):
	def __init__(self): pass

	def outSet(self,node):
		node.sets.sort()

	def outRelation(self,node):
		node.relations.sort()

	def outConjunction(self,node):
		node.constraints.sort()

	def outEquality(self,node):
		node._set_largest_exp()

	def outNormExp(self,node):
		node.terms.sort()
