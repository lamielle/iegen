from iegen.ast.visitor import DFVisitor

#Given a variable name, 'var_name', searches a Set/Relation
#for any occurrence of that name in a VarExp or Symbolic in.
#Symbolics, tuple variables, and constraints are all searched.
#If that name is found, True is placed in 'is_var'
#Otherwise, False is placed in 'is_var'
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
