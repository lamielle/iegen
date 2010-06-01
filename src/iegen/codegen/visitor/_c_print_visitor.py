from iegen.codegen.visitor import DFVisitor

class CPrintVisitor(DFVisitor):
	def __init__(self,code,indent):
		DFVisitor.__init__(self)
		self.code=code
		self.indent=indent

	def _get_param_string(self,param):
		start_end=[' ','*']
		if param.type[-1] in start_end or param.name[0] in start_end:
			return '%s%s'%(param.type,param.name)
		elif '%' in param.type:
			return param.type%(param.name)
		else:
			return '%s %s'%(param.type,param.name)

	def betweenFunctions(self,node):
		print >>self.code

	def inFunction(self,node):
		self.code.write('%s %s('%(node.return_type,node.name))
	def betweenParameters(self,node):
		self.code.write(',')
	def betweenParamsStatements(self,node):
		self.code.write(')\n{\n')
	def outFunction(self,node):
		self.code.write('}\n')

	def inParameter(self,node):
		self.code.write(self._get_param_string(node))

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
		var_vals=[(node.var_names[i],node.values[i]) for i in xrange(len(node.values))]
		for var_name,value in var_vals:
			strings+=(var_name,value)
		for var_name in node.var_names[len(node.values):]:
			strings+=(var_name,)
		print >>self.code,decl%(strings)

	def inComment(self,node):
		indent= self.indent if self.in_function else ''
		print >>self.code,indent+'// '+node.text
