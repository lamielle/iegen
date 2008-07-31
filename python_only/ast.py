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
class Node(object):
	def apply(self,visitor):
		raise NotImplementedError('All node types should override the apply method.')

#---------- Presburger Sets ----------
# Presburger set interface
class IPresSet(Node):
	pass

# A single presburger set.
class PresSet(IPresSet):
	__slots__=('_setTuple','_conjunct')

	def __init__(self, setTuple, conjunct):
		self._setTuple = setTuple
		self._conjunct = conjunct

	def __repr__(self):
		return 'PresSet("%s,%s")'%(self._setTuple,self._conjunct)

	def apply(self,visitor):
		v.visitPresSet(self)

	def union(self, other):
		if (isinstance(other,PresSet)):
			return PresSetUnion([self,other])
		elif (isinstance(other,PresSetUnion)):
			return other.union(self)
		else:
			assert(0)

# A list of presburger sets involved in a union.
class PresSetUnion(IPresSet):
	__slots__=('_sets')

	def __init__(self, sets):
		self._sets = sets

	def __repr__(self):
		return "PresSetUnion(%s)"%(self._sets)

	def apply(self,visitor):
		v.visitPresSetUnion(self)

	def union(self, other):
		if (isinstance(other,PresSet)):
			self._sets.append(other)
			return self
		elif (isinstance(other,PresSetUnion)):
			self._sets.extend(other._sets)
			return self
		else:
			assert(0)
#-------------------------------------

#---------- Presburger Relations ----------
# Presburger relation interface
class IPresRelation(Node):
	pass

# A single presburger relation
class PresRelation(IPresRelation):
	__slots__=('_inTuple','_outTuple','_conjunct')

	def __init__(self, inTuple, outTuple, conjunct):
		self._inTuple = tuple
		self._outTuple = tuple
		self._conjunct = conjunct

	def __repr__(self):
		return 'PresRelation("%s,%s,%s")'%(self._inTuple,self._outTuple,self._conjunct)

	def apply(self,visitor):
		v.visitPresRelation(self)

	def union(self, other):
		if (isinstance(other,PresRelation)):
			return PresRelationUnion([self,other])
		elif (isinstance(other,PresRelationUnion)):
			return other.union(self)
		else:
			assert(0)

# A list of presburger relations involved in a union.
class PresRelationUnion(IPresRelation):
	__slots__=('_relations')

	def __init__(self, relations):
		self._relations = relations

	def __repr__(self):
		return "PresRelationUnion(%s)"%(self._relations)

	def apply(self,visitor):
		v.visitPresRelationUnion(self)

	def union(self, other):
		if (isinstance(other,PresRelation)):
			self._relations.append(other)
			return self
		elif (isinstance(other,PresRelationUnion)):
			self._relations.extend(other._relations)
			return self
		else:
			assert(0)
#------------------------------------------

#---------- Variable Nodes ----------
# Tuple of variables.
class VarTuple(Node):
	__slots__=('_idList')

	def __init__(self, idList):
		self._idList = idList

	def __repr__(self):
		return 'VarTuple("%s")'%(self._idList)

	def apply(self,visitor):
		v.visitVarTuple(self)
#------------------------------------

#---------- Conjunction Nodes ----------
# A set of constraints that are all part of a conjunction (IOW ANDed together).
class Conjunction(Node):
	__slots__=('_constraintList')

	def __init__(self, constraintList):
		self._constraintList = constraintList

	def __repr__(self):
		return 'Conjunction("%s")'%(self._constraintList)

	def apply(self,visitor):
		v.visitConjunction(self)
#---------------------------------------

#---------- Constraint Nodes ----------
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

	def __repr__(self):
		return 'Inequality("%s,%s")'%(self._lhs,self._rhs)

	def apply(self,visitor):
		v.visitInequality(self)

class Equality(IConstraint):
	__slots__=('_lhs','_rhs')

	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

	def __repr__(self):
		return 'Equality("%s,%s")'%(self._lhs,self._rhs)

	def apply(self,visitor):
		v.visitEquality(self)
#--------------------------------------

#---------- Expression Nodes ----------
class IExp(Node):
	pass

# Integer expressions
class IntExp(IExp):
	__slots__=('_val')

	def __init__(self, val):
		self._val = val

	def __repr__(self):
		return 'IntExp("%s")'%(self._val)

	def __eq__(self, other):
		# An IntExp is not equal to any other object instance type.
		if (isinstance(other,IntExp)==False):
			return False
		# Check equality when other is a IntExp.
		if (self._val==other._val): return True
		else: return False

	def apply(self,visitor):
		v.visitIntExp(self)

# Identifier expressions
class IdExp(IExp):
	__slots__=('_id')

	def __init__(self, id):
		self._id = id

	def __repr__(self):
		return 'IdExp("%s")'%(self._id)

	def __eq__(self, other):
		# An IdExp is not equal to any other object instance type.
		if (isinstance(other,IdExp)==False):
			return False
		# Check equality when other is a IdExp.
		if (self._id==other._id): return True
		else: return False

	def apply(self,visitor):
		v.visitIdExp(self)


# Unary Minus
class UMinusExp(IExp):
	__slots__=('_exp')

	def __init__(self, exp):
		self._exp = exp

	def __repr__(self):
		return 'UMinusExp("%s")'%(self._exp)

	def __eq__(self, other):
		# A UMinusExp is not equal to any other object instance type.
		if (isinstance(other,UMinusExp)==False):
			return False
		# Check equality when other is a UMinusExp.
		# Multiplication is associative.
		if (self._exp==other._exp): return True
		else: return False

	def apply(self,visitor):
		v.visitUMinusExp(self)


# Binary multiplication
class MulExp(IExp):
	__slots__=('_lhs','_rhs')

	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs
		# FIXME: should canonicalize to an IntMulExp if
		# the lhs or rhs is an IntExp

	def __repr__(self):
		return 'MulExp("%s,%s")'%(self._lhs,self._rhs)

	def __eq__(self, other):
		# A MulExp is not equal to any other object instance type.
		if (isinstance(other,MulExp)==False):
			return False
		# Check equality when other is a MulExp.
		# Multiplication is associative.
		if (self._lhs==other._lhs and self._rhs==other._rhs): return True
		elif (self._lhs==other._rhs and self._rhs==other._lhs): return True
		else: return False

	def apply(self,visitor):
		v.visitMulExp(self)


# Binary Addition
class PlusExp(IExp):
	__slots__=('_lhs','_rhs')

	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

	def __repr__(self):
		return 'PlusExp("%s,%s")'%(self._lhs,self._rhs)

	def __eq__(self, other):
		# A PlusExp is not equal to any other object instance type.
		if (isinstance(other,PlusExp)==False):
			return False
		# Check equality when other is a PlusExp.
		# Addition is associative.
		if (self._lhs==other._lhs and self._rhs==other._rhs): return True
		elif (self._lhs==other._rhs and self._rhs==other._lhs): return True
		else: return False

	def apply(self,visitor):
		v.visitPlusExp(self)


# Binary Subtraction
class MinusExp(IExp):
	__slots__=('_lhs','_rhs')

	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

	def __repr__(self):
		return 'MinusExp("%s,%s")'%(self._lhs,self._rhs)

	def __eq__(self, other):
		# A MinusExp is not equal to any other object instance type.
		if (isinstance(other,MinusExp)==False):
			return False
		# check equality when other is a MinusExp
		if (self._lhs==other._lhs and self._rhs==other._rhs): return True
		else: return False

	def apply(self,visitor):
		v.visitMinusExp(self)


# Multiplication by a constant integer
class IntMulExp(IExp):
	__slots__=('_int','_exp')

	def __init__(self, int, exp):
		self._int = int
		self._exp = exp

	def __repr__(self):
		return 'IntMulExp("%s,%s")'%(self._int,self._exp)

	def __eq__(self, other):
		# A IntMulExp is not equal to any other object instance type
		# We are assuming that a MulExp will be canonicalized to an
		# IntMulExp upon construction if appropriate.
		if (isinstance(other,IntMulExp)==False):
			return False
		# check equality when other is a IntMulExp
		if (self._int==other._int and self._exp==other._exp): return True
		else: return False

	def apply(self,visitor):
		v.visitIntMulExp(self)


# Uninterpreted function calls
class FuncExp(IExp):
	__slots__=('_func','_expList')

	def __init__(self, func, expList):
		self._func = func
		self._expList = expList

	def __repr__(self):
		return 'FuncExp("%s,%s")'%(self._func,self._expList)

	# Compare this uninterpreted function expression with another
	# uninterpreted function expression.  If the same function is
	# being called on equivalent parameters, then we know this expression
	# is equal, otherwise, we don't know whether it is equal or not.
	def __eq__(self, other):
		# A FuncExp is not equal to any other object instance type
		if (isinstance(other,FuncExp)==False):
			return False
		# check equality when other is a FuncExp
		if (self._func==other._func and self._expList==other._expList):
			return True
		else:
			return False

	def apply(self,visitor):
		v.visitFuncExp(self)
#---------------------------------------
