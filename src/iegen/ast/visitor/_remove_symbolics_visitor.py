from iegen.ast.visitor import DFVisitor

#Removes any duplicate or unused symbolic variables in PresSets and PresRelations
class RemoveSymbolicsVisitor(DFVisitor):
	def __init__(self):
		#By default we have not removed any formulas
		self.removed_symbolic=False

	def _inPresForm(self,node):
		new_syms=[]

		#Get all unique symbolic variables that are used
		for sym in  node.symbolics:
			if sym not in new_syms and node.is_constraint_var(sym.name):
				new_syms.append(sym)

		#See if any were removed
		if len(new_syms)!=len(node.symbolics):
			self.removed_symbolic=True

		#Update the node's symbolics list
		node.symbolics=new_syms

	def inPresSet(self,node):
		self._inPresForm(node)
	def inPresRelation(self,node):
		self._inPresForm(node)
