from iegen.ast.visitor import DFVisitor

#Makes tuple vars in PresRelations and PresSets unique:
#If a set such as {[a,a]} is found, this is changed
# to {[a_0,a_1]:a_0=a_1}
#If a relation such as {[a]->[a]} is found, this is changed
# to {[a_in0]->[a_out0]:a_in0=a_out0}
class UniqueTupleVarsVisitor(DFVisitor):
	def __init__(self):
		self.changed=False

		#---------- Visiting state variables ----------
		#True if we are within a PresSet
		self.in_pres_set=False

		#True if we are within a PresRelation
		self.in_pres_relation=False

		#True if we are within a VarTuple
		self.in_var_tuple=False

		#True if we are within a tuple_set
		self.in_tuple_set=False

		#True if we are within a tuple_in
		self.in_tuple_in=False

		#Position within a VarTuple
		self.var_pos=None

		#Dictionary mapping tuple variable names to a list of tuples:
		#pos 0) name: '', 'in', or 'out'
		#pos 1) position in tuple: 0, 1, ...
		self.vars_info={}
		#----------------------------------------------

	#Returns true if renaming is needed, based on the current state of vars_info
	def needs_rename(self):
		if self.vars_info is not None:
			return any([len(var_info)>1 for var_info in self.vars_info.values()])
		else:
			return False

	#The method that actually does renaming for PresSets
	#This method uses the current state of vars_info to do renaming
	def set_rename(self,node):
		from iegen.ast import Equality,NormExp,VarExp

		for old_var_name,var_info in self.vars_info.items():
			#Do we have info for more than one tuple variable?
			if len(var_info)>1:
				#For each necessary renaming
				for info in var_info:
					#Build the new variable name
					new_var_name=old_var_name+'_%s'%(info[1])

					#Rename the variable in the tuple_set
					node.tuple_set.vars[info[1]].id=new_var_name

					#Add an equality constraint: new_var_name=old_var_name
					node.conjunct.constraints.append(Equality(NormExp([VarExp(1,old_var_name),VarExp(-1,new_var_name)],0)))

	#The method that actually does renaming for PresRelations
	#This method uses the current state of vars_info to do renaming
	def relation_rename(self,node):
		from iegen.ast import Equality,NormExp,VarExp

		for old_var_name,var_info in self.vars_info.items():
			#Do we have info for more than one tuple variable?
			if len(var_info)>1:
				#For each necessary renaming
				for info in var_info:
					#Build the new variable name
					new_var_name=old_var_name+'_%s%s'%(info[0],info[1])

					if 'in'==info[0]:
						#Rename the variable in the tuple_set
						node.tuple_in.vars[info[1]].id=new_var_name
					else:
						#Rename the variable in the tuple_set
						node.tuple_out.vars[info[1]].id=new_var_name

					#Add an equality constraint: new_var_name=old_var_name
					node.conjunct.constraints.append(Equality(NormExp([VarExp(1,old_var_name),VarExp(-1,new_var_name)],0)))

	def init_vars_info(self,node):
		if self.in_pres_set:
			all_vars=node.tuple_set.vars
		elif self.in_pres_relation:
			all_vars=node.tuple_in.vars+node.tuple_out.vars

		self.vars_info=dict([(var.id,[]) for var in all_vars])

	def _inPresFormula(self,node):
		if self.in_pres_set:
			self.in_tuple_set=True
		elif self.in_pres_relation:
			self.in_tuple_in=True
		self.init_vars_info(node)
	def _outPresFormula(self,node):
		#Rename if necessary
		if self.needs_rename():
			if self.in_pres_set:
				self.set_rename(node)
			elif self.in_pres_relation:
				self.relation_rename(node)

		self.vars_info=None
		self.in_tuple_in=False
		self.in_tuple_set=False

	def inPresSet(self,node):
		self.in_pres_set=True
		self._inPresFormula(node)
	def outPresSet(self,node):
		self._outPresFormula(node)
		self.in_pres_set=False
	def inPresRelation(self,node):
		self.in_pres_relation=True
		self._inPresFormula(node)
	def outPresRelation(self,node):
		self._outPresFormula(node)
		self.in_pres_relation=False

	def inVarTuple(self,node):
		#We only care if we are within a PresSet or PresRelation
		if self.in_pres_set or self.in_pres_relation:
			self.in_var_tuple=True
			self.var_pos=0
	
	def outVarTuple(self,node):
		self.in_var_tuple=False
		self.in_tuple_set=False
		self.in_tuple_in=False
		self.var_pos=None

	def inVarExp(self,node):
		if self.in_var_tuple:
			if self.in_tuple_set:
				name=''
			elif self.in_tuple_in:
				name='in'
			else:
				name='out'
			self.vars_info[node.id].append((name,self.var_pos))

	def outVarExp(self,node):
		if self.in_var_tuple:
			self.var_pos+=1
