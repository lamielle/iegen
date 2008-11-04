from iegen.ast.visitor import DFVisitor

#Removes any duplicated formulas in either the Set.sets
#or the Relation.relations collections
#These two collections are really just the Formula.formulas list
#so we can combine common code using this list instead
class RemoveDuplicateFormulasVisitor(DFVisitor):
	def __init__(self):
		#By default we have not removed any formulas
		self.removed_formula=False

	def _inFormula(self,node):
		#Create a new list of unique formulas
		new_formulas=[]
		for formula in node.formulas:
			if formula not in new_formulas:
				new_formulas.append(formula)

		#See if any formulas were removed
		if len(new_formulas)!=len(node.formulas):
			self.removed_formula=True

			#Use this new list as the list of formulas
			node.formulas=new_formulas

	def inSet(self,node):
		self._inFormula(node)

	def inRelation(self,node):
		self._inFormula(node)
