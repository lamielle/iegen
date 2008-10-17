from iegen.ast.visitor import DFVisitor

#Searches a Set/Relation for Inequality constraints containing the given variable.
#Any that are found categorized as upper and lower bounds as appropriate.
#The expressions without the variable in question are then placed in the 2-tuple 'bounds':
#-The first element is a collection of lower bounds
#-The second element is a collection of upper bounds
#
#Each item in the bounds collections consist of a 3-tuple:
#-The first element is the coefficient on the variable in question
#-The second element is the bound on the variable
#-The third element is the inequality itself
#
#As an example, suppose we have the following inequalities:
# 5<=3a and a<=n-1 and 2a<=m
#
#The collected bounds are as follows:
#-1 lower bound: (3,5,5<=3a)
#-2 upper bounds: (1,n-1,a<=n-1) and (2,m,2a<=m)
class CollectBoundsVisitor(DFVisitor):

	def __init__(self,var_name):
		from iegen.ast import Equality,Inequality

		#The variable name we are searching for
		self.var_name=var_name

		#Initialize the result to two empty lists
		self.bounds=([],[])

		#---------- Visiting state variables ----------
		#True if we are within a constraint (Equality or Inequality)
		self.in_inequality=False

		#If we are within an inequality, will be equal to that inequality, None otherwise
		self.inequality=None

		#Depth of function nesting:
		#0= not in a function
		#n= n functions deep
		self.function_depth=0
		#----------------------------------------------

	def inInequality(self,node):
		self.in_inequality=True
		self.inequality=node
	def outInequality(self,node):
		self.in_inequality=False
		self.inequality=None

	def inFuncExp(self,node):
		#Entering next function depth
		self.function_depth+=1
	def outFuncExp(self,node):
		#Leaving current function depth
		self.function_depth-=1

	def inVarExp(self,node):
		from copy import deepcopy
		from iegen.ast import NormExp
		#If we are within a inequality
		if self.in_inequality:
			#If we are not within a function
			if 0==self.function_depth:
				#If this is the variable we are searching for
				if self.var_name==node.id:
					exp=deepcopy(self.inequality.exp)
					exp=exp-NormExp([deepcopy(node)],0)
					#Place a copy of the current inequality in the proper bound collection
					if node.coeff>0:
						#Lower bound
						self.bounds[0].append((node.coeff,NormExp([],-1)*exp,self.inequality))
					else:
						#Upper bound
						self.bounds[1].append((-1*node.coeff,exp,self.inequality))
