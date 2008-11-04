from iegen.ast.visitor import DFVisitor,FindFreeVarConstraintVisitor
from iegen.util import get_basic_term,find_term,sign
from iegen.ast import NormExp

#Searches for a free variable constraint within PresSets and PresRelations
#If one is found, removes this constraint and replaces every use of the
#free variable with the expression it is equal to
#
#The type of constraint that is search for is specified as a parameter:
#constraint_type should either be the Equality type of the Inequality type

class RemoveFreeVarConstraintVisitor(DFVisitor):

	def __init__(self,constraint_type):
		from iegen.ast import Equality,Inequality

		#Make sure we were given either the Equality or Inequality type
		if Equality is not constraint_type and Inequality is not constraint_type:
			raise ValueError("'constraint_type' must be either Equality or Inequality")

		#The type of constraint we are removing
		self.constraint_type=constraint_type

		#Determine if we are removing equalities or inequalities
		if constraint_type==Equality:
			self.remove_equality=True
		else:
			self.remove_equality=False

		#By default we have not changed the formula
		self.changed=False

		#---------- Visiting state variables ----------
		#Holds the free variable equality, if one was found
		self.constraint=None

		#Holds the expression that will replace all uses of the free variable
		self.exp=None

		#True if we replaced the free variable with its equivalent expression
		self.replaced=False

		#Holds the free variable, if one was found
		self.free_var=None

		#Depth of function nesting:
		#0= not in a function
		#n= n functions deep
		self.function_depth=0

		#True if we are with an Inequality constraint
		self.in_inequality=False
		#----------------------------------------------

	def _inFormula(self,node):
		#Search for an constraint with a free variable
		var_constraint_tuple=FindFreeVarConstraintVisitor(self.constraint_type).visit(node).var_constraint_tuple
		if None is not var_constraint_tuple:
			self.free_var,self.constraint=var_constraint_tuple

			#Calculate the expression that will replace the uses of the free variable
			#This is done by removing the free variable from the expression
			#and multiplying by the opposite of the free variables coefficient (1 or -1)
			#This multiplication is done since we must account for cases when we have exp-free_var=0 rather than free_var-exp=0
			self.exp=self.constraint.exp
			self.exp=self.exp-NormExp([self.free_var],0)
			self.exp=NormExp([],-1*self.free_var.coeff)*self.exp

	def _outFormula(self,node):
		self.free_var=None
		self.constraint=None
		self.exp=None
		self.replaced=False

	def inPresSet(self,node):
		self._inFormula(node)
	def outPresSet(self,node):
		self._outFormula(node)

	def inPresRelation(self,node):
		self._inFormula(node)
	def outPresRelation(self,node):
		self._outFormula(node)

	def inConjunction(self,node):
		#Remove the free var constraint if one was found
		if None is not self.constraint:
			node.constraints.remove(self.constraint)
			self.changed=True

	def outConjunction(self,node):
		#If we are removing inequalities
		if not self.remove_equality:
			#Add the constraint back if no replacement was done
			#(We don't want to loose any information)
			if not self.replaced and None is not self.constraint:
				node.constraints.append(self.constraint)
				self.changed=False

	def inInequality(self,node):
		#Within an inequality constraint
		self.in_inequality=True
	def outInequality(self,node):
		#Not within an inequality constraint
		self.in_inequality=False

	def inFuncExp(self,node):
		#Entering next function depth
		self.function_depth+=1
	def outFuncExp(self,node):
		#Leaving current function depth
		self.function_depth-=1

	#Replaces any occurrences of self.free_var with 
	def _doReplace(self,norm_exp):
		#Search for the free variable in the norm_exp's terms
		pos=find_term(self.free_var,norm_exp.terms)

		#If we found the variable
		if None is not pos:
			#Get the variable to potentially be removed
			remove_var=norm_exp.terms[pos]

			#If we are removing equalities OR
			#If we are removing inequalities AND the var has the opposite sign of the found variable
			#remove the found var and add in the equivalent expression
			if self.remove_equality or (not self.remove_equality and self.free_var.coeff*-1==sign(remove_var.coeff)):
				#Multiply the expression to replace the free variable by its coefficient
				replace_exp=NormExp([],remove_var.coeff)*self.exp

				#Subtract off the variable
				new_exp=norm_exp-NormExp([remove_var],0)

				#Add in the replacement expression
				new_exp=new_exp+replace_exp

				#Update the current norm_exp with the new terms and constant
				norm_exp.terms=new_exp.terms
				norm_exp.const=new_exp.const

				self.replaced=True
				self.changed=True

	def inNormExp(self,node):
		if self.remove_equality:
			#Replace uses of the free variable if we found a free var constraint
			if None is not self.constraint:
				self._doReplace(node)
		else:
			#Only do replacement if we are within a inequality and not within a function
			if self.in_inequality and 0==self.function_depth:
				#Replace uses of the free variable if we found a free var constraint
				if None is not self.constraint:
					self._doReplace(node)
