#Classes related to the SparseSet and SparseRelation classes that use the new data structure rather than an AST as a representation

from collections import defaultdict
import iegen
from iegen import IEGenObject,Symbolic
from iegen.parser import PresParser
from iegen.ast.visitor import CollectVarsVisitor,SparseTransVisitor
from iegen.util import biject,raise_objs_not_like_types

#--------------------------------------------------
# Start SparseFormula class

#Represents a sparse set or relation
class SparseFormula(IEGenObject):
	__slots__=('_tuple_var_cols','_symbolic_cols','_free_var_cols','_columns','_functions','_disjunction','_frozen')

	#--------------------------------------------------
	# Start SparseFormula constructor
	def __init__(self,tuple_var_names,free_var_names,symbolics,functions,disjunction):
		#--------------------
		#Init various fields
		#'var name' <--> TupleVarCol(pos)
		self._tuple_var_cols=biject()

		#List of SymbolicCol(Symbolic)
		self._symbolic_cols=[]

		#List of FreeVarCol(name)
		self._free_var_cols=[]

		#Set of SparseExpColumnType (columns) for this formula, including UFCalls
		self._columns=set()

		#Set of UFCalls present in this formula
		self._functions=set(functions)

		#SparseDisjunction containing all conjunctions in this formula (equalities or inequalities)
		self._disjunction=SparseDisjunction() if disjunction is None else disjunction

		#Start off unfrozen
		self._frozen=False
		#--------------------

		#Ensure we are given Symbolic objects
		raise_objs_not_like_types(symbolics,Symbolic,'Formula construction failure: symbolics must be a collection of objects that look like a Symbolic')

		#Build the names collections
		self._build_cols_collections(tuple_var_names,symbolics,free_var_names)

		#Create the columns collection
		self._create_columns_collection()
	#--------------------------------------------------

	#--------------------------------------------------
	# Start construction utility methods

	def _construct(self,pres_formulas=None,tuple_var_names=None,free_var_names=None,symbolics=None,functions=None,disjunction=None,freeze=True):
		#Get an empty list if no symbolics were given
		symbolics=[] if symbolics is None else sorted(symbolics)

		#Get an empty list if no functions were given
		functions=[] if functions is None else functions

		#Determine how to construct based on the presence of the pres_formulas argument
		if pres_formulas is None:
			#Construct this formula using the SparseFormula constructor and the parsed information
			SparseFormula.__init__(self,tuple_var_names,free_var_names,symbolics,functions,disjunction)
		else:
			#Get the names of the tuple variables
			tuple_var_names=self._get_tuple_var_names(pres_formulas)

			#Get the names of the free variables
			free_var_names=self._get_free_var_names(pres_formulas,tuple_var_names,symbolics)

			#Construct this formula using the SparseFormula constructor and the parsed information
			SparseFormula.__init__(self,tuple_var_names,free_var_names,symbolics,[],disjunction)

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
		#Copy the functions of the formula
		functions_copy=set()
		for function in self.functions:
			functions_copy.add(function.copy(new_var_pos,new_var_names))

		#Copy the constraints of the formula
		disjunction_copy=self.disjunction.copy(new_var_pos,new_var_names,freeze=freeze)

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
		selfcopy=FormulaClass(tuple_var_names=tuple_var_names,free_var_names=self.free_vars,symbolics=self.symbolics,functions=functions_copy,disjunction=disjunction_copy,freeze=freeze)

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

	#Create the columns collection
	def _create_columns_collection(self):
		#Add the tuple variables
		for tuple_var_name in self.tuple_vars:
			self._columns.add(self._tuple_var_cols[tuple_var_name])

		#Add the symbolics
		self._columns|=set(self._symbolic_cols)

		#Add the free variables
		self._columns|=set(self._free_var_cols)

		#Add the functions
		self._columns|=set(self._functions)

		#Add the constant column
		self._columns.add(ConstantCol())

	# End construction utility methods
	#--------------------------------------------------

	#--------------------------------------------------
	# Hash and equality methods
	def __hash__(self):
		self._check_frozen()
		return hash((self._columns,self._functions,self._disjunction))

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

	#Get the functions in the formula
	def _get_functions(self):
		return list(self._functions)

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

		#Ensure that a constant column is specificed in the expression
		if self.get_constant_column() not in exp_coeff:
			exp_coeff[self.get_constant_column()]=0

		#Return a new constraint
		return ConstraintType(exp_coeff)

	#End misc utility methods
	#--------------------------------------------------

	#--------------------------------------------------
	# Start operation utility methods

	def _union(self,other):
		#Make sure both formulas are frozen
		self._check_frozen()
		other._check_frozen()

		#Make sure the arity of both formulas matches
		if self.arity()!=other.arity():
			raise ValueError("Cannot union formulas with differing arity: '%s' (arity %s) and '%s' (arity %s)"%(self,self.arity(),other,other.arity()))

		#Make a copy of self
		selfcopy=self.copy(freeze=False)

		#New variable names mapping
		new_var_names={}
		for pos in xrange(len(selfcopy.tuple_vars)):
			new_var_names[other.tuple_vars[pos]]=selfcopy.tuple_vars[pos]

		#Add a copy of the other formula's disjunction to the copied self
		selfcopy.add_disjunction(other.disjunction.copy(new_var_names=new_var_names))

		#Freeze the unioned formulas
		selfcopy.freeze()

		return selfcopy

	# End operation utility methods
	#--------------------------------------------------

	#--------------------------------------------------
	# Start public methods/properties

	#Property creation
	tuple_vars=property(_get_tuple_vars)
	symbolics=property(_get_symbolics)
	symbolic_names=property(_get_symbolic_names)
	free_vars=property(_get_free_vars)
	functions=property(_get_functions)
	disjunction=property(_get_disjunction)
	frozen=property(_get_frozen)

	#Freezes this formula
	def freeze(self):
		#Freeze the necessary fields
		self._columns=frozenset(self._columns)
		self._functions=frozenset(self._functions)
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

	#Add a function with the given expression coefficients to the formula
	def add_function(self,name,arg_exps):
		self._check_mutate()
		args=[SparseExp(arg_exp) for arg_exp in arg_exps]
		ufcall=UFCall(name,args)
		self._functions.add(ufcall)
		self._columns.add(ufcall)

		return ufcall

	#Returns the lower bound of the given tuple variable
	def lower_bound(self,tuple_var_name):
		return self.bounds(tuple_var_name)[0]
	#Returns the upper bound of the given tuple variable
	def upper_bound(self,tuple_var_name):
		return self.bounds(tuple_var_name)[1]

	#TODO: implement
	def bounds(self,tuple_var_name):
		pass

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
	def __init__(self,set_string=None,symbolics=None,tuple_var_names=None,free_var_names=None,functions=None,disjunction=None,freeze=True):
		#Determine how to construct this set based on the presence of the set string
		if set_string is None:
			#Construct this set using the given tuple variable names, free variable names, and symbolics
			self._construct(tuple_var_names=tuple_var_names,free_var_names=free_var_names,symbolics=symbolics,functions=functions,disjunction=disjunction,freeze=freeze)
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
		selfcopy=self._copy(new_var_pos,new_var_names,freeze,SparseSet)

		return selfcopy

	#The union operation
	def union(self,other):
		res=self._union(other)
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

		#Gather the new tuple variables, free variables, and symbolics
		new_tuple_vars=other.tuple_out
		new_free_vars=list(set(other.tuple_in+other.free_vars+self.tuple_set+self.free_vars))
		new_symbolics=list(set(other.symbolics+self.symbolics))

		#Create a new set with no constraints, we will build the constraints
		new_set=SparseSet(tuple_var_names=new_tuple_vars,free_var_names=new_free_vars,symbolics=new_symbolics,freeze=False)

		#Create equality constraints
		old_tuple_vars=self.tuple_vars
		old_in_vars=other.tuple_in
		equality_conjunction=new_set.get_conjunction()

		for pos in xrange(len(old_tuple_vars)):
			exp_coeff=defaultdict(int)
			exp_coeff[new_set.get_column(old_tuple_vars[pos])]+=1
			exp_coeff[new_set.get_column(old_in_vars[pos])]+=-1
			equality_conjunction.add_constraint(new_set.get_equality(exp_coeff))

		#Create new collection of conjunctions (cartesian product of both sets of conjunctions)
		for set_conjunction in self.disjunction.conjunctions:
			for rel_conjunction in other.disjunction.conjunctions:
				#Merge the two conjunctions and add to the resulting set being created
				#TODO: Need to change types of some columns while copying depending on tuple/free variables and how they've changed
				merged_conjunction=new_set.get_conjunction()
				merged_conjunction.add_conjunction(set_conjunction)
				merged_conjunction.add_conjunction(rel_conjunction)
				merged_conjunction.add_conjunction(equality_conjunction)
				new_set.add_conjunction(merged_conjunction)

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
	def __init__(self,relation_string=None,symbolics=None,tuple_var_names=None,free_var_names=None,functions=None,disjunction=None,freeze=True):
		#Determine how to construct this relation based on the presence of the relation string
		if relation_string is None:
			#Construct this relation using the given tuple variable names, free variable names, and symbolics
			self._construct(tuple_var_names=tuple_var_names,free_var_names=free_var_names,symbolics=symbolics,functions=functions,disjunction=disjunction,freeze=freeze)
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
		selfcopy=self._copy(new_var_pos,new_var_names,freeze,SparseRelation)

		#Determine the input arity
		selfcopy._arity_in=self.arity_in()

		return selfcopy

	def union(self,other):
		res=self._union(other)
		self.print_debug('Relation Union: %s.union(%s)=%s'%(self,other,res))
		return res

	def inverse(self):
		#Make sure this relation is frozen
		self._check_frozen()

		#Mapping from int -> int (old pos to new pos)
		new_var_pos={}

		#Move the input tuple vars to the output tuple vars
		for pos in xrange(self.arity_in()):
			new_var_pos[pos]=pos+self.arity_in()

		#Move the output tuple vars to the input tuple vars
		for pos in xrange(self.arity_in(),self.arity_in()+self.arity_out()):
			new_var_pos[pos]=pos-self.arity_in()

		#Create a copy of self and update the tuple columns during the copy
		selfcopy=self.copy(new_var_pos=new_var_pos)

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

		#Gather the new tuple variables, free variables, and symbolics
		new_tuple_vars=other.tuple_in+self.tuple_out
		new_free_vars=list(set(other.tuple_out+other.free_vars+self.tuple_in+self.free_vars))
		new_symbolics=list(set(other.symbolics+self.symbolics))

		#Create a new relation with no constraints, we will build the constraints
		new_relation=SparseRelation(tuple_var_names=new_tuple_vars,free_var_names=new_free_vars,symbolics=new_symbolics,freeze=False)

		#Create equality constraints
		old_out_vars=other.tuple_out
		old_in_vars=self.tuple_in
		equality_conjunction=new_relation.get_conjunction()

		for pos in xrange(len(old_out_vars)):
			exp_coeff=defaultdict(int)
			exp_coeff[new_relation.get_column(old_out_vars[pos])]+=1
			exp_coeff[new_relation.get_column(old_in_vars[pos])]+=-1
			equality_conjunction.add_constraint(new_relation.get_equality(exp_coeff))

		#Create new collection of conjunctions (cartesian product of both sets of conjunctions)
		for rel1_conjunction in other.disjunction.conjunctions:
			for rel2_conjunction in self.disjunction.conjunctions:
				#Merge the two conjunctions and add to the resulting relation being created
				#TODO: Need to change types of some columns while copying depending on tuple/free variables and how they've changed
				merged_conjunction=new_relation.get_conjunction()
				merged_conjunction.add_conjunction(rel1_conjunction)
				merged_conjunction.add_conjunction(rel2_conjunction)
				merged_conjunction.add_conjunction(equality_conjunction)
				new_relation.add_conjunction(merged_conjunction)

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
		return FreeVarCol(self.name)

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
		if new_var_pos is not None:
			pos=new_var_pos[self.pos]

		#Change the name if necessary
		if new_var_names is not None:
			name=new_var_names[self.name]

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
		self.args=tuple(args)

	def __hash__(self):
		return hash((self.name,self.args))

	def __repr__(self):
		return '%s(%s,%s)'%(self.__class__.__name__,repr(self.name),repr(self.args))

	def __str__(self):
		arg_strs=[str(arg) for arg in self.args]
		return '%s(%s)'%(self.name,','.join(arg_strs))

	def copy(self,new_var_pos=None,new_var_names=None):
		return UFCall(self.name,[arg.copy(new_var_pos,new_var_names) for arg in self.args])

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

	def __hash__(self):
		return hash(frozenset(self.exp.items()))

	def __eq__(self,other):
		return hash(self)==hash(other)

	def __ne__(self,other):
		return not self==other

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.exp))

	def __str__(self):
		sub_exp_strs=[]

		#Look at each sub-expression
		for sub_exp in self.exp:
			#Grab the current sub_exp's coefficient
			coeff=self.exp[sub_exp]

			#Only work with non-zero coefficients
			if 0!=coeff:
				#Handle the constant
				if ConstantCol()==sub_exp:
					sub_exp_strs.append('%s'%(coeff))
				else:
					#If the coefficient is not 0, add it to the list of expression strings
					if 1==coeff:
						sub_exp_strs.append('%s'%(sub_exp.exp_str()))
					else:
						sub_exp_strs.append('%s*%s'%(coeff,sub_exp.exp_str()))

		#Return a string for the sum of all expression strings
		return '+'.join(sub_exp_strs)

	def _get_exp(self):
		return self._exp
	exp=property(_get_exp)

	def copy(self,new_var_pos=None,new_var_names=None):
		exp_copy={}

		for sub_exp,coeff in self.exp.items():
			exp_copy[sub_exp.copy(new_var_pos,new_var_names)]=coeff

		return SparseExp(exp_copy)

	#Returns the complement of this sparse expression
	#That is, the same sparse expression with all coefficients negated
	def complement(self):
		comp_exp=defaultdict(int,self.exp)

		for sub_exp,coeff in comp_exp.items():
			comp_exp[sub_exp]=-1*coeff

		return SparseExp(comp_exp)

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
		#TODO: Add a more sophisticated routine that produces more readable constraint strings
		return str(self.sparse_exp)+self.op+'0'

	def _get_sparse_exp(self):
		return self._sparse_exp
	def _set_sparse_exp(self,sparse_exp):
		self._sparse_exp=sparse_exp
	sparse_exp=property(_get_sparse_exp,_set_sparse_exp)

	def _get_op(self):
		return self._op
	op=property(_get_op)

#Class representing a sparse equality constraint
class SparseEquality(SparseConstraint):
	__slots__=('_comp_sparse_exp',)
	_op='='

	def __init__(self,exp_coeff=None,sparse_exp=None):
		SparseConstraint.__init__(self,exp_coeff=exp_coeff,sparse_exp=sparse_exp)
		self.comp_sparse_exp=self.sparse_exp.complement()

	def _get_comp_sparse_exp(self):
		return self._comp_sparse_exp
	def _set_comp_sparse_exp(self,comp_sparse_exp):
		self._comp_sparse_exp=comp_sparse_exp
	comp_sparse_exp=property(_get_comp_sparse_exp,_set_comp_sparse_exp)

	def _get_hash_exp(self):
		return frozenset([self.sparse_exp,self.comp_sparse_exp])
	hash_exp=property(_get_hash_exp)

	def copy(self,new_var_pos=None,new_var_names=None):
		return SparseEquality(sparse_exp=self.sparse_exp.copy(new_var_pos,new_var_names))

#Class representing a sparse inequality constraint
class SparseInequality(SparseConstraint):
	_op='>='

	def _get_hash_exp(self):
		return self.sparse_exp
	hash_exp=property(_get_hash_exp)

	def copy(self,new_var_pos=None,new_var_names=None):
		return SparseInequality(sparse_exp=self.sparse_exp.copy(new_var_pos,new_var_names))

# End SparseConstraint classes
#--------------------------------------------------

#--------------------------------------------------
# Start SparseConjunction class

class SparseConjunction(IEGenObject):
	__slots__=('_constraints','_frozen')

	def __init__(self,constraints=None):
		constraints=[] if constraints is None else constraints

		self._constraints=set(constraints)
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

		self._constraints.add(constraint)

	def add_conjunction(self,conjunction):
		self._check_mutate()

		conjunction.freeze()

		self._constraints|=conjunction.constraints

	def freeze(self):
		self._constraints=frozenset(self.constraints)

		self._frozen=True

	def copy(self,new_var_pos=None,new_var_names=None):
		selfcopy=SparseConjunction()

		for constraint in self.constraints:
			selfcopy.add_constraint(constraint.copy(new_var_pos,new_var_names))

		if self.frozen:
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

		self._conjunctions=set(conjunctions)
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

		conjunction.freeze()

		self._conjunctions.add(conjunction)

	def add_disjunction(self,disjunction):
		self._check_mutate()

		disjunction.freeze()

		self._conjunctions|=disjunction.conjunctions

	def clear(self):
		self._check_mutate()

		self._conjunctions=set()

	def freeze(self):
		self._conjunctions=frozenset(self.conjunctions)

		self._frozen=True

	def copy(self,new_var_pos=None,new_var_names=None,freeze=True):
		selfcopy=SparseDisjunction()

		for conjunction in self.conjunctions:
			selfcopy.add_conjunction(conjunction.copy(new_var_pos,new_var_names))

		if self.frozen and freeze:
			selfcopy.freeze()

		return selfcopy

# End SparseDisjunction class
#--------------------------------------------------
