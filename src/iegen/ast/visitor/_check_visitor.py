from iegen.ast.visitor import DFVisitor
from iegen.util import raise_objs_not_like_types,raise_objs_not_like_types

class CheckVisitor(DFVisitor):
	def __init__(self):
		self.arity=None
		self.in_var_tuple=False

	def inSet(self,node):
		from iegen.ast import PresSet
		raise_objs_not_like_types(node.sets,PresSet,True)

	def inRelation(self,node):
		from iegen.ast import PresRelation
		raise_objs_not_like_types(node.relations,PresRelation)

	def inPresSet(self,node):
		from iegen import Symbolic
		from iegen.ast import VarTuple,Conjunction
		raise_objs_not_like_types(node.tuple_set,VarTuple)
		raise_objs_not_like_types(node.conjunct,Conjunction)
		raise_objs_not_like_types(node.symbolics,Symbolic)

		if None is self.arity:
			self.arity=node.arity()
		elif node.arity()!=self.arity:
					raise ValueError('All sets in a Set must have the same arity.')

	def inPresRelation(self,node):
		from iegen import Symbolic
		from iegen.ast import VarTuple,Conjunction
		raise_objs_not_like_types(node.tuple_in,VarTuple)
		raise_objs_not_like_types(node.tuple_out,VarTuple)
		raise_objs_not_like_types(node.conjunct,Conjunction)
		raise_objs_not_like_types(node.symbolics,Symbolic)

		if None is self.arity:
			self.arity=node.arity()
		elif node.arity()!=self.arity:
			raise ValueError('All relations in a Relation must have the same input and output arity.')

	def inVarTuple(self,node):
		from iegen.ast import VarExp
		raise_objs_not_like_types(node.vars,VarExp)
		self.in_var_tuple=True

	def outVarTuple(self,node):
		self.in_var_tuple=False

	def inConjunction(self,node):
		from iegen.ast import Equality,Inequality
		raise_objs_not_like_types(node.constraints,[Equality,Inequality])

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

		if self.in_var_tuple:
			if node.coeff!=1:
				raise ValueError('VarExp.coeff must be 1 for VarTuple variables.')

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
