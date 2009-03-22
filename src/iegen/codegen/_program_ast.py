#_program_ast.py:
#Classes for representing the programs being generated
#rather than simply printing to a buffer

from iegen import IEGenObject

class ProgramASTNode(IEGenObject):
	pass

#Represents a whole program
class Program(ProgramASTNode):
	__slots__=('preamble','functions')

	def __init__(self):
		self.preamble=[]
		self.functions=[]

	def apply_visitor(self,visitor):
		visitor.visitProgram(self)

#Represents a function definition
class Function(ProgramASTNode):
	__slots__=('name','return_type','params','body')

	def __init__(self,name,return_type,params):
		self.name=name
		self.return_type=return_type
		self.params=params
		self.body=[]

	def newline(self):
		from iegen.codegen import Statement
		self.body.append(Statement())

	def apply_visitor(self,visitor):
		visitor.visitFunction(self)

#Represents a parameter to a function
class Parameter(ProgramASTNode):
	__slots__=('type','name')

	def __init__(self,type,name):
		self.type=type
		self.name=name

	def apply_visitor(self,visitor):
		visitor.visitParameter(self)

#Represents a statement
class Statement(ProgramASTNode):
	__slots__=('text',)

	def __init__(self,text=''):
		self.text=text

	def apply_visitor(self,visitor):
		visitor.visitStatement(self)

#Represents a variable declaration
class VarDecl(ProgramASTNode):
	__slots__=('type','var_names','values')

	def __init__(self,type,var_names=None,values=None):
		self.type=type
		self.var_names=[] if var_names is None else var_names
		self.values=[] if values is None else values

	def apply_visitor(self,visitor):
		visitor.visitVarDecl(self)

#Represents a comment
class Comment(ProgramASTNode):
	__slots__=('text',)

	def __init__(self,text):
		self.text=text

	def apply_visitor(self,visitor):
		visitor.visitComment(self)
