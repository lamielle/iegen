from iegen.ast.visitor import DFVisitor

#Removes any duplicated formulas in either the Set.sets
#or the Relation.relations collections
class RemoveDuplicateFormulasVisitor(DFVisitor):
	def __init__(self):
		#By default we have not removed any formulas
		self.removed_formula=False

	def inSet(self,node):
		#Create a new list of unique sets
		new_sets=[]
		for set in node.sets:
			if set not in new_sets:
				new_sets.append(set)

		#See if any sets were removed
		if len(new_sets)!=len(node.sets):
			self.removed_formula=True

		#Use this new list as the list of sets
		node.sets=new_sets

	def inRelation(self,node):
		#Create a new list of unique relations
		new_relations=[]
		for relation in node.relations:
			if relation not in new_relations:
				new_relations.append(relation)

		#See if any relations were removed
		if len(new_relations)!=len(node.relations):
			self.removed_formula=True

		#Use this new list as the list of relations
		node.relations=new_relations
