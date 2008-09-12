from iegen.ast.visitor import DFVisitor
from copy import deepcopy

#Combines common terms in each NormExp
#For example, if a VarExp(1,'a') and a VarExp(3,'a') are present
#in the terms list of a NormExp, they will be combined into a
#single VarExp(4,'a')
class MergeExpTermsVisitor(DFVisitor):
	def __init__(self):
		#By default we have not merged any terms
		self.merged_terms=False

	#Given a term (VarExp or FuncExp), returns the equivalent term
	#With a coefficient of 1
	#Returns a new object that is a copy of the given term
	def _get_basic_term(self,term):
		term=deepcopy(term)
		term.coeff=1
		return term

	#Search for the given term in the given collection of terms
	#Searching is done by variable name and function name/arguments
	#Coefficients are not used
	#
	#Returns the position of the term if found, None otherwise
	def _find_term(self,term,terms):
		term=self._get_basic_term(term)
		terms=[self._get_basic_term(t) for t in terms]

		#Try to find the index of the term
		try:
			res=terms.index(term)
		except:
			res=None
		return res

	def inNormExp(self,node):
		new_terms=[]

		#Look at each term in the terms collection
		for term in node.terms:
			#Search for a similar term is present in the new_terms
			pos=self._find_term(term,new_terms)

			#If one is not found, append the term
			if None is pos:
				new_terms.append(term)
			else:
				#Otherwise update the located term's coefficient
				new_terms[pos].coeff+=term.coeff
				self.merged_terms=True
		node.terms=new_terms
