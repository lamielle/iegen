from iegen.ast.visitor import DFVisitor

class IsTupleVarVisitor(DFVisitor):
	def __init__(self,var_name):
		self.in_var_tuple=False
		self.var_name=var_name
		self.is_tuple_var=False

	def inVarTuple(self,node):
		self.in_var_tuple=True
	def outVarTuple(self,node):
		self.in_var_tuple=False

	def inVarExp(self,node):
		if self.in_var_tuple:
			if self.var_name==node.id:
				self.is_tuple_var=True
