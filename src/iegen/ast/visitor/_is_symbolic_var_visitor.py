from iegen.ast.visitor import DFVisitor

#Given a variable name, 'var_name', searches all symbolics of a
#Set/Relation for that name.
#If that name is found in the symbolics, True is placed in 'is_symbolic_var'
#Otherwise, False is placed in 'is_symbolic_var'
class IsSymbolicVarVisitor(DFVisitor):
	def __init__(self,var_name):
		self.var_name=var_name
		self.is_symbolic_var=False

	def inSymbolic(self,node):
		if self.var_name==node.name:
			self.is_symbolic_var=True
