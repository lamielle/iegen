from iegen.codegen.visitor import DFVisitor

class CPrintVisitor(DFVisitor):
	def __init__(self,code,indent):
		self.code=code
		self.indent=indent
		self.in_function=False

	def _get_arg_string(self,args):
		var_strings=[]
		for arg in args:
			print 'arg.var_names=%s'%(arg.var_names)
			for var_name in arg.var_names:
				print 'appending %s'%(arg.type+var_name)
				var_strings.append(arg.type+var_name)
		return ('%s,'*len(var_strings))[:-1]%tuple(var_strings)

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

	def inVarDecl(self,node):
		decl='%s%s '
		decl+=('%s=%s,'*len(node.values))
		decl+=('%s,'*(len(node.var_names)-len(node.values)))
		decl=decl[:-1]+';'
		strings=(self.indent,node.type)
		var_vals=[(node.var_names[i],node.values[i]) for i in range(len(node.values))]
		for var_name,value in var_vals:
			strings+=(var_name,value)
		for var_name in node.var_names[len(node.values):]:
			strings+=(var_name,)
		print >>self.code,decl%(strings)

	def inComment(self,node):
		print >>self.code,self.indent+'/* '+node.text+' */'
