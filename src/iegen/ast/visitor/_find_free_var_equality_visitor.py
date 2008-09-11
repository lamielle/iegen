from iegen.ast.visitor import DFVisitor

#Searches a Set/Relation for an Equality constraint that is of the form:
#free_var=exp
#In other words, looks for an Equality that contains a free variable.
#If such a constraint exists, it is placed in 'equality'
#Otherwise, 'equality' will be None
class FindFreeVarEqualityVisitor(DFVisitor):
	def __init__(self):

		#By default we do not find an equality with a free variable
		self.equality=None

		#---------- Visiting state variables ----------
		#Used to determine if a given variable is a free variable
		self.formula=None

		#True if we are within an Equality constraint
		self.in_equality=False

		#Depth of function nesting:
		#0= not in a function
		#n= n functions deep
		self.function_depth=0

		#True if we find an equality with a free variable
		self.is_free_var_equality=False
		#----------------------------------------------

	def inSet(self,node):
		#Save the Set for use later
		self.formula=node
	def inRelation(self,node):
		#Save the Relation for use later
		self.formula=node

	def inEquality(self,node):
		self.in_equality=True
		self.is_free_var_equality=False
	def outEquality(self,node):
		self.in_equality=False

		#If we found that this equality has a free variable and
		#we have not already found an equality, store this one
		if self.is_free_var_equality and None is self.equality:
			self.equality=node

	def inFuncExp(self,node):
		#Entering next function depth
		self.function_depth+=1
	def outFuncExp(self,node):
		#Leaving current function depth
		self.function_depth-=1

	def inVarExp(self,node):
		#If we are within an equality and not within a function
		if self.in_equality and 0==self.function_depth:
			#If this variable has a coefficient of 1
			if 1==node.coeff or -1==node.coeff:
				#Make sure this variable is a free variable
				if self.formula.is_free_var(node.id):
					self.is_free_var_equality=True
