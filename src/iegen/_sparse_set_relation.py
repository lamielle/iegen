#Classes related to the SparseSet and SparseRelation classes that use the new data structure rather than an AST as a representation

from iegen import IEGenObject
from iegen.util import biject

#Represents a sparse set or relation
class SparseFormula(IEGenObject):
	__slots__=('names','columns','functions','constraints')

	def __init__(self):
		self.names=biject()
		self.columns=biject()
		self.functions=frozenset()
		self.constraints=frozenset()

	#Returns the arity (number of tuple variables) of this forumla
	def _arity(self):
		return len(self.names)

#Represents a sparse set
class SparseSet(SparseFormula):

	#Returns the arity of this set
	def arity(self):
		return self._arity()

#Represents a sparse relation
class SparseRelation(SparseFormula):
	__slots__=('_arity_in',)

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
	pass
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
class SparseConstraint(IEGenObject):
	pass

#Class representing a sparse equality constraint
class SparseEquality(SparseConstraint):
	pass

#Class representing a sparse inequality constraint
class SparseInequality(SparseConstraint):
	pass
