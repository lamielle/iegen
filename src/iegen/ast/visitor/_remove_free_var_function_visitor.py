from iegen.ast.visitor import DFVisitor
from iegen.util import like_type
from iegen.ast import VarExp,FuncExp

#Searches for equality constraints of the form: a=f(b)
#a is a tuple variable and b is a free variable
#If f is in the list of given permutation function names, this constraint
# can be simplified to: b=f_suffix(a)
class RemoveFreeVarFunctionVisitor(DFVisitor):

	def __init__(self,permutations,suffix):
		#The type of constraint we are removing
		self.permutations=permutations

		#The suffix to append to function names when simplifying
		self.suffix=suffix

		#By default we have not changed the formula
		self.changed=False

		#---------- Visiting state variables ----------
		#Used to determine if a given variable is a free variable
		self.formula=None

		#Depth of function nesting:
		#0= not in a function
		#n= n functions deep
		self.function_depth=0

		#True if we are with an Inequality constraint
		self.in_equality=False
		#----------------------------------------------

	def inPresSet(self,node):
		#Save the set for use later
		self.formula=node
	def inPresRelation(self,node):
		#Save the relation for use later
		self.formula=node

	def inEquality(self,node):
		self.in_equality=True

	def inNormExp(self,node):
		#Are we within a formula?
		if self.formula is not None:
			#Are we within an equality constraint and not within a function's arguments?
			if self.in_equality and 0==self.function_depth:
				#For now we are looking for a=f(b)-like constraints
				if 2==len(node.terms):
					#If first term is a variable and second is a function
					if like_type(node.terms[0],VarExp) and like_type(node.terms[1],FuncExp):
						var=node.terms[0]
						func=node.terms[1]
					#If first term is a function and second is a variable
					elif like_type(node.terms[0],FuncExp) and like_type(node.terms[1],VarExp):
						var=node.terms[1]
						func=node.terms[0]
					else:
						var=None
						func=None

					#If a var and a function were found
					if var is not None and func is not None:
						#Check that there is only one argument to the function
						# and that there is no constant:
						if 1==len(func.args) and 1==len(func.args[0].terms) and 0==func.args[0].const:
							func_arg=func.args[0].terms[0]

							#Ensure that the single argument to the function is a VarExp
							if like_type(func_arg,VarExp):
								#Ensure that this argument is a free variable
								if self.formula.is_free_var(func_arg.id):
									#Ensure that the function is permutable
									if func.name in self.permutations:
										#Apply the rule a=f(b) -> b=f_inv(a)

										#Swap ids and coefficients
										var.id,func_arg.id=func_arg.id,var.id
										var.coeff,func_arg.coeff=func_arg.coeff,var.coeff

										#Append the suffix to the function name
										func.name+=self.suffix

										#Set the changed flag
										self.changed=True
