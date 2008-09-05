from iegen.ast.visitor import DFVisitor
from iegen.util import raise_objs_not_like_types,raise_objs_not_like_types

class CheckVisitor(DFVisitor):
	def __init__(self): pass

	#Do nothing by default
	def defaultIn(self,node): pass
	def defaultOut(self,node): pass

	def inPresSet(self,node):
		from iegen.ast import VarTuple,Conjunction
		raise_objs_not_like_types(node.tuple_set,VarTuple)
		raise_objs_not_like_types(node.conjunct,Conjunction)

	def inPresRelation(self,node):
		from iegen.ast import VarTuple,Conjunction
		raise_objs_not_like_types(node.tuple_in,VarTuple)
		raise_objs_not_like_types(node.tuple_out,VarTuple)
		raise_objs_not_like_types(node.conjunct,Conjunction)

	def inVarTuple(self,node):
		from iegen.ast import VarExp
		raise_objs_not_like_types(node.vars,VarExp)

	def inConjunction(self,node):
		from iegen.ast import Equality,Inequality
		raise_objs_not_like_types(node.constraint_list,[Equality,Inequality])

	def inEquality(self,node):
		from iegen.ast import VarExp,FuncExp,NormExp
		raise_objs_not_like_types(node.exp,NormExp)

	def inInequality(self,node):
		from iegen.ast import VarExp,FuncExp,NormExp
		raise_objs_not_like_types(node.exp,NormExp)

	def inVarExp(self,node):
		if type('')!=type(node.id):
			raise ValueError('VarExp.id must be a string.')
		if type(0)!=type(node.coeff):
			raise ValueError('VarExp.coeff must be an integer.')

	def inFuncExp(self,node):
		from iegen.ast import NormExp
		if type(0)!=type(node.coeff):
			raise ValueError('FuncExp.coeff must be an integer.')
		if type('')!=type(node.name):
			raise ValueError('FuncExp.name must be a string.')
		raise_objs_not_like_types(node.args,NormExp)

	def inNormExp(self,node):
		from iegen.ast import VarExp,FuncExp
		raise_objs_not_like_types(node.terms,[VarExp,FuncExp])
		if type(0)!=type(node.const):
			raise ValueError('NormExp.const must be an integer.')
