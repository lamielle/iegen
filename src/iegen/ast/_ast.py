# ast.py
#
# Abstract syntax tree representaton for presburger sets and relations
# with uninterpreted function symbols.
#
# Grammar for AST
#
#    PresSet -> tuple_set:VarTuple conjunct:Conjunction // PresSet
#
#    PresRelation -> tuple_in:VarTuple tuple_out:VarTuple conjunct:Conjunction // PresSet
#
#    VarTuple -> vars:ID*
#
#    Conjunction -> constraint_list:Constraint*
#
#    Constraint -> NormExp>=0 // Inequality
#               -> NormExp=0  // Equality
#
#    NormExp -> 
#
#    Exp  -> INT                // IntExp
#          -> IExp:operand       // UMinusExp
#          -> IExp:lhs Expr:rhs  // MulExp, PlusExp, MinusExp
#          -> INT IExp           // IntMulExp
#          -> ID                 // VarExp
#          -> ID:func IExp*      // FuncExp
#
# Started by: Michelle Strout 7/22/08
# Modified by: Alan LaMielle starting around 7/30/08
# AML 8/25/2008: Removed PresSetUnion and PresRelationUnion
#

from copy import deepcopy
from iegen.util import like_type,sort_self,sort_result,check

#---------- Base AST Node class ----------
class Node(object):
	def apply_visitor(self,visitor):
		raise NotImplementedError('All node types should override the apply_visitor method.')
#-----------------------------------------

#---------- Presburger Set ----------
#A single presburger set
class PresSet(Node):
	__slots__=('tuple_set','conjunct')

	@check
	def __init__(self,tuple_set,conjunct):
		self.tuple_set=tuple_set
		self.conjunct=conjunct

	def __repr__(self):
		return 'PresSet(%s,%s)'%(self.tuple_set,self.conjunct)

	#Comparison operator
	def __cmp__(self,other):
		#Compare PresSets by their VarTuple and Conjunction
		if like_type(other,PresSet):
			return cmp((self.tuple_set,self.conjunct),(other.tuple_set,other.conjunct))
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	def arity(self):
		return len(self.tuple_set)

	def apply_visitor(self,visitor):
		visitor.visitPresSet(self)
#-------------------------------------

#---------- Presburger Relation ----------
#A single presburger relation
class PresRelation(Node):
	__slots__=('tuple_in','tuple_out','conjunct')

	@check
	def __init__(self,tuple_in,tuple_out,conjunct):
		self.tuple_in=tuple_in
		self.tuple_out=tuple_out
		self.conjunct=conjunct

	def __repr__(self):
		return 'PresRelation(%s,%s,%s)'%(self.tuple_in,self.tuple_out,self.conjunct)

	#Comparison operator
	def __cmp__(self,other):
		#Compare PresRelations by their VarTuple and Conjunction
		if like_type(other,PresRelation):
			return cmp((self.tuple_in,self.tuple_out,self.conjunct),(other.tuple_in,self.tuple_out,other.conjunct))
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	def arity(self):
		return (self.arity_in(),self.arity_out())
	def arity_in(self):
		return len(self.tuple_in)
	def arity_out(self):
		return len(self.tuple_out)

	def apply_visitor(self,visitor):
		visitor.visitPresRelation(self)
#------------------------------------------

#---------- Variable Tuple Node ----------
#Tuple of variables.
class VarTuple(Node):
	__slots__=('vars',)

	@check
	def __init__(self,vars):
		self.vars=vars

	def __repr__(self):
		return 'VarTuple(%s)'%(self.vars)

	def __len__(self):
		return len(self.vars)

	#Comparison operator
	def __cmp__(self,other):
		#Compare VarTuples by their vars
		if like_type(other,VarTuple):
			return cmp(self.vars,other.vars)
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	def apply_visitor(self,visitor):
		visitor.visitVarTuple(self)
#------------------------------------

#---------- Conjunction Node ----------
#A set of constraints that are all part of a conjunction (IOW ANDed together).
class Conjunction(Node):
	__slots__=('constraint_list',)

	@sort_self
	@check
	def __init__(self,constraint_list):
		self.constraint_list=constraint_list

	def __repr__(self):
		return 'Conjunction(%s)'%(self.constraint_list)

	#Comparison operator
	def __cmp__(self,other):
		#Compare Conjunctions by their constraint_lists
		if like_type(other,Conjunction):
			return cmp(self.constraint_list,other.constraint_list)
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	def apply_visitor(self,visitor):
		visitor.visitConjunction(self)
#---------------------------------------

#---------- Constraint Nodes ----------
class Constraint(Node):
	__slots__=('_equality','exp')

	#Comparison operator
	def __cmp__(self,other):
		#Compare Constraints by their expression and Equality/Inequality type
		if like_type(other,Constraint):
			return cmp((self._equality,self.exp),(other._equality,other.exp))
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))


class Equality(Constraint):
	@sort_self
	@check
	def __init__(self,exp):
		self.exp=exp
		self._equality=True

	#Canonicalize the expression by taking the 'larger' of exp and -1*exp since Equality is reflexive and both expressions are equivalent in this case
	def _set_largest_exp(self):
		neg_exp=NormExp([],-1)*self.exp

		if neg_exp>self.exp:
			self.exp=neg_exp

	def __repr__(self):
		return 'Equality(%s)'%self.exp

	def apply_visitor(self,visitor):
		visitor.visitEquality(self)


#It is assummed that all constraints are converted to GTE
#inequalities.
class Inequality(Constraint):
	@check
	def __init__(self,exp):
		self.exp=exp
		self._equality=False

	def __repr__(self):
		return 'Inequality(%s)'%self.exp

	def apply_visitor(self,visitor):
		visitor.visitInequality(self)
#--------------------------------------

#---------- Expression Nodes ----------
class Expression(Node):
	pass

#Variable expression
class VarExp(Expression):
	__slots__=('coeff','id')

	@check
	def __init__(self,coeff,id):
		self.coeff=coeff
		self.id=id

	def __repr__(self):
		#Use double quotes if this variable's name has a "'" in it
		if self.id.find("'")>=0:
			return 'VarExp(%s,"%s")'%(self.coeff,self.id)
		else:
			return "VarExp(%s,'%s')"%(self.coeff,self.id)

	#Comparison operator
	def __cmp__(self,other):
		#Compare other variables by their coefficients and ids
		if like_type(other,VarExp):
			return cmp((self.coeff,self.id),(other.coeff,other.id))
		#Variables are 'greater' than functions
		elif like_type(other,FuncExp):
			return -1
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	#Multiplication operator:
	#This is only defined between a variable and an integer
	def __mul__(self,other):
		if type(0) is not type(other):
			raise ValueError("Multiplication between a '%s' and a '%s' is undefined."%(type(self),type(other)))

		self=deepcopy(self)
		self.coeff*=other
		return self

	#Reflexive multiplication
	def __rmul__(self,other):
		return self*other

	def apply_visitor(self,visitor):
		visitor.visitVarExp(self)


#Function expression
class FuncExp(Expression):
	__slots__=('coeff','name','args')

	@sort_self
	@check
	def __init__(self,coeff,name,args):
		self.coeff=coeff
		self.name=name
		self.args=args

	def __repr__(self):
		#Use double quotes if this function's name has a "'" in it
		if self.name.find("'")>=0:
			return 'FuncExp(%s,"%s",%s)'%(self.coeff,self.name,self.args)
		else:
			return "FuncExp(%s,'%s',%s)"%(self.coeff,self.name,self.args)

	#Comparison operator
	def __cmp__(self,other):
		#Functions are 'less' than IDs
		if like_type(other,VarExp):
			return 1
		elif like_type(other,FuncExp):
			return cmp((self.coeff,self.name,self.args),(other.coeff,other.name,other.args))
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	#Multiplication operator:
	#This is only defined between a function and an integer
	def __mul__(self,other):
		if type(0) is not type(other):
			raise ValueError("Multiplication between a '%s' and a '%s' is undefined."%(type(self),type(other)))

		self=deepcopy(self)
		self.coeff*=other
		return self

	#Reflexive multiplication
	def __rmul__(self,other):
		return self*other

	def apply_visitor(self,visitor):
		visitor.visitFuncExp(self)


#Normalized expression containing:
#-A collection of variables and their coefficients
#   and of function calls and their coefficients (terms)
#-A constant value (const)
class NormExp(Expression):
	__slots__=('terms','const')

	@sort_self
	@check
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
		if like_type(other,NormExp):
			return cmp((self.const,self.terms),(other.const,other.terms))
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	#Addition operator:
	#Adds the two given NormExp expressions
	#This operator is non-destructive: A complete copy of the arguments
	#are made while leaving 'self' and 'other' untouched
	@sort_result
	def __add__(self,other):
		if not like_type(other,NormExp):
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
	@sort_result
	def __mul__(self,other):
		if not like_type(other,NormExp):
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
		return [term for term in terms if like_type(term,VarExp)]

	#Returns a collection of all of the function terms in this expression
	def _funcs(self):
		return [term for term in self.terms if like_type(term,FuncExp)]

	def apply_visitor(self,visitor):
		visitor.visitNormExp(self)
#---------------------------------------
