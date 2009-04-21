from iegen.ast.visitor import DFVisitor
from iegen.util import like_type
from iegen.ast import Equality,NormExp,VarExp,FuncExp
import iegen.util

#Searches for two equality constraints of the form: a=f(...) and b=f(...)
#where a and b are tuple variables and the f(...) expressions are equal
#
#If such a case is found, these two constraints are replaced with a=b
#
class RemoveEqualFunctionVisitor(DFVisitor):

	def __init__(self):
		#By default we have not changed the formula
		self.changed=False

		#---------- Visiting state variables ----------
		#Used keep track of var/func equalities
		self.equalities={}
		#----------------------------------------------

	def add_var_func_equality(self,var,func):
		#Check if this variable name exists in the collection yet
		if var.id not in self.equalities:
			self.equalities[var.id]=[]

		self.equalities[var.id].append(func)

	def inConjunction(self,node):
		self.equalities={}

	def outConjunction(self,node):
		#Find 'equality sets', sets of variables equal to the same function
		equality_sets=iegen.util.equality_sets(self.equalities)

		#For each set of equal variables
		for equal_value,equal_vars in equality_sets.items():
			#Get a list equal variables (rather than a set)
			equal_vars=list(equal_vars)

			#Add equality constraints for each pair of variables
			first_var=equal_vars[0]
			for other_var in equal_vars[1:]:
				#Add the equality constraint first_var=other_var
				node.constraints.append(Equality(NormExp([VarExp(1,first_var),VarExp(-1,other_var)],0)))

				#Remove the old equality constraint for the current variable
				equal_var=VarExp(equal_value.coeff*-1,other_var)
				node.constraints.remove(Equality(NormExp([equal_value,equal_var],0)))

			#Remove the old equality constraint for the first variable
			equal_var=VarExp(equal_value.coeff*-1,first_var)
			node.constraints.remove(Equality(NormExp([equal_value,equal_var],0)))

			#Mark that we changed the object we are visiting
			self.changed=True

	def inEquality(self,node):
		#Check that:
		#-The constraint has two terms
		#-The constant on this constraint is 0
		if 2==len(node.exp.terms) and 0==node.exp.const:
			#Get the two terms
			term1=node.exp.terms[0]
			term2=node.exp.terms[1]

			#Check for one variable expression and one function expression
			#If first term is a variable and second is a function
			if like_type(term1,VarExp) and like_type(term2,FuncExp):
				var=term1
				func=term2
			#If first term is a function and second is a variable
			elif like_type(term1,FuncExp) and like_type(term2,VarExp):
				var=term2
				func=term1
			else:
				var=None
				func=None

			#If one var and one function were found
			if var is not None and func is not None:
				#Make sure the coefficients are 1/-1
				if (1==var.coeff or 1==func.coeff) and (var.coeff==-1*func.coeff):
					#Add the var=func mapping to the collection of equalities
					self.add_var_func_equality(var,func)
