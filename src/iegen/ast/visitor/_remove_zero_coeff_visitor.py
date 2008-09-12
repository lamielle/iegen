from iegen.ast.visitor import DFVisitor

#Removes any terms in a NormExp that have a coefficient of 0
class RemoveZeroCoeffVisitor(DFVisitor):
	def __init__(self):
		#By default we have not removed any terms
		self.removed_term=False

	def inNormExp(self,node):
		#Filter out all zero coefficient terms
		new_terms=[term for term in node.terms if 0!=term.coeff]

		#See if we removed and terms
		if len(new_terms)!=len(node.terms):
			self.removed_term=True

		#Update the term list
		node.terms=new_terms
