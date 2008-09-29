from iegen.ast.visitor import DFVisitor,FindFreeVarConstraintVisitor
from iegen.util import get_basic_term,find_term
from iegen.ast import NormExp

#Searches for a free variable equality within PresSets and PresRelations
#If one is found, removes this equality and replaces every use of the
#free variable with the expression it is equal to
class RemoveFreeVarConstraintVisitor(DFVisitor):
	def __init__(self):

		#By default we have not changed the formula
		self.changed=False

		#---------- Visiting state variables ----------
		#Holds the free variable equality, if one was found
		self.equality=None

		#Holds the expression that will replace all uses of the free variable
		self.exp=None

		#Holds the free variable, if one was found
		self.free_var=None
		#----------------------------------------------

	def _inFormula(self,node):
		#Search for an equality with a free variable
		var_equality_tuple=FindFreeVarConstraintVisitor().visit(node).var_equality_tuple
		if None is not var_equality_tuple:
			self.free_var,self.equality=var_equality_tuple

			#Calculate the expression that will replace the uses of the free variable
			#This is done by removing the free variable from the expression
			#and multiplying by the opposite of the free variables coefficient (1 or -1)
			#This multiplication is done since we must account for cases when we have exp-free_var=0 rather than free_var-exp=0
			self.exp=self.equality.exp
			self.exp=self.exp-NormExp([self.free_var],0)
			self.exp=NormExp([],-1*self.free_var.coeff)*self.exp

	def _outFormula(self,node):
		self.free_var=None
		self.equality=None
		self.exp=None

	def inPresSet(self,node):
		self._inFormula(node)
	def outPresSet(self,node):
		self._outFormula(node)

	def inPresRelation(self,node):
		self._inFormula(node)
	def outPresRelation(self,node):
		self._outFormula(node)

	def inConjunction(self,node):
		#Remove the free var equality if one was found
		if None is not self.equality:
			node.constraint_list.remove(self.equality)
			self.changed=True

	def inNormExp(self,node):
		#Replace uses of the free variable if we found a free var equality
		if None is not self.equality:
			#Search for the free variable in this node's terms
			pos=find_term(self.free_var,node.terms)

			#If we found the variable, remove it and add in the equivalent expression
			if None is not pos:
				#Get the variable to be removed
				remove_var=node.terms[pos]

				#Multiply the expression to replace the free variable by its coefficient
				replace_exp=NormExp([],remove_var.coeff)*self.exp

				#Subtract off the variable
				new_exp=node-NormExp([remove_var],0)

				#Add in the replacement expression
				new_exp=new_exp+replace_exp

				#Update the current node with the new terms and constant
				node.terms=new_exp.terms
				node.const=new_exp.const

				self.changed=True
