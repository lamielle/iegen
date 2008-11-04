from iegen.ast.visitor import DFVisitor

#Removes any duplicated formulas in either the Set.sets
#or the Relation.relations collections
class RemoveDuplicateConstraintsVisitor(DFVisitor):
	def __init__(self):
		#By default we have not removed any formulas
		self.removed_constraint=False

	def inConjunction(self,node):
		#Create a new list of unique constraints
		new_constraints=[]
		for constraint in node.constraints:
			if constraint not in new_constraints:
				new_constraints.append(constraint)

		#See if any constraints were removed
		if len(new_constraints)!=len(node.constraints):
			self.removed_constraint=True

			#Use this new list as the list of constraints
			node.constraints=new_constraints
