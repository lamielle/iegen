#_program_ast.py:
#Classes for representing the programs being generated
#rather than simply printing to a buffer

#Represents a whole program
class Program(object):
	__slots__=('preamble','functions')

	def __init__(self):
		self.preamble=[]
		self.functions=[]

	def apply_visitor(self,visitor):
		visitor.visitProgram(self)

#Represents a function definition
class Function(object):
	__slots=('name','res','args','body')

	def __init__(self,name,res,args):
		self.name=name
		self.res=res
		self.args=args
		self.body=[]

	def apply_visitor(self,visitor):
		visitor.visitFunction(self)

#Represents a statement
class Statement(object):
	__slots__=('text',)

	def __init__(self,text=''):
		self.text=text

	def apply_visitor(self,visitor):
		visitor.visitStatement(self)

#Represents a variable declaration
class VarDecl(object):
	__slots__=('type','var_names','values')

	def __init__(self,type,var_names=None,values=None):
		self.type=type
		self.var_names=[] if var_names is None else var_names
		self.values=[] if values is None else values

	def apply_visitor(self,visitor):
		visitor.visitVarDecl(self)

#Represents a comment
class Comment(object):
	__slots__=('text',)

	def __init__(self,text):
		self.text=text

	def apply_visitor(self,visitor):
		visitor.visitComment(self)
