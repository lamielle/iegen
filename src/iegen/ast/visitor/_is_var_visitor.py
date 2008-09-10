from iegen.ast.visitor import DFVisitor

class IsVarVisitor(DFVisitor):
	def __init__(self,var_name):
		self.var_name=var_name
		self.is_var=False

	def inVarExp(self,node):
		if self.var_name==node.id:
			self.is_var=True

	def inSymbolic(self,node):
		if self.var_name==node.name:
			self.is_var=True
