from iegen.ast.visitor import DFVisitor
from iegen.ast import Equality,NormExp,VarExp
from iegen.util import get_unique_var

#Makes tuple vars in PresRelations and PresSets unique:
#If a set such as {[a,a]} is found, this is changed
# to {[a0,a1]:a0=a1}
#If a relation such as {[a]->[a]} is found, this is changed
# to {[a0]->[a1]:a0=a1}
class UniqueTupleVarsVisitor(DFVisitor):
	def __init__(self):
		self.changed=False

		#---------- Visiting state variables ----------
		#True if we are within a VarTuple
		self.in_var_tuple=False

		#Used tuple variable names
		self.used_vars=set()

		#Collection of new equality constraints
		self.new_equalities=[]
		#----------------------------------------------

	def _outPresFormula(self,node):
		#Add each new equality constraint to the formula
		for equality in self.new_equalities:
			node.conjunct.constraints.append(equality)

		#Reset the state variables
		self.used_vars=set()
		self.new_equalities=[]

	def outPresSet(self,node):
		self._outPresFormula(node)

	def outPresRelation(self,node):
		self._outPresFormula(node)

	def inVarTuple(self,node):
		self.in_var_tuple=True

	def outVarTuple(self,node):
		self.in_var_tuple=False

	def inVarExp(self,node):
		if self.in_var_tuple:
			#Get a unique name for the current tuple variable
			new_var_name=get_unique_var(node.id,self.used_vars)

			#Add the variable name to the collection of used variable names
			self.used_vars.add(new_var_name)

			#If the unique name is different from the current name,
			# change the name in this tuple variable and add an equality constraint
			if new_var_name!=node.id:
				#Grab the old tuple variable name
				old_var_name=node.id

				#Update the current variable name to the new one
				node.id=new_var_name

				#Create an equality constraint: new_var_name=old_var_name
				self.new_equalities.append(Equality(NormExp([VarExp(1,old_var_name),VarExp(-1,new_var_name)],0)))

				#Note that we have changed the formula
				self.changed=True
