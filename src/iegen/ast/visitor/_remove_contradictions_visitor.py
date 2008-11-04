from iegen.ast.visitor import DFVisitor

class RemoveContradictionsVisitor(DFVisitor):
	def __init__(self):
		#By default we have not removed any terms
		self.removed_contradiction=False

	def _inFormula(self,node):
		from copy import deepcopy
		from iegen.ast import Equality,NormExp

		#Remove all contradictory formulas
		new_formulas=[formula for formula in node.formulas if not formula.is_contradiction()]

		#See if we removed any formulas
		if len(new_formulas)!=len(node.formulas):
			#If we removed all of the formulas, add one back that is a contradiction
			if 0==len(new_formulas):
				empty_formula=deepcopy(node.formulas[0])
				empty_formula.conjunct.constraints=[]
				empty_formula.conjunct.constraints.append(Equality(NormExp([],1)))
				new_formulas.append(empty_formula)


			#Use the new list of formulas
			orig_node=deepcopy(node)
			node.formulas=new_formulas

			#Make sure we actually changed the node
			if node!=orig_node:
				self.removed_contradiction=True

	def inSet(self,node):
		from iegen import Set
		self._inFormula(node)

	def inRelation(self,node):
		from iegen import Relation
		self._inFormula(node)
