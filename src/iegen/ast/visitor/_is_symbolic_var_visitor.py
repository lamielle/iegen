from iegen.ast.visitor import DFVisitor

class IsSymbolicVarVisitor(DFVisitor):
	def __init__(self,var_name):
		self.var_name=var_name
		self.is_symbolic_var=False

	def inSymbolic(self,node):
		if self.var_name==node.name:
			self.is_symbolic_var=True
