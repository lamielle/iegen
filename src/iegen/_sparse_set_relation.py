#Classes related to the Set and Relation classes that use the new data structure rather than an AST as a representation

from collections import defaultdict
import iegen
from iegen import IEGenObject,Symbolic
from iegen.parser import PresParser
from iegen.ast.visitor import CollectVarsVisitor,SparseTransVisitor
from iegen.util import biject,raise_objs_not_like_types,sign,get_unique_vars

#--------------------------------------------------
# Start SparseFormula class

#Represents a sparse set or relation
class SparseFormula(IEGenObject):
	__slots__=('_tuple_vars_col','_tuple_vars','_symbolic_cols','_free_var_cols','_disjunction','_frozen')

	#--------------------------------------------------
	# Start SparseFormula constructor
	def __init__(self,tuple_var_names,free_var_names,symbolics,disjunction):
		#--------------------
		#Init various fields
		#'var name' --> TupleVarCol(pos)
		self._tuple_vars_col={}

		#List of 'var name'
		self._tuple_vars=[]

		#List of SymbolicCol(Symbolic)
		self._symbolic_cols=[]

		#List of FreeVarCol(name)
		self._free_var_cols=[]

		#SparseDisjunction containing all conjunctions in this formula (equalities or inequalities)
		self._disjunction=SparseDisjunction() if disjunction is None else disjunction

		#Start off unfrozen
		self._frozen=False
		#--------------------

		#Ensure we are given Symbolic objects
		raise_objs_not_like_types(symbolics,Symbolic,'Formula construction failure: symbolics must be a collection of objects that look like a Symbolic')

		#Build the names collections
		self._build_cols_collections(tuple_var_names,symbolics,free_var_names)
	#--------------------------------------------------

	#--------------------------------------------------
	# Start construction utility methods

	def _construct(self,pres_formulas=None,tuple_var_names=None,free_var_names=None,symbolics=None,disjunction=None,freeze=True):
		#Get an empty list if no symbolics were given
		symbolics=[] if symbolics is None else sorted(symbolics)

		#Determine how to construct based on the presence of the pres_formulas argument
		if pres_formulas is None:
			#Construct this formula using the SparseFormula constructor and the parsed information
			SparseFormula.__init__(self,tuple_var_names,free_var_names,symbolics,disjunction)
		else:
			#Get the names of the tuple variables
			tuple_var_names=self._get_tuple_var_names(pres_formulas)

			#Get the names of the free variables
			free_var_names=self._get_free_var_names(pres_formulas,tuple_var_names,symbolics)

			#Construct this formula using the SparseFormula constructor and the parsed information
			SparseFormula.__init__(self,tuple_var_names,free_var_names,symbolics,disjunction)

			#Run the translation visitor
			v=SparseTransVisitor(self)
			for pres_formula in pres_formulas:
				v.visit(pres_formula)

		#Freeze this formula if necessary
		if freeze:
			self.freeze()

	#Makes a copy of a sparse formula of type FormulaClass
	def _copy(self,FormulaClass,new_var_pos=None,new_var_names=None,freeze=True,**kwargs):
		#Copy the constraints of the formula
		disjunction_copy=self.disjunction.copy(new_var_pos=new_var_pos,new_var_names=new_var_names,freeze=False,**kwargs)

		#Reorder the tuple variables if needed
		if new_var_pos is None:
			tuple_var_names=self.tuple_vars
		else:
			tuple_var_names=[0]*len(self.tuple_vars)
			for old_pos,new_pos in new_var_pos.items():
				tuple_var_names[new_pos]=self.tuple_vars[old_pos]

		#Rename the tuple variables if needed
		if new_var_names is None:
			tuple_var_names=tuple_var_names
		else:
			for pos in xrange(len(tuple_var_names)):
				if tuple_var_names[pos] in new_var_names:
					tuple_var_names[pos]=new_var_names[tuple_var_names[pos]]

		#Copy the structure of the formula
		selfcopy=FormulaClass(tuple_var_names=tuple_var_names,free_var_names=self.free_vars,symbolics=self.symbolics,disjunction=disjunction_copy,freeze=False)

		#Freeze the copy if necessary
		if freeze:
			selfcopy.freeze()

		return selfcopy

	#Parses the given formula string using the given parsing function
	@staticmethod
	def _parse_formula_string(formula_string,symbolics,parse_func):
		pres_formulas=[parse_func(formula_string,symbolics)]

		return pres_formulas

	#Returns the names of the tuple variables in _pres_formulas
	@staticmethod
	def _get_tuple_var_names(pres_formulas):
		#Get the names of all tuple variables, in order
		tuple_var_names=pres_formulas[0]._get_tuple_vars()

		#Ensure that all variable tuples are the same
		for pres_formula in pres_formulas[1:]:
			if pres_formula._get_tuple_vars()!=tuple_var_names:
				raise ValueError('Variable tuples do not match across conjunctions')

		return tuple_var_names

	#Determine the names of all free variables in _pres_formulas
	#We exclude the names of the given tuple variables and symbolics
	@staticmethod
	def _get_free_var_names(pres_formulas,tuple_var_names,symbolics):
		#Start with the names of all variables
		free_var_names=CollectVarsVisitor(all_vars=True)
		for pres_form in pres_formulas:
			free_var_names.visit(pres_form)
		free_var_names=set(free_var_names.vars)

		#Remove the names of the tuple variables
		free_var_names-=set(tuple_var_names)

		#Remove the names of the symbolics
		free_var_names-=set([symbolic.name for symbolic in symbolics])

		#We now have the final list of free variables
		return sorted(free_var_names)

	#Build the collections of tuple variables, free variables, and symbolics
	def _build_cols_collections(self,tuple_var_names,symbolics,free_var_names):

		#Build the tuple variable column bijection
		for pos,tuple_var_name in enumerate(tuple_var_names):
			self._tuple_vars_col[tuple_var_name]=TupleVarCol(pos,tuple_var_name)
			self._tuple_vars.append(tuple_var_name)

		#Build the symbolic list
		for symbolic in symbolics:
			self._symbolic_cols.append(SymbolicCol(symbolic))

		#Build the free variable list
		for free_var_name in free_var_names:
			self._free_var_cols.append(FreeVarCol(free_var_name))

	# End construction utility methods
	#--------------------------------------------------

	#--------------------------------------------------
	# Hash, equality, length, and iterable methods
	def __hash__(self):
		self._check_frozen()
		return hash(self._disjunction)

	def __eq__(self,other):
		try:
			self._check_frozen()
			other._check_frozen()
			return self._disjunction==other._disjunction
		except AttributeError as e:
			return False

	def __ne__(self,other):
		return not self==other

	def __len__(self):
		return len(self.disjunction)

	def __iter__(self):
		for conjunction_pos in xrange(len(self)):
			yield self.copy(conjunction_pos=conjunction_pos)
	#--------------------------------------------------

	#--------------------------------------------------
	# Start property support methods

	#Returns the arity (number of tuple variables) of this forumla
	def _arity(self):
		return len(self._tuple_vars)

	#Returns the number of symbolics in this formula
	def _num_symbolics(self):
		return len(self._symbolic_cols)

	#Returns the number of free variables in this formula
	def _num_free_vars(self):
		return len(self._free_var_cols)

	#Get the names of all tuple variables in the formula
	def _get_tuple_vars(self):
		return list(self._tuple_vars)

	#Get the symbolics in this forumula
	def _get_symbolics(self):
		return [symbolic_col.sym for symbolic_col in self._symbolic_cols]

	#Get the names of all symbolics
	def _get_symbolic_names(self):
		return [symbolic_col.sym.name for symbolic_col in self._symbolic_cols]

	#Get the names of all functions
	def _get_function_names(self):
		return self.disjunction.get_function_names()

	#Get the names of all free variables in the formula
	def _get_free_vars(self):
		return [free_var_col.name for free_var_col in self._free_var_cols]

	#Get the disjunction of the formula
	def _get_disjunction(self):
		return self._disjunction

	#Get the frozen state
	def _get_frozen(self):
		return self._frozen

	# End property support methods
	#--------------------------------------------------

	#--------------------------------------------------
	#Start misc utility methods

	def __repr__(self):
		symbolic_strings=repr(self.symbolics)
		class_name=self.__class__.__name__
		return '%s("%s",%s)'%(class_name,str(self),symbolic_strings)

	def __str__(self):
		#Create the tuple variable string based on whether we are a sparse set or relation
		try:
			#Assume we are a sparse relation
			tuple_var_string='['+','.join(self.tuple_in)+']'
			tuple_var_string+='->'
			tuple_var_string+='['+','.join(self.tuple_out)+']'
		except AttributeError as e:
			#We must be a sparse set
			tuple_var_string='['+','.join(self.tuple_vars)+']'

		#Create strings for each conjunction
		conjunction_strings=[]
		for conjunction in sorted(self.disjunction.conjunctions,key=lambda conj: hash(conj)):
			#Get a string for the current conjunction
			constraints_string=str(conjunction)

			#Add a ': ' if we have any constraints
			if len(conjunction)>0:
				constraints_string=': '+constraints_string

			symbolics_string=','.join(self.symbolic_names)

			if len(symbolics_string)>0:
				conjunction_strings.append('{%s%s | %s}'%(tuple_var_string,constraints_string,symbolics_string))
			else:
				conjunction_strings.append('{%s%s}'%(tuple_var_string,constraints_string))

		return ' union '.join(conjunction_strings)

	def _check_frozen(self):
		#Make sure we're frozen
		if not self.frozen:
			raise ValueError('Cannot operate on a non-frozen sparse formula')

	def _check_mutate(self):
		#Make sure we're not frozen
		if self.frozen:
			raise ValueError('Cannot modify a frozen sparse formula')

	def _get_constraint(self,exp_coeff,ConstraintType):
		#Make sure this sparse formula can be modified
		self._check_mutate()

		#Return a new constraint
		return ConstraintType(exp_coeff)

	def _get_mat(self,pos_map,make_positive,make_negative):
		return self.disjunction.get_mat(pos_map,make_positive,make_negative)

	#End misc utility methods
	#--------------------------------------------------

	#--------------------------------------------------
	# Start operation utility methods

	def _union(self,other,FormulaClass):
		#Make sure both formulas are frozen
		self._check_frozen()
		other._check_frozen()

		#Make sure the arity of both formulas matches
		if self.arity()!=other.arity():
			raise ValueError("Cannot union formulas with differing arity: '%s' (arity %s) and '%s' (arity %s)"%(self,self.arity(),other,other.arity()))

		#Collections for building the new formula
		new_tuple_vars=[]
		new_free_vars=[]
		self_var_map={}
		other_var_map={}
		used_vars=set()

		#Determine the resutling formula's tuple variable names
		get_unique_vars(self.tuple_vars,new_tuple_vars,used_vars,self_var_map)

		#Determine the resulting formula's free variable names
		get_unique_vars(self.free_vars,new_free_vars,used_vars,self_var_map)
		get_unique_vars(other.free_vars,new_free_vars,used_vars,other_var_map)

		#New variable names mapping
		for pos in xrange(len(self.tuple_vars)):
			other_var_map[other.tuple_vars[pos]]=self.tuple_vars[pos]

		#Get the combined symbolics for the new formula
		new_symbolics=list(set(other.symbolics+self.symbolics))

		#Create a new formula with no constraints, we will build the constraints
		new_formula=FormulaClass(tuple_var_names=new_tuple_vars,free_var_names=new_free_vars,symbolics=new_symbolics,freeze=False)

		#Add copies of the constraints of both formulas
		new_formula.add_disjunction(self.disjunction.copy(new_var_names=self_var_map,freeze=False))
		new_formula.add_disjunction(other.disjunction.copy(new_var_names=other_var_map,freeze=False))

		return new_formula

	#Adds new constraints from the cartesian product of the disjunctions of two given formulas
	#Adds equality constraints for each pair of variables to each item in the cartesian product
	#Converts any tuple variable columns to free variable columns to match this formula's free/tuple variables
	#This utility method is used by the apply and compose operations
	def _join(self,formula1,formula1_equality_vars,formula1_var_map,formula2,formula2_equality_vars,formula2_var_map,formula2_pos_map):
		#Create a conjunction with equalities for the given variable pairs
		#AND create a mapping from old tuple variable columns to new free variable columns
		equality_conjunction=self.get_conjunction()
		formula1_new_cols={}
		formula2_new_cols={}
		for formula1_var,formula2_var in zip(formula1_equality_vars,formula2_equality_vars):
			#Create/add the equality constraint for this variable pair
			exp_coeff=defaultdict(int)
			exp_coeff[self.get_column(formula1_var_map[formula1_var])]=1
			exp_coeff[self.get_column(formula2_var_map[formula2_var])]=-1
			equality_conjunction.add_constraint(self.get_equality(exp_coeff))

			#Add the column mapping from the old formulas to the new one (tuple -> free var columns)
			formula1_new_cols[formula1.get_column(formula1_var)]=self.get_column(formula1_var_map[formula1_var])
			formula2_new_cols[formula2.get_column(formula2_var)]=self.get_column(formula2_var_map[formula2_var])

		#Create new collection of conjunctions (cartesian product of both sets of conjunctions)
		for formula1_conjunction in formula1.disjunction.conjunctions:
			for formula2_conjunction in formula2.disjunction.conjunctions:
				#Merge the two conjunctions and add to the resulting formula being created
				merged_conjunction=self.get_conjunction()
				merged_conjunction.add_conjunction(formula1_conjunction.copy(new_var_names=formula1_var_map,new_cols=formula1_new_cols))
				merged_conjunction.add_conjunction(formula2_conjunction.copy(new_var_pos=formula2_pos_map,new_var_names=formula2_var_map,new_cols=formula2_new_cols))
				merged_conjunction.add_conjunction(equality_conjunction.copy())
				self.add_conjunction(merged_conjunction)

	# End operation utility methods
	#--------------------------------------------------

	#--------------------------------------------------
	# Start public methods/properties

	#Property creation
	tuple_vars=property(_get_tuple_vars)
	symbolics=property(_get_symbolics)
	symbolic_names=property(_get_symbolic_names)
	free_vars=property(_get_free_vars)
	function_names=property(_get_function_names)
	disjunction=property(_get_disjunction)
	frozen=property(_get_frozen)

	#Simplifies this formula
	def simplify(self):
		self.disjunction.simplify()

	#Freezes this formula
	def freeze(self):
		#Project each free variable out of the disjunction
		for free_var in self.free_vars:
			#Simplify the whole formula recursively before attempting to project out
			self.simplify()

			#Attempt to project the current free variable out of this formula
			projected_out=self.disjunction.project_out(self.get_column(free_var))

			if projected_out:
				self._free_var_cols.remove(self.get_column(free_var))

		#Simplify one final time before freezing
		self.simplify()

		#Freeze the disjunction
		self.disjunction.freeze()

		#Set this sparse formula's state to frozen
		self._frozen=True

	#Returns the SparseExpColumnType object for the column with the given name:
	#The name could be a symbolic, tuple variable, or free variable
	def get_column(self,name):
		column=None

		if name in self.symbolic_names:
			for symbolic_col in self._symbolic_cols:
				if symbolic_col.sym.name==name:
					column=symbolic_col
					break
			if column is None:
				raise ValueError("Could not find symbolic '%s'"%(name))

		elif name in self.tuple_vars:
			column=self._tuple_vars_col[name]

		elif name in self.free_vars:
			for free_var_col in self._free_var_cols:
				if free_var_col.name==name:
					column=free_var_col
					break
			if column is None:
				raise ValueError("Could not find free variable'%s'"%(name))

		else:
			raise ValueError("Unknown name '%s'"%(name))

		return column

	#Returns the current constant column position
	def get_constant_column(self):
		return ConstantCol()

	#Returns an expression object for the given column->coeff mapping
	def get_expression(self,exp_coeff):
		return SparseExp(exp_coeff)

	#Get an equality constraint with the given expression coefficients
	def get_equality(self,exp_coeff):
		return self._get_constraint(exp_coeff,SparseEquality)

	#Get an inequality constraint with the given expression coefficients
	def get_inequality(self,exp_coeff):
		return self._get_constraint(exp_coeff,SparseInequality)

	#Get a SparseConjunction with the given constraints
	def get_conjunction(self,constraints=None):
		return SparseConjunction(constraints)

	#Clears this formula's disjunction of all conjunctions
	def clear(self):
		self._check_mutate()
		self.disjunction.clear()

	#Add the given SparseConjunction (collection of constraints) to the formula
	def add_conjunction(self,conjunction):
		#Make sure this sparse formula can be modified
		self._check_mutate()

		#Add the constraint to the constraints collection
		self.disjunction.add_conjunction(conjunction)

	#Merge the given SparseDisjunction (collection of conjunctions) with the existing disjunction
	def add_disjunction(self,disjunction):
		#Make sure this sparse formula can be modified
		self._check_mutate()

		#Merge the disjunctions
		self.disjunction.add_disjunction(disjunction)

	#Get a function with the given expression coefficients
	def get_function(self,name,arg_exps):
		args=[SparseExp(arg_exp) for arg_exp in arg_exps]
		ufcall=UFCall(name,args)
		return ufcall

	#Returns all of the lower bound expressions of each conjunction for the given variable
	#The format is: (set(lb_conj1),...,set(lb_conjn))
	def lower_bounds(self,tuple_var_name):
		return tuple([bounds[0] for bounds in self.bounds(tuple_var_name)])

	#Returns all of the upper bound expressions of each conjunction for the given variable
	#The format is: (set(ub_conj1),...,set(ub_conjn))
	def upper_bounds(self,tuple_var_name):
		return tuple([bounds[1] for bounds in self.bounds(tuple_var_name)])

	#Returns all of the lower and upper bound expressions of each conjunction for the given variable
	#The format is: ((set(lb_conj1),set(ub_conj1)),...,(set(lb_conjn),set(ub_conjn)))
	def bounds(self,tuple_var_name):
		return self.disjunction.bounds(self.get_column(tuple_var_name))

	#Returns True if this formula contains an instance of the given nested functions
	#Example: nest=('f','g')
	#Returns True if this formula's constraints contain the function nesting f(g(...))
	def contains_nest(self,nest):
		return self.disjunction.contains_nest(nest)

	# End public methods/properties
	#--------------------------------------------------

# End SparseFormula class
#--------------------------------------------------

#--------------------------------------------------
# Start Set class

#Represents a sparse set
class Set(SparseFormula):

	#--------------------------------------------------
	# Start Set constructor

	#Takes a set string, ex {[a]: a>10}
	#Also, an optional parameter, 'symbolics', is a collection
	#of instances of the iegen.Symbolic class.
	def __init__(self,set_string=None,symbolics=None,tuple_var_names=None,free_var_names=None,disjunction=None,freeze=True):
		#Determine how to construct this set based on the presence of the set string
		if set_string is None:
			#Construct this set using the given tuple variable names, free variable names, and symbolics
			self._construct(tuple_var_names=tuple_var_names,free_var_names=free_var_names,symbolics=symbolics,disjunction=disjunction,freeze=freeze)
		else:
			#Parse the given set string
			pres_formulas=self._parse_formula_string(set_string,symbolics,PresParser.parse_set)

			#Construct this set using the construction utility method
			self._construct(pres_formulas=pres_formulas,symbolics=symbolics,freeze=freeze)

	# End Set constructor
	#--------------------------------------------------

	#--------------------------------------------------
	# Start property support methods

	#Returns the set tuple variables
	def _tuple_set(self):
		return self.tuple_vars

	# End property support methods
	#--------------------------------------------------

	#--------------------------------------------------
	# Start public methods/properties

	#Property creation
	tuple_set=property(_tuple_set)

	#Returns the arity of this set
	def arity(self):
		return self._arity()

	#Returns a copy of this Set
	def copy(self,**kwargs):
		#Make a copy of this Set
		selfcopy=self._copy(FormulaClass=Set,**kwargs)

		return selfcopy

	#The union operation
	def union(self,other):
		res=self._union(other,Set)
		res.freeze()
		self.print_debug('Set Union: %s.union(%s)=%s'%(self,other,res))
		return res

	#Application of a relation to a set: other(self)
	#Application of unions of relations to unions of sets is defined as:
	#Let S=S1 union S2 union ... union SN
	#Let R=R1 union R2 union ... union RM
	#
	#Then R(S)=R1(S1) union R1(S2) union ... union R1(SN) union
	#          R2(S1) union R2(S2) union ... union R2(SN) union
	#          ...
	#          RM(S1) union RM(S2) union ... union RM(SN)
	def apply(self,other):
		#Make sure the set and relation are frozen
		self._check_frozen()
		other._check_frozen()

		#Make sure the set's arity matches the input arity of the relation
		if self.arity()!=other.arity_in():
			raise ValueError('Apply failure: Input arity of relation (%d) does not match arity of set (%d)'%(other.arity_in(),self.arity()))

		#Collections for building the new set
		new_tuple_vars=[]
		new_free_vars=[]
		other_var_map={}
		self_var_map={}
		used_vars=set()

		#Determine the resutling set's tuple variable names
		get_unique_vars(other.tuple_out,new_tuple_vars,used_vars,other_var_map)

		#Determine the resulting set's free variable names
		get_unique_vars(other.tuple_in,new_free_vars,used_vars,other_var_map)
		get_unique_vars(self.tuple_set,new_free_vars,used_vars,self_var_map)
		get_unique_vars(other.free_vars,new_free_vars,used_vars,other_var_map)
		get_unique_vars(self.free_vars,new_free_vars,used_vars,self_var_map)

		#Get the combined symbolics for the new set
		new_symbolics=list(set(other.symbolics+self.symbolics))

		#Reposition the relation's output tuple variables
		new_var_pos={}
		for i in xrange(other.arity_in(),other.arity_in()+other.arity_out()):
			new_var_pos[i]=i-other.arity_in()

		#Create a new set with no constraints, we will build the constraints
		new_set=Set(tuple_var_names=new_tuple_vars,free_var_names=new_free_vars,symbolics=new_symbolics,freeze=False)

		#Create the constraints: cartesian product of both disjunctions + free variable equalities
		new_set._join(self,self.tuple_set,self_var_map,other,other.tuple_in,other_var_map,new_var_pos)

		#Freeze the new resulting set now that we're done modifying it
		new_set.freeze()

		self.print_debug('Apply: %s.apply(%s)=%s'%(self,other,new_set))

		return new_set

	#Returns the constraint matrix for this set
	def get_constraint_mat(self,symbolics=None):
		pos_map={}
		pos_count=1

		#Assign positions for variable names:
		# tuple vars - symbolics - constant column
		#Tuple vars
		for var_name in self.tuple_vars:
			pos_map[self.get_column(var_name)]=pos_count
			pos_count+=1

		#The given symbolics
		if symbolics is not None:
			for symbolic in symbolics:
				pos_map[SymbolicCol(symbolic)]=pos_count
				pos_count+=1

		#Constaint column
		pos_map[self.get_constant_column()]=pos_count

		return self._get_mat(pos_map,True,False)

	# End public methods
	#--------------------------------------------------

# End Set class
#--------------------------------------------------

#--------------------------------------------------
# Start Relation class

#Represents a sparse relation
class Relation(SparseFormula):
	__slots__=('_arity_in',)

	#--------------------------------------------------
	# Start Relation constructor

	#Takes a relation string, ex {[a]->[a']: a>10}
	#Also, an optional parameter, 'symbolics', is a collection
	#of instances of the iegen.Symbolic class.
	def __init__(self,relation_string=None,symbolics=None,tuple_var_names=None,arity_in=None,free_var_names=None,disjunction=None,freeze=True):
		#Determine how to construct this relation based on the presence of the relation string
		if relation_string is None:
			#Construct this relation using the given tuple variable names, free variable names, and symbolics
			self._construct(tuple_var_names=tuple_var_names,free_var_names=free_var_names,symbolics=symbolics,disjunction=disjunction,freeze=freeze)

			self._arity_in=arity_in
		else:
			#Parse the given relation string
			pres_formulas=self._parse_formula_string(relation_string,symbolics,PresParser.parse_relation)

			#Construct this relation using the construction utility method
			self._construct(pres_formulas=pres_formulas,symbolics=symbolics,freeze=freeze)

			#Determine the input arity
			self._arity_in=pres_formulas[0].arity_in()

	# End Relation constructor
	#--------------------------------------------------

	#--------------------------------------------------
	# Start property support methods

	#Returns the input tuple variables
	def _tuple_in(self):
		return self.tuple_vars[:self.arity_in()]

	#Returns the output tuple variables
	def _tuple_out(self):
		return self.tuple_vars[self.arity_in():]

	# End property support methods
	#--------------------------------------------------

	#--------------------------------------------------
	# Start public methods/properties

	#Property creation
	tuple_in=property(_tuple_in)
	tuple_out=property(_tuple_out)

	#Returns a 2-tuple of the input/output arity of this relation
	def arity(self):
		return (self.arity_in(),self.arity_out())

	#Returns the input arity of this relation
	def arity_in(self):
		return self._arity_in

	#Returns the output arity of this relation
	def arity_out(self):
		return self._arity()-self._arity_in

	#Returns a copy of this Relation
	def copy(self,**kwargs):
		#Make a copy of this Relation
		selfcopy=self._copy(FormulaClass=Relation,**kwargs)

		#Determine the input arity
		selfcopy._arity_in=self.arity_in()

		return selfcopy

	def union(self,other):
		res=self._union(other,Relation)
		res._arity_in=self.arity_in()
		res.freeze()
		self.print_debug('Relation Union: %s.union(%s)=%s'%(self,other,res))
		return res

	def inverse(self):
		#Make sure this relation is frozen
		self._check_frozen()

		#Mapping from int -> int (old pos to new pos)
		new_var_pos={}

		#Move the input tuple vars to the output tuple vars
		for pos in xrange(self.arity_in()):
			new_var_pos[pos]=pos+self.arity_out()

		#Move the output tuple vars to the input tuple vars
		for pos in xrange(self.arity_in(),self.arity_in()+self.arity_out()):
			new_var_pos[pos]=pos-self.arity_in()

		#Create a copy of self and update the tuple columns during the copy
		selfcopy=self.copy(new_var_pos=new_var_pos,freeze=False)

		#Set the input arity of the inverse relation
		selfcopy._arity_in=self.arity_out()

		selfcopy.freeze()

		self.print_debug('Relation Inverse: %s.inverse()=%s'%(self,selfcopy))

		return selfcopy

	#Relation composition: self(other)
	#Composition of unions of relations is defined as:
	#Let R1=R11 union R12 union ... union R1N
	#Let R2=R21 union R22 union ... union R2M
	#
	#Then R1(R2)=R11(R21) union R11(R22) union ... union R11(R2M) union
	#            R12(R21) union R12(R22) union ... union R12(R2M) union
	#            ...
	#            R1N(R21) union R1N(R22) union ... union R1N(R2M)
	def compose(self,other):
		#Make sure the relations are frozen
		self._check_frozen()
		other._check_frozen()

		#Make sure the second relations's output arity matches the first relation's input arity
		if other.arity_out()!=self.arity_in():
			raise ValueError('Compose failure: Output arity of second relation (%d) does not match input arity of first relation (%d)'%(other.arity_out(),self.arity_in()))

		#Collections for building the new relation
		new_tuple_vars=[]
		new_free_vars=[]
		other_var_map={}
		self_var_map={}
		used_vars=set()

		#Determine the resutling relation's tuple variable names
		get_unique_vars(other.tuple_in,new_tuple_vars,used_vars,other_var_map)
		get_unique_vars(self.tuple_out,new_tuple_vars,used_vars,self_var_map)

		#Determine the resulting relation's free variable names
		get_unique_vars(other.tuple_out,new_free_vars,used_vars,other_var_map)
		get_unique_vars(self.tuple_in,new_free_vars,used_vars,self_var_map)
		get_unique_vars(other.free_vars,new_free_vars,used_vars,other_var_map)
		get_unique_vars(self.free_vars,new_free_vars,used_vars,self_var_map)

		#Get the combined symbolics for the new relation
		new_symbolics=list(set(other.symbolics+self.symbolics))

		#Reposition the relation's output tuple variables
		new_var_pos={}
		for i in xrange(self.arity_in(),self.arity_in()+self.arity_out()):
			new_var_pos[i]=i+other.arity_in()-self.arity_in()

		#Create a new relation with no constraints, we will build the constraints
		new_relation=Relation(tuple_var_names=new_tuple_vars,arity_in=other.arity_in(),free_var_names=new_free_vars,symbolics=new_symbolics,freeze=False)

		#Create the constraints: cartesian product of both disjunctions + free variable equalities
		new_relation._join(other,other.tuple_out,other_var_map,self,self.tuple_in,self_var_map,new_var_pos)

		#Freeze the new resulting relation now that we're done modifying it
		new_relation.freeze()

		self.print_debug('Compose: \n\t%s\n\n\t.compose(%s)\n\n\t' %(self,other) )
		self.print_debug('\n\tCompose output: %s\n' %(new_relation))

		return new_relation

	#Restrict domain:
	#Let R=R1 union R2 union ... union RN
	#Let S=S1 union S2 union ... union SM
	#
	#Then R\S=R1\S1 union R1\S2 union ... union R1\SM union
	#         R2\S1 union R2\S2 union ... union R2\SM union
	#         ...
	#         RN\S1 union RN\S2 union ... union RN\SM
	def restrict_domain(self,other):
		#Make sure the relations are frozen
		self._check_frozen()
		other._check_frozen()

		#Make sure the set's arity matches the relation's input arity
		if other.arity()!=self.arity_in():
			raise ValueError('Restrict domain failure: Input arity of relation (%d) does not match arity of set (%d)'%(self.arity_in(),other.arity()))

		#Collections for building the new relation
		new_tuple_vars=[]
		new_free_vars=[]
		other_var_map={}
		self_var_map={}
		used_vars=set()

		#Determine the resutling relation's tuple variable names
		get_unique_vars(self.tuple_in,new_tuple_vars,used_vars,self_var_map)
		get_unique_vars(self.tuple_out,new_tuple_vars,used_vars,self_var_map)

		#Determine the resulting relation's free variable names
		get_unique_vars(other.tuple_vars,new_free_vars,used_vars,other_var_map)
		get_unique_vars(other.free_vars,new_free_vars,used_vars,other_var_map)
		get_unique_vars(self.free_vars,new_free_vars,used_vars,self_var_map)

		#Get the combined symbolics for the new relation
		new_symbolics=list(set(other.symbolics+self.symbolics))

		#Create a new relation with no constraints, we will build the constraints
		new_relation=Relation(tuple_var_names=new_tuple_vars,arity_in=self.arity_in(),free_var_names=new_free_vars,symbolics=new_symbolics,freeze=False)

		#Create the constraints: cartesian product of both disjunctions + free variable equalities
		new_relation._join(self,self.tuple_in,self_var_map,other,other.tuple_vars,other_var_map,None)

		#Freeze the new resulting relation now that we're done modifying it
		new_relation.freeze()

		self.print_debug('Compose: \n\t%s\n\n\t.compose(%s)\n\n\t' %(self,other) )
		self.print_debug('\n\tCompose output: %s\n' %(new_relation))

		return new_relation

	#Restrict range:
	#Let R=R1 union R2 union ... union RN
	#Let S=S1 union S2 union ... union SM
	#
	#Then R/S=R1/S1 union R1/S2 union ... union R1/SM union
	#         R2/S1 union R2/S2 union ... union R2/SM union
	#         ...
	#         RN/S1 union RN/S2 union ... union RN/SM
	def restrict_range(self,other):
		#Make sure the relations are frozen
		self._check_frozen()
		other._check_frozen()

		#Make sure the set's arity matches the relation's input arity
		if other.arity()!=self.arity_out():
			raise ValueError('Restrict range failure: Output arity of relation (%d) does not match arity of set (%d)'%(self.arity_out(),other.arity()))

		#Collections for building the new relation
		new_tuple_vars=[]
		new_free_vars=[]
		other_var_map={}
		self_var_map={}
		used_vars=set()

		#Determine the resutling relation's tuple variable names
		get_unique_vars(self.tuple_in,new_tuple_vars,used_vars,self_var_map)
		get_unique_vars(self.tuple_out,new_tuple_vars,used_vars,self_var_map)

		#Determine the resulting relation's free variable names
		get_unique_vars(other.tuple_vars,new_free_vars,used_vars,other_var_map)
		get_unique_vars(other.free_vars,new_free_vars,used_vars,other_var_map)
		get_unique_vars(self.free_vars,new_free_vars,used_vars,self_var_map)

		#Get the combined symbolics for the new relation
		new_symbolics=list(set(other.symbolics+self.symbolics))

		#Create a new relation with no constraints, we will build the constraints
		new_relation=Relation(tuple_var_names=new_tuple_vars,arity_in=self.arity_in(),free_var_names=new_free_vars,symbolics=new_symbolics,freeze=False)

		#Create the constraints: cartesian product of both disjunctions + free variable equalities
		new_relation._join(self,self.tuple_out,self_var_map,other,other.tuple_vars,other_var_map,None)

		#Freeze the new resulting relation now that we're done modifying it
		new_relation.freeze()

		self.print_debug('Compose: \n\t%s\n\n\t.compose(%s)\n\n\t' %(self,other) )
		self.print_debug('\n\tCompose output: %s\n' %(new_relation))

		return new_relation

	#Returns the constraint matrix for the scattering function for this relation
	def get_scatter_mat(self,symbolics=None):
		pos_map={}
		pos_count=1

		#Assign positions for variable names:
		# out tuple vars - in tuple vars - given symbolics - constant column
		#Output tuple variables and input tuple variables
		for var_name in self.tuple_out+self.tuple_in:
			pos_map[self.get_column(var_name)]=pos_count
			pos_count+=1

		#The given symbolics
		if symbolics is not None:
			for symbolic in symbolics:
				pos_map[SymbolicCol(symbolic)]=pos_count
				pos_count+=1

		#Constant column
		pos_map[self.get_constant_column()]=pos_count

		return self._get_mat(pos_map,False,True)

	# End public methods/properties
	#--------------------------------------------------

# End Relation class
#--------------------------------------------------

#--------------------------------------------------
# Start SparseExpColumnType classes

#Parent class of the various sparse expression column type classes
class SparseExpColumnType(IEGenObject):
	def __hash__(self):
		raise ValueError('This __hash__ implementation should never be called')

	def __eq__(self,other):
		raise ValueError('This __eq__ implementation should never be called')

	def __ne__(self,other):
		return not self==other

	def __str__(self):
		return repr(self)

	def get_function_names(self):
		return []

	def is_function(self):
		return False

	def is_tuple_var(self):
		return False

	def is_free_var(self):
		return False

	def contains_nest(self,nest):
		return False

class SparseExpNameColumnType(SparseExpColumnType):
	__slots__=('name','_mem_hash')

	def __init__(self,name):
		self.name=name
		self._mem_hash=hash((self.__class__.__name__,self.name))

	def __hash__(self):
		return self._mem_hash

	def __eq__(self,other):
		try:
			return self.__class__.__name__==other.__class__.__name__ and self.name==other.name
		except AttributeError as e:
			return False

	def __repr__(self):
		return "%s(%s)"%(self.__class__.__name__,repr(self.name))

	def exp_str(self,**kwargs):
		return self.name

class FreeVarCol(SparseExpNameColumnType):
	def __init__(self,name):
		SparseExpNameColumnType.__init__(self,name)

	def copy(self,new_var_names=None,**kwargs):
		name=self.name

		#Change the name if necessary
		if new_var_names is not None and name in new_var_names:
			name=new_var_names[self.name]

		return FreeVarCol(name)

	def is_free_var(self):
		return True

class ConstantCol(SparseExpNameColumnType):
	def __init__(self):
		SparseExpNameColumnType.__init__(self,'')

	def copy(self,**kwargs):
		return ConstantCol()

class TupleVarCol(SparseExpColumnType):
	__slots__=('pos','name')

	def __init__(self,pos,name=None):
		self.pos=pos
		self.name=name
		self._mem_hash=hash((self.__class__.__name__,self.pos))

	def __hash__(self):
		return self._mem_hash

	def __eq__(self,other):
		try:
			return self.__class__.__name__==other.__class__.__name__ and self.pos==other.pos
		except AttributeError as e:
			return False

	def __lt__(self,other):
		try:
			return self.pos<other.pos
		except AttributeError as e:
			return False

	def __gt__(self,other):
		try:
			return other.__lt__(self)
		except AttributeError as e:
			return False

	def __le__(self,other):
		return self==other or self<other

	def __ge__(self,other):
		return other<=self

	def __repr__(self):
		return '%s(%s,%s)'%(self.__class__.__name__,repr(self.pos),repr(self.name))

	def __str__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.pos))

	def copy(self,new_var_pos=None,new_var_names=None,**kwargs):
		pos=self.pos
		name=self.name

		#Change the column position if necessary
		if new_var_pos is not None and pos in new_var_pos:
			pos=new_var_pos[pos]

		#Change the name if necessary
		if new_var_names is not None and name in new_var_names:
			name=new_var_names[name]

		return TupleVarCol(pos,name)

	def exp_str(self,**kwargs):
		return self.name

	def is_tuple_var(self):
		return True

class SymbolicCol(SparseExpColumnType):
	__slots__=('sym',)

	def __init__(self,sym):
		self.sym=sym

	def __hash__(self):
		return hash(self.sym)

	def __eq__(self,other):
		try:
			return self.sym==other.sym
		except AttributeError as e:
			return False

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.sym))

	def __str__(self):
		return '%s(%s)'%(self.__class__.__name__,self.sym.name)

	def copy(self,**kwargs):
		return SymbolicCol(self.sym)

	def exp_str(self,**kwargs):
		return self.sym.name

#Represents an instance of an uninterpreted function call
class UFCall(SparseExpColumnType):
	__slots__=('name','args')

	def __init__(self,name,args):
		self.name=name

		#Simplify each argument
		for arg in args:
			arg.simplify()

		self.args=tuple(args)

	def __hash__(self):
		return hash((self.name,self.args))

	def __eq__(self,other):
		try:
			return self.name==other.name and self.args==other.args
		except AttributeError as e:
			return False

	def __repr__(self):
		return '%s(%s,%s)'%(self.__class__.__name__,repr(self.name),repr(self.args))

	def __str__(self):
		return self.value_string()

	def value_string(self,function_name_map=None):
		if function_name_map is None:
			function_name_map={}

		arg_strs=[arg.value_string(function_name_map) for arg in self.args]

		name_start=self.name+'('
		name_end=')'
		if self.name in function_name_map:
			name_start,name_end=function_name_map[self.name]

		return '%s%s%s'%(name_start,','.join(arg_strs),name_end)

	def get_function_names(self):
		function_names=[function_name for arg in self.args for function_name in arg.get_function_names()]
		function_names.append(self.name)
		return list(set(function_names))

	def is_function(self):
		return True

	def var_is_function_input(self,var_col):
		return any((var_col in arg or arg.var_is_function_input(var_col) for arg in self.args))

	def contains_nest(self,nest):
		if self.name==nest[0] and 1==len(self.args) and 1==len(self.args[0]):
			if len(nest)==1:
				return self.args[0]
			else:
				return list(self.args[0])[0][0].contains_nest(nest[1:])
		else:
			return None

	def replace_var(self,var_col,equal_coeff,equal_exp):
		for arg in self.args:
			arg.replace_var(var_col,equal_coeff,equal_exp.copy())

	def copy(self,collapse=None,**kwargs):
		copy_args=None
		copy_name=self.name
		if collapse is not None:
			for nest in collapse:
				inner=self.contains_nest(nest)
				if inner:
					copy_args=[inner.copy(collapse=collapse,**kwargs)]
					copy_name='_'.join(nest)
					break

		if copy_args is None:
			copy_args=[arg.copy(**kwargs) for arg in self.args]

		return UFCall(copy_name,copy_args)

	def exp_str(self,function_name_map=None,**kwargs):
		return self.value_string(function_name_map)

# End SparseExpColumnType classes
#--------------------------------------------------

#--------------------------------------------------
# Start SparseExp class

#Represents a sparse expression (an affine expression plus uninterpreted function symbols)
class SparseExp(IEGenObject):
	__slots__=('exp','_mem_hash','_mem_fset')

	def __init__(self,exp_coeff={}):
		self._mem_hash=None
		self._mem_fset=None
		self.exp=defaultdict(int,exp_coeff)
		self.simplify()

	def __hash__(self):
		if self._mem_hash is None:
			self._update()
		return self._mem_hash

	def _update(self):
		self._mem_fset=frozenset(((col,str(coeff)) for col,coeff in sorted(self)))
		self._mem_hash=hash(self._mem_fset)

	def __eq__(self,other):
		try:
			if self._mem_fset is None:
				self._update()
			if other._mem_fset is None:
				other._update()

			return self._mem_fset==other._mem_fset
		except AttributeError as e:
			return False

	def __ne__(self,other):
		return not self==other

	def __len__(self):
		return len(self.exp)

	def __iter__(self):
		return self.exp.iteritems()

	def __getitem__(self,key):
		return self.exp[key]

	def __setitem__(self,key,value):
		self.exp[key]=value

	def __contains__(self,item):
		return item in self.exp

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.exp))

	def __str__(self):
		return self.value_string()

	def value_string(self,function_name_map=None):
		if function_name_map is None:
			function_name_map={}

		term_strs=[]

		#If there are no terms, just return '0'
		if 0==len(self):
			return '0'
		else:
			#Look at each term
			for term,coeff in self:
				#Handle the constant
				if ConstantCol()==term:
					term_strs.append('%s'%(coeff))
				else:
					#If the coefficient is not 0, add it to the list of expression strings
					if 1==coeff:
						term_strs.append('%s'%(term.exp_str(function_name_map=function_name_map)))
					else:
						term_strs.append('%s%s'%(coeff,term.exp_str(function_name_map=function_name_map)))

			#Return a string for the sum of all expression strings
			return '+'.join(term_strs)

	def get_function_names(self):
		return list(set([function_name for term,coeff in self for function_name in term.get_function_names()]))

	def var_is_function_input(self,var_col):
		return any((term.is_function() and term.var_is_function_input(var_col) for term,coeff in self))

	def function_terms(self):
		return ((term,coeff) for term,coeff in self if term.is_function())

	def remove_term(self,var_col):
		if var_col in self:
			del self.exp[var_col]
			self._update()
		else:
			raise ValueError("Column '%s' is not present in this expression (%s)"%(var_col,self))

	def multiply(self,factor):
		for key in self.exp.keys():
			#TODO: Bug is here?
			coeff=self[key]
			coeff*=factor
			self[key]=coeff
		self._update()

	def add_exp(self,other_exp):
		for term,coeff in other_exp:
			self[term]+=coeff
		self._update()

	def get_equality_pair(self,var_col):
		#Grab the coefficient of the variable
		equal_coeff=self[var_col]

		#Grab a copy of thise expression
		equal_exp=self.copy()

		#Remove the variable from the expression
		equal_exp.remove_term(var_col)

		#Multiply all of the terms by the opposite of the sign
		# of the variable's coefficient
		equal_exp.multiply(-1*sign(equal_coeff))

		#Make the coefficient positive
		equal_coeff=sign(equal_coeff)*equal_coeff

		return (equal_coeff,equal_exp)

	def get_mat(self,pos_map,make_positive,make_negative):
		mat=[0]*(len(pos_map)+1)

		for col,pos in pos_map.iteritems():
			mat[pos]=self[col]

		#Make sure the first non-zero coefficient is either
		# positive or negative, depending on the given parameter
		negate_terms=False
		found_nonzero=False
		for pos in xrange(len(mat)):
			if 0!=mat[pos] and not found_nonzero:
				found_nonzero=True
				if make_positive and mat[pos]<0:
					negate_terms=True
				elif make_negative and mat[pos]>0:
					negate_terms=True
				else:
					break

			if negate_terms:
				mat[pos]*=-1

		#If there is only one non-zero coefficient AND
		# make_negative is true, make the single coefficient positive
		if 1==sum(map(lambda x: 0 if x==0 else 1,mat)):
			for pos in xrange(len(mat)):
				if 0!=mat[pos]:
					mat[pos]=abs(mat[pos])

		return mat

	def contains_nest(self,nest):
		return any((term.contains_nest(nest) for term,coeff in self))

	def replace_var(self,var_col,equal_coeff,equal_exp):
		#Replace the variable within any function terms of this expression
		for term in self.exp.keys():
			if term.is_function():
				#Grab the current coefficient for the function term
				coeff=self[term]

				#Remove the term from the expression
				self.remove_term(term)

				#Replace the variable within the function's arguments
				term.replace_var(var_col,equal_coeff,equal_exp)

				#Add the term back to the expression
				self[term]+=coeff

		#Determine if the given variable is present in this expression
		if var_col in self:
			#Get the coefficient of the variable in this expression
			var_coeff=self[var_col]

			#Remove the variable from this expression
			self.remove_term(var_col)

			#Multiply all other terms by the coefficient of the variable
			# in the original equality
			self.multiply(equal_coeff)

			#Multiply the equal expression by the coefficient
			# of the variable in this expression
			equal_exp.multiply(var_coeff)

			#Add the equal expression to this expression
			self.add_exp(equal_exp)

		self._update()

	def simplify(self):
		#Remove all terms with a coefficient of 0
		remove_terms=[]
		for term,coeff in self:
			if 0==coeff:
				remove_terms.append(term)
		for remove_term in remove_terms:
			self.remove_term(remove_term)

		self._update()

	def copy(self,new_cols=None,**kwargs):
		new_cols={} if new_cols is None else new_cols
		exp_copy={}

		for term,coeff in self:
			if term in new_cols:
				exp_copy[new_cols[term].copy(new_cols=new_cols,**kwargs)]=coeff
			else:
				exp_copy[term.copy(new_cols=new_cols,**kwargs)]=coeff

		return SparseExp(exp_copy)

	#Returns the complement of this sparse expression
	#That is, the same sparse expression with all coefficients negated
	def complement(self):
		comp_exp=self.copy()
		comp_exp.multiply(-1)
		return comp_exp

# End SparseExp class
#--------------------------------------------------

#--------------------------------------------------
# Start SparseConstraint classes

#Represents a sparse constraint (equality or inequality)
#Create instances of SparseEquality and SparseInequality not SparseConstraint
class SparseConstraint(IEGenObject):
	__slots__=('_sparse_exp',)

	def __init__(self,exp_coeff=None,sparse_exp=None):
		if exp_coeff is None:
			self._sparse_exp=sparse_exp
		else:
			self._sparse_exp=SparseExp(exp_coeff)

	def __hash__(self):
		return hash(self.op+str(hash(self.hash_exp)))

	def __eq__(self,other):
		try:
			return self.op==other.op and self.hash_exp==other.hash_exp
		except AttributeError as e:
			return False

	def __ne__(self,other):
		return not self==other

	def __len__(self):
		return len(self._sparse_exp)

	def __iter__(self):
		return iter(self._sparse_exp)

	def __getitem__(self,key):
		return self._sparse_exp[key]

	def __contains__(self,item):
		return item in self._sparse_exp

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,self._sparse_exp.exp)

	def __str__(self):
		lhs_exp_strs=[]
		rhs_exp_strs=[]

		#Look at each term
		for term,coeff in self:
			#Only work with non-zero coefficients
			if 0!=coeff:
				#Handle the constant
				if ConstantCol()==term:
					if coeff>0:
						lhs_exp_strs.append('%s'%(coeff))
					else:
						rhs_exp_strs.append('%s'%(-1*coeff))
				else:
					#If the coefficient is not 0, add it to the list of expression strings
					if coeff>0:
						if 1==coeff:
							lhs_exp_strs.append('%s'%(term.exp_str()))
						else:
							lhs_exp_strs.append('%s%s'%(coeff,term.exp_str()))
					else:
						if -1==coeff:
							rhs_exp_strs.append('%s'%(term.exp_str()))
						else:
							rhs_exp_strs.append('%s%s'%(-1*coeff,term.exp_str()))

		lhs_exp_str='+'.join(lhs_exp_strs)
		rhs_exp_str='+'.join(rhs_exp_strs)

		if ''==lhs_exp_str:
			lhs_exp_str='0'

		if ''==rhs_exp_str:
			rhs_exp_str='0'

		return lhs_exp_str+self.op+rhs_exp_str

	def _get_op(self):
		return self._op
	op=property(_get_op)

	def _get_mat_id(self):
		return self._mat_id
	mat_id=property(_get_mat_id)

	def get_sparse_exp(self):
		return self._sparse_exp

	def is_equality(self):
		return False

	def get_function_names(self):
		return self._sparse_exp.get_function_names()

	def is_contradiction(self):
		return False

	def var_is_function_input(self,var_col):
		return self._sparse_exp.var_is_function_input(var_col)

	def function_terms(self):
		return self._sparse_exp.function_terms()

	def get_equality_pair(self,var_col):
		return self._sparse_exp.get_equality_pair(var_col)

	def get_mat(self,pos_map,make_positive,make_negative):
		if not self.is_equality():
			make_positive=False
			make_negative=False

		mat=self._sparse_exp.get_mat(pos_map,make_positive,make_negative)
		mat[0]=self.mat_id
		return tuple(mat)

	def replace_var(self,var_col,equal_coeff,equal_exp):
		self._sparse_exp.replace_var(var_col,equal_coeff,equal_exp)

	def simplify(self):
		self._sparse_exp.simplify()
		self.inverse_simplify()
		self.remove_function_simplify()
		self.move_functions_simplify()
		self.move_function_simplify()

	#Inverse simplification
	def inverse_simplify(self):
		#Only consider equality constraints
		if self.is_equality():
			#Look at each function term in this constraint
			for function_term,function_coeff in self.function_terms():
				#Only consider function terms that:
				#-Have a coefficient of 1
				#-Have an inverse
				#-Have a single argument that is a free variable
				if 1==abs(function_coeff) and function_term.name in iegen.simplify.inverse_pairs() and 1==len(function_term.args) and list(function_term.args[0])[0][0].is_free_var():
					new_exp=SparseExp()
					new_arg=SparseExp()

					#Create the argument to the new function
					for term,coeff in self:
						#Exclude the function itself
						if term!=function_term:
							new_arg[term.copy()]=-1*sign(function_coeff)*coeff

					#Create the new function
					func_name=function_term.name
					new_func_name=iegen.simplify.inverse_pairs()[func_name]
					new_func=UFCall(new_func_name,[new_arg])

					#Add the new function to the new expression
					new_exp.add_exp(SparseExp({new_func:-1}))

					#Add the argument from the function to the new expression
					new_exp.add_exp(function_term.args[0].copy())

					#Set the new expression for this constraint to the new expression
					self._sparse_exp=new_exp

					#Notify all listeners that this rule has fired
					iegen.simplify.notify_inverse_simplify_listeners(func_name,new_func_name)

	#Converts f(i)=f(j) -> i=j if f has an inverse
	def remove_function_simplify(self):
		#Only consider equalities with 2 constraints
		if self.is_equality() and 2==len(self):
			#Get the terms of this constraint that are functions
			function_terms=list(self.function_terms())

			#If both terms are functions
			if 2==len(function_terms):
				f1,f1_coeff=function_terms[0]
				f2,f2_coeff=function_terms[1]

				#If both functions:
				#-have the same name
				#-the function has a known inverse
				#-have 1/-1 coefficients
				#-are on opposite sides of the equality
				#-have only one argument each
				if f1.name==f2.name and f1.name in iegen.simplify.inverse_pairs() and 1==abs(f1_coeff) and 1==abs(f2_coeff) and f1_coeff==-1*f2_coeff and 1==len(f1.args) and 1==len(f2.args):
					f1_arg,f1_arg_coeff=list(f1.args[0])[0]
					f2_arg,f2_arg_coeff=list(f2.args[0])[0]

					#Create the constraint f1.args = f2.args instead
					self._sparse_exp=SparseExp({f1_arg.copy():f1_arg_coeff,f2_arg.copy():-1*f2_arg_coeff})

	#Converts f(i)=g(j) -> i=f_inv(g(j)) if the inverse of f is f_inv
	#Also, the tuple variable with the 'largest' position will be i in the above example
	def move_functions_simplify(self):
		#Only consider equalities with 2 constraints
		if self.is_equality() and 2==len(self):
			#Get the terms of this constraint that are functions
			function_terms=list(self.function_terms())

			#If both terms are functions
			if 2==len(function_terms):
				f1,f1_coeff=function_terms[0]
				f2,f2_coeff=function_terms[1]

				#If both functions:
				#-have 1/-1 coefficients
				#-are on opposite sides of the equality
				#-have only one argument each
				#-each argument has only a single term
				if 1==abs(f1_coeff) and 1==abs(f2_coeff) and f1_coeff==-1*f2_coeff and 1==len(f1.args) and 1==len(f2.args) and 1==len(f1.args[0]) and 1==len(f2.args[0]):
					#Get each function's single term argument
					f1_arg,f1_arg_coeff=list(f1.args[0])[0]
					f2_arg,f2_arg_coeff=list(f2.args[0])[0]

					#If both arguments are tuple variables
					if f1_arg.is_tuple_var() and f2_arg.is_tuple_var():
						move=False

						if f1_arg.pos>f2_arg.pos and f1.name in iegen.simplify.inverse_pairs():
							move=True
						elif f2_arg.pos>f1_arg.pos and f2.name in iegen.simplify.inverse_pairs():
							move=True
							f1,f2=f2,f1
							f1_coeff,f2_coeff=f2_coeff,f1_coeff
							f1_arg,f2_arg=f2_arg,f1_arg
							f1_arg_coeff,f2_arg_coeff=f2_arg_coeff,f1_arg_coeff

						if move:
							lhs=f1_arg.copy()
							f1_inv_name=iegen.simplify.inverse_pairs()[f1.name]
							rhs=UFCall(f1_inv_name,[SparseExp({f2.copy():1})])
							self._sparse_exp=SparseExp({lhs:1,rhs:-1})

							#Notify that we created and instance of f1_inv_name
							iegen.simplify.notify_inverse_simplify_listeners(f1.name,f1_inv_name)

	def move_function_simplify(self):
		#Only consider equalities with 2 constraints
		if self.is_equality() and 2==len(self):
			terms=list(self)
			term1,term1_coeff=terms[0]
			term2,term2_coeff=terms[1]

			#If one term is a function and the other is a tuple variable
			if (term1.is_tuple_var() and term2.is_function()) or (term1.is_function() and term2.is_tuple_var()):
				if term1.is_function():
					function,function_coeff=term1,term1_coeff
					tuple_var,tuple_var_coeff=term2,term2_coeff
				else:
					function,function_coeff=term2,term2_coeff
					tuple_var,tuple_var_coeff=term1,term1_coeff

				#If both terms:
				#-have 1/-1 coefficients
				#-are on opposite sides of the equality
				if 1==abs(tuple_var_coeff) and 1==abs(function_coeff) and tuple_var_coeff==-1*function_coeff:
					#If the function has a registered inverse
					if function.name in iegen.simplify.inverse_pairs():
						#If the function has a single argument with a single term
						if 1==len(function.args) and 1==len(function.args[0]):
							function_arg,function_arg_coeff=list(function.args[0])[0]

							#If that term is a tuple variable with a coefficient of 1
							# and that tuple variable's position is less that the other tuple variable's position
							if function_arg.is_tuple_var() and 1==function_arg_coeff and function_arg.pos>tuple_var.pos:
								function_inv_name=iegen.simplify.inverse_pairs()[function.name]
								new_function=UFCall(function_inv_name,[SparseExp({tuple_var.copy():1})])
								new_tuple_var=function_arg.copy()
								self._sparse_exp=SparseExp({new_tuple_var:1,new_function:-1})

								#Notify that we created an instance of the inverse function
								iegen.simplify.notify_inverse_simplify_listeners(function.name,function_inv_name)

	def contains_nest(self,nest):
		return self._sparse_exp.contains_nest(nest)

#Class representing a sparse equality constraint
class SparseEquality(SparseConstraint):
	_op='='
	_mat_id=0

	def __init__(self,exp_coeff=None,sparse_exp=None):
		SparseConstraint.__init__(self,exp_coeff=exp_coeff,sparse_exp=sparse_exp)

	def _get_hash_exp(self):
		complement=self._sparse_exp.complement()
		return frozenset([self._sparse_exp,complement])
	hash_exp=property(_get_hash_exp)

	def is_equality(self):
		return True

	#A contradiction is i=0 where i!=0 (1=0, -1=0, 10=0, etc.)
	#By design, the ConstantCol() is only present in a constraint
	# when a constant is present AND non-zero
	#Therefore, checking for a length of 1 and that the ConstantCol()
	# is present in a constraint is sufficient to check for a contradiction
	def is_contradiction(self):
		res=False
		if len(self)==1:
			if ConstantCol() in self:
				res=True

		return res

	def copy(self,**kwargs):
		return SparseEquality(sparse_exp=self._sparse_exp.copy(**kwargs))

#Class representing a sparse inequality constraint
class SparseInequality(SparseConstraint):
	_op='>='
	_mat_id=1

	def _get_hash_exp(self):
		return self._sparse_exp
	hash_exp=property(_get_hash_exp)

	def copy(self,**kwargs):
		return SparseInequality(sparse_exp=self._sparse_exp.copy(**kwargs))

# End SparseConstraint classes
#--------------------------------------------------

#--------------------------------------------------
# Start SparseConjunction class

class SparseConjunction(IEGenObject):
	__slots__=('_constraints','_frozen')

	def __init__(self,constraints=None):
		constraints=[] if constraints is None else constraints

		self._constraints=list(constraints)
		self._frozen=False

	def __hash__(self):
		self._check_frozen()
		return hash(self.constraints)

	def __eq__(self,other):
		try:
			self._check_frozen()
			other._check_frozen()
			return self._constraints==other._constraints
		except AttributeError as e:
			return False

	def __ne__(self,other):
		return not self==other

	def __len__(self):
		return len(self.constraints)

	def __iter__(self):
		return iter(self.constraints)

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.constraints))

	def __str__(self):
		#Create strings for the constraints
		constraint_strings=[str(constraint) for constraint in self]

		#Create a single string for all of the constraints
		constraints_string=' and '.join(constraint_strings)

		return constraints_string

	def _check_frozen(self):
		#Make sure we're frozen
		if not self.frozen:
			raise ValueError('Cannot operate on a non-frozen sparse conjunction')

	def _check_mutate(self):
		#Make sure we're not frozen
		if self.frozen:
			raise ValueError('Cannot modify a frozen sparse conjunction')

	def _get_constraints(self):
		return self._constraints

	def _get_frozen(self):
		return self._frozen

	constraints=property(_get_constraints)
	frozen=property(_get_frozen)

	def get_function_names(self):
		return list(set([function_name for constraint in self for function_name in constraint.get_function_names()]))

	def contains_constraint(self,constraint):
		return constraint in self.constraints

	#Returns True if this conjunction contains a 0=1 constraint
	def is_contradiction(self):
		return any((constraint.is_contradiction() for constraint in self))

	def add_constraint(self,constraint):
		self._check_mutate()

		self._constraints.append(constraint)

	def remove_constraint(self,constraint):
		self._check_mutate()

		if self.contains_constraint(constraint):
			self._constraints.remove(constraint)
		else:
			raise ValueError("Cannot remove constraint '%s': constraint not present in conjunction"%(constraint))

	def add_conjunction(self,conjunction):
		self._check_mutate()

		#Add the given conjunctions constraints to this conjunction
		self._constraints.extend(conjunction.constraints)

		#Make the collection of constraints unique
		self._constraints=list(set(self._constraints))

	def find_equalities_with_var(self,var_col):
		equality_constraints=[]

		#Search through all constraints
		for constraint in self:
			#Make sure this constraint is an equality constraint
			if '='==constraint.op:
				if var_col in constraint:
					equality_constraints.append(constraint)

		return equality_constraints

	#Searches for all constraints with UFSs and determines
	# if any of these have the given variable as an input
	#This includes direct arguments and nested function arguments
	def var_is_function_input(self,var_col):
		return any((constraint.var_is_function_input(var_col) for constraint in self))

	def project_out(self,var_col):
		self._check_mutate()

		res=False

		#Search for equality constraints with the given variable column
		equality_constraints=self.find_equalities_with_var(var_col)

		#Attempt replacement using each equality constraint containing
		# the given variable column
		for equality_constraint in equality_constraints:
			#Get the coefficient/expression pair the variable is equal to
			equal_coeff,equal_exp=equality_constraint.get_equality_pair(var_col)

			#Replace all uses of the variable with the expression it is equal to if either:
			#-The variable we are replacing is not an input to a UFS
			#-The coefficient of the variable we are replacing is 1
			if not self.var_is_function_input(var_col) or equal_coeff==1:
				#Remove the equality constraint from this conjunction
				self.remove_constraint(equality_constraint)

				#Replace all uses of the variable in the remaining constraints
				for constraint in self:
					constraint.replace_var(var_col,equal_coeff,equal_exp.copy())

				res=True
				iegen.simplify.notify_equality_simplify_listeners()
				break

		#If equality replacement couldn't be performed, run standard Fourier-Motzkin
		if not res and not self.var_is_function_input(var_col):
			#Get the lower and upper bounds for the variable we are projecting out
			lower_bounds,upper_bounds=self.bounds(var_col,extra_info=True)

			#New constraints to be added
			add_constraints=[]

			#Constraint to be removed
			remove_constraints=set()

			if len(lower_bounds)>0 and len(upper_bounds)>0:
				iegen.simplify.notify_fm_listeners()

			#Look at each pair of lower/upper bounds
			for lb_coeff,lower_bound_orig,lb_constraint in lower_bounds:
				for ub_coeff,upper_bound_orig,ub_constraint in upper_bounds:
					lower_bound=lower_bound_orig.copy()
					upper_bound=upper_bound_orig.copy()

					#Create the new constraint:
					#ub_coeff*lower_bound <= lb_coeff*upper_bound
					lower_bound.multiply(ub_coeff)
					upper_bound.multiply(-1*lb_coeff)

					new_exp=SparseExp()
					new_exp.add_exp(lower_bound)
					new_exp.add_exp(upper_bound)
					new_exp=new_exp.complement()

					new_constraint=SparseInequality(sparse_exp=new_exp)
					add_constraints.append(new_constraint)

					remove_constraints.add(lb_constraint)
					remove_constraints.add(ub_constraint)

			#Remove all necessary constraints
			for constraint in remove_constraints:
				self.remove_constraint(constraint)

			#Add all new constraints
			for constraint in add_constraints:
				self.add_constraint(constraint)

			res=True

		return res

	def simplify(self):
		#Simplify all constraints
		for constraint in self:
			constraint.simplify()

		#Remove empty constraints
		self.remove_empty_constraints()

		#Remove 'true' constraints: these have the form:
		# constant >=0
		# where constant is >=0 itself
		self.remove_true_constraints()

		#Remove all constraints and replace with a 0=1 constraint IF
		# we find a pair of equalities such as v=0 and v=1
		self.remove_all_if_empty()

		#Discover equalities
		self.discover_equalities()

	def discover_equalities(self):
		remove_constraints=set()
		add_equalities=set()

		#Look at all pairs of inequality constraints
		for constraint1 in (c for c in self if not c.is_equality()):
			if constraint1 not in remove_constraints:
				for constraint2 in (c for c in self if not c.is_equality()):
					if constraint2 not in remove_constraints:
						if constraint1.get_sparse_exp()==constraint2.get_sparse_exp().complement():
							remove_constraints.add(constraint1)
							remove_constraints.add(constraint2)
							add_equalities.add(SparseEquality(sparse_exp=constraint1.get_sparse_exp().copy()))

		#Remove all necessary constraints
		for constraint in remove_constraints:
			self.remove_constraint(constraint)

		#Add all new equalities
		for constraint in add_equalities:
			self.add_constraint(constraint)

	def remove_empty_constraints(self):
		self._constraints=[constraint for constraint in self if len(constraint)>0]

	def remove_true_constraints(self):
		constraints=list(self.constraints)
		for constraint in constraints:
			if 1==len(constraint) and ConstantCol() in constraint:
				const_value=constraint[ConstantCol()]

				if constraint.is_equality() and 0==const_value:
					self.remove_constraint(constraint)
				elif not constraint.is_equality() and const_value>=0:
					self.remove_constraint(constraint)

	def remove_all_if_empty(self):
		is_empty=False

		#Map of tuple vars to constants they are equal to
		var_const_map=defaultdict(set)

		#Look at each equality constraint
		for constraint in (constraint for constraint in self if constraint.is_equality()):
			#Only consider equalities with one or two terms
			#Does the constraint have a single term?
			if len(constraint)==1:
				tuple_vars=[term for term,coeff in constraint if term.is_tuple_var()]

				#If the constraint contains exactly one tuple variable
				if 1==len(tuple_vars):
					#Get the tuple var
					tuple_var=tuple_vars[0]

					#Record the fact that it is equal to 0
					var_const_map[tuple_var].add(0)
			#Does the constraint have two terms?
			elif len(constraint)==2:
				tuple_vars=[(term,coeff) for term,coeff in constraint if term.is_tuple_var()]

				#If the constraint contains exactly one tuple variable
				if 1==len(tuple_vars):
					#Get the tuple vari
					tuple_var,coeff=tuple_vars[0]

					#If the constraint contains exactly one tuple variable
					if 1==abs(coeff):
						#If the other term is a constant
						if ConstantCol() in constraint:
							var_const_map[tuple_var].add(coeff*constraint[ConstantCol()])

		#If any tuple variable is equal to more than one constant,
		# this constraint is empty
		is_empty=any((len(consts)>1 for consts in var_const_map.itervalues()))

		#If we found a tuple variable equal to two different constants
		if is_empty:
			#Define a single constraint to be only 0=1
			self._constraints=[SparseEquality(sparse_exp=SparseExp({ConstantCol():-1}))]

	def bounds(self,var_col,extra_info=False):
		lower_bounds=set()
		upper_bounds=set()

		#Look at each constraint in the conjunction
		for constraint in self:
			constraint=constraint.copy()

			#See if the given variable is present in the constraint
			if var_col in constraint:
				#Get the coefficient of the variable in the constraint
				var_coeff=constraint[var_col]

				#Get the coefficient/expression pair the variable is equal to
				equal_coeff,equal_exp=constraint.get_equality_pair(var_col)

				#Cannot handle cases where the equal_coeff!=1
				if not extra_info and 1!=equal_coeff:
					raise ValueError("Coefficient of variable '%s' is not 1 or -1"%(var_col))

				#Equality constraint: lower and upper bounds
				if constraint.is_equality():
					if extra_info:
						lower_bounds.add((equal_coeff,equal_exp,constraint))
						upper_bounds.add((equal_coeff,equal_exp,constraint))
					else:
						lower_bounds.add(equal_exp)
						upper_bounds.add(equal_exp)
				#Inequality constraint: lower or upper bound
				else:
					#Lower bound
					if var_coeff>0:
						if extra_info:
							lower_bounds.add((equal_coeff,equal_exp,constraint))
						else:
							lower_bounds.add(equal_exp)
					#Upper bound
					else:
						if extra_info:
							upper_bounds.add((equal_coeff,equal_exp,constraint))
						else:
							upper_bounds.add(equal_exp)

		return (lower_bounds,upper_bounds)

	def get_mat(self,pos_map,make_positive,make_negative):
		return tuple([constraint.get_mat(pos_map,make_positive,make_negative) for constraint in self])

	def contains_nest(self,nest):
		return any((constraint.contains_nest(nest) for constraint in self))

	def freeze(self):
		if not self.frozen:
			self._constraints=frozenset(self.constraints)
			self._frozen=True

	def copy(self,freeze=True,**kwargs):
		selfcopy=SparseConjunction()

		for constraint in self:
			selfcopy.add_constraint(constraint.copy(**kwargs))

		if self.frozen and freeze:
			selfcopy.freeze()

		return selfcopy

# End SparseConjunction class
#--------------------------------------------------

#--------------------------------------------------
# Start SparseDisjunction class

class SparseDisjunction(IEGenObject):
	__slots__=('_conjunctions','_frozen')

	def __init__(self,conjunctions=None):
		conjunctions=[] if conjunctions is None else conjunctions

		self._conjunctions=list(conjunctions)
		self._frozen=False

	def __hash__(self):
		self._check_frozen()
		return hash(self.conjunctions)

	def __eq__(self,other):
		try:
			self._check_frozen()
			other._check_frozen()
			return self._conjunctions==other._conjunctions
		except AttributeError as e:
			return False

	def __ne__(self,other):
		return not self==other

	def __len__(self):
		return len(self.conjunctions)

	def __iter__(self):
		return iter(self.conjunctions)

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.conjunctions))

	def _check_frozen(self):
		#Make sure we're frozen
		if not self.frozen:
			raise ValueError('Cannot operate on a non-frozen sparse disjunction')

	def _check_mutate(self):
		#Make sure we're not frozen
		if self.frozen:
			raise ValueError('Cannot modify a frozen sparse disjunction')

	def _get_conjunctions(self):
		return self._conjunctions

	def _get_frozen(self):
		return self._frozen

	conjunctions=property(_get_conjunctions)
	frozen=property(_get_frozen)

	def get_function_names(self):
		return list(set([function_name for conjunction in self for function_name in conjunction.get_function_names()]))

	def add_conjunction(self,conjunction):
		self._check_mutate()
		self._conjunctions.append(conjunction)

	def add_disjunction(self,disjunction):
		self._check_mutate()
		self._conjunctions.extend(disjunction.conjunctions)

	def clear(self):
		self._check_mutate()
		self._conjunctions=[]

	def project_out(self,var_col):
		self._check_mutate()

		iegen.simplify.notify_project_out_listeners()

		projected_out=True
		for conjunction in self:
			projected_out=conjunction.project_out(var_col) and projected_out

		return projected_out

	def simplify(self):
		for conjunction in self:
			conjunction.simplify()

		self.remove_contradictions()

	def remove_contradictions(self):
		self._check_mutate()

		#Remove 'empty' conjunctions: i.e. conjunctions that have
		# a 0=1 constraint and represent an empty set of integer tuples
		self._conjunctions=[conjunction for conjunction in self if not conjunction.is_contradiction()]

		#If all conjunctions were removed, add one back that has the single constraint 0=1
		if 0==len(self):
			conj=SparseConjunction(constraints=[SparseEquality(sparse_exp=SparseExp({ConstantCol():-1}))])
			self._conjunctions=[conj]

	def bounds(self,var_col):
		return tuple([conjunction.bounds(var_col) for conjunction in self])

	def get_mat(self,pos_map,make_positive,make_negative):
		return tuple([conjunction.get_mat(pos_map,make_positive,make_negative) for conjunction in self])

	def contains_nest(self,nest):
		return any((conjunction.contains_nest(nest) for conjunction in self))

	def freeze(self):
		#Only freeze this disjunction if it isn't yet frozen
		if not self.frozen:
			#Freeze each conjunction in the disjunction
			for conjunction in self:
				conjunction.freeze()

			self._conjunctions.sort()
			self._conjunctions=frozenset(self.conjunctions)
			self._frozen=True

	def copy(self,freeze=True,conjunction_pos=None,**kwargs):
		selfcopy=SparseDisjunction()

		if conjunction_pos is None:
			for conjunction in self:
				selfcopy.add_conjunction(conjunction.copy(freeze=freeze,conjunction_pos=conjunction_pos,**kwargs))
		else:
			selfcopy.add_conjunction(list(self.conjunctions)[conjunction_pos].copy(freeze=freeze,conjunction_pos=conjunction_pos,**kwargs))

		if self.frozen and freeze:
			selfcopy.freeze()

		return selfcopy

# End SparseDisjunction class
#--------------------------------------------------
