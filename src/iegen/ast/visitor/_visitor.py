# visitor.py
#
# Visitor classes for traversing an AST of a presburger set or relation

# Alan LaMielle 7/30/08

from iegen import IEGenObject

#---------- Depth First Visitor ----------
class DFVisitor(IEGenObject):

	#---------- Default In/Out Methods ----------
	#Do nothing by default
	def defaultIn(self,node): pass
	def defaultOut(self,node): pass
	def defaultBetween(self,node): pass
	#--------------------------------------------

	#---------- In/Out Methods ----------
	def inSet(self,node):
		self.defaultIn(node)
	def outSet(self,node):
		self.defaultOut(node)

	def inPresSet(self,node):
		self.defaultIn(node)
	def outPresSet(self,node):
		self.defaultOut(node)

	def inRelation(self,node):
		self.defaultIn(node)
	def outRelation(self,node):
		self.defaultOut(node)

	def inPresRelation(self,node):
		self.defaultIn(node)
	def outPresRelation(self,node):
		self.defaultOut(node)

	def inSymbolic(self,node):
		self.defaultIn(node)
	def outSymbolic(self,node):
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
	def betweenNormExp(self,node):
		self.defaultBetween(node)
	#------------------------------------

	#---------- Visit methods ----------
	def visit(self,node):
		node.apply_visitor(self)
		return self

	def visitSet(self,node):
		self.inSet(node)
		for set in node.sets:
			set.apply_visitor(self)
		self.outSet(node)

	def visitPresSet(self,node):
		self.inPresSet(node)
		node.tuple_set.apply_visitor(self)
		node.conjunct.apply_visitor(self)
		for symbolic in node.symbolics:
			symbolic.apply_visitor(self)
		self.outPresSet(node)

	def visitRelation(self,node):
		self.inRelation(node)
		for relation in node.relations:
			relation.apply_visitor(self)
		self.outRelation(node)

	def visitPresRelation(self,node):
		self.inPresRelation(node)
		node.tuple_in.apply_visitor(self)
		node.tuple_out.apply_visitor(self)
		node.conjunct.apply_visitor(self)
		for symbolic in node.symbolics:
			symbolic.apply_visitor(self)
		self.outPresRelation(node)

	def visitSymbolic(self,node):
		self.inSymbolic(node)
		self.outSymbolic(node)

	def visitVarTuple(self,node):
		self.inVarTuple(node)
		for var in node.vars:
			var.apply_visitor(self)
		self.outVarTuple(node)

	def visitConjunction(self,node):
		self.inConjunction(node)
		for conjunction in node.constraints:
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
		for i in xrange(len(node.terms)):
			term=node.terms[i]
			term.apply_visitor(self)
			if i<len(node.terms)-1: self.betweenNormExp(node)
		self.outNormExp(node)
	#-----------------------------------
#-----------------------------------------
