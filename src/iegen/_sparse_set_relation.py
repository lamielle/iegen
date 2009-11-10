#Classes related to the SparseSet and SparseRelation classes that use the new data structure rather than an AST as a representation

from collections import defaultdict
import iegen
from iegen import IEGenObject,Symbolic
from iegen.parser import PresParser
from iegen.ast.visitor import CollectVarsVisitor,SparseTransVisitor
from iegen.util import biject,raise_objs_not_like_types

#Represents a sparse set or relation
class SparseFormula(IEGenObject):
	__slots__=('_tuple_var_cols','_symbolic_cols','_free_var_cols','_columns','_functions','_constraints','_pres_formulas','_frozen')

	def __init__(self,formula_string,symbolics,parse_func):
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
		self._functions=set()

		#Set of SparseConstraints in this formula (equality or inequality)
		self._constraints=set()

		self._frozen=False

		#Get an empty list if no symbolics were given
		symbolics=[] if symbolics is None else sorted(symbolics)

		#Ensure we are given Symbolic objects
		raise_objs_not_like_types(symbolics,Symbolic,'Set construction failure: symbolics must be a collection of objects that look like a Symbolic')

		#Get the names of all symbolic variables
		symbolic_names=[symbolic.name for symbolic in symbolics]

		#Parse the formula string
		iegen.settings.enable_processing=False
		self._pres_formulas=[parse_func(formula_string,symbolics)]
		iegen.settings.enable_processing=True

		#Get the names of the tuple variables
		tuple_var_names=self._get_tuple_var_names()

		#Get the names of the free variables
		free_var_names=self._get_free_var_names(tuple_var_names,symbolic_names)

		#Build the names collections
		self._build_names_collections(tuple_var_names,symbolics,free_var_names)

		#Create the columns collection
		self._create_columns_collection()

		#Run the translation visitor
		v=SparseTransVisitor(self)
		for pres_formula in self._pres_formulas:
			v.visit(pres_formula)

		#Freeze this formula
		self.freeze()

	def __hash__(self):
		return hash(self._constraints)

	def __eq__(self,other):
		return hash(self)==hash(other)

	def __ne__(self,other):
		return not self==other

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

	#Get the frozen state
	def _get_frozen(self):
		return self._frozen

	#Property creation
	tuple_vars=property(_get_tuple_vars)
	symbolics=property(_get_symbolics)
	symbolic_names=property(_get_symbolic_names)
	free_vars=property(_get_free_vars)
	frozen=property(_get_frozen)

	#Returns the names of the tuple variables in _pres_formulas
	def _get_tuple_var_names(self):
		#Get the names of all tuple variables, in order
		tuple_var_names=self._pres_formulas[0]._get_tuple_vars()

		#Ensure that all variable tuples are the same
		for pres_formula in self._pres_formulas[1:]:
			if pres_formula._get_tuple_vars()!=tuple_var_names:
				raise ValueError('Variable tuples do not match across conjunctions')

		return tuple_var_names

	#Determine the names of all free variables in _pres_formulas
	#We exclude the names of the given tuple variables and symbolics
	def _get_free_var_names(self,tuple_var_names,symbolic_names):
		#Start with the names of all variables
		free_var_names=CollectVarsVisitor(all_vars=True)
		for pres_form in self._pres_formulas:
			free_var_names.visit(pres_form)
		free_var_names=set(free_var_names.vars)

		#Remove the names of the tuple variables
		free_var_names-=set(tuple_var_names)

		#Remove the names of the symbolics
		free_var_names-=set(symbolic_names)

		#We now have the final list of free variables
		return sorted(free_var_names)

	#Build the pos <--> name bijections for the tuple variables, symbolics, and free variables
	def _build_names_collections(self,tuple_var_names,symbolics,free_var_names):

		#Build the tuple variable bijection
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

		#Add the constant column
		self._columns.add(ConstantCol())

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

		#Create strings for the constraints
		constraints_strings=[]
		for constraint in self._constraints:
			constraints_strings.append(str(constraint))

		#Create a single string for all of the constraints
		constraints_string=' and '.join(constraints_strings)

		#Add a ': ' if we have any constraints
		if len(self._constraints)>0:
			constraints_string=': '+constraints_string

		symbolics_string=','.join(self.symbolic_names)

		if len(symbolics_string)>0:
			res='{%s%s | %s}'%(tuple_var_string,constraints_string,symbolics_string)
		else:
			res='{%s%s}'%(tuple_var_string,constraints_string)

		return res

	#Freezes this formula
	def freeze(self):
		#Freeze the necessary fields
		self._constraints=frozenset(self._constraints)

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

	def _check_mutate(self):
		#Make sure we're not frozen
		if self.frozen:
			raise ValueError('Cannot modify a frozen sparse formula')

	#Add an equality with the given expression coefficients to the formula
	def add_equality(self,exp_coeff):
		self._add_constraint(exp_coeff,SparseEquality)

	#Add an inequality with the given expression coefficients to the formula
	def add_inequality(self,exp_coeff):
		self._add_constraint(exp_coeff,SparseInequality)

	def _add_constraint(self,exp_coeff,ConstraintType):
		#Make sure this sparse formula can be modified
		self._check_mutate()

		#Add the constraint to the constraints collection
		self._constraints.add(ConstraintType(exp_coeff))

	#Add a function with the given expression coefficients to the formula
	def add_function(self,name,arg_exps):
		args=[SparseExp(arg_exp) for arg_exp in arg_exps]
		ufcall=UFCall(name,args)
		self._functions.add(ufcall)
		self._columns.add(ufcall)

		return ufcall

#Represents a sparse set
class SparseSet(SparseFormula):

	#Constructor for SparseSet:
	#Takes a set string, ex {[a]: a>10}
	#Also, an optional parameter, 'symbolics', is a collection
	#of instances of the iegen.Symbolic class.
	def __init__(self,set_string,symbolics=None):
		SparseFormula.__init__(self,set_string,symbolics,PresParser.parse_set)

	#Returns the set tuple variables
	def _tuple_set(self):
		return self.tuple_vars
	tuple_set=property(_tuple_set)

	#Returns the arity of this set
	def arity(self):
		return self._arity()

#Represents a sparse relation
class SparseRelation(SparseFormula):
	__slots__=('_arity_in',)

	#Constructor for Relation:
	#Takes a relation string, ex {[a]->[a']: a>10}
	#Also, an optional parameter, 'symbolics', is a collection
	#of instances of the iegen.Symbolic class.
	def __init__(self,relation_string,symbolics=None):
		SparseFormula.__init__(self,relation_string,symbolics,PresParser.parse_relation)

		#Determine the input arity
		self._arity_in=len(self._pres_formulas[0].tuple_in.vars)

	#Returns the input tuple variables
	def _tuple_in(self):
		return self.tuple_vars[:self.arity_in()]
	tuple_in=property(_tuple_in)

	#Returns the output tuple variables
	def _tuple_out(self):
		return self.tuple_vars[self.arity_in():]
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

class ConstantCol(SparseExpNameColumnType):
	def __init__(self):
		SparseExpNameColumnType.__init__(self,'')

class TupleVarCol(SparseExpColumnType):
	__slots__=('pos','name')

	def __init__(self,pos,name=None):
		self.pos=pos
		self.name=name

	def __repr__(self):
		return '%s(%s,%s)'%(self.__class__.__name__,repr(self.pos),repr(self.name))

	def __str__(self):
		return '%s(%s)'%(self.__class__.__name__,repr(self.pos))

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

	def exp_str(self):
		return str(self)

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

	#Returns the complement of this sparse expression
	#That is, the same sparse expression with all coefficients negated
	def complement(self):
		comp_exp=defaultdict(int,self.exp)

		for sub_exp,coeff in comp_exp.items():
			comp_exp[sub_exp]=-1*coeff

		return SparseExp(comp_exp)

#Represents a sparse constraint (equality or inequality)
#Create instances of SparseEquality and SparseInequality not SparseConstraint
class SparseConstraint(IEGenObject):
	__slots__=('_sparse_exp',)

	def __init__(self,exp_coeff):
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

	def __init__(self,exp_coeff):
		SparseConstraint.__init__(self,exp_coeff)
		self.comp_sparse_exp=self.sparse_exp.complement()

	def _get_comp_sparse_exp(self):
		return self._comp_sparse_exp
	def _set_comp_sparse_exp(self,comp_sparse_exp):
		self._comp_sparse_exp=comp_sparse_exp
	comp_sparse_exp=property(_get_comp_sparse_exp,_set_comp_sparse_exp)

	def _get_hash_exp(self):
		return frozenset([self.sparse_exp,self.comp_sparse_exp])
	hash_exp=property(_get_hash_exp)

#Class representing a sparse inequality constraint
class SparseInequality(SparseConstraint):
	_op='>='

	def _get_hash_exp(self):
		return self.sparse_exp
	hash_exp=property(_get_hash_exp)
