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

	def inIntExp(self,node):
		self.defaultIn(node)
	def outIntExp(self,node):
		self.defaultOut(node)

	def inIdExp(self,node):
		self.defaultIn(node)
	def outIdExp(self,node):
		self.defaultOut(node)

	def inUMinusExp(self,node):
		self.defaultIn(node)
	def outUMinusExp(self,node):
		self.defaultOut(node)

	def inMulExp(self,node):
		self.defaultIn(node)
	def outMulExp(self,node):
		self.defaultOut(node)

	def inPlusExp(self,node):
		self.defaultIn(node)
	def outPlusExp(self,node):
		self.defaultOut(node)

	def inMinusExp(self,node):
		self.defaultIn(node)
	def outMinusExp(self,node):
		self.defaultOut(node)

	def inIntMulExp(self,node):
		self.defaultIn(node)
	def outIntMulExp(self,node):
		self.defaultOut(node)

	def inFuncExp(self,node):
		self.defaultIn(node)
	def outFuncExp(self,node):
		self.defaultOut(node)
	#------------------------------------

	#---------- Visit methods ----------
	def visit(self,node):
		node.apply_visitor(self)

	def visitPresSet(self,node):
		self.inPresSet(node)
		node._setTuple.apply_visitor(self)
		node._conjunct.apply_visitor(self)
		self.outPresSet(node)

	def visitPresSetUnion(self,node):
		self.inPresSetUnion(node)
		for set in node._sets:
			set.apply_visitor(self)
		self.outPresSetUnion(node)

	def visitPresRelation(self,node):
		self.inPresRelation(node)
		node._inTuple.apply_visitor(self)
		node._outTuple.apply_visitor(self)
		node._conjunct.apply_visitor(self)
		self.outPresRelation(node)

	def visitPresRelationUnion(self,node):
		self.inPresRelationUnion(node)
		for relation in node._relations:
			relation.apply_visitor(self)
		self.outPresRelationUnion(node)

	def visitVarTuple(self,node):
		self.inVarTuple(node)
		self.outVarTuple(node)

	def visitConjunction(self,node):
		self.inConjunction(node)
		for conjunction in node._constraintList:
			conjunction.apply_visitor(self)
		self.outConjunction(node)

	def visitInequality(self,node):
		self.inInequality(node)
		node._exp.apply_visitor(self)
		self.outInequality(node)

	def visitEquality(self,node):
		self.inEquality(node)
		node._exp.apply_visitor(self)
		self.outEquality(node)

	def visitIntExp(self,node):
		self.inIntExp(node)
		self.outIntExp(node)

	def visitIdExp(self,node):
		self.inIdExp(node)
		self.outIdExp(node)

	def visitUMinusExp(self,node):
		self.inUMinusExp(node)
		node._exp.apply_visitor(self)
		self.outUMinusExp(node)

	def visitMulExp(self,node):
		self.inMulExp(node)
		node._lhs.apply_visitor(self)
		node._rhs.apply_visitor(self)
		self.outMulExp(node)

	def visitPlusExp(self,node):
		self.inPlusExp(node)
		node._lhs.apply_visitor(self)
		node._rhs.apply_visitor(self)
		self.outPlusExp(node)

	def visitMinusExp(self,node):
		self.inMinusExp(node)
		node._lhs.apply_visitor(self)
		node._rhs.apply_visitor(self)
		self.outMinusExp(node)

	def visitIntMulExp(self,node):
		self.inIntMulExp(node)
		node._int.apply_visitor(self)
		node._exp.apply_visitor(self)
		self.outIntMulExp(node)

	def visitFuncExp(self,node):
		self.inFuncExp(node)
		for exp in node._expList:
			exp.apply_visitor(self)
		self.outFuncExp(node)
	#-----------------------------------
