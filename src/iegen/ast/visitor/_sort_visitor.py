from iegen.ast.visitor import DFVisitor

class SortVisitor(DFVisitor):
	def __init__(self): pass

	#Do nothing by default
	def defaultIn(self,node): pass
	def defaultOut(self,node): pass

	def inSet(self,node):
		node.sets.sort()

	def inRelation(self,node):
		node.relations.sort()

	def inConjunction(self,node):
		node.constraint_list.sort()

	def inEquality(self,node):
		node._set_largest_exp()

	def inFuncExp(self,node):
		node.args.sort()

	def inNormExp(self,node):
		node.terms.sort()
