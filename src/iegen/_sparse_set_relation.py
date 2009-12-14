#Classes related to the SparseSet and SparseRelation classes that use the new data structure rather than an AST as a representation

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
	__slots__=('_tuple_var_cols','_symbolic_cols','_free_var_cols','_disjunction','_frozen')

	#--------------------------------------------------
	# Start SparseFormula constructor
	def __init__(self,tuple_var_names,free_var_names,symbolics,disjunction):
		#--------------------
		#Init various fields
		#'var name' <--> TupleVarCol(pos)
		self._tuple_var_cols=biject()

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
	#The constraints are copied if copy_constraints is True
	def _copy(self,new_var_pos,new_var_names,freeze,FormulaClass):
		#Copy the constraints of the formula
		disjunction_copy=self.disjunction.copy(new_var_pos=new_var_pos,new_var_names=new_var_names,freeze=freeze)

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
		selfcopy=FormulaClass(tuple_var_names=tuple_var_names,free_var_names=self.free_vars,symbolics=self.symbolics,disjunction=disjunction_copy,freeze=freeze)

		return selfcopy

	#Parses the given formula string using the given parsing function
	@staticmethod
	def _parse_formula_string(formula_string,symbolics,parse_func):
		iegen.settings.enable_processing=False
		pres_formulas=[parse_func(formula_string,symbolics)]
		iegen.settings.enable_processing=True

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
			self._tuple_var_cols[tuple_var_name]=TupleVarCol(pos,tuple_var_name)

		#Build the symbolic list
		for symbolic in symbolics:
			self._symbolic_cols.append(SymbolicCol(symbolic))

		#Build the free variable list
		for free_var_name in free_var_names:
			self._free_var_cols.append(FreeVarCol(free_var_name))

	# End construction utility methods
	#--------------------------------------------------

	#--------------------------------------------------
	# Hash and equality methods
	def __hash__(self):
		self._check_frozen()
		return hash(self._disjunction)

	def __eq__(self,other):
		return hash(self)==hash(other)

	def __ne__(self,other):
		return not self==other
	#--------------------------------------------------

	#--------------------------------------------------
	# Start property support methods

	#Returns the arity (number of tuple variables) of this forumla
	def _arity(self):
		return len(self._tuple_var_cols)

	#Returns the number of symbolics in this formula
	def _num_symbolics(self):
		return len(self._symbolic_cols)

	#Returns the number of free variables in this formula
	def _num_free_vars(self):
		return len(self._free_var_cols)

	#Get the names of all tuple variables in the formula
	def _get_tuple_vars(self):
		return [self._tuple_var_cols[TupleVarCol(pos)] for pos in xrange(self._arity())]

	#Get the symbolics in this forumula
	def _get_symbolics(self):
		return [symbolic_col.sym for symbolic_col in self._symbolic_cols]

	#Get the names of all symbolics
	def _get_symbolic_names(self):
		return [symbolic_col.sym.name for symbolic_col in self._symbolic_cols]

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
		except AttributeError,e:
			#We must be a sparse set
			tuple_var_string='['+','.join(self.tuple_vars)+']'

		#Create strings for each conjunction
		conjunction_strings=[]
		for conjunction in self.disjunction.conjunctions:
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
	disjunction=property(_get_disjunction)
	frozen=property(_get_frozen)

	#Freezes this formula
	def freeze(self):
		#Project each free variable out of the disjunction
		for free_var in self.free_vars:
			projected_out=self.disjunction.project_out(self.get_column(free_var))

			if projected_out:
				self._free_var_cols.remove(self.get_column(free_var))

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
			column=self._tuple_var_cols[name]

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

	# End public methods/properties
	#--------------------------------------------------

# End SparseFormula class
#--------------------------------------------------

#--------------------------------------------------
# Start SparseSet class

#Represents a sparse set
class SparseSet(SparseFormula):

	#--------------------------------------------------
	# Start SparseSet constructor

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

	# End SparseSet constructor
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

	#Returns a copy of this SparseSet
	def copy(self,new_var_pos=None,new_var_names=None,freeze=True):
		#Make a copy of this SparseSet
		selfcopy=self._copy(new_var_pos=new_var_pos,new_var_names=new_var_names,freeze=freeze,FormulaClass=SparseSet)

		return selfcopy

	#The union operation
	def union(self,other):
		res=self._union(other,SparseSet)
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
		new_set=SparseSet(tuple_var_names=new_tuple_vars,free_var_names=new_free_vars,symbolics=new_symbolics,freeze=False)

		#Create the constraints: cartesian product of both disjunctions + free variable equalities
		new_set._join(self,self.tuple_set,self_var_map,other,other.tuple_in,other_var_map,new_var_pos)

		#Freeze the new resulting set now that we're done modifying it
		new_set.freeze()

		self.print_debug('Apply: %s.apply(%s)=%s'%(self,other,new_set))

		return new_set

	# End public methods
	#--------------------------------------------------

# End SparseSet class
#--------------------------------------------------

#--------------------------------------------------
# Start SparseRelation class

#Represents a sparse relation
class SparseRelation(SparseFormula):
	__slots__=('_arity_in',)

	#--------------------------------------------------
	# Start SparseRelation constructor

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

	# End SparseRelation constructor
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

	#Returns a copy of this SparseRelation
	def copy(self,new_var_pos=None,new_var_names=None,freeze=True):
		#Make a copy of this SparseRelation
		selfcopy=self._copy(new_var_pos=new_var_pos,new_var_names=new_var_names,freeze=freeze,FormulaClass=SparseRelation)

		#Determine the input arity
		selfcopy._arity_in=self.arity_in()

		return selfcopy

	def union(self,other):
		res=self._union(other,SparseRelation)
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
		new_relation=SparseRelation(tuple_var_names=new_tuple_vars,arity_in=other.arity_in(),free_var_names=new_free_vars,symbolics=new_symbolics,freeze=False)

		#Create the constraints: cartesian product of both disjunctions + free variable equalities
		new_relation._join(other,other.tuple_out,other_var_map,self,self.tuple_in,self_var_map,new_var_pos)

		#Freeze the new resulting relation now that we're done modifying it
		new_relation.freeze()

		self.print_debug('Compose: \n\t%s\n\n\t.compose(%s)\n\n\t' %(self,other) )
		self.print_debug('\n\tCompose output: %s\n' %(new_relation))

		return new_relation

		return self

	# End public methods/properties
	#--------------------------------------------------

# End SparseRelation class
#--------------------------------------------------

#--------------------------------------------------
# Start SparseExpColumnType classes

#Parent class of the various sparse expression column type classes
class SparseExpColumnType(IEGenObject):
	def __hash__(self):
		return hash(str(self))

	def __eq__(self,other):
		return hash(self)==hash(other)

	def __ne__(self,other):
		return not self==other

	def __str__(self):
		return repr(self)

class SparseExpNameColumnType(SparseExpColumnType):
	__slots__=('name',)

	def __init__(self,name):
		self.name=name

	def __repr__(self):
		return "%s(%s)"%(self.__class__.__name__,repr(self.name))

	def exp_str(self):
		return self.name

class FreeVarCol(SparseExpNameColumnType):
	def __init__(self,name):
		SparseExpNameColumnType.__init__(self,name)

	def copy(self,new_var_pos=None,new_var_names=None):
		name=self.name

		#Change the name if necessary
		if new_var_names is not None and name in new_var_names:
			name=new_var_names[self.name]

		return FreeVarCol(name)

class ConstantCol(SparseExpNameColumnType):
	def __init__(self):
		SparseExpNameColumnType.__init__(self,'')

	def copy(self,new_var_pos=None,new_var_names=None):
		return ConstantCol()

class TupleVarCol(SparseExpColumnType):
	__slots__=('pos','name')

	def __init__(self,pos,name=None):
		self.pos=pos
		self.name=name

	def __repr__(self):
		return '%s(%s,%s)'%(self.__class__.__name__,repr(self.pos),repr(self.name))

	def __str__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.pos))

	def copy(self,new_var_pos=None,new_var_names=None):
		pos=self.pos
		name=self.name

		#Change the column position if necessary
		if new_var_pos is not None and pos in new_var_pos:
			pos=new_var_pos[pos]

		#Change the name if necessary
		if new_var_names is not None:
			name=new_var_names[name]

		return TupleVarCol(pos,name)

	def exp_str(self):
		return self.name

class SymbolicCol(SparseExpColumnType):
	__slots__=('sym',)

	def __init__(self,sym):
		self.sym=sym

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.sym))

	def __str__(self):
		return '%s(%s)'%(self.__class__.__name__,self.sym.name)

	def copy(self,new_var_pos=None,new_var_names=None):
		return SymbolicCol(self.sym)

	def exp_str(self):
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

	def __repr__(self):
		return '%s(%s,%s)'%(self.__class__.__name__,repr(self.name),repr(self.args))

	def __str__(self):
		arg_strs=[str(arg) for arg in self.args]
		return '%s(%s)'%(self.name,','.join(arg_strs))

	def var_is_function_input(self,var_col):
		for arg in self.args:
			for term in arg.exp:
				#Check if this term is the variable we're looking for
				#'These are not the droids you're looking for...'
				if var_col==term:
					return True
				#Check if this term is a UFCall
				elif hasattr(term,'name') and hasattr(term,'args'):
					if term.var_is_function_input(var_col):
						return True
		return False

	def copy(self,new_var_pos=None,new_var_names=None):
		return UFCall(self.name,[arg.copy(new_var_pos=new_var_pos,new_var_names=new_var_names) for arg in self.args])

	def exp_str(self):
		return str(self)

# End SparseExpColumnType classes
#--------------------------------------------------

#--------------------------------------------------
# Start SparseExp class

#Represents a sparse expression (an affine expression plus uninterpreted function symbols)
class SparseExp(IEGenObject):
	__slots__=('_exp',)

	def __init__(self,exp_coeff):
		self._exp=defaultdict(int,exp_coeff)
		self.simplify()

	def __hash__(self):
		return hash(frozenset(self.exp.items()))

	def __eq__(self,other):
		return hash(self)==hash(other)

	def __ne__(self,other):
		return not self==other

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.exp))

	def __str__(self):
		term_strs=[]

		#If there are no terms, just return '0'
		if 0==len(self.exp):
			return '0'
		else:
			#Look at each term
			for term,coeff in self.exp.items():
				#Handle the constant
				if ConstantCol()==term:
					term_strs.append('%s'%(coeff))
				else:
					#If the coefficient is not 0, add it to the list of expression strings
					if 1==coeff:
						term_strs.append('%s'%(term.exp_str()))
					else:
						term_strs.append('%s*%s'%(coeff,term.exp_str()))

			#Return a string for the sum of all expression strings
			return '+'.join(term_strs)

	def _get_exp(self):
		return self._exp
	exp=property(_get_exp)

	def remove_term(self,var_col):
		if var_col in self.exp:
			del self.exp[var_col]
		else:
			raise ValueError("Column '%s' is not present in this expression (%s)"%(var_col,self))

	def multiply(self,factor):
		for term,coeff in self.exp.items():
			self.exp[term]*=factor

	def add_exp(self,other_exp):
		for term,coeff in other_exp.exp.items():
			self.exp[term]+=coeff

	def get_equality_pair(self,var_col):
		#Grab the coefficient of the variable
		equal_coeff=self.exp[var_col]

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

	def replace_var(self,var_col,equal_coeff,equal_exp):
		#Determine if the given variable is present in this expression
		if var_col in self.exp:
			#Get the coefficient of the variable in this expression
			var_coeff=self.exp[var_col]

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

	def simplify(self):
		#Remove all terms with a coefficient of 0
		for term,coeff in self.exp.items():
			if 0==coeff:
				self.remove_term(term)

	def copy(self,new_var_pos=None,new_var_names=None,new_cols=None):
		new_cols={} if new_cols is None else new_cols
		exp_copy={}

		for term,coeff in self.exp.items():
			if term in new_cols:
				exp_copy[new_cols[term].copy(new_var_pos=new_var_pos,new_var_names=new_var_names)]=coeff
			else:
				exp_copy[term.copy(new_var_pos=new_var_pos,new_var_names=new_var_names)]=coeff

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
			self.sparse_exp=sparse_exp
		else:
			self.sparse_exp=SparseExp(exp_coeff)

	def __hash__(self):
		return hash(self.op+str(hash(self.hash_exp)))

	def __eq__(self,other):
		return hash(self)==hash(other)

	def __ne__(self,other):
		return not self==other

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,self.sparse_exp.exp)

	def __str__(self):
		lhs_exp_strs=[]
		rhs_exp_strs=[]

		#Look at each term
		for term,coeff in self.sparse_exp.exp.items():
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

	def _get_sparse_exp(self):
		return self._sparse_exp
	def _set_sparse_exp(self,sparse_exp):
		self._sparse_exp=sparse_exp
	sparse_exp=property(_get_sparse_exp,_set_sparse_exp)

	def _get_op(self):
		return self._op
	op=property(_get_op)

	def replace_var(self,var_col,equal_coeff,equal_exp):
		self.sparse_exp.replace_var(var_col,equal_coeff,equal_exp)

	def simplify(self):
		self.sparse_exp.simplify()

#Class representing a sparse equality constraint
class SparseEquality(SparseConstraint):
	__slots__=('_comp_sparse_exp',)
	_op='='

	def __init__(self,exp_coeff=None,sparse_exp=None):
		SparseConstraint.__init__(self,exp_coeff=exp_coeff,sparse_exp=sparse_exp)

	def _get_comp_sparse_exp(self):
		return self._comp_sparse_exp
	def _set_comp_sparse_exp(self,comp_sparse_exp):
		self._comp_sparse_exp=comp_sparse_exp
	comp_sparse_exp=property(_get_comp_sparse_exp,_set_comp_sparse_exp)

	def _get_hash_exp(self):
		complement=self.sparse_exp.complement()
		return frozenset([self.sparse_exp,complement])
	hash_exp=property(_get_hash_exp)

	def copy(self,new_var_pos=None,new_var_names=None,new_cols=None):
		return SparseEquality(sparse_exp=self.sparse_exp.copy(new_var_pos=new_var_pos,new_var_names=new_var_names,new_cols=new_cols))

#Class representing a sparse inequality constraint
class SparseInequality(SparseConstraint):
	_op='>='

	def _get_hash_exp(self):
		return self.sparse_exp
	hash_exp=property(_get_hash_exp)

	def copy(self,new_var_pos=None,new_var_names=None,new_cols=None):
		return SparseInequality(sparse_exp=self.sparse_exp.copy(new_var_pos=new_var_pos,new_var_names=new_var_names,new_cols=new_cols))

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
		return hash(self)==hash(other)

	def __ne__(self,other):
		return not self==other

	def __len__(self):
		return len(self.constraints)

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.constraints))

	def __str__(self):
		#Create strings for the constraints
		constraint_strings=[str(constraint) for constraint in self.constraints]

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

	def add_constraint(self,constraint):
		self._check_mutate()

		self._constraints.append(constraint)

	def remove_constraint(self,constraint):
		self._check_mutate()

		if constraint in self._constraints:
			self._constraints.remove(constraint)
		else:
			raise ValueError("Cannot remove constraint '%s': constraint not present in conjunction"%(constraint))

	def add_conjunction(self,conjunction):
		self._check_mutate()

		#Add the given conjunctions constraints to this conjunction
		self._constraints.extend(conjunction.constraints)

		#Make the collection of constraints unique
		self._constraints=list(set(self._constraints))

	def find_equality_with_var(self,var_col):
		equality_constraint=None

		#Search through all constraints
		for constraint in self.constraints:
			#Make sure this constraint is an equality constraint
			if '='==constraint.op:
				if var_col in constraint.sparse_exp.exp:
					equality_constraint=constraint
					break

		return equality_constraint

	#Searches for all constraints with UFSs and determines
	# if any of these have the given variable as an input
	#This includes direct arguments and nested function arguments
	def var_is_function_input(self,var_col):
		for constraint in self.constraints:
			for term in constraint.sparse_exp.exp:
				#Check if this term is a UFCall
				if hasattr(term,'name') and hasattr(term,'args'):
					if term.var_is_function_input(var_col):
						return True
		return False

	def project_out(self,var_col):
		self._check_mutate()

		#Search for an equality constraint with the given variable column
		equality_constraint=self.find_equality_with_var(var_col)

		#If we found an equality constraint AND that variable isn't an input to a UFS
		# THEN replace all uses of the variable with the expression it is equal to
		if equality_constraint is not None and not self.var_is_function_input(var_col):
			#Get the coefficient/expression pair the variable is equal to
			equal_coeff,equal_exp=equality_constraint.sparse_exp.get_equality_pair(var_col)

			#Remove the equality constraint from this conjunction
			self.remove_constraint(equality_constraint)

			#Replace all uses of the variable in the remaining constraints
			for constraint in self.constraints:
				constraint.replace_var(var_col,equal_coeff,equal_exp.copy())

			res=True

		#No equality constraints contained the variable, run standard FM
		else:
			res=False

		return res

	def simplify(self):
		self._check_mutate()

		#Simplify all constraints
		for constraint in self.constraints:
			constraint.simplify()

		#Remove all empty constraints
		self._constraints=[constraint for constraint in self.constraints if len(constraint.sparse_exp.exp)>0]

	def bounds(self,var_col):
		lower_bounds=set()
		upper_bounds=set()

		#Look at each constraint in the conjunction
		for constraint in self.constraints:
			#See if the given variable is present in the constraint
			if var_col in constraint.sparse_exp.exp:
				#Get the coefficient of the variable in the constraint
				var_coeff=constraint.sparse_exp.exp[var_col]

				#Get the coefficient/expression pair the variable is equal to
				equal_coeff,equal_exp=constraint.sparse_exp.get_equality_pair(var_col)

				#Cannot handle cases where the abs(var_coeff) != 1
				if 1!=abs(var_coeff):
					raise ValueError("Coefficient of variable '%s' is not 1 or -1"%(var_col))

				#Equality constraint: lower and upper bounds
				if '='==constraint.op:
					lower_bounds.add(equal_exp)
					upper_bounds.add(equal_exp)
				#Inequality constraint: lower or upper bound
				else:
					#Lower bound
					if var_coeff>0:
						lower_bounds.add(equal_exp)
					#Upper bound
					else:
						upper_bounds.add(equal_exp)

		return (lower_bounds,upper_bounds)

	def freeze(self):
		if not self.frozen:
			self.simplify()

			self._constraints=frozenset(self.constraints)

			self._frozen=True

	def copy(self,new_var_pos=None,new_var_names=None,new_cols=None,freeze=True):
		selfcopy=SparseConjunction()

		for constraint in self.constraints:
			selfcopy.add_constraint(constraint.copy(new_var_pos=new_var_pos,new_var_names=new_var_names,new_cols=new_cols))

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
		return hash(self)==hash(other)

	def __ne__(self,other):
		return not self==other

	def __len__(self):
		return len(self.conjunctions)

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

		projected_out=True
		for conjunction in self.conjunctions:
			projected_out=conjunction.project_out(var_col) and projected_out

		return projected_out

	def bounds(self,var_col):
		return tuple([conjunction.bounds(var_col) for conjunction in self.conjunctions])

	def freeze(self):
		#Only freeze this disjunction if it isn't yet frozen
		if not self.frozen:
			#Freeze each conjunction in the disjunction
			for conjunction in self.conjunctions:
				conjunction.freeze()

			self._conjunctions.sort()
			self._conjunctions=frozenset(self.conjunctions)

			self._frozen=True

	def copy(self,new_var_pos=None,new_var_names=None,new_cols=None,freeze=True):
		selfcopy=SparseDisjunction()

		for conjunction in self.conjunctions:
			selfcopy.add_conjunction(conjunction.copy(new_var_pos=new_var_pos,new_var_names=new_var_names,new_cols=new_cols,freeze=freeze))

		if self.frozen and freeze:
			selfcopy.freeze()

		return selfcopy

# End SparseDisjunction class
#--------------------------------------------------
