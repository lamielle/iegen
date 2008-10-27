# _visitor.py
#
# Visitor class for traversing an AST of a program

# Alan LaMielle 10/20/2008

#---------- Depth First Visitor ----------
class DFVisitor(object):

	#---------- Default In/Out Methods ----------
	#Do nothing by default
	def defaultIn(self,node): pass
	def defaultOut(self,node): pass
	#--------------------------------------------

	#---------- In/Out Methods ----------
	def inProgram(self,node):
		self.defaultIn(node)
	def outProgram(self,node):
		self.defaultOut(node)

	def inFunction(self,node):
		self.defaultIn(node)
	def outFunction(self,node):
		self.defaultOut(node)

	def inStatement(self,node):
		self.defaultIn(node)
	def outStatement(self,node):
		self.defaultOut(node)

	def inVarDecl(self,node):
		self.defaultIn(node)
	def outVarDecl(self,node):
		self.defaultOut(node)

	def inComment(self,node):
		self.defaultIn(node)
	def outComment(self,node):
		self.defaultOut(node)
	#------------------------------------

	#---------- Visit methods ----------
	def visit(self,node):
		node.apply_visitor(self)
		return self

	def visitProgram(self,node):
		self.inProgram(node)
		for statement in node.preamble:
			statement.apply_visitor(self)
		for function in node.functions:
			function.apply_visitor(self)
		self.outProgram(node)

	def visitFunction(self,node):
		self.inFunction(node)
		for statement in node.body:
			statement.apply_visitor(self)
		self.outFunction(node)

	def visitStatement(self,node):
		self.inStatement(node)
		self.outStatement(node)

	def visitVarDecl(self,node):
		self.inVarDecl(node)
		self.outVarDecl(node)

	def visitComment(self,node):
		self.inComment(node)
		self.outComment(node)
	#-----------------------------------
#-----------------------------------------
