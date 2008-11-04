from iegen.ast.visitor import DFVisitor

#Removes any constraints that are tautologies
class RemoveTautologiesVisitor(DFVisitor):
	def __init__(self):
		#By default we have not removed any terms
		self.removed_tautology=False

	def inConjunction(self,node):
		#Create a new collection of constraints that are not tautologies
		new_constraints=[constraint for constraint in node.constraints if not constraint.is_tautology()]

		#See if any constraints were removed
		if len(new_constraints)!=len(node.constraints):
			self.removed_tautology=True

		#Use the new list of constraints in the conjunction
		node.constraints=new_constraints
