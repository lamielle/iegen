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
		print node.body
		for statement in node.body:
			print statement,statement.__class__
			statement.apply_visitor(self)
		self.outFunction(node)

	def visitStatement(self,node):
		self.inStatement(node)
		self.outStatement(node)
	#-----------------------------------
#-----------------------------------------
