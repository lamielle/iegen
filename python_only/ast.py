# ast.py
#
# Abstract syntax tree representaton for presburger sets and relations
# with uninterpreted function symbols.
#
# Grammar for AST
#
#    IPresSet -> VarTuple Conjunction    // PresSet
#             -> PresSet*                // PresSetUnion
#    
#    VarTuple -> ID*
#    Conjunction -> IConstraint*
#    
#    IConstraint -> IExp:lhs IExp:rhs // Inequality (LTE assummed)
#                -> IExp:lhs IExp:rhs // Equality
#    
#    IExp  -> INT                // IntExp
#          -> IExp:operand       // UMinusExp
#          -> IExp:lhs Expr:rhs  // MulExp, PlusExp, MinusExp
#          -> INT IExp           // IntMulExp
#          -> ID                 // IdExp
#          -> ID:func IExp*      // FuncExp
#
# Naming Convention
#	A class prefixed with "I" is an interface class.
#
# Michelle Strout 7/22/08
#

# base Node class
# Not an interface, because might have a generic child list in the Node class
# later.
class Node:
	pass

##### Presburger Sets

# Presburger set interface
class IPresSet(Node):
	pass

# A single presburger set.
class PresSet(IPresSet):
	__slots__=('_tuple','_conjunct')
	
	def __init__(self, tuple, conjunct):
		self._tuple = tuple
		self._conjunct = conjunct

# A list of presburger sets involved in a union.
class PresSetUnion(IPresSet):
	__slots__=('_presSetList')
	
	def __init__(self, presSetList):
		self._presSetList = presSetList


	
# Tuple of variables.
class VarTuple(Node):
	__slots__=('_idList')
	
	def __init__(self, idList):
		self._idList = idList
		
# A set of constraints that are all part of a conjunction (IOW ANDed together).		
class Conjunction(Node):
	__slots__=('_constraintList')
	
	def __init__(self, constraintList):
		self._constraintList = constraintList

	def __init__(self, conj1, conj2):
		self._constraintList = conj1._constraintList.append(conj2._constraintList)


# Interface for constraints.
class IConstraint(Node):
	pass
	
# It is assummed that all constraints are converted to LTE
# inequalities.
class Inequality(IConstraint):
	__slots__=('_lhs','_rhs')
	
	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

class Equality(IConstraint):
	__slots__=('_lhs','_rhs')
	
	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

##### Expressions
class IExp(Node):
	pass

class IntExp(IExp):
	__slots__=('_val')
	
	def __init__(self, val):
		self._val = val
		
class IdExp(IExp):
	__slots__=('_id')
	
	def __init__(self, id):
		self._id = id

class UMinusExp(IExp):
	__slots__=('_exp')
	
	def __init__(self, exp):
		self._exp = exp

class MulExp(IExp):
	__slots__=('_lhs','_rhs')
	
	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

class PlusExp(IExp):
	__slots__=('_lhs','_rhs')
	
	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

class MinusExp(IExp):
	__slots__=('_lhs','_rhs')
	
	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

class IntMulExp(IExp):
	__slots__=('_int','_exp')
	
	def __init__(self, int, exp):
		self._int = int
		self._exp = exp

class FuncExp(IExp):
	__slots__=('_func','_expList')
	
	def __init__(self, func, expList):
		self._func = func
		self._expList = expList


	