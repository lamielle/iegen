from iegen.ast.visitor import DFVisitor

#Sparse Translation Visitor: Translate the visited Set or Relation into
# a SparseSet or SparseRelation.
class SparseTransVisitor(DFVisitor):
	def __init__(self,sparse_formula):

		self.sparse_formula=sparse_formula

		#---------- Visiting state variables ----------
		#Are we within a variable tuple?
		self.in_var_tuple=False

		#Are we within a constraint?
		self.in_constraint=False

		#Stack of function contexts
		self.func_context=[]
		#----------------------------------------------

	class FunctionContext(object):
		def __init__(self,name,num_args,zero_coefficients):
			self.name=name
			self.arg_exps=[list(zero_coefficients) for i in xrange(num_args)]
			self.curr_arg=-1

		def curr_arg_exp(self):
			return self.arg_exps[self.curr_arg]

		def next_arg(self):
			self.curr_arg+=1

	def _get_zero_coefficients(self):
		return [0]*self.sparse_formula.num_columns()

	def inSet(self,node):
		raise ValueError('Translation of a Set not supported')

	def inRelation(self,node):
		raise ValueError('Translation of a Relation not supported')

	def inPresSet(self,node): pass

	def outPresSet(self,node): pass


	def inPresRelation(self,node): pass

	def outPresRelation(self,node): pass

	def inVarTuple(self,node):
		self.in_var_tuple=True

	def outVarTuple(self,node):
		self.in_var_tuple=False

	def _inConstraint(self,node):
		self.in_constraint=True
		self.constraint_coeff=self._get_zero_coefficients()

	def _outConstraint(self,node):
		self.in_constraint=False

	def inEquality(self,node):
		self._inConstraint(node)

	def outEquality(self,node):
		self._outConstraint(node)
		self.sparse_formula.add_equality(self.constraint_coeff)

	def inInequality(self,node):
		self._inConstraint(node)

	def outInequality(self,node):
		self._outConstraint(node)
		self.sparse_formula.add_inequality(self.constraint_coeff)

	def inVarExp(self,node):
		#Do nothing unless we are in a constraint (this ignores tuple variables)
		if self.in_constraint:
			#Check if we are in a function or not
			if len(self.func_context)>0:
				self.func_context[-1].curr_arg_exp()[self.sparse_formula.get_column(node.id)]=node.coeff
			else:
				self.constraint_coeff[self.sparse_formula.get_column(node.id)]=node.coeff

	def inNormExp(self,node):
		#Move to the next function argument if we are in a function
		if len(self.func_context)>0:
			self.func_context[-1].next_arg()

	def outNormExp(self,node):
		#Check if we are in a function or not
		if len(self.func_context)>0:
			self.func_context[-1].curr_arg_exp()[self.sparse_formula.get_constant_column()]=node.const
		else:
			self.constraint_coeff[self.sparse_formula.get_constant_column()]=node.const

	def inFuncExp(self,node):
		self.func_context.append(self.FunctionContext(node.name,len(node.args),self._get_zero_coefficients()))

	def outFuncExp(self,node):
		#Grab the function context from the stack
		curr_func_context=self.func_context.pop()

		#Add the function to the formula
		self.sparse_formula.add_function(curr_func_context.name,curr_func_context.arg_exps)

		#TODO: Set the corresponding function coefficient
