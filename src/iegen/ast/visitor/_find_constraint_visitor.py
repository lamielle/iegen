from iegen.ast.visitor import DFVisitor

#Searches a Set/Relation for a constraint with the given variable
#
#The type of constraint (Equality or Inequality) is given.
#The variable name is given
#
#Only variables with coefficient 1 or -1 are considered
#
#The result is a collection of 2-tuples, one for each constraint found, placed in 'var_constraints'
#The elements of the 2-tuple are as follows:
#-The first element is a VarExp of the variable (with a coefficient of 1 or -1)
#-The second element is the constraint itself
#
#Otherwise, if no constraints were found, 'var_constraints' will be an empty list
class FindConstraintVisitor(DFVisitor):

	def __init__(self,constraint_type,var_name):
		from iegen.ast import Equality,Inequality

		#Make sure we were given either the Equality or Inequality type
		if Equality is not constraint_type and Inequality is not constraint_type:
			raise ValueError("'constraint_type' must be either Equality or Inequality")

		#Determine if we are searching for equalities or inequalities
		if constraint_type==Equality:
			self.find_equality=True
		else:
			self.find_equality=False

		#Store the name of the variable we are searching for
		self.var_name=var_name

		#By default we do not find any constraints
		self.var_constraints=[]

		#---------- Visiting state variables ----------
		#True if we are within a constraint (Equality or Inequality)
		self.in_constraint=False

		#Depth of function nesting:
		#0= not in a function
		#n= n functions deep
		self.function_depth=0

		#True if we should store the constraint as it contains the given variable
		self.store_constraint=False

		#Will hold the variable if one is found
		self.var=None
		#----------------------------------------------

	def _inConstraint(self,node):
		self.in_constraint=True
		self.store_constraint=False
	def _outConstraint(self,node):
		self.in_constraint=False

		#If we found that this constraint that contains the
		#given variable, store it
		if self.store_constraint:
			self.var_constraints.append((self.var,node))

		self.store_constraint=False
		self.var=None

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
				#If this variable has the name we are searching for
				if node.id==self.var_name:
					self.store_constraint=True
					self.var=node
