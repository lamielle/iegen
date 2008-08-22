# visitor.py
#
# Visitor classes for traversing an AST of a presburger set or relation

# Alan LaMielle 7/30/08

#---------- Depth First Visitor ----------
class DFVisitor(object):

	#---------- Default In/Out Methods ----------
	def defaultIn(self,node):
		print 'In:',node
	def defaultOut(self,node):
		print 'Out:',node
	#--------------------------------------------

	#---------- In/Out Methods ----------
	def inPresSet(self,node):
		self.defaultIn(node)
	def outPresSet(self,node):
		self.defaultOut(node)

	def inPresSetUnion(self,node):
		self.defaultIn(node)
	def outPresSetUnion(self,node):
		self.defaultOut(node)

	def inPresRelation(self,node):
		self.defaultIn(node)
	def outPresRelation(self,node):
		self.defaultOut(node)

	def inPresRelationUnion(self,node):
		self.defaultIn(node)
	def outPresRelationUnion(self,node):
		self.defaultOut(node)

	def inVarTuple(self,node):
		self.defaultIn(node)
	def outVarTuple(self,node):
		self.defaultOut(node)

	def inConjunction(self,node):
		self.defaultIn(node)
	def outConjunction(self,node):
		self.defaultOut(node)

	def inInequality(self,node):
		self.defaultIn(node)
	def outInequality(self,node):
		self.defaultOut(node)

	def inEquality(self,node):
		self.defaultIn(node)
	def outEquality(self,node):
		self.defaultOut(node)

	def inVarExp(self,node):
		self.defaultIn(node)
	def outVarExp(self,node):
		self.defaultOut(node)

	def inFuncExp(self,node):
		self.defaultIn(node)
	def outFuncExp(self,node):
		self.defaultOut(node)

	def inNormExp(self,node):
		self.defaultIn(node)
	def outNormExp(self,node):
		self.defaultOut(node)
	#------------------------------------

	#---------- Visit methods ----------
	def visit(self,node):
		node.apply_visitor(self)

	def visitPresSet(self,node):
		self.inPresSet(node)
		node.set_tuple.apply_visitor(self)
		node.conjunct.apply_visitor(self)
		self.outPresSet(node)

	def visitPresSetUnion(self,node):
		self.inPresSetUnion(node)
		for set in node.sets:
			set.apply_visitor(self)
		self.outPresSetUnion(node)

	def visitPresRelation(self,node):
		self.inPresRelation(node)
		node.in_tuple.apply_visitor(self)
		node.out_tuple.apply_visitor(self)
		node.conjunct.apply_visitor(self)
		self.outPresRelation(node)

	def visitPresRelationUnion(self,node):
		self.inPresRelationUnion(node)
		for relation in node.relations:
			relation.apply_visitor(self)
		self.outPresRelationUnion(node)

	def visitVarTuple(self,node):
		self.inVarTuple(node)
		self.outVarTuple(node)

	def visitConjunction(self,node):
		self.inConjunction(node)
		for conjunction in node.constraint_list:
			conjunction.apply_visitor(self)
		self.outConjunction(node)

	def visitInequality(self,node):
		self.inInequality(node)
		node.exp.apply_visitor(self)
		self.outInequality(node)

	def visitEquality(self,node):
		self.inEquality(node)
		node.exp.apply_visitor(self)
		self.outEquality(node)

	def visitVarExp(self,node):
		self.inVarExp(node)
		self.outVarExp(node)

	def visitFuncExp(self,node):
		self.inFuncExp(node)
		for exp in node.args:
			exp.apply_visitor(self)
		self.outFuncExp(node)

	def visitNormExp(self,node):
		self.inNormExp(node)
		for term in node.terms:
			term.apply_visitor(self)
		self.outNormExp(node)
	#-----------------------------------
