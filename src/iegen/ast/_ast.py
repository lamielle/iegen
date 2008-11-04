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
#    Conjunction -> constraints:Constraint*
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
from cStringIO import StringIO
from iegen.util import like_type,raise_objs_not_like_types,normalize_self,normalize_result,check

#---------- Base AST Node class ----------
class Node(object):
	def apply_visitor(self,visitor):
		raise NotImplementedError('All node types should override the apply_visitor method.')
#-----------------------------------------

#---------- Presburger Formula ----------
#A presburger formula: either a set or a relation
class PresForm(Node):
	__slots__=('conjunct',)

	def __str__(self,vars,constraints=''):
		if len(self.symbolics)>0:
			syms=StringIO()
			syms.write(' | ')
			for symbolic in self.symbolics:
				syms.write('%s,'%symbolic.name)
			syms=syms.getvalue()[:-1]
		else:
			syms=''

		if len(constraints)>0:
			return '{%s: %s%s}'%(vars,constraints,syms)
		else:
			return '{%s%s}'%(vars,syms)

	#Determines if the given variable name exists as a variable anywhere in the formula
	#Returns True if the variable name exists
	#Returns False otherwise
	def is_var(self,var_name):
		from iegen.ast.visitor import IsVarVisitor
		return IsVarVisitor(var_name).visit(self).is_var

	#Determines if the given variable name is a symbolic variable
	#Returns True if the name is a symbolic variable
	#Returns False otherwise
	def is_symbolic_var(self,var_name):
		from iegen.ast.visitor import IsVarVisitor
		return IsVarVisitor(var_name).visit(self).is_symbolic_var

	#Determines if the given variable name is a variable used in the constraints
	#Returns True if the name is used in the constraints
	#Returns False otherwise
	def is_constraint_var(self,var_name):
		from iegen.ast.visitor import IsVarVisitor
		return IsVarVisitor(var_name).visit(self).is_constraint_var

	#Determines if the given variable name is a tuple variable
	#Returns True if the name is a tuple variable
	#Returns False otherwise
	def is_tuple_var(self,var_name):
		from iegen.ast.visitor import IsVarVisitor
		return IsVarVisitor(var_name).visit(self).is_tuple_var

	#Determines if the given variable name is a free variable
	#Returns True if the name is neither a tuple variable nor a symbolic variable
	#Returns False otherwise
	def is_free_var(self,var_name):
		from iegen.ast.visitor import IsVarVisitor
		v=IsVarVisitor(var_name).visit(self)
		return v.is_var and not v.is_symbolic_var and not v.is_tuple_var

	#Returns True if this PresFormula is a true statement (all terms in its conjunction are tautologies)
	#Returns False otherwise
	#Determines the 'truthiness' of the formula
	def is_tautology(self):
		res=True
		for term in self.conjunct.constraints:
			res=res and term.is_tautology()
		return res

	#Returns True if this PresFormula is a false statement (any term in its conjunction is a contradiction)
	#Returns False otherwise
	#Determines the 'truthiness' of the formula
	def is_contradiction(self):
		res=False
		for term in self.conjunct.constraints:
			res=res or term.is_contradiction()
		return res

#----------------------------------------

#---------- Presburger Set ----------
#A single presburger set
class PresSet(PresForm):
	__slots__=('tuple_set','conjunct','symbolics')

	@check
	def __init__(self,tuple_set,conjunct,symbolics=None):
		self.tuple_set=tuple_set
		self.conjunct=conjunct
		self.symbolics=[] if symbolics is None else symbolics

	def __repr__(self):
		if len(self.symbolics)>0:
			return 'PresSet(%s,%s,%s)'%(repr(self.tuple_set),repr(self.conjunct),repr(self.symbolics))
		else:
			return 'PresSet(%s,%s)'%(repr(self.tuple_set),repr(self.conjunct))

	def __str__(self):
		if len(self.conjunct)>0:
			return PresForm.__str__(self,str(self.tuple_set),str(self.conjunct))
		else:
			return PresForm.__str__(self,str(self.tuple_set))

	#Comparison operator
	def __cmp__(self,other):
		#Compare PresSets by their VarTuple, Conjunction, and Symbolics
		if like_type(other,PresSet):
			return cmp((self.tuple_set,self.conjunct,self.symbolics),(other.tuple_set,other.conjunct,self.symbolics))
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	def arity(self):
		return len(self.tuple_set)

	def apply_visitor(self,visitor):
		visitor.visitPresSet(self)
#-------------------------------------

#---------- Presburger Relation ----------
#A single presburger relation
class PresRelation(PresForm):
	__slots__=('tuple_in','tuple_out','conjunct','symbolics')

	@check
	def __init__(self,tuple_in,tuple_out,conjunct,symbolics=None):
		self.tuple_in=tuple_in
		self.tuple_out=tuple_out
		self.conjunct=conjunct
		self.symbolics=[] if symbolics is None else symbolics

	def __repr__(self):
		if len(self.symbolics)>0:
			return 'PresRelation(%s,%s,%s,%s)'%(repr(self.tuple_in),repr(self.tuple_out),repr(self.conjunct),repr(self.symbolics))
		else:
			return 'PresRelation(%s,%s,%s)'%(repr(self.tuple_in),repr(self.tuple_out),repr(self.conjunct))

	def __str__(self):
		if len(self.conjunct)>0:
			return PresForm.__str__(self,'%s->%s'%(self.tuple_in,self.tuple_out),str(self.conjunct))
		else:
			return PresForm.__str__(self,'%s->%s'%(self.tuple_in,self.tuple_out))

	#Comparison operator
	def __cmp__(self,other):
		#Compare PresRelations by their VarTuples, Conjunction, and Symbolics
		if like_type(other,PresRelation):
			return cmp((self.tuple_in,self.tuple_out,self.conjunct,self.symbolics),(other.tuple_in,self.tuple_out,other.conjunct,self.symbolics))
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
		return 'VarTuple(%s)'%repr(self.vars)

	def __str__(self):
		s=StringIO()
		for var in self.vars:
			s.write('%s%s'%(str(var),','))
		return '%s%s%s'%('[',s.getvalue()[:-1],']')

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
	__slots__=('constraints',)

	@normalize_self
	@check
	def __init__(self,constraints):
		self.constraints=constraints

	def __repr__(self):
		return 'Conjunction(%s)'%repr(self.constraints)

	def __str__(self):
		s=StringIO()
		for constraint in self.constraints:
			s.write('%s%s'%(str(constraint),' and '))
		return s.getvalue()[:-5]

	def __len__(self):
		return len(self.constraints)

	#Comparison operator
	def __cmp__(self,other):
		#Compare Conjunctions by their constraintss
		if like_type(other,Conjunction):
			return cmp(self.constraints,other.constraints)
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

	#Returns True if this constraints expression is empty
	#Returns False otherwise
	def empty(self):
		return self.exp.empty()

class Equality(Constraint):
	@normalize_self
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
		return 'Equality(%s)'%repr(self.exp)

	def __str__(self):
		return '%s=0'%str(self.exp)

	#Returns True if this Equality is a true statement (0=0)
	#Returns False otherwise
	#Determines the 'truthiness' of the constraint
	def is_tautology(self):
		res=False
		if self.exp.is_const():
			if 0==self.exp.const:
				res=True
		return res

	#Returns True if this Equality is a true statement (c=0)
	#Returns False otherwise
	#Determines the 'truthiness' of the constraint
	def is_contradiction(self):
		res=False
		if self.exp.is_const():
			if 0!=self.exp.const:
				res=True
		return res

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
		return 'Inequality(%s)'%repr(self.exp)

	def __str__(self):
		return '%s>=0'%str(self.exp)

	#Returns True if this Inequality is a true statement (non-neg_c>=0)
	#Returns False otherwise
	#Determines the 'truthiness' of the constraint
	def is_tautology(self):
		res=False
		if self.exp.is_const():
			if self.exp.const>=0:
				res=True
		return res

	#Returns True if this Inequality is a true statement (neg_c>=0)
	#Returns False otherwise
	#Determines the 'truthiness' of the constraint
	def is_contradiction(self):
		res=False
		if self.exp.is_const():
			if self.exp.const<0:
				res=True
		return res

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
			return 'VarExp(%s,"%s")'%(repr(self.coeff),self.id)
		else:
			return "VarExp(%s,'%s')"%(repr(self.coeff),self.id)

	def __str__(self):
		if self.coeff==1:
			return self.id
		else:
			return '%s%s'%(self.coeff,self.id)

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

	@normalize_self
	@check
	def __init__(self,coeff,name,args):
		self.coeff=coeff
		self.name=name
		self.args=args

	def __repr__(self):
		#Use double quotes if this function's name has a "'" in it
		if self.name.find("'")>=0:
			return 'FuncExp(%s,"%s",%s)'%(repr(self.coeff),self.name,repr(self.args))
		else:
			return "FuncExp(%s,'%s',%s)"%(repr(self.coeff),self.name,repr(self.args))

	def __str__(self):
		arg_str=StringIO()
		for arg in self.args:
			arg_str.write('%s%s'%(str(arg),','))
		arg_str=arg_str.getvalue()[:-1]

		if self.coeff==1:
			return '%s(%s)'%(self.name,arg_str)
		else:
			return '%s%s(%s)'%(self.coeff,self.name,arg_str)

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

	@normalize_self
	@check
	def __init__(self,terms,const):
		self.terms=terms
		self.const=const

	def __repr__(self):
		return 'NormExp(%s,%s)'%(repr(self.terms),repr(self.const))

	def __str__(self):
		terms_str=StringIO()
		for term in self.terms:
			terms_str.write('%s%s'%(str(term),'+'))
		terms_str=terms_str.getvalue()[:-1]

		if len(self.terms)>0:
			if 0!=self.const:
				return '%s%s%s'%(terms_str,'+',self.const)
			else:
				return terms_str
		else:
			return str(self.const)

	#Returns True if this NormExp has any variables or functions (terms)
	#Returns False if this NormExp is only a constant value
	#and has no variables or functions
	def _has_terms(self):
		return True if 0!=len(self.terms) else False

	#Returns True if this NormExp has no terms and the constant is 0
	#Returns False otherwise
	def empty(self):
		return not self._has_terms() and 0==self.const

	#Given a collection of Symbolic constants...
	#Returns True if this NormExp has only symbolic constants in its terms
	#Returns False otherwise
	#
	#Note that providing a collection of symbolic is optional
	#If the collection is not provided, this method will essentially
	#check that the expression has no terms
	def is_const(self,syms=None):
		from iegen import Symbolic
		syms=[] if syms is None else syms
		raise_objs_not_like_types(syms,Symbolic)

		if not self._has_terms():
			return True
		else:
			res=True
			for term in self.terms:
				term_matches_sym=False
				for sym in syms:
					if term.id==sym.name:
						term_matches_sym=True
				if not term_matches_sym:
					res=False
			return res

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
	@normalize_result
	def __add__(self,other):
		if not like_type(other,NormExp):
			raise ValueError("Addition between a '%s' and a '%s' is undefined."%(type(self),type(other)))

		self=deepcopy(self)
		other=deepcopy(other)

		#Add the terms from other to self (merging will happen during normalization)
		for term in other.terms:
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
	@normalize_result
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
