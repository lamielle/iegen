# _visitor.py
#
# Visitor class for traversing an AST of a program

# Alan LaMielle 10/20/2008

#---------- Depth First Visitor ----------
class DFVisitor(object):

	def __init__(self):
		#---------- State members ----------
		#Will be True if we are within a function, False otherwise
		self.in_function=False
		#-----------------------------------

	#---------- Default In/Out Methods ----------
	#Do nothing by default
	def defaultIn(self,node): pass
	def defaultOut(self,node): pass
	def defaultBetween(self,node): pass
	#--------------------------------------------

	#---------- In/Out/Between Methods ----------
	def inProgram(self,node):
		self.defaultIn(node)
	def outProgram(self,node):
		self.defaultOut(node)
	def betweenFunctions(self,node):
		self.defaultBetween(node)

	def inFunction(self,node):
		self.defaultIn(node)
	def outFunction(self,node):
		self.defaultOut(node)
	def betweenParamsStatements(self,node):
		self.defaultBetween(node)

	def inParameter(self,node):
		self.defaultIn(node)
	def outParameter(self,node):
		self.defaultOut(node)
	def betweenParameters(self,node):
		self.defaultBetween(node)

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
		from iegen.util import iter_islast
		self.inProgram(node)
		for statement in node.preamble:
			statement.apply_visitor(self)
		for function,is_last in iter_islast(node.functions):
			function.apply_visitor(self)
			if not is_last:
				self.betweenFunctions(node)
		self.outProgram(node)

	def visitFunction(self,node):
		from iegen.util import iter_islast
		self.in_function=True
		self.inFunction(node)
		for param,is_last in iter_islast(node.params):
			param.apply_visitor(self)
			if not is_last:
				self.betweenParameters(param)
		self.betweenParamsStatements(node)
		for statement in node.body:
			statement.apply_visitor(self)
		self.outFunction(node)
		self.in_function=False

	def visitParameter(self,node):
		self.inParameter(node)
		self.outParameter(node)

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
