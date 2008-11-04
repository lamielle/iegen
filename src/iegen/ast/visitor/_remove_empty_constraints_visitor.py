from iegen.ast.visitor import DFVisitor

#Removes any empty constraints from a conjunction
#An empty constraint is defined as an Equality or Inequality
#with an expression equal to NormExp([],0)
class RemoveEmptyConstraintsVisitor(DFVisitor):
	def __init__(self):
		#By default we have not removed any constraints
		self.removed_constraint=False

	def inConjunction(self,node):
		#Filter out all empty constraints
		new_constraints=[constraint for constraint in node.constraints if not constraint.empty()]

		#See if we removed any constraints
		if len(new_constraints)!=len(node.constraints):
			self.removed_constraint=True

		#Update the constraint list
		node.constraints=new_constraints
