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
#    IConstraint -> IExp:lhs IExp:rhs // Inequality (GTE assummed)
#                -> IExp:lhs IExp:rhs // Equality
#
#    IExp  -> INT                // IntExp
#          -> IExp:operand       // UMinusExp
#          -> IExp:lhs Expr:rhs  // MulExp, PlusExp, MinusExp
#          -> INT IExp           // IntMulExp
#          -> ID                 // VarExp
#          -> ID:func IExp*      // FuncExp
#
# Naming Convention
#	A class prefixed with "I" is an interface class.
#
# Michelle Strout 7/22/08
#

from copy import deepcopy

#base Node class
#Not an interface, because might have a generic child list in the Node class
#later.
class Node(object):
	def apply_visitor(self,visitor):
		raise NotImplementedError('All node types should override the apply_visitor method.')

#---------- Presburger Sets ----------
#Presburger set interface
class IPresSet(Node):
	pass

#A single presburger set.
class PresSet(IPresSet):
	__slots__=('set_tuple','conjunct')

	def __init__(self,set_tuple,conjunct):
		self.set_tuple=set_tuple
		self.conjunct=conjunct

	def __repr__(self):
		return 'PresSet(%s,%s)'%(self.set_tuple,self.conjunct)

	def arity(self):
		return len(self.set_tuple)

	def apply_visitor(self,visitor):
		visitor.visitPresSet(self)

	def union(self,other):
		if isinstance(other,PresSet):
			return PresSetUnion([self,other])
		elif isinstance(other,PresSetUnion):
			return other.union(self)
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))


#A list of presburger sets involved in a union.
class PresSetUnion(IPresSet):
	__slots__=('sets',)

	def __init__(self,sets):
		self.sets=sets
		self._arity_check()

	def __repr__(self):
		return "PresSetUnion(%s)"%(self.sets)

	def _arity_check(self):
		if len(self.sets)>0:
			set_arity=self.sets[0].arity()
		for set in self.sets[1:]:
			if set.arity()!=set_arity:
				raise ValueError('All sets in a PresSetUnion must have the same arity.')

	def _add_set(self,set):
		if not isinstance(set,PresSet):
			raise ValueError("Cannot add object of type '%s' to PresSetUnion."%type(set))
		self.sets.append(set)

	def _add_union(self,union):
		if not isinstance(set,PresSetUnion):
			raise ValueError("Cannot add sets from object of type '%s' to PresSetUnion."%type(set))
		self.sets.extend(union.sets)

	def arity(self):
		if len(self.sets)>0:
			return self.sets[0].arity()
		else:
			raise ValueError('Cannot determine arity of a PresSetUnion that contains no sets.')

	def apply_visitor(self,visitor):
		visitor.visitPresSetUnion(self)

	def union(self,other):
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
#Presburger relation interface
class IPresRelation(Node):
	pass

#A single presburger relation
class PresRelation(IPresRelation):
	__slots__=('in_tuple','out_tuple','conjunct')

	def __init__(self,in_tuple,out_tuple,conjunct):
		self.in_tuple=in_tuple
		self.out_tuple=out_tuple
		self.conjunct=conjunct

	def __repr__(self):
		return 'PresRelation(%s,%s,%s)'%(self.in_tuple,self.out_tuple,self.conjunct)

	def arity_in(self):
		return len(self.in_tuple)
	def arity_out(self):
		return len(self.out_tuple)

	def apply_visitor(self,visitor):
		visitor.visitPresRelation(self)

	def union(self,other):
		if isinstance(other,PresRelation):
			result=PresRelationUnion([self])
			result.union(other)
			return result
		elif isinstance(other,PresRelationUnion):
			return other.union(self)
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))

	def inverse(self):
		outTemp=self.out_tuple
		self.out_tuple=self.in_tuple
		self.in_tuple=outTemp
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
				constraint=Equality(MinusExp(VarExp(other.in_tuple[i]),VarExp(self.out_tuple[i])))
				self.conjunct.constraint_list.append(constraint)

			#Add the other's constraints to this relation
			self.conjunct.extend(other.conjunct.constraint_list)

			return self
		#Composing a relation with union of relations?
		elif isinstance(other,PresRelationUnion):
			new_union=PresRelationUnion([])
			for relation in other.relations:
				new_union._add_relation(self.compose(relation))
			return new_union
		else:
			raise ValueError("Unsupported argument of type '%s' for operation compose."%type(other))


#A list of presburger relations involved in a union.
class PresRelationUnion(IPresRelation):
	__slots__=('relations',)

	def __init__(self,relations):
		self.relations=relations
		self._arity_check()

	def __repr__(self):
		return "PresRelationUnion(%s)"%(self.relations)

	def _arity_check(self):
		if len(self.relations)>0:
			in_arity=self.relations[0].arity_in()
			out_arity=self.relations[0].arity_out()
		for relation in self.relations[1:]:
			if relation.arity_in()!=arity_in:
				raise ValueError('All relations in a PresRelationUnion must have the same input arity.')
			if relation.arity_out()!=arity_out:
				raise ValueError('All relations in a PresRelationUnion must have the same output arity.')

	def _add_relation(self,relation):
		if not isinstance(relation,PresRelation):
			raise ValueError("Cannot add object of type '%s' to PresRelationUnion."%type(relation))
		self.relations.append(relation)

	def _add_union(self,union):
		if not isinstance(relation,PresRelationUnion):
			raise ValueError("Cannot add relations from object of type '%s' to PresRelationUnion."%type(relation))
		self.relations.extend(union.relations)

	def arity_in(self):
		if len(self.relations)>0:
			return self.relations[0].arity_in()
		else:
			raise ValueError('Cannot determine input arity of a PresRelationUnion that contains no relations.')

	def arity_out(self):
		if len(self.relations)>0:
			return self.relations[0].arity_out()
		else:
			raise ValueError('Cannot determine output arity of a PresRelationUnion that contains no relations.')

	def apply_visitor(self,visitor):
		visitor.visitPresRelationUnion(self)

	def union(self,other):
		#Unioning a single relation?
		if isinstance(other,PresRelation):
			if 0==len(self.relations):
				self._add_relation(other)
			else:
				#Assuming that all relations already within the union
				#have matching arities
				if self.relations[0].arity_in()==other.arity_in() and \
				   self.relations[0].arity_out()==other.arity_out():
					self._add_relation(other)
				else:
					raise ValueError('Cannot union relations with differing in or out arity')
			return self
		#Unioning another union?
		elif isinstance(other,PresRelationUnion):
			if 0==len(self.relations) or 0==len(other.relations):
				self._add_union(other)
			else:
				#Assuming that all relations already within the unions
				#have matching arities
				if self.relations[0].arity_in()==other.relations[0].arity_in() and \
				   self.relations[0].arity_out()==other.relations[0].arity_out():
					self._add_union(other)
				else:
					raise ValueError('Cannot union relations with differing in or out arity')
			return self
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))

	def inverse(self):
		for relation in self.relations:
			relation.inverse()
		return self

	def compose(self,other):
		#Composing with a single relation?
		if isinstance(other,PresRelation):
			new_union=PresRelationUnion([])
			for relation in self.relations:
				new_union._add_relation(relation.compose(other))
			return new_union
		#Composing two unions?
		elif isinstance(other,PresRelationUnion):
			new_union=PresRelationUnion([])
			for self_relation in self.relations:
				for other_relation in other.relations:
					new_union._add_relation(self_relation.compose(other_relation))
			return new_union
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))
#------------------------------------------

#---------- Variable Tuple Node ----------
#Tuple of variables.
class VarTuple(Node):
	__slots__=('id_list',)

	def __init__(self,id_list):
		self.id_list=id_list

	def __repr__(self):
		return 'VarTuple(%s)'%(self.id_list)

	def __len__(self):
		return len(self.id_list)

	def apply_visitor(self,visitor):
		visitor.visitVarTuple(self)
#------------------------------------

#---------- Conjunction Node ----------
#A set of constraints that are all part of a conjunction (IOW ANDed together).
class Conjunction(Node):
	__slots__=('constraint_list',)

	def __init__(self,constraint_list):
		self.constraint_list=constraint_list

	def __repr__(self):
		return 'Conjunction(%s)'%(self.constraint_list)

	def apply_visitor(self,visitor):
		visitor.visitConjunction(self)
#---------------------------------------

#---------- Constraint Nodes ----------
#Interface for constraints.
class IConstraint(Node):
	pass


class Equality(IConstraint):
	__slots__=('exp',)

	def __init__(self,exp):
		self.exp=exp

	def __repr__(self):
		return 'Equality(%s)'%self.exp

	def apply_visitor(self,visitor):
		visitor.visitEquality(self)


#It is assummed that all constraints are converted to GTE
#inequalities.
class Inequality(IConstraint):
	__slots__=('exp',)

	def __init__(self,exp):
		self.exp=exp

	def __repr__(self):
		return 'Inequality(%s)'%self.exp

	def apply_visitor(self,visitor):
		visitor.visitInequality(self)
#--------------------------------------

#---------- Expression Nodes ----------
class IExp(Node):
	pass

#Variable expression
class VarExp(IExp):
	__slots__=('coeff','id')

	def __init__(self,coeff,id):
		self.coeff=coeff
		self.id=id

	def __repr__(self):
		return 'VarExp(%s,%s)'%(self.coeff,self.id)

	#Comparison operator
	def __cmp__(self,other):
		#Compare other variables by their coefficients and ids
		if hasattr(other,'id'):
			return cmp((self.coeff,self.id),(other.coeff,other.id))
		#Variables are 'less' than functions
		elif hasattr(other,'name') and hasattr(other,'exp_list'):
			return -1
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

#	#Equality operator
#	def __eq__(self,other):
#		return 0==cmp(self,other)

	#Multiplication operator:
	#This is only defined between a variable and an integer
	def __mul__(self,other):
		if hasattr(self,'coeff') and hasattr(other,'coeff'):
			raise ValueError("Multiplication between a '%s' and a '%s' is undefined."%(type(self),type(other)))

		#Swap self and other if necessary so that self is the constant expression
		if hasattr(self,'coeff'):
			self,other=other,self

		other=deepcopy(other)
		other.coeff*=self
		return other

	def apply_visitor(self,visitor):
		visitor.visitVarExp(self)


#Function expression
class FuncExp(IExp):
	__slots__=('coeff','name','exp_list')

	def __init__(self,coeff,name,exp_list):
		self.coeff=coeff
		self.name=name
		self.exp_list=exp_list

	def __repr__(self):
		return 'FuncExp(%s,%s,%s)'%(self.coeff,self.name,self.exp_list)

	#Comparison operator
	def __cmp__(self,other):
		#Functions are 'greater' than IDs
		if hasattr(other,'id'):
			return 1
		elif hasattr(other,'name') and hasattr(other,'exp_list'):
			return cmp((self.coeff,self.name,self.exp_list),(other.coeff,other.name,other.exp_list))
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

#	#Equality operator
#	def __eq__(self,other):
#		return 0==cmp(self,other)

	#Multiplication operator:
	#This is only defined between a function and an integer
	def __mul__(self,other):
		if hasattr(self,'coeff') and hasattr(other,'coeff'):
			raise ValueError("Multiplication between a '%s' and a '%s' is undefined."%(type(self),type(other)))

		#Swap self and other if necessary so that self is the constant expression
		if hasattr(self,'coeff'):
			self,other=other,self

		other=deepcopy(other)
		other.coeff*=self
		return other

	def apply_visitor(self,visitor):
		visitor.visitFuncExp(self)


#Normalized expression containing:
#-A collection of variables and their coefficients
#   and of function calls and their coefficients (terms)
#-A constant value (const)
class NormExp(IExp):
	__slots__=('terms','const')

	def __init__(self,terms,const):
		self.terms=terms
		self.const=const

	def __repr__(self):
		return 'NormExp(%s,%s)'%(self.terms,self.const)

	#Returns True if this NormExp has any variables or functions (terms)
	#Returns False if this NormExp is only a constant value
	#and has no variables or functions
	def _has_terms(self):
		return True if 0!=len(self.terms) else False

	#Comparison operator
	def __cmp__(self,other):
		#Functions are 'greater' than IDs
		if hasattr(other,'terms') and hasattr(other,'const'):
			return cmp((self.terms,self.const),(other.terms,other.const))
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

#	#Equality operator
#	def __eq__(self,other):
#		return 0==cmp(self,other)

	#Addition operator:
	#Adds the two given NormExp expressions
	#This operator is non-destructive: A complete copy of the arguments
	#are made while leaving 'self' and 'other' untouched
	def __add__(self,other):
		if not hasattr(self,'terms') or not hasattr(self,'const') or not hasattr(other,'terms') or not hasattr(other,'const'):
			raise ValueError("Addition between a '%s' and a '%s' is undefined."%(type(self),type(other)))

		self=deepcopy(self)
		other=deepcopy(other)

		#Add the terms from other to self
		for term in other.terms:
			if term in self.terms:
				index=self.terms.index(term)
				self.terms[index].coeff+=term.coeff
			else:
				self.terms.append(term)

		#Add the constant value from other to self
		self.const+=other.const

		return self

	#Multiplication operator:
	#This is only defined between two NormExps where
	#one is a constant expression (NormExp.has_terms==False)
	#Multiplication of two NormExps that both have terms is undefined
	#This operator is non-destructive: A complete copy of the arguments
	#are made while leaving 'self' and 'other' untouched
	def __mul__(self,other):
		if not hasattr(self,'terms') or not hasattr(self,'const') or not hasattr(other,'terms') or not hasattr(other,'const'):
			raise ValueError("Multiplication between a '%s' and a '%s' is undefined."%(type(self),type(other)))

		#Make sure one of the terms is only a constant and has no terms
		#Multiplication of variablies is undefined here
		if self._has_terms() and other._has_terms():
			raise ValueError("Multiplication of variables/functions with other variables/functions is not defined.");

		self=deepcopy(self)
		other=deepcopy(other)

		#Swap self and other if necessary so that self is the constant expression
		if self._has_terms():
			self,other=other,self
		const=self.const

		#Now do the multiplication of the variables, functions, and constant
		new_terms=[]
		for term in other.terms:
			new_terms.append(term*const)
		other.terms=new_terms

		other.const*=const

		return other

	#Negation operator
	def __neg__(self):
		return NormExp([],-1)*self

	#Subtraction operator
	def __sub__(self,other):
		return self+(-other)

	#Returns a collection of all of the variable terms in this expression
	def _vars(self):
		return [term for term in terms if hasattr(term,'id')]

	#Returns a collection of all of the function terms in this expression
	def _funcs(self):
		return [term for term in self.terms if hasattr(term,'name') and hasattr(term,'exp_list')]

	def apply_visitor(self,visitor):
		visitor.visitNormExp(self)
#---------------------------------------
