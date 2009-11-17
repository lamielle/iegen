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
	__slots__=('_tuple_var_cols','_symbolic_cols','_free_var_cols','_columns','_functions','_conjunctions','_frozen')

	#--------------------------------------------------
	# Start SparseFormula constructor
	def __init__(self,tuple_var_names,free_var_names,symbolics,functions,conjunctions):
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

		#Set of SparseConstraints in this formula (equality or inequality)
		self._conjunctions=set(conjunctions)

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

	def _construct(self,pres_formulas=None,tuple_var_names=None,free_var_names=None,symbolics=None,functions=None,conjunctions=None,freeze=True):
		#Get an empty list if no symbolics were given
		symbolics=[] if symbolics is None else sorted(symbolics)

		#Get an empty list if no functions were given
		functions=[] if functions is None else functions

		#Get an empty list if no conjunctions were given
		conjunctions=[] if conjunctions is None else conjunctions

		#Determine how to construct based on the presence of the pres_formulas argument
		if pres_formulas is None:
			#Construct this formula using the SparseFormula constructor and the parsed information
			SparseFormula.__init__(self,tuple_var_names,free_var_names,symbolics,functions,conjunctions)
		else:
			#Get the names of the tuple variables
			tuple_var_names=self._get_tuple_var_names(pres_formulas)

			#Get the names of the free variables
			free_var_names=self._get_free_var_names(pres_formulas,tuple_var_names,symbolics)

			#Construct this formula using the SparseFormula constructor and the parsed information
			SparseFormula.__init__(self,tuple_var_names,free_var_names,symbolics,[],[])

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
		functions=set()
		for function in self.functions:
			functions.add(function.copy(new_var_pos,new_var_names))

		#Copy the constraints of the formula
		conjunctions=set()
		for conjunction in self.conjunctions:
			conjunction_copy=set()
			for constraint in conjunction:
				conjunction_copy.add(constraint.copy(new_var_pos,new_var_names))
			conjunctions.add(frozenset(conjunction_copy))

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
		selfcopy=FormulaClass(tuple_var_names=tuple_var_names,free_var_names=self.free_vars,symbolics=self.symbolics,functions=functions,conjunctions=conjunctions,freeze=freeze)

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
		return hash((self._columns,self._functions,self._conjunctions))

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

	#Get the conjunctions in the formula
	def _get_conjunctions(self):
		return list(self._conjunctions)

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
		try:
			#Try to obtain the input arity (assume we're a sparse relation)
			arity_in=self.arity_in()
		except AttributeError,e:
			#We must be a sparse set
			arity_in=None

		#Create the tuple variable string based on whether we are a sparse set or relation
		if arity_in is None:
			tuple_var_string='['+','.join(self.tuple_vars)+']'
		else:
			tuple_var_string='['+','.join(self.tuple_vars[:arity_in])+']'
			tuple_var_string+='->'
			tuple_var_string+='['+','.join(self.tuple_vars[arity_in:])+']'

		#Create strings for each conjunction
		conjunction_strings=[]
		for conjunction in self.conjunctions:
			#Create strings for the constraints
			constraint_strings=[]
			for constraint in conjunction:
				constraint_strings.append(str(constraint))

			#Create a single string for all of the constraints
			constraints_string=' and '.join(constraint_strings)

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
		if self.arity()==other.arity():
			#Make a copy of self
			selfcopy=self.copy(freeze=False)

			#New variable names mapping
			new_var_names={}
			for pos in xrange(len(selfcopy.tuple_vars)):
				new_var_names[other.tuple_vars[pos]]=selfcopy.tuple_vars[pos]

			#Add a copy of each conjunction of the other formula to the copied self
			for conjunction in other.conjunctions:
				conjunction_copy=set()
				for constraint in conjunction:
					conjunction_copy.add(constraint.copy(new_var_names=new_var_names))
				selfcopy.add_conjunction(conjunction_copy)

			#Freeze the unioned formulas
			selfcopy.freeze()
		else:
			raise ValueError("Cannot union formulas with differing arity: '%s' (arity %s) and '%s' (arity %s)"%(self,self.arity(),other,other.arity()))

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
	conjunctions=property(_get_conjunctions)
	frozen=property(_get_frozen)

	#Freezes this formula
	def freeze(self):
		#Freeze the necessary fields
		self._columns=frozenset(self._columns)
		self._functions=frozenset(self._functions)
		self._conjunctions=frozenset(self._conjunctions)

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

	#Removes all conjunctions from this formula
	def clear(self):
		self._conjunctions=set()

	#Add the given conjunction (collection of constraints) to the formula
	def add_conjunction(self,conjunction):
		#Make sure this sparse formula can be modified
		self._check_mutate()

		#Add the constraint to the constraints collection
		self._conjunctions.add(frozenset(conjunction))

	#Add a function with the given expression coefficients to the formula
	def add_function(self,name,arg_exps):
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
	def __init__(self,set_string=None,symbolics=None,tuple_var_names=None,free_var_names=None,functions=None,conjunctions=None,freeze=True):
		#Determine how to construct this set based on the presence of the set string
		if set_string is None:
			#Construct this set using the given tuple variable names, free variable names, and symbolics
			self._construct(tuple_var_names=tuple_var_names,free_var_names=free_var_names,symbolics=symbolics,functions=functions,conjunctions=conjunctions,freeze=freeze)
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

	#TODO: implement
	def apply(self,other):
		pass

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
	def __init__(self,relation_string=None,symbolics=None,tuple_var_names=None,free_var_names=None,functions=None,conjunctions=None,freeze=True):
		#Determine how to construct this relation based on the presence of the relation string
		if relation_string is None:
			#Construct this relation using the given tuple variable names, free variable names, and symbolics
			self._construct(tuple_var_names=tuple_var_names,free_var_names=free_var_names,symbolics=symbolics,functions=functions,conjunctions=conjunctions,freeze=freeze)
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

	#TODO: implement
	def compose(self,other):
		pass

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
