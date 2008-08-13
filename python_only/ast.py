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
	def apply_visitor(self,visitor):
		raise NotImplementedError('All node types should override the apply_visitor method.')

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
		return 'PresSet(%s,%s)'%(self._setTuple,self._conjunct)

	def arity(self):
		return len(self._setTuple)

	def apply_visitor(self,visitor):
		v.visitPresSet(self)

	def union(self, other):
		if isinstance(other,PresSet):
			return PresSetUnion([self,other])
		elif isinstance(other,PresSetUnion):
			return other.union(self)
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))

# A list of presburger sets involved in a union.
class PresSetUnion(IPresSet):
	__slots__=('_sets')

	def __init__(self, sets):
		self._sets = sets
		self._arity_check()

	def __repr__(self):
		return "PresSetUnion(%s)"%(self._sets)

	def _arity_check(self):
		if len(self._sets)>0:
			set_arity=self._sets[0].arity()
		for set in self._sets[1:]:
			if set.arity()!=set_arity:
				raise ValueError('All sets in a PresSetUnion must have the same arity.')

	def _add_set(self,set):
		if not isinstance(set,PresSet):
			raise ValueError("Cannot add object of type '%s' to PresSetUnion."%type(set))
		self._sets.append(set)

	def _add_union(self,union):
		if not isinstance(set,PresSetUnion):
			raise ValueError("Cannot add sets from object of type '%s' to PresSetUnion."%type(set))
		self._sets.extend(union._sets)

	def arity(self):
		if len(self._sets)>0:
			return self._sets[0].arity()
		else:
			raise ValueError('Cannot determine arity of a PresSetUnion that contains no sets.')

	def apply_visitor(self,visitor):
		v.visitPresSetUnion(self)

	def union(self, other):
		if isinstance(other,PresSet):
			self._add_set(other)
			return self
		elif isinstance(other,PresSetUnion):
			self._add_union(other)
			return self
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))
#-------------------------------------

#---------- Presburger Relations ----------
# Presburger relation interface
class IPresRelation(Node):
	pass

# A single presburger relation
class PresRelation(IPresRelation):
	__slots__=('_inTuple','_outTuple','_conjunct')

	def __init__(self, inTuple, outTuple, conjunct):
		self._inTuple = inTuple
		self._outTuple = outTuple
		self._conjunct = conjunct

	def __repr__(self):
		return 'PresRelation(%s,%s,%s)'%(self._inTuple,self._outTuple,self._conjunct)

	def arity_in(self):
		return len(self._inTuple)
	def arity_out(self):
		return len(self._outTuple)

	def apply_visitor(self,visitor):
		v.visitPresRelation(self)

	def union(self, other):
		if isinstance(other,PresRelation):
			result=PresRelationUnion([self])
			result.union(other)
			return result
		elif isinstance(other,PresRelationUnion):
			return other.union(self)
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))

	def inverse(self):
		outTemp=self._outTuple
		self._outTuple=self._inTuple
		self._inTuple=outTemp
		return self

	#Relation composition: self(other)
	def compose(self,other):
		#Composing two relations?
		if isinstance(other,PresRelation):
			#Make sure the arities are valid
			if other.arity_out()!=self.arity_in():
				raise ValueError('Output arity of first relation (%d) does not match input arity of second relation (%d)'%(other.arity_out(),self.arity_in()))

			#Add equalities of tuple variables
			#We know there are the same number of variables since we checked above
			for i in xrange(self.arity_in()):
				constraint=Equality(IdExp(other._inTuple[i]),IdExp(self._outTuple[i]))
				self._conjunct._constraintList.append(constraint)

			#Add the other's constraints to this relation
			self._conjunct.extend(other._conjunct._constraintList)

			return self
		#Composing a relation with union of relations?
		elif isinstance(other,PresRelationUnion):
			new_union=PresRelationUnion([])
			for relation in other._relations:
				new_union._add_relation(self.compose(relation))
			return new_union
		else:
			raise ValueError("Unsupported argument of type '%s' for operation compose."%type(other))


# A list of presburger relations involved in a union.
class PresRelationUnion(IPresRelation):
	__slots__=('_relations')

	def __init__(self, relations):
		self._relations = relations
		self._arity_check()

	def __repr__(self):
		return "PresRelationUnion(%s)"%(self._relations)

	def _arity_check(self):
		if len(self._relations)>0:
			in_arity=self._relations[0].arity_in()
			out_arity=self._relations[0].arity_out()
		for relation in self._relations[1:]:
			if relation.arity_in()!=arity_in:
				raise ValueError('All relations in a PresRelationUnion must have the same input arity.')
			if relation.arity_out()!=arity_out:
				raise ValueError('All relations in a PresRelationUnion must have the same output arity.')

	def _add_relation(self,relation):
		if not isinstance(relation,PresRelation):
			raise ValueError("Cannot add object of type '%s' to PresRelationUnion."%type(relation))
		self._relations.append(relation)

	def _add_union(self,union):
		if not isinstance(relation,PresRelationUnion):
			raise ValueError("Cannot add relations from object of type '%s' to PresRelationUnion."%type(relation))
		self._relations.extend(union._relations)

	def arity_in(self):
		if len(self._relations)>0:
			return self._relations[0].arity_in()
		else:
			raise ValueError('Cannot determine input arity of a PresRelationUnion that contains no relations.')

	def arity_out(self):
		if len(self._relations)>0:
			return self._relations[0].arity_out()
		else:
			raise ValueError('Cannot determine output arity of a PresRelationUnion that contains no relations.')

	def apply_visitor(self,visitor):
		v.visitPresRelationUnion(self)

	def union(self, other):
		#Unioning a single relation?
		if isinstance(other,PresRelation):
			if 0==len(self._relations):
				self._add_relation(other)
			else:
				#Assuming that all relations already within the union
				#have matching arities
				if self._relations[0].arity_in()==other.arity_in() and \
				   self._relations[0].arity_out()==other.arity_out():
					self._add_relation(other)
				else:
					raise ValueError('Cannot union relations with differing in or out arity')
			return self
		#Unioning another union?
		elif isinstance(other,PresRelationUnion):
			if 0==len(self._relations) or 0==len(other._relations):
				self._add_union(other)
			else:
				#Assuming that all relations already within the unions
				#have matching arities
				if self._relations[0].arity_in()==other._relations[0].arity_in() and \
				   self._relations[0].arity_out()==other._relations[0].arity_out():
					self._add_union(other)
				else:
					raise ValueError('Cannot union relations with differing in or out arity')
			return self
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))

	def inverse(self):
		for relation in self._relations:
			relation.inverse()
		return self

	def compose(self,other):
		#Composing with a single relation?
		if isinstance(other,PresRelation):
			new_union=PresRelationUnion([])
			for relation in self._relations:
				new_union._add_relation(relation.compose(other))
			return new_union
		#Composing two unions?
		elif isinstance(other,PresRelationUnion):
			new_union=PresRelationUnion([])
			for self_relation in self._relations:
				for other_relation in other._relations:
					new_union._add_relation(self_relation.compose(other_relation))
			return new_union
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))
#------------------------------------------

#---------- Variable Nodes ----------
# Tuple of variables.
class VarTuple(Node):
	__slots__=('_idList')

	def __init__(self, idList):
		self._idList = idList

	def __repr__(self):
		return 'VarTuple(%s)'%(self._idList)

	def __len__(self):
		return len(self._idList)

	def apply_visitor(self,visitor):
		v.visitVarTuple(self)
#------------------------------------

#---------- Conjunction Nodes ----------
# A set of constraints that are all part of a conjunction (IOW ANDed together).
class Conjunction(Node):
	__slots__=('_constraintList')

	def __init__(self, constraintList):
		self._constraintList = constraintList

	def __repr__(self):
		return 'Conjunction(%s)'%(self._constraintList)

	def apply_visitor(self,visitor):
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
		return 'Inequality(%s,%s)'%(self._lhs,self._rhs)

	def apply_visitor(self,visitor):
		v.visitInequality(self)

class Equality(IConstraint):
	__slots__=('_lhs','_rhs')

	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

	def __repr__(self):
		return 'Equality(%s,%s)'%(self._lhs,self._rhs)

	def apply_visitor(self,visitor):
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
		return 'IntExp(%s)'%(self._val)

	def __eq__(self, other):
		# An IntExp is not equal to any other object instance type.
		if isinstance(other,IntExp)==False:
			return False
		# Check equality when other is a IntExp.
		if (self._val==other._val): return True
		else: return False

	def apply_visitor(self,visitor):
		v.visitIntExp(self)

# Identifier expressions
class IdExp(IExp):
	__slots__=('_id')

	def __init__(self, id):
		self._id = id

	def __repr__(self):
		return 'IdExp(%s)'%(self._id)

	def __eq__(self, other):
		# An IdExp is not equal to any other object instance type.
		if isinstance(other,IdExp)==False:
			return False
		# Check equality when other is a IdExp.
		if (self._id==other._id): return True
		else: return False

	def apply_visitor(self,visitor):
		v.visitIdExp(self)


# Unary Minus
class UMinusExp(IExp):
	__slots__=('_exp')

	def __init__(self, exp):
		self._exp = exp

	def __repr__(self):
		return 'UMinusExp(%s)'%(self._exp)

	def __eq__(self, other):
		# A UMinusExp is not equal to any other object instance type.
		if isinstance(other,UMinusExp)==False:
			return False
		# Check equality when other is a UMinusExp.
		# Multiplication is associative.
		if (self._exp==other._exp): return True
		else: return False

	def apply_visitor(self,visitor):
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
		return 'MulExp(%s,%s)'%(self._lhs,self._rhs)

	def __eq__(self, other):
		# A MulExp is not equal to any other object instance type.
		if isinstance(other,MulExp)==False:
			return False
		# Check equality when other is a MulExp.
		# Multiplication is associative.
		if (self._lhs==other._lhs and self._rhs==other._rhs): return True
		elif (self._lhs==other._rhs and self._rhs==other._lhs): return True
		else: return False

	def apply_visitor(self,visitor):
		v.visitMulExp(self)


# Binary Addition
class PlusExp(IExp):
	__slots__=('_lhs','_rhs')

	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

	def __repr__(self):
		return 'PlusExp(%s,%s)'%(self._lhs,self._rhs)

	def __eq__(self, other):
		# A PlusExp is not equal to any other object instance type.
		if isinstance(other,PlusExp)==False:
			return False
		# Check equality when other is a PlusExp.
		# Addition is associative.
		if (self._lhs==other._lhs and self._rhs==other._rhs): return True
		elif (self._lhs==other._rhs and self._rhs==other._lhs): return True
		else: return False

	def apply_visitor(self,visitor):
		v.visitPlusExp(self)


# Binary Subtraction
class MinusExp(IExp):
	__slots__=('_lhs','_rhs')

	def __init__(self, lhs, rhs):
		self._lhs = lhs
		self._rhs = rhs

	def __repr__(self):
		return 'MinusExp(%s,%s)'%(self._lhs,self._rhs)

	def __eq__(self, other):
		# A MinusExp is not equal to any other object instance type.
		if isinstance(other,MinusExp)==False:
			return False
		# check equality when other is a MinusExp
		if (self._lhs==other._lhs and self._rhs==other._rhs): return True
		else: return False

	def apply_visitor(self,visitor):
		v.visitMinusExp(self)


# Multiplication by a constant integer
class IntMulExp(IExp):
	__slots__=('_int','_exp')

	def __init__(self, int, exp):
		self._int = int
		self._exp = exp

	def __repr__(self):
		return 'IntMulExp(%s,%s)'%(self._int,self._exp)

	def __eq__(self, other):
		# A IntMulExp is not equal to any other object instance type
		# We are assuming that a MulExp will be canonicalized to an
		# IntMulExp upon construction if appropriate.
		if isinstance(other,IntMulExp)==False:
			return False
		# check equality when other is a IntMulExp
		if (self._int==other._int and self._exp==other._exp): return True
		else: return False

	def apply_visitor(self,visitor):
		v.visitIntMulExp(self)


# Uninterpreted function calls
class FuncExp(IExp):
	__slots__=('_func','_expList')

	def __init__(self, func, expList):
		self._func = func
		self._expList = expList

	def __repr__(self):
		return 'FuncExp(%s,%s)'%(self._func,self._expList)

	# Compare this uninterpreted function expression with another
	# uninterpreted function expression.  If the same function is
	# being called on equivalent parameters, then we know this expression
	# is equal, otherwise, we don't know whether it is equal or not.
	def __eq__(self, other):
		# A FuncExp is not equal to any other object instance type
		if isinstance(other,FuncExp)==False:
			return False
		# check equality when other is a FuncExp
		if (self._func==other._func and self._expList==other._expList):
			return True
		else:
			return False

	def apply_visitor(self,visitor):
		v.visitFuncExp(self)
#---------------------------------------
