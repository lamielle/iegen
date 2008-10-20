from iegen.codegen.visitor import DFVisitor

class CPrintVisitor(DFVisitor):
	def __init__(self,code,indent):
		self.code=code
		self.indent=indent
		self.in_function=False

	def _get_arg_string(self,args):
		return ('%s,'*len(args))[:-1]%tuple(args)

	def inFunction(self,node):
		print >>self.code,'%s %s(%s)'%(node.res,node.name,self._get_arg_string(node.args))
		print >>self.code,'{'
		self.in_function=True
	def outFunction(self,node):
		print >>self.code,'}'
		self.in_function=False

	def inStatement(self,node):
		if self.in_function and len(node.text)>0:
			print >>self.code,self.indent+node.text
		else:
			print >>self.code,node.text
