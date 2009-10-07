from iegen.ast.visitor import DFVisitor
from iegen.util import like_type
from iegen.ast import VarExp,FuncExp

#Searches for equality constraints of the form: a=f(b)
#a is a tuple variable and b is a free variable
#
#If f is in the dictionary of given function name mappings, this constraint
# can be simplified to: b='permutations[f]'(a)
#
#permutations: A dictionary mapping names to their associated inverse name
#              It is assumed that for a pair (f,f_inv), both f->f_inv and
#              f_inv->f is present in the dictionary
class RemoveFreeVarFunctionVisitor(DFVisitor):

	def __init__(self,permutations):
		#Dictionary mapping function names to their inverses
		self.permutations=permutations

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
		#Check that:
		#-We are within a formula
		#-We are within an equality constraint
		#-We are not within a function's arguments
		#-The node only has 2 terms: For now we are looking for a=f(b)-like constraints
		if self.formula is not None and self.in_equality and 0==self.function_depth and 2==len(node.terms):
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

					#Check that:
					#-The single argument to the function is a VarExp
					#-This argument is a free variable
					#-The function is permutable
					if like_type(func_arg,VarExp) and self.formula.is_free_var(func_arg.id) and func.name in self.permutations:
						#Apply the rule a=f(b) -> b=f_inv(a)

						#Swap ids and coefficients
						var.id,func_arg.id=func_arg.id,var.id
						var.coeff,func_arg.coeff=func_arg.coeff,var.coeff

						#Save the function/inverse function names
						self.func_name=func.name
						self.func_inv_name=self.permutations[func.name]

						#Change the function name to its associated inverse name
						func.name=self.permutations[func.name]

						#Set the changed flag
						self.changed=True
