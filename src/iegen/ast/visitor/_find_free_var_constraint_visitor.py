from iegen.ast.visitor import DFVisitor

#Searches a Set/Relation for an Equality or Inequality constraint that is of the form:
#free_var{=,>=}exp
#In other words, looks for a constraint that contains a free variable.
#The type of constraint that is search for is specified as a parameter:
#constraint_type should either be the Equality type of the Inequality type
#
#If such a constraint is found, either 'var_equality_tuple' or 'var_inequality_tuple' will be a 2-tuple:
#-The first element is a VarExp of the free variable (with a coefficient of 1)
#-The second element is the equality or inequality itself
#Otherwise, if no constraint was found, 'var_equality_tuple'/'var_inequality_tuple' will be None
#The attribute that is used depends on the type of constraint that is being searched for.
class FindFreeVarConstraintVisitor(DFVisitor):

	def __init__(self,constraint_type):
		from iegen.ast import Equality,Inequality

		#Make sure we were given either the Equality or Inequality type
		if Equality is not constraint_type and Inequality is not constraint_type:
			raise ValueError("'constraint_type' must be either Equality or Inequality")

		#Determine if we are searching for equalities or inequalities
		if constraint_type==Equality:
			self.find_equality=True
		else:
			self.find_equality=False

		#By default we do not find a constraint with a free variable
		if self.find_equality:
			self.var_equality_tuple=None
		else:
			self.var_inequality_tuple=None

		#---------- Visiting state variables ----------
		#Used to determine if a given variable is a free variable
		self.formula=None

		#True if we are within an Equality constraint
		self.in_constraint=False

		#Depth of function nesting:
		#0= not in a function
		#n= n functions deep
		self.function_depth=0

		#True if we find a constraint with a free variable
		self.is_free_var_constraint=False

		#Will hold the name of the free variable if one is found
		self.free_var=None
		#----------------------------------------------

	def inPresSet(self,node):
		#Save the Set for use later
		self.formula=node
	def inPresRelation(self,node):
		#Save the Relation for use later
		self.formula=node

	def _inConstraint(self,node):
		self.in_constraint=True
		self.is_free_var_constraint=False
	def _outConstraint(self,node):
		self.in_equality=False

		#If we found that this constraint has a free variable and
		#we have not already found a constraint, store this one
		if self.is_free_var_constraint:
			if self.find_equality:
				if None is self.var_equality_tuple:
					self.var_equality_tuple=(self.free_var,node)
			else:
				if None is self.var_inequality_tuple:
					self.var_inequality_tuple=(self.free_var,node)

	def inEquality(self,node):
		if self.find_equality:
			self._inConstraint(node)
	def outEquality(self,node):
		if self.find_equality:
			self._outConstraint(node)

	def inInequality(self,node):
		if not self.find_equality:
			self._inConstraint(node)
	def outInequality(self,node):
		if not self.find_equality:
			self._outConstraint(node)

	def inFuncExp(self,node):
		#Entering next function depth
		self.function_depth+=1
	def outFuncExp(self,node):
		#Leaving current function depth
		self.function_depth-=1

	def inVarExp(self,node):
		#If we are within a constraint and not within a function
		if self.in_constraint and 0==self.function_depth:
			#If this variable has a coefficient of 1 or -1
			if 1==node.coeff or -1==node.coeff:
				#Make sure this variable is a free variable
				if self.formula.is_free_var(node.id):
					self.is_free_var_constraint=True
					self.free_var=node
