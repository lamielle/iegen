#Classes related to the SparseSet and SparseRelation classes that use the new data structure rather than an AST as a representation

from iegen import IEGenObject,Symbolic
from iegen.parser import PresParser
from iegen.ast.visitor import CollectVarsVisitor,SparseTransVisitor
from iegen.util import biject,raise_objs_not_like_types

#Represents a sparse set or relation
class SparseFormula(IEGenObject):
	__slots__=('_tuple_vars','_symbolics','_free_vars','_columns','_functions','_constraints','_pres_formulas')

	def __init__(self,formula_string,symbolics,parse_func):
		#Init various fields
		self._tuple_vars=biject()
		self._symbolics=biject()
		self._free_vars=biject()
		self._columns=biject()
		self._functions=set()
		self._constraints=set()

		#Get an empty list if no symbolics were given
		symbolics=[] if symbolics is None else sorted(symbolics)

		#Ensure we are given Symbolic objects
		raise_objs_not_like_types(symbolics,Symbolic,'Set construction failure: symbolics must be a collect of objects that look like a Symbolic')

		#Get the names of all symbolic variables
		symbolic_names=[symbolic.name for symbolic in symbolics]

		#Parse the formula string
		self._pres_formulas=[parse_func(formula_string,symbolics)]

		#Get the names of the tuple variables
		tuple_var_names=self._get_tuple_var_names()

		#Get the names of the free variables
		free_var_names=self._get_free_var_names(tuple_var_names,symbolic_names)

		#Build the names bijections
		self._build_names_bijections(tuple_var_names,symbolics,free_var_names)

		#Run the translation visitor
		v=SparseTransVisitor(self)
		for pres_formula in self._pres_formulas:
			v.visit(pres_formula)

		#Freeze this formula
		#self.freeze()

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

	#Property creation
	tuple_vars=property(_get_tuple_vars)
	symbolics=property(_get_symbolics)
	symbolic_names=property(_get_symbolic_names)
	free_vars=property(_get_free_vars)

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

	#Build the pos<-->name bijections for the tuple variables, symbolics, and free variables
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
		constraints_string='and'.join(constraints_strings)

		#Add a ': ' if we have any constraints
		if len(self._constraints)>0:
			constraints_string=': '+constraints_string

		return '{%s%s}'%(tuple_var_string,constraints_string)

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
	pass

class TupleVarCol(SparseExpColumnType):
	__slots__=('_pos',)

	def __init__(self,pos):
		self._pos=pos

	def _get_pos(self):
		return self._pos
	pos=property(_get_pos)

class SymbolicCol(SparseExpColumnType):
	pass
class FreeVarCol(SparseExpColumnType):
	pass
class ConstantCol(SparseExpColumnType):
	pass

#Represents an instance of an uninterpreted function call
class UFCall(SparseExpColumnType):
	pass

#Represents a sparse expression (an affine expression plus uninterpreted function symbols)
class SparseExp(IEGenObject):
	pass

#Represents a sparse constraint (equality or inequality)
#Create instances of SparseEquality and SparseInequality not SparseConstraint
class SparseConstraint(IEGenObject):
	__slots__=('_sparse_exp',)

	def __init__(self,exp):
		self._sparse_exp=exp

	def __str__(self):
		return str(self.exp)+self.op+'0'

	def _get_exp(self):
		return self._sparse_exp
	exp=property(_get_exp)

#Class representing a sparse equality constraint
class SparseEquality(SparseConstraint):
	__slots__=('_op',)

	def __init__(self,exp):
		SparseConstraint.__init__(self,exp)
		self._op='='

	def _get_op(self):
		return self._op
	op=property(_get_op)

#Class representing a sparse inequality constraint
class SparseInequality(SparseConstraint):
	__slots__=('_op',)

	def __init__(self,exp):
		SparseConstraint.__init__(self,exp)
		self._op='>='

	def _get_op(self):
		return self._op
	op=property(_get_op)
