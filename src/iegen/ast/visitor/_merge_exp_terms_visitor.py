from iegen.ast.visitor import DFVisitor
from copy import deepcopy
from iegen.util import find_term

#Combines common terms in each NormExp
#For example, if a VarExp(1,'a') and a VarExp(3,'a') are present
#in the terms list of a NormExp, they will be combined into a
#single VarExp(4,'a')
class MergeExpTermsVisitor(DFVisitor):
	def __init__(self):
		#By default we have not merged any terms
		self.merged_terms=False

	def inNormExp(self,node):
		new_terms=[]

		#Look at each term in the terms collection
		for term in node.terms:
			#Search for a similar term is present in the new_terms
			pos=find_term(term,new_terms)

			#If one is not found, append the term
			if None is pos:
				new_terms.append(term)
			else:
				#Otherwise update the located term's coefficient
				new_terms[pos].coeff+=term.coeff
				self.merged_terms=True
		node.terms=new_terms
