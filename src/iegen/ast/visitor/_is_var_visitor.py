from iegen.ast.visitor import DFVisitor

#Given a variable name, 'var_name', searches an AST
#for occurrences of that name in a VarExp or Symbolic.
#Symbolics, tuple variables, and constraints are all searched.

#If that name is found anywhere, 'is_var' is True
#Otherwise, 'is_var' is False

#If that name is found in a variable tuple, 'is_tuple_var' is True
#Otherwise, 'is_tuple_var' is False

#If that name is found in the symbolics, 'is_symbolic_var' is True
#Otherwise, 'is_symbolic_var' is False
class IsVarVisitor(DFVisitor):
	def __init__(self,var_name):
		self.var_name=var_name

		self.in_tuple_var=False

		self.is_var=False
		self.is_tuple_var=False
		self.is_symbolic_var=False

	def inVarTuple(self,node):
		self.in_var_tuple=True
	def outVarTuple(self,node):
		self.in_var_tuple=False

	def inVarExp(self,node):
		if self.var_name==node.id:
			self.is_var=True
			if self.in_var_tuple:
				self.is_tuple_var=True

	def inSymbolic(self,node):
		if self.var_name==node.name:
			self.is_var=True
			self.is_symbolic_var=True
