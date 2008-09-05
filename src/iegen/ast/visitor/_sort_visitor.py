from iegen.ast.visitor import DFVisitor

class SortVisitor(DFVisitor):
	def __init__(self): pass

	#Do nothing by default
	def defaultIn(self,node): pass
	def defaultOut(self,node): pass

	def outSet(self,node):
		node.sets.sort()

	def outRelation(self,node):
		node.relations.sort()

	def outConjunction(self,node):
		node.constraint_list.sort()

	def outEquality(self,node):
		node._set_largest_exp()

	def outFuncExp(self,node):
		node.args.sort()

	def outNormExp(self,node):
		node.terms.sort()
