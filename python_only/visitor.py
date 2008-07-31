# visitor.py
#
# Visitor classes for traversing an AST of a presburger set or relation

# Alan LaMielle 7/30/08

#---------- Depth First Visitor ----------
class DFVisitor(object):

	#---------- Visit methods ----------
	def visit(self,node):
		node.apply(self)

	def visitPresSet(self,node):
		self.inPresSet(node)
		node._setTuple.apply(self)
		node._conjunct.apply(self)
		self.outPresSet(node)

	def visitPresSetUnion(self,node):
		self.inPresSetUnion(node)
		for set in node._sets:
			set.apply(self)
		self.outPresSetUnion(node)

	def visitPresRelation(self,node):
		self.inPresRelation(node)
		node._inTuple.apply(self)
		node._outTuple.apply(self)
		node._conjunct.apply(self)
		self.outPresRelation(node)

	def visitPresRelationUnion(self,node):
		self.inPresRelationUnion(node)
		for relation in node._relations:
			relation.apply(self)
		self.outPresRelationUnion(node)

	def visitVarTuple(self,node):
		self.inVarTuple(node)
		self.outVarTuple(node)

	def visitConjunction(self,node):
		pass

	def visitInequality(self,node):
		pass

	def visitEquality(self,node):
		pass

	def visitIntExp(self,node):
		pass

	def visitIdExp(self,node):
		pass

	def visitUMinusExp(self,node):
		pass

	def visitMulExp(self,node):
		pass

	def visitPlusExp(self,node):
		pass

	def visitMinusExp(self,node):
		pass

	def visitIntMulExp(self,node):
		pass

	def visitFuncExp(self,node):
		pass
	#-----------------------------------
