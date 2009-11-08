#Classes related to the SparseSet and SparseRelation classes that use the new data structure rather than an AST as a representation

import iegen
from iegen import IEGenObject,Symbolic
from iegen.parser import PresParser
from iegen.ast.visitor import CollectVarsVisitor,SparseTransVisitor
from iegen.util import biject,raise_objs_not_like_types

#Represents a sparse set or relation
class SparseFormula(IEGenObject):
	__slots__=('_tuple_vars','_symbolics','_free_vars','_columns','_functions','_constraints','_pres_formulas','_frozen')

	def __init__(self,formula_string,symbolics,parse_func):
		#Init various fields
		self._tuple_vars=biject()
		self._symbolics=biject()
		self._free_vars=biject()
		self._columns=biject()
		self._functions=set()
		self._constraints=set()
		self._frozen=False

		#Get an empty list if no symbolics were given
		symbolics=[] if symbolics is None else sorted(symbolics)

		#Ensure we are given Symbolic objects
		raise_objs_not_like_types(symbolics,Symbolic,'Set construction failure: symbolics must be a collect of objects that look like a Symbolic')

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

		#Build the names bijections
		self._build_names_bijections(tuple_var_names,symbolics,free_var_names)

		#Setup the column positions
		self._build_columns_bijection()

		#Run the translation visitor
		v=SparseTransVisitor(self)
		for pres_formula in self._pres_formulas:
			v.visit(pres_formula)

		#Freeze this formula
		self.freeze()

#	def __hash__(self):
#		return hash(self.op+str(hash(self.sparse_exp)))
#
#	def __eq__(self,other):
#		return hash(self)==hash(other)
#
#	def __ne__(self,other):
#		return not self==other

	#Returns the arity (number of tuple variables) of this forumla
	def _arity(self):
		return len(self._tuple_vars)

	#Returns the number of symbolics in this formula
	def _num_symbolics(self):
		return len(self._symbolics)

	#Returns the number of free variables in this formula
	def _num_free_vars(self):
		return len(self._free_vars)

	#Get the names of all tuple variables in the formula
	def _get_tuple_vars(self):
		return [self._tuple_vars[pos] for pos in xrange(self._arity())]

	#Get the symbolics in this forumula
	def _get_symbolics(self):
		return [self._symbolics[pos] for pos in xrange(self._arity(),self._arity()+self._num_symbolics())]

	#Get the names of all symbolics
	def _get_symbolic_names(self):
		return [symbolic.name for symbolic in self.symbolics]

	#Get the names of all free variables in the formula
	def _get_free_vars(self):
		return [self._free_vars[pos] for pos in xrange(self._arity()+self._num_symbolics(),self._arity()+self._num_symbolics()+self._num_free_vars())]

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
	def _build_names_bijections(self,tuple_var_names,symbolics,free_var_names):

		#Build the tuple variable bijection
		for pos,tuple_var_name in enumerate(tuple_var_names):
			self._tuple_vars[pos]=tuple_var_name

		#Build the symbolic bijection
		for pos,symbolic in enumerate(symbolics):
			self._symbolics[pos+self._arity()]=symbolic

		#Build the free variable bijection
		for pos,free_var_name in enumerate(free_var_names):
			self._free_vars[pos+self._arity()+self._num_symbolics()]=free_var_name

	#Build the column bijection
	def _build_columns_bijection(self):
		#Add the tuple variables
		for tuple_var_name in self.tuple_vars:
			self._columns[TupleVarCol(tuple_var_name)]=self._tuple_vars[tuple_var_name]

		#Add the symbolics
		for symbolic in self.symbolics:
			self._columns[SymbolicCol(symbolic.name)]=self._symbolics[symbolic]

		#Add the free variables
		for free_var_name in self.free_vars:
			self._columns[FreeVarCol(free_var_name)]=self._free_vars[free_var_name]

		#Add the constant column
		self._columns[ConstantCol()]=len(self._columns)

	def __repr__(self):
		symbolic_strings=','.join(["Symbolic('%s')"%sym.name for sym in self.symbolics])
		class_name=self.__class__.__name__
		return "%s('%s',[%s])"%(class_name,str(self),symbolic_strings)

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
		self._functions=frozenset(self._functions)
		self._constraints=frozenset(self._constraints)

		#Set this sparse formula's state to frozen
		self._frozen=True

	#Returns the current number of columns in this sparse formula's constraints
	def num_columns(self):
		return len(self._columns)

	#Returns the current column position of the given name:
	#The name could be a symbolic, tuple variable, or free variable
	def get_column(self,name):
		if name in self.symbolic_names:
			column=self._columns[SymbolicCol(name)]
		elif name in self.tuple_vars:
			column=self._columns[TupleVarCol(name)]
		elif name in self.free_vars:
			column=self._columns[FreeVarCol(name)]
		else:
			raise ValueError("Unknown name '%s'"%(name))

		return column

	#Returns the current constant column position
	def get_constant_column(self):
		return self._columns[ConstantCol()]

	def _check_mutate(self):
		#Make sure we're not frozen
		if self.frozen:
			raise ValueError('Cannot modify a frozen sparse formula')

	def _check_num_coeff(self,exp_coeff):
		if self.num_columns()!=len(exp_coeff):
			raise ValueError('Number of coefficients given (%d) does not match number of columns in sparse formula (%d).'%(len(exp_coeff),self.num_columns()))

	#Returns a new exp_coeff where there first coefficient is positive
	def _make_first_coeff_positive(self,exp_coeff):
		for coeff_pos in xrange(len(exp_coeff)):
			if exp_coeff[coeff_pos]!=0:
				break

		coeff=exp_coeff[coeff_pos]
		if coeff<0:
			for coeff_pos in xrange(len(exp_coeff)):
				exp_coeff[coeff_pos]*=-1

		return exp_coeff

	#Add an equality with the given expression coefficients to the formula
	def add_equality(self,exp_coeff):
		#Make sure the first non-zero coefficient is positive
		#This avoids ambiguous equality expressions
		exp_coeff=self._make_first_coeff_positive(exp_coeff)

		self._add_constraint(exp_coeff,SparseEquality)

	#Add an inequality with the given expression coefficients to the formula
	def add_inequality(self,exp_coeff):
		self._add_constraint(exp_coeff,SparseInequality)

	def _add_constraint(self,exp_coeff,ConstraintType):
		#Make sure this sparse formula can be modified
		self._check_mutate()

		#Make sure the number of coefficients matches the number of columns
		self._check_num_coeff(exp_coeff)

		#Add the constraint to the constraints collection
		self._constraints.add(ConstraintType(exp_coeff,self._columns))

	#Add a function with the given expression coefficients to the formula
	def add_function(self,name,arg_exps):
		args=[SparseExp(arg_exp,self._columns) for arg_exp in arg_exps]
		self._functions.add(UFCall(name,args))

		print self._functions

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

class SparseExpNameColumnType(SparseExpColumnType):
	__slots__=('_name',)

	def __init__(self,name):
		self._name=name

	def _get_name(self):
		return self._name
	name=property(_get_name)

	def __repr__(self):
		return '%s(%s)'%(self.__class__.__name__,self.name)

	def __str__(self):
		return self.name

class TupleVarCol(SparseExpNameColumnType):
	def __init__(self,name):
		SparseExpNameColumnType.__init__(self,name)

class SymbolicCol(SparseExpNameColumnType):
	def __init__(self,name):
		SparseExpNameColumnType.__init__(self,name)

class FreeVarCol(SparseExpNameColumnType):
	def __init__(self,name):
		SparseExpNameColumnType.__init__(self,name)

class ConstantCol(SparseExpNameColumnType):
	def __init__(self):
		SparseExpNameColumnType.__init__(self,'')

	def __str__(self):
		return repr(self)

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

#Represents a sparse expression (an affine expression plus uninterpreted function symbols)
class SparseExp(IEGenObject):
	__slots__=('_exp','_columns')

	def __init__(self,exp_coeff,columns):
		self._exp=tuple(exp_coeff)
		self._columns=columns

	def __hash__(self):
		return hash(self.exp)

	def __eq__(self,other):
		return hash(self)==hash(other)

	def __ne__(self,other):
		return not self==other

	def __repr__(self):
		return '%s(%s,%s)'%(self.__class__.__name__,repr(self.exp),repr(self.columns))

	def __str__(self):
		exp_strs=[]

		#Look at each coefficient
		for col_pos in xrange(len(self.columns)):
			#Grab the current coefficient
			coeff=self.exp[col_pos]

			#Only work with non-zero coefficients
			if 0!=coeff:
				#Handle the constant column
				if self.columns[ConstantCol()]==col_pos:
					exp_strs.append('%s'%(coeff))
				else:
					#If the coefficient is not 0, add it to the list of expression strings
					if 1==coeff:
						exp_strs.append('%s'%(self.columns[col_pos].name))
					else:
						exp_strs.append('%s*%s'%(coeff,self.columns[col_pos]))

		#Return a string for the sum of all expression strings
		return '+'.join(exp_strs)

	def _get_exp(self):
		return self._exp
	exp=property(_get_exp)

	def _get_columns(self):
		return self._columns
	columns=property(_get_columns)

#Represents a sparse constraint (equality or inequality)
#Create instances of SparseEquality and SparseInequality not SparseConstraint
class SparseConstraint(IEGenObject):
	__slots__=('_sparse_exp',)

	def __init__(self,exp_coeff,columns):
		self._sparse_exp=SparseExp(exp_coeff,columns)

	def __hash__(self):
		return hash(self.op+str(hash(self.sparse_exp)))

	def __eq__(self,other):
		return hash(self)==hash(other)

	def __ne__(self,other):
		return not self==other

	def __repr__(self):
		return '%s(%s,%s)'%(self.__class__.__name__,self.sparse_exp.exp,self.sparse_exp.columns)

	def __str__(self):
		return str(self.sparse_exp)+self.op+'0'

	def _get_sparse_exp(self):
		return self._sparse_exp
	sparse_exp=property(_get_sparse_exp)

	def _get_op(self):
		return self._op
	op=property(_get_op)

#Class representing a sparse equality constraint
class SparseEquality(SparseConstraint):
	_op='='

#Class representing a sparse inequality constraint
class SparseInequality(SparseConstraint):
	_op='>='
