from unittest import TestCase
from iegen.lib.nose.tools import raises

#---------- Import Tests ----------
#Test importing of iegen.ast
class ImportTestCase(TestCase):

	#Test simple importing of iegen.ast
	def testImport(self):
		try:
			import iegen.ast
		except Exception,e:
			self.fail("'import iegen.ast' failed: "+str(e))

	#Test simple importing of iegen.ast classes
	def testNameImport(self):
		try:
			from iegen.ast import Node,PresSet,PresRelation,VarTuple,Conjunction,Constraint,Equality,Inequality,Expression,VarExp,FuncExp,NormExp
		except Exception,e:
			self.fail('Importing classes from iegen.ast failed: '+str(e))
#----------------------------------

#---------- PresSet Tests ----------
class SetTestCase(TestCase):

	#Tests that the PresSet constructor takes an optional symbolics argument for the collection of symbolics
	def testSetSymbolics(self):
		from iegen.ast import PresSet,Conjunction,VarTuple
		from iegen import Symbolic

		set=PresSet(VarTuple([]),Conjunction([]),[Symbolic('n')])
		set=PresSet(VarTuple([]),Conjunction([]),symbolics=[Symbolic('n')])

	#Tests that all objects in the symbolics collection must 'look like' Symbolics
	@raises(ValueError)
	def testNonSymbolicFail(self):
		from iegen import Symbolic
		from iegen.ast import PresSet,VarTuple,Conjunction
		from iegen.parser import PresParser

		PresSet(VarTuple([]),Conjunction([]),[Symbolic('n'),'m'])

	#Tests that all objects in the symbolics collection must 'look like' Symbolics
	def testLikeSymbolic(self):
		from iegen.ast import PresSet,VarTuple,Conjunction,Node

		class DummySymbolic(Node):
			def __init__(self,name):
				self.name=name
			def apply_visitor(self,visitor):
				visitor.visitSymbolic(self)

		PresSet(VarTuple([]),Conjunction([]),[DummySymbolic('n')])

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp
		from iegen.util import test_sets

		for set_str,set_exp in test_sets:
			exec('new_set_exp=repr('+set_exp+')')
			self.failUnless(set_exp==new_set_exp,'%s!=%s'%(set_exp,new_set_exp))

			exec('new_set_exp2=repr('+new_set_exp+')')
			self.failUnless(new_set_exp2==new_set_exp,'%s!=%s'%(new_set_exp2,new_set_exp))
			self.failUnless(new_set_exp2==set_exp,'%s!=%s'%(new_set_exp2,set_exp))

	#Tests the __str__ method
	def testStr(self):
		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,NormExp,VarExp

		set=PresSet(VarTuple([]),Conjunction([]))
		set_str='{[]}'
		self.failUnless(set_str==str(set),'%s!=%s'%(set_str,str(set)))

		set=PresSet(VarTuple([VarExp(1,'a')]),Conjunction([]))
		set_str='{[a]}'
		self.failUnless(set_str==str(set),'%s!=%s'%(set_str,str(set)))

		set=PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'b')]),Conjunction([]))
		set_str='{[a,b]}'
		self.failUnless(set_str==str(set),'%s!=%s'%(set_str,str(set)))

		set=PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')]),Conjunction([]))
		set_str='{[a,b,c]}'
		self.failUnless(set_str==str(set),'%s!=%s'%(set_str,str(set)))

		set=PresSet(VarTuple([]),Conjunction([Equality(NormExp([VarExp(-1,'a')],5))]))
		set_str='{[]: -1a+5=0}'
		self.failUnless(set_str==str(set),'%s!=%s'%(set_str,str(set)))

		set=PresSet(VarTuple([]),Conjunction([Equality(NormExp([VarExp(-1,'a')],5)),Equality(NormExp([VarExp(-1,'b')],5))]))
		set_str='{[]: -1a+5=0 and -1b+5=0}'
		self.failUnless(set_str==str(set),'%s!=%s'%(set_str,str(set)))

		set=PresSet(VarTuple([]),Conjunction([Equality(NormExp([VarExp(-1,'a')],5)),Equality(NormExp([VarExp(-1,'b')],5)),Equality(NormExp([VarExp(-1,'c')],5))]))
		set_str='{[]: -1a+5=0 and -1b+5=0 and -1c+5=0}'
		self.failUnless(set_str==str(set),'%s!=%s'%(set_str,str(set)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp
		from iegen.util import test_sets

		for set_str,set_exp in test_sets:
			exec('new_set_exp1='+set_exp)
			exec('new_set_exp2='+set_exp)
			self.failUnless(new_set_exp1==new_set_exp2,'%s!=%s'%(new_set_exp1,new_set_exp2))
			self.failIf(new_set_exp1>new_set_exp2,'%s>%s'%(new_set_exp1,new_set_exp2))
			self.failIf(new_set_exp1<new_set_exp2,'%s<%s'%(new_set_exp1,new_set_exp2))
			new_set_exp1.tuple_set.vars.append(VarExp(1,'asdfghjkl'))
			self.failIf(new_set_exp1==new_set_exp2,'%s==%s'%(new_set_exp1,new_set_exp2))
			self.failUnless(new_set_exp1>new_set_exp2,'%s<%s'%(new_set_exp1,new_set_exp2))
			self.failUnless(new_set_exp2<new_set_exp1,'%s>%s'%(new_set_exp2,new_set_exp1))

	#Tests that the __cmp__ method doesn't use 'isinstance'
	#but instead checks for properties of the object
	def testCmpNoIsInstance(self):
		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp,Node
		from iegen.util import test_sets

		class DummyPresSet(Node):
			def __init__(self,tuple_set,conjunct):
				self.tuple_set=tuple_set
				self.conjunct=conjunct
				self.symbolics=[]

		for set_str,set_exp in test_sets:
			exec('new_set_exp1='+set_exp)
			set_exp=set_exp.replace('PresSet','DummyPresSet')
			exec('new_set_exp2='+set_exp)
			self.failUnless(new_set_exp1==new_set_exp2,'%s!=%s'%(new_set_exp1,new_set_exp2))
			new_set_exp1.tuple_set.vars.append(VarExp(1,'asdfghjkl'))
			self.failIf(new_set_exp1==new_set_exp2,'%s==%s'%(new_set_exp1,new_set_exp2))

	#Tests for the arity method(s)
	def testArity(self):
		from iegen.ast import PresSet

		self.failUnless(hasattr(PresSet,'arity'),"PresSet has no 'arity' method.")
#-----------------------------------

#---------- PresRelation Tests ----------
class RelationTestCase(TestCase):

	#Tests that the PresRelation constructor takes an optional symbolics argument for the collection of symbolics
	def testRelationSymbolics(self):
		from iegen.ast import PresRelation,Conjunction,VarTuple
		from iegen import Symbolic

		set=PresRelation(VarTuple([]),VarTuple([]),Conjunction([]),[Symbolic('n')])
		set=PresRelation(VarTuple([]),VarTuple([]),Conjunction([]),symbolics=[Symbolic('n')])

	#Tests that all objects in the symbolics collection must 'look like' Symbolics
	@raises(ValueError)
	def testNonSymbolicFail(self):
		from iegen import Symbolic
		from iegen.ast import PresRelation,VarTuple,Conjunction

		PresRelation(VarTuple([]),VarTuple([]),Conjunction([]),[Symbolic('n'),'m'])

	#Tests that all objects in the symbolics collection must 'look like' Symbolics
	def testLikeSymbolic(self):
		from iegen.ast import PresRelation,VarTuple,Conjunction,Node

		class DummySymbolic(Node):
			def __init__(self,name):
				self.name=name
			def apply_visitor(self,visitor):
				visitor.visitSymbolic(self)

		PresRelation(VarTuple([]),VarTuple([]),Conjunction([]),[DummySymbolic('n')])

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import PresRelation,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp
		from iegen.util import test_relations

		for rel_str,rel_exp in test_relations:
			exec('new_rel_exp=repr('+rel_exp+')')
			self.failUnless(rel_exp==new_rel_exp,'%s!=%s'%(rel_exp,new_rel_exp))

			exec('new_rel_exp2=repr('+new_rel_exp+')')
			self.failUnless(new_rel_exp2==new_rel_exp,'%s!=%s'%(new_rel_exp2,new_rel_exp))
			self.failUnless(new_rel_exp2==rel_exp,'%s!=%s'%(new_rel_exp2,rel_exp))

	#Tests the __str__ method
	def testStr(self):
		from iegen.ast import PresRelation,VarTuple,Conjunction,Equality,NormExp,VarExp

		rel=PresRelation(VarTuple([]),VarTuple([]),Conjunction([]))
		rel_str='{[]->[]}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([]),Conjunction([]))
		rel_str='{[a]->[]}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([VarExp(1,'a'),VarExp(1,'b')]),VarTuple([]),Conjunction([]))
		rel_str='{[a,b]->[]}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')]),VarTuple([]),Conjunction([]))
		rel_str='{[a,b,c]->[]}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([]),VarTuple([]),Conjunction([]))
		rel_str='{[]->[]}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([]),VarTuple([VarExp(1,'a')]),Conjunction([]))
		rel_str='{[]->[a]}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([]),VarTuple([VarExp(1,'a'),VarExp(1,'b')]),Conjunction([]))
		rel_str='{[]->[a,b]}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([]),VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')]),Conjunction([]))
		rel_str='{[]->[a,b,c]}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([]),VarTuple([]),Conjunction([]))
		rel_str='{[]->[]}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([]),VarTuple([]),Conjunction([Equality(NormExp([VarExp(-1,'a')],5))]))
		rel_str='{[]->[]: -1a+5=0}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([]),VarTuple([]),Conjunction([Equality(NormExp([VarExp(-1,'a')],5)),Equality(NormExp([VarExp(-1,'b')],5))]))
		rel_str='{[]->[]: -1a+5=0 and -1b+5=0}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

		rel=PresRelation(VarTuple([]),VarTuple([]),Conjunction([Equality(NormExp([VarExp(-1,'a')],5)),Equality(NormExp([VarExp(-1,'b')],5)),Equality(NormExp([VarExp(-1,'c')],5))]))
		rel_str='{[]->[]: -1a+5=0 and -1b+5=0 and -1c+5=0}'
		self.failUnless(rel_str==str(rel),'%s!=%s'%(rel_str,str(rel)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import PresRelation,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp
		from iegen.util import test_relations

		for rel_str,rel_exp in test_relations:
			exec('new_rel_exp1='+rel_exp)
			exec('new_rel_exp2='+rel_exp)
			self.failUnless(new_rel_exp1==new_rel_exp2,'%s!=%s'%(new_rel_exp1,new_rel_exp2))
			self.failIf(new_rel_exp1>new_rel_exp2,'%s>%s'%(new_rel_exp1,new_rel_exp2))
			self.failIf(new_rel_exp1<new_rel_exp2,'%s<%s'%(new_rel_exp1,new_rel_exp2))
			new_rel_exp1.tuple_in.vars.append(VarExp(1,'asdfghjkl'))
			self.failIf(new_rel_exp1==new_rel_exp2,'%s==%s'%(new_rel_exp1,new_rel_exp2))
			self.failUnless(new_rel_exp1>new_rel_exp2,'%s<%s'%(new_rel_exp1,new_rel_exp2))
			self.failUnless(new_rel_exp2<new_rel_exp1,'%s>%s'%(new_rel_exp2,new_rel_exp1))

	#Tests that the __cmp__ method doesn't use 'isinstance'
	#but instead checks for properties of the object
	def testCmpNoIsInstance(self):
		from iegen.ast import PresRelation,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp,Node
		from iegen.util import test_relations

		class DummyPresRelation(Node):
			def __init__(self,tuple_in,tuple_out,conjunct):
				self.tuple_in=tuple_in
				self.tuple_out=tuple_out
				self.conjunct=conjunct
				self.symbolics=[]

		for rel_str,rel_exp in test_relations:
			exec('new_rel_exp1='+rel_exp)
			rel_exp=rel_exp.replace('PresRelation','DummyPresRelation')
			exec('new_rel_exp2='+rel_exp)
			self.failUnless(new_rel_exp1==new_rel_exp2,'%s!=%s'%(new_rel_exp1,new_rel_exp2))
			new_rel_exp1.tuple_in.vars.append(VarExp(1,'asdfghjkl'))
			self.failIf(new_rel_exp1==new_rel_exp2,'%s==%s'%(new_rel_exp1,new_rel_exp2))

	#Tests for the arity method(s)
	def testArity(self):
		from iegen.ast import PresRelation

		self.failUnless(hasattr(PresRelation,'arity_in'),"PresRelation has no 'arity_in' method.")
		self.failUnless(hasattr(PresRelation,'arity_out'),"PresRelation has no 'arity_out' method.")
		self.failUnless(hasattr(PresRelation,'arity'),"PresRelation has no 'arity' method.")
#----------------------------------------

#---------- VarTuple Tests ----------
class VarTupleTestCase(TestCase):

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import VarTuple,VarExp

		vs="VarTuple([VarExp(1,'a'), VarExp(1,'b'), VarExp(1,'c')])"
		exec('v='+vs)

		self.failUnless(vs==repr(v),'%s!=%s'%(vs,repr(v)))

	#Tests the __str__ method
	def testStr(self):
		from iegen.ast import VarTuple,VarExp

		v=VarTuple([])
		v_str='[]'
		self.failUnless(v_str==str(v),'%s!=%s'%(v_str,str(v)))

		v=VarTuple([VarExp(1,'a')])
		v_str='[a]'
		self.failUnless(v_str==str(v),'%s!=%s'%(v_str,str(v)))

		v=VarTuple([VarExp(1,'a'),VarExp(1,'b')])
		v_str='[a,b]'
		self.failUnless(v_str==str(v),'%s!=%s'%(v_str,str(v)))

		v=VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')])
		v_str='[a,b,c]'
		self.failUnless(v_str==str(v),'%s!=%s'%(v_str,str(v)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import VarTuple,VarExp

		vs1="VarTuple([VarExp(1,'a'), VarExp(1,'b'), VarExp(1,'c'), VarExp(1,'d')])"
		vs2="VarTuple([VarExp(1,'a'), VarExp(1,'b'), VarExp(1,'c'), VarExp(1,'e')])"
		exec('v1a='+vs1)
		exec('v1b='+vs1)
		exec('v2='+vs2)

		self.failUnless(vs1==repr(v1a),'%s!=%s'%(vs1,repr(v1a)))
		self.failUnless(vs1==repr(v1b),'%s!=%s'%(vs1,repr(v1b)))
		self.failUnless(vs2==repr(v2),'%s!=%s'%(vs2,repr(v2)))

		self.failUnless(v1a==v1b,'%s!=%s'%(v1a,v1b))
		self.failIf(v1a<v1b,'%s<%s'%(v1a,v1b))
		self.failIf(v1a>v1b,'%s>%s'%(v1a,v1b))
		self.failIf(v1a==v2,'%s==%s'%(v1a,v2))
		self.failUnless(v1a<v2,'%s>%s'%(v1a,v2))
		self.failUnless(v2>v1a,'%s<%s'%(v2,v1a))

	#Tests that the __cmp__ method doesn't use 'isinstance'
	#but instead checks for properties of the object
	def testCmpNoIsInstance(self):
		from iegen.ast import VarTuple,VarExp,Node
		from iegen.util import test_relations

		class DummyVarTuple(Node):
			def __init__(self,vars):
				self.vars=vars

		vs="VarTuple([VarExp(1,'a'), VarExp(1,'b')])"
		dvs="DummyVarTuple([VarExp(1,'a'), VarExp(1,'b')])"
		exec('v='+vs)
		exec('dv='+dvs)

		self.failUnless(v==dv,'%s!=%s'%(v,dv))
		v.vars.append('c')
		self.failIf(v==dv,'%s==%s'%(v,dv))

	#Validate VarTuple's __len__ method
	def testLen(self):
		from iegen.ast import VarTuple,VarExp

		v0=VarTuple([])
		v1=VarTuple([VarExp(1,'a')])
		v2=VarTuple([VarExp(1,'a'),VarExp(1,'b')])
		v3=VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')])

		self.failUnless(0==len(v0),'len(%s)!=0'%v1)
		self.failUnless(1==len(v1),'len(%s)!=1'%v1)
		self.failUnless(2==len(v2),'len(%s)!=2'%v2)
		self.failUnless(3==len(v3),'len(%s)!=3'%v3)

	#Tests that an object does not 'look like' a VarExp is invalid
	@raises(ValueError)
	def testNormExpInvalid(self):
		from iegen.ast import VarTuple,NormExp
		VarTuple([NormExp([],0)])
	@raises(ValueError)
	def testFuncExpInvalid(self):
		from iegen.ast import VarTuple,FuncExp
		VarTuple([FuncExp(1,'f',[])])
	@raises(ValueError)
	def testIntInvalid(self):
		from iegen.ast import VarTuple
		VarTuple([10])
	@raises(ValueError)
	def testStrInvalid(self):
		from iegen.ast import VarTuple
		VarTuple(['hello'])

	#Tests that only VarExps with coefficient 1 are allowed in a VarTuple
	@raises(ValueError)
	def testCoeffNotOneFail(self):
		from iegen.ast import VarTuple,VarExp

		VarTuple([VarExp(2,'a')])
#------------------------------------

#---------- Conjunction Tests ----------
class ConjunctionTestCase(TestCase):

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import Conjunction,Inequality,VarExp,NormExp

		cs="Conjunction([Inequality(NormExp([VarExp(2,'c')],0))])"
		exec('c='+cs)

		self.failUnless(cs==repr(c),'%s!=%s'%(cs,repr(c)))

	#Tests the __str__ method
	def testStr(self):
		from iegen.ast import Conjunction,Equality,NormExp,VarExp

		c=Conjunction([])
		c_str=''
		self.failUnless(c_str==str(c),'%s!=%s'%(c_str,str(c)))

		c=Conjunction([Equality(NormExp([VarExp(-1,'a')],5))])
		c_str='-1a+5=0'
		self.failUnless(c_str==str(c),'%s!=%s'%(c_str,str(c)))

		c=Conjunction([Equality(NormExp([VarExp(-1,'a')],5)),Equality(NormExp([VarExp(-1,'b')],5))])
		c_str='-1a+5=0 and -1b+5=0'
		self.failUnless(c_str==str(c),'%s!=%s'%(c_str,str(c)))

		c=Conjunction([Equality(NormExp([VarExp(-1,'a')],5)),Equality(NormExp([VarExp(-1,'b')],5)),Equality(NormExp([VarExp(-1,'c')],5))])
		c_str='-1a+5=0 and -1b+5=0 and -1c+5=0'
		self.failUnless(c_str==str(c),'%s!=%s'%(c_str,str(c)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import Conjunction,Equality,NormExp,VarExp

		cs1="Conjunction([Equality(NormExp([VarExp(5,'a')],5))])"
		cs2="Conjunction([Equality(NormExp([VarExp(5,'b')],5))])"
		exec('c1a='+cs1)
		exec('c1b='+cs1)
		exec('c2='+cs2)

		self.failUnless(cs1==repr(c1a),'%s!=%s'%(cs1,repr(c1a)))
		self.failUnless(cs1==repr(c1b),'%s!=%s'%(cs1,repr(c1b)))
		self.failUnless(cs2==repr(c2),'%s!=%s'%(cs2,repr(c2)))

		self.failUnless(c1a==c1b,'%s!=%s'%(c1a,c1b))
		self.failIf(c1a<c1b,'%s<%s'%(c1a,c1b))
		self.failIf(c1a>c1b,'%s>%s'%(c1a,c1b))
		self.failIf(c1a==c2,'%s==%s'%(c1a,c2))
		self.failUnless(c1a<c2,'%s>%s'%(c1a,c2))
		self.failUnless(c2>c1a,'%s<%s'%(c2,c1a))

	#Tests that the __cmp__ method doesn't use 'isinstance'
	#but instead checks for properties of the object
	def testCmpNoIsInstance(self):
		from iegen.ast import Conjunction,Equality,NormExp,VarExp,Node

		class DummyConjunction(Node):
			def __init__(self,constraint_list):
				self.constraint_list=constraint_list

		cs="Conjunction([Equality(NormExp([VarExp(-5,'a')],-5))])"
		dcs="DummyConjunction([Equality(NormExp([VarExp(-5,'a')],-5))])"
		exec('c='+cs)
		exec('dc='+dcs)

		self.failUnless(c==dc,'%s!=%s'%(c,dc))
		c.constraint_list.append(VarExp(1,'b'))
		self.failIf(c==dc,'%s==%s'%(c,dc))

	#Validate Conjunction's __len__ method
	def testLen(self):
		from iegen.ast import Conjunction,Equality,NormExp,VarExp

		c0=Conjunction([])
		c1=Conjunction([Equality(NormExp([VarExp(1,'a')],0))])
		c2=Conjunction([Equality(NormExp([VarExp(1,'a')],0)),Equality(NormExp([VarExp(1,'a')],0))])
		c3=Conjunction([Equality(NormExp([VarExp(1,'a')],0)),Equality(NormExp([VarExp(1,'a')],0)),Equality(NormExp([VarExp(1,'a')],0))])

		self.failUnless(0==len(c0),'len(%s)!=0'%c0)
		self.failUnless(1==len(c1),'len(%s)!=1'%c1)
		self.failUnless(2==len(c2),'len(%s)!=2'%c2)
		self.failUnless(3==len(c3),'len(%s)!=3'%c3)

#---------------------------------------

#---------- Equality Tests ----------
class EqualityTestCase(TestCase):

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import Equality,NormExp,FuncExp,VarExp

		es1="Equality(NormExp([VarExp(1,'a')],1))"
		exec('e1='+es1)

		self.failUnless(es1==repr(e1),'%s!=%s'%(es1,repr(e1)))

	#Tests the __str__ method
	def testStr(self):
		from iegen.ast import Equality,NormExp,VarExp

		e=Equality(NormExp([],0))
		e_str='0=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=Equality(NormExp([],5))
		e_str='5=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=Equality(NormExp([VarExp(1,'a')],0))
		e_str='a=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=Equality(NormExp([VarExp(1,'a'),VarExp(1,'b')],0))
		e_str='a+b=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=Equality(NormExp([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')],0))
		e_str='a+b+c=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=Equality(NormExp([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')],5))
		e_str='a+b+c+5=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import Equality,NormExp,VarExp

		es1="Equality(NormExp([VarExp(9,'f')],9))"
		es2="Equality(NormExp([VarExp(9,'g')],9))"
		exec('e1a='+es1)
		exec('e1b='+es1)
		exec('e2='+es2)

		self.failUnless(es1==repr(e1a),'%s!=%s'%(es1,repr(e1a)))
		self.failUnless(es1==repr(e1b),'%s!=%s'%(es1,repr(e1b)))
		self.failUnless(es2==repr(e2),'%s!=%s'%(es2,repr(e2)))

		self.failUnless(e1a==e1b,'%s!=%s'%(e1a,e1b))
		self.failIf(e1a<e1b,'%s<%s'%(e1a,e1b))
		self.failIf(e1a>e1b,'%s>%s'%(e1a,e1b))
		self.failIf(e1a==e2,'%s==%s'%(e1a,e2))
		self.failUnless(e1a<e2,'%s>%s'%(e1a,e2))
		self.failUnless(e2>e1a,'%s<%s'%(e2,e1a))

	#Tests that the __cmp__ method doesn't use 'isinstance'
	#but instead checks for properties of the object
	def testCmpNoIsInstance(self):
		from iegen.ast import Equality,NormExp,VarExp,Node

		class DummyEquality(Node):
			def __init__(self,exp,equality):
				self.exp=exp
				self._equality=equality

		es="Equality(NormExp([VarExp(5,'a')],5))"
		des="DummyEquality(NormExp([VarExp(5,'a')],5),True)"
		exec('e='+es)
		exec('de='+des)

		self.failUnless(e==de,'%s!=%s'%(e,de))
		e.exp.terms.append(VarExp(1,'b'))
		self.failIf(e==de,'%s==%s'%(e,de))

	#Tests that Equalities are 'greater' than Inequalities
	def testGreaterThanInequality(self):
		from iegen.ast import Equality,Inequality,VarExp,NormExp

		e=Equality(NormExp([VarExp(1,'a')],0))
		i=Inequality(NormExp([VarExp(1,'a')],0))

		self.failUnless(e>i,'%s<=%s'%(e,i))
		self.failUnless(i<e,'%s>=%s'%(i,e))

	#Tests that a=b and b=a are considered equal
	def testEqualityReflexive(self):
		from iegen.ast import Equality,VarExp,NormExp

		e1=Equality(NormExp([VarExp(1,'a')],-10))
		e2=Equality(NormExp([VarExp(-1,'a')],10))

		self.failUnless(e1==e2,'%s!=%s'%(e1,e2))

		e1=Equality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],-10))
		e2=Equality(NormExp([VarExp(-1,'a'),VarExp(1,'b')],10))

		self.failUnless(e1==e2,'%s!=%s'%(e1,e2))

	#Tests that Equality uses the 'larger' expression of exp vs. -exp
	def testEqualityGreaterExp(self):
		from iegen.ast import Equality,VarExp,FuncExp,NormExp

		l1=[Equality(NormExp([VarExp(1,'b')],-10)),Equality(NormExp([VarExp(-1,'a')],10))]
		l2=[Equality(NormExp([VarExp(-1,'b')],10)),Equality(NormExp([VarExp(-1,'a')],10))]

		l1.sort()
		l2.sort()

		self.failUnless(l1==l2,'%s!=%s'%(l1,l2))

		l1=[Equality(NormExp([FuncExp(1,'f',[NormExp([VarExp(1,'b')],0)])],-10)),Equality(NormExp([FuncExp(-1,'f',[NormExp([VarExp(1,'a')],0)])],10))]
		l2=[Equality(NormExp([FuncExp(-1,'f',[NormExp([VarExp(1,'b')],0)])],10)),Equality(NormExp([FuncExp(-1,'f',[NormExp([VarExp(1,'a')],0)])],10))]

		l1.sort()
		l2.sort()

		self.failUnless(l1==l2,'%s!=%s'%(l1,l2))

	#Tests that the Equality.empty() method works
	def testEmpty(self):
		from iegen.ast import Equality,NormExp,VarExp

		i=Equality(NormExp([],0))
		self.failUnless(i.empty(),'%s is not empty.'%i)

		i=Equality(NormExp([VarExp(1,'a')],0))
		self.failIf(i.empty(),'%s is empty'%i)
#------------------------------------

#---------- Inequality Tests ----------
class InequalityTestCase(TestCase):

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import Inequality,NormExp,FuncExp,VarExp

		is1="Inequality(NormExp([FuncExp(1,'f',[NormExp([VarExp(1,'b')],0)])],1))"
		exec('i1='+is1)

		self.failUnless(is1==repr(i1),'%s!=%s'%(is1,repr(i1)))

	#Tests the __str__ method
	def testStr(self):
		from iegen.ast import Inequality,NormExp,VarExp

		e=Inequality(NormExp([],0))
		e_str='0>=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=Inequality(NormExp([],5))
		e_str='5>=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=Inequality(NormExp([VarExp(1,'a')],0))
		e_str='a>=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=Inequality(NormExp([VarExp(1,'a'),VarExp(1,'b')],0))
		e_str='a+b>=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=Inequality(NormExp([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')],0))
		e_str='a+b+c>=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=Inequality(NormExp([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')],5))
		e_str='a+b+c+5>=0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import Inequality,NormExp,VarExp

		is1="Inequality(NormExp([VarExp(-9,'f')],-9))"
		is2="Inequality(NormExp([VarExp(-9,'g')],-9))"
		exec('i1a='+is1)
		exec('i1b='+is1)
		exec('i2='+is2)

		self.failUnless(is1==repr(i1a),'%s!=%s'%(is1,repr(i1a)))
		self.failUnless(is1==repr(i1b),'%s!=%s'%(is1,repr(i1b)))
		self.failUnless(is2==repr(i2),'%s!=%s'%(is2,repr(i2)))

		self.failUnless(i1a==i1b,'%s!=%s'%(i1a,i1b))
		self.failIf(i1a<i1b,'%s<%s'%(i1a,i1b))
		self.failIf(i1a>i1b,'%s>%s'%(i1a,i1b))
		self.failIf(i1a==i2,'%s==%s'%(i1a,i2))
		self.failUnless(i1a<i2,'%s>%s'%(i1a,i2))
		self.failUnless(i2>i1a,'%s<%s'%(i2,i1a))

	#Tests that the __cmp__ method doesn't use 'isinstance'
	#but instead checks for properties of the object
	def testCmpNoIsInstance(self):
		from iegen.ast import Inequality,NormExp,VarExp,Node

		class DummyInequality(Node):
			def __init__(self,exp,equality):
				self.exp=exp
				self._equality=equality

		iss="Inequality(NormExp([VarExp(-5,'a')],-5))"
		dis="DummyInequality(NormExp([VarExp(-5,'a')],-5),False)"
		exec('i='+iss)
		exec('di='+dis)

		self.failUnless(i==di,'%s!=%s'%(i,di))
		i.exp.terms.append(VarExp(1,'b'))
		self.failIf(i==di,'%s==%s'%(i,di))

	#Tests that Inequalities are 'less' than Equalities
	def testLessThanEquality(self):
		from iegen.ast import Inequality,Equality,VarExp,NormExp

		i=Inequality(NormExp([VarExp(1,'a')],0))
		e=Equality(NormExp([VarExp(1,'a')],0))

		self.failUnless(i<e)
		self.failUnless(e>i)

	#Tests that the Inequality.empty() method works
	def testEmpty(self):
		from iegen.ast import Inequality,NormExp,VarExp

		i=Inequality(NormExp([],0))
		self.failUnless(i.empty(),'%s is not empty.'%i)

		i=Inequality(NormExp([VarExp(1,'a')],0))
		self.failIf(i.empty(),'%s is empty'%i)
#--------------------------------------

#---------- VarExp Tests ----------
class VarExpTestCase(TestCase):

	var_exps=(
	          "VarExp(0,'')",
	          "VarExp(1,'a')",
	          "VarExp(-10,'b')",
	          "VarExp(-5,'c')",
	          "VarExp(100,'abc')",
	          "VarExp(42,'x')")

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import VarExp

		for var_exp in self.var_exps:
			exec('v='+var_exp)

			#Test VarExp's repr function
			self.failUnless(repr(v)==var_exp,'%s!=%s'%(repr(v),var_exp))

	#Tests the __str__ method
	def testStr(self):
		from iegen.ast import VarExp

		e=VarExp(0,'a')
		e_str='0a'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=VarExp(1,'a')
		e_str='a'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=VarExp(2,'a')
		e_str='2a'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=VarExp(5,'a')
		e_str='5a'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=VarExp(-5,'a')
		e_str='-5a'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import VarExp

		for var_exp in self.var_exps:
			exec('v='+var_exp)

			#Test VarExp's comparison operator
			self.failUnless(v==v,'%s!=%s'%(v,v))
			self.failIf(v!=v,'%s!=%s'%(v,v))

			for var_exp2 in [v2 for v2 in self.var_exps if v2!=var_exp]:
				exec('v2='+var_exp2)
				self.failUnless(v2!=v,'%s==%s'%(v2,v))
				self.failIf(v2==v,'%s==%s'%(v2,v))

				greater=((v2.coeff,v2.id)>(v.coeff,v.id))
				if greater:
					self.failUnless(v2>v,'%s<%s'%(v2,v))
				else:
					self.failUnless(v2<v,'%s>%s'%(v2,v))

	#Tests that using something other than a string for the name fails
	@raises(ValueError)
	def testNonStringNameFail1(self):
		from iegen.ast import VarExp

		VarExp(1,10)
	@raises(ValueError)
	def testNonStringNameFail2(self):
		from iegen.ast import VarExp

		VarExp(1,['a'])

	#Tests that using something other than an integer for the coefficient fails
	@raises(ValueError)
	def testNonIntCoeffFail1(self):
		from iegen.ast import VarExp

		VarExp('a','a')
	@raises(ValueError)
	def testNonIntCoeffFail2(self):
		from iegen.ast import VarExp

		VarExp([1],'a')

	#Tests the __mul__ method
	def testMul(self):
		from iegen.ast import VarExp

		for var_exp in self.var_exps:
			exec('v='+var_exp)

			#Test VarExp's multiplication operator
			coeff=v.coeff
			id=v.id

			#Test multiplication from -5 to 9
			for i in xrange(-5,10):
				v_i=v*i
				i_v=i*v
				i_coeff=i*coeff
				new_v=VarExp(i_coeff,id)

				#Make sure multiplication returns a new object
				self.failIf(v is v_i,'%s is %s'%(v,v_i))
				self.failIf(v is i_v,'%s is %s'%(v,i_v))

				#Make sure multiplication works correctly
				self.failUnless(v_i==new_v,'%s!=%s'%(v_i,new_v))
				self.failUnless(i_v==new_v,'%s!=%s'%(i_v,new_v))
#----------------------------------

#---------- FuncExp Tests ----------
class FuncExpTestCase(TestCase):
	func_exps=(
	          "FuncExp(0,'',[])",
	          "FuncExp(1,'f',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(1,'f',[NormExp([VarExp(1,'a'), VarExp(1,'b')],0)])",
	          "FuncExp(1,'f',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(1,'g',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(1,'f',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(2,'f',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(2,'g',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(3,'fog',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(4,'rain',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(42,'test',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(-81,'z',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(101,'x',[NormExp([VarExp(1,'a')],0)])",
	          "FuncExp(16,'wxyz',[NormExp([VarExp(1,'a'), VarExp(2,'b')],0)])",
	          "FuncExp(16,\"f'\",[NormExp([VarExp(1,'a'), VarExp(2,'b')],0)])",
	          "FuncExp(16,\"f'\",[NormExp([FuncExp(2,\"g'\",[NormExp([VarExp(1,'a')],0)])],0)])")

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import VarExp,FuncExp,NormExp

		for func_exp in self.func_exps:
			exec('f='+func_exp)

			#Test FuncExp's repr function
			self.failUnless(repr(f)==func_exp,'%s!=%s'%(repr(f),func_exp))

	#Tests the __str__ method
	def testStr(self):
		from iegen.ast import FuncExp,VarExp,NormExp

		e=FuncExp(0,'f',[])
		e_str='0f()'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=FuncExp(1,'f',[])
		e_str='f()'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=FuncExp(2,'f',[])
		e_str='2f()'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=FuncExp(5,'f',[])
		e_str='5f()'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=FuncExp(-5,'f',[])
		e_str='-5f()'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=FuncExp(1,'f',[NormExp([VarExp(1,'a')],0)])
		e_str='f(a)'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=FuncExp(1,'f',[NormExp([VarExp(1,'a')],0),NormExp([VarExp(1,'b')],0)])
		e_str='f(a,b)'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=FuncExp(1,'f',[NormExp([VarExp(1,'a')],0),NormExp([VarExp(1,'b')],0),NormExp([VarExp(1,'c')],0)])
		e_str='f(a,b,c)'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import FuncExp,VarExp,NormExp

		for func_exp in self.func_exps:
			exec('f='+func_exp)

			#Test FuncExp's comparison operator
			self.failUnless(f==f,'%s!=%s'%(f,f))
			self.failIf(f!=f,'%s!=%s'%(f,f))

			for func_exp2 in [f2 for f2 in self.func_exps if f2!=func_exp]:
				exec('f2='+func_exp2)
				self.failUnless(f2!=f,'%s==%s'%(f2,f))
				self.failIf(f2==f,'%s==%s'%(f2,f))

				greater=((f2.coeff,f2.name,f2.args)>(f.coeff,f.name,f.args))
				if greater:
					self.failUnless(f2>f,'%s<%s'%(f2,f))
				else:
					self.failUnless(f2<f,'%s>%s'%(f2,f))

	#Tests that using something other than a string for the name fails
	@raises(ValueError)
	def testNonStringNameFail1(self):
		from iegen.ast import FuncExp

		FuncExp(1,10,[])
	@raises(ValueError)
	def testNonStringNameFail2(self):
		from iegen.ast import FuncExp

		FuncExp(1,['a'],[])

	#Tests that using something other than an integer for the coefficient fails
	@raises(ValueError)
	def testNonIntCoeffFail1(self):
		from iegen.ast import FuncExp

		FuncExp('a','a',[])
	@raises(ValueError)
	def testNonIntCoeffFail2(self):
		from iegen.ast import FuncExp

		FuncExp([1],'a',[])

	#Tests the __mul__ method
	def testMul(self):
		from iegen.ast import FuncExp,VarExp,NormExp

		for func_exp in self.func_exps:
			exec('f='+func_exp)

			#Test FuncExp's multiplication operator
			coeff=f.coeff
			name=f.name
			exps=f.args

			#Test multiplication from -5 to 9
			for i in xrange(-5,10):
				f_i=f*i
				i_f=i*f
				i_coeff=i*coeff
				new_f=FuncExp(i_coeff,name,exps)

				#Make sure multiplication returns a new object
				self.failIf(f is f_i,'%s is %s'%(f,f_i))
				self.failIf(f is i_f,'%s is %s'%(f,i_f))

				#Make sure multiplication works correctly
				self.failUnless(f_i==new_f,'%s!=%s'%(f_i,new_f))
				self.failUnless(i_f==new_f,'%s!=%s'%(i_f,new_f))
#-----------------------------------

#---------- FuncExp Tests ----------
class NormExpTestCase(TestCase):

	norm_exps=(
	          "NormExp([],0)",
	          "NormExp([],1)",
	          "NormExp([VarExp(1,'a')],5)",
	          "NormExp([VarExp(1,'a')],1)",
	          "NormExp([VarExp(1,'a'), FuncExp(2,'f',[NormExp([VarExp(1,'b')],0)])],5)",
	          "NormExp([VarExp(1,'a'), FuncExp(2,'f',[NormExp([VarExp(1,'b')],0)])],5)",
	          "NormExp([VarExp(1,'b')],5)",
	          "NormExp([VarExp(1,'a')],6)")

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import NormExp,FuncExp,VarExp

		for norm_exp in self.norm_exps:
			exec('n='+norm_exp)

			#Test NormExp's repr function
			self.failUnless(repr(n)==norm_exp,'%s!=%s'%(repr(n),norm_exp))

	#Tests the __str__ method
	def testStr(self):
		from iegen.ast import FuncExp,VarExp,NormExp

		e=NormExp([],0)
		e_str='0'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=NormExp([],1)
		e_str='1'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=NormExp([],-1)
		e_str='-1'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=NormExp([VarExp(1,'a')],0)
		e_str='a'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=NormExp([VarExp(1,'a'),VarExp(1,'b')],0)
		e_str='a+b'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=NormExp([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')],0)
		e_str='a+b+c'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

		e=NormExp([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c')],5)
		e_str='a+b+c+5'
		self.failUnless(e_str==str(e),'%s!=%s'%(e_str,str(e)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import NormExp,FuncExp,VarExp

		for norm_exp in self.norm_exps:
			exec('n='+norm_exp)

			#Test NormExp's comparison operator
			self.failUnless(n==n,'%s!=%s'%(n,n))
			self.failIf(n!=n,'%s!=%s'%(n,n))

			for norm_exp2 in [n2 for n2 in self.norm_exps if n2!=norm_exp]:
				exec('n2='+norm_exp2)
				self.failUnless(n2!=n,'%s==%s'%(n2,n))
				self.failIf(n2==n,'%s==%s'%(n2,n))

				greater=((n2.const,n2.terms)>(n.const,n.terms))
				if greater:
					self.failUnless(n2>n,'%s<%s'%(n2,n))
				else:
					self.failUnless(n2<n,'%s>%s'%(n2,n))

	#Tests that using something other than an integer for the constant fails
	@raises(ValueError)
	def testNonIntConstFail1(self):
		from iegen.ast import NormExp

		NormExp([],'a')
	@raises(ValueError)
	def testNonIntConstFail2(self):
		from iegen.ast import NormExp

		NormExp([],['a'])

	#Tests that objects that 'look like' VarExps are valid terms for a NormExp
	def testVarExpValid(self):
		from iegen.ast import NormExp,Node
		class DummyVarExp(Node):
			def __init__(self):
				self.coeff=0
				self.id=''
			def apply_visitor(self,visitor):
				visitor.visitVarExp(self)

		NormExp([DummyVarExp()],0)

	#Tests that objects that 'look like' FuncExps are valid terms for a NormExp
	def testFuncExpValid(self):
		from iegen.ast import NormExp,Node
		class DummyFuncExp(Node):
			def __init__(self):
				self.coeff=0
				self.name=''
				self.args=[]
			def apply_visitor(self,visitor):
				visitor.visitFuncExp(self)
		NormExp([DummyFuncExp()],0)

	#Tests that an object that 'looks like' neither a VarExp nor a FuncExp is not a valid term for a NormExp
	@raises(ValueError)
	def testNormExpInvalid(self):
		from iegen.ast import NormExp
		NormExp([NormExp([],0)],0)
	@raises(ValueError)
	def testIntInvalid(self):
		from iegen.ast import NormExp
		NormExp([10],0)
	@raises(ValueError)
	def testStrInvalid(self):
		from iegen.ast import NormExp
		NormExp(['hello'],0)

	#Tests the empty method
	def testEmpty(self):
		from iegen.ast import NormExp,VarExp,FuncExp

		e=NormExp([],0)
		self.failUnless(e.empty(),'%s is not empty'%e)

		e=NormExp([VarExp(1,'a')],0)
		self.failIf(e.empty(),'%s is empty'%e)

		e=NormExp([FuncExp(1,'f',[])],0)
		self.failIf(e.empty(),'%s is empty'%e)

		e=NormExp([],1)
		self.failIf(e.empty(),'%s is empty'%e)

	#Tests the __mul__ method
	def testMul(self):
		from iegen.ast import NormExp,FuncExp,VarExp

		for norm_exp in self.norm_exps:
			exec('n='+norm_exp)

			#Test NormExp's multiplication operator
			const=n.const
			terms=n.terms

			#Test multiplication from -5 to 9
			for i in xrange(-5,10):
				ni=NormExp([],i)
				n_i=n*ni
				i_n=ni*n

				#Calculate what we should have
				new_const=const*i
				new_terms=[i*term for term in terms]
				new_n=NormExp(new_terms,new_const)

				#Make sure multiplication returns a new object
				self.failIf(n is n_i,'%s is %s'%(n,n_i))
				self.failIf(n is i_n,'%s is %s'%(n,i_n))

				#Make sure multiplication works correctly
				self.failUnless(n_i==new_n,'%s!=%s'%(n_i,new_n))
				self.failUnless(i_n==new_n,'%s!=%s'%(i_n,new_n))

	#Tests adding constants using the __add__ method
	def testAddConst(self):
		from iegen.ast import NormExp,FuncExp,VarExp

		for norm_exp in self.norm_exps:
			exec('n='+norm_exp)

			#Test NormExp's addition operator
			const=n.const
			terms=n.terms

			#Test adding constants from -5 to 9
			for i in xrange(-5,10):
				ni=NormExp([],i)
				n_i=n+ni
				i_n=ni+n

				#Calculate what we should have
				new_const=const+i
				new_terms=[1*term for term in terms]
				new_n=NormExp(new_terms,new_const)

				#Make sure addition returns a new object
				self.failIf(n is n_i,'%s is %s'%(n,n_i))
				self.failIf(n is i_n,'%s is %s'%(n,i_n))

				#Make sure addition works correctly
				self.failUnless(n_i==new_n,'%s!=%s'%(n_i,new_n))
				self.failUnless(i_n==new_n,'%s!=%s'%(i_n,new_n))

	#Tests adding constants and terms using the __add__ method
	def testAddTermConst(self):
		from iegen.ast import NormExp,FuncExp,VarExp

		for norm_exp in self.norm_exps:
			exec('n='+norm_exp)

			#Test adding terms and constants
			for norm_exp2 in [n2 for n2 in self.norm_exps if n2!=norm_exp]:
				exec('n2='+norm_exp2)
				n_n2=n+n2
				n2_n=n2+n

				const=n.const
				terms=n.terms
				const2=n2.const
				terms2=n2.terms

				#Calculate what we should have
				new_const=const+const2
				new_terms=[1*term for term in terms]
				for term in terms2:
					if term in new_terms:
						index=terms.index(term)
						new_terms[index].coeff+=term.coeff
					else:
						new_terms.append(term)
				new_terms.sort()
				new_n=NormExp(new_terms,new_const)

				#Make sure addition returns a new object
				self.failIf(n is n_n2,'%s is %s'%(n,n_n2))
				self.failIf(n is n2_n,'%s is %s'%(n,n_n2))

				#Make sure addition works correctly
				self.failUnless(n_n2==new_n,'%s!=%s'%(n_n2,new_n))
				self.failUnless(n2_n==new_n,'%s!=%s'%(n2_n,new_n))

	#Tests the __add__ method by adding a single variable
	def testAddVar(self):
		from iegen.ast import NormExp,VarExp,FuncExp

		n=NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)
		n=n+NormExp([VarExp(4,'a')],0)

		n_res=NormExp([VarExp(8,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)

		self.failUnless(n_res==n,'%s!=%s'%(n_res,n))

	#Tests the __add__ method by adding a single function
	def testAddFunc(self):
		from iegen.ast import NormExp,VarExp,FuncExp

		n=NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)
		n=n+NormExp([FuncExp(2,'f',[NormExp([VarExp(1,'y')],0)])],0)

		n_res=NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)]),FuncExp(2,'f',[NormExp([VarExp(1,'y')],0)])],2)

		self.failUnless(n_res==n,'%s!=%s'%(n_res,n))

	#Tests the __add__ method by adding a variable and a function
	def testAddVarFunc(self):
		from iegen.ast import NormExp,VarExp,FuncExp

		n=NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)
		n=n+NormExp([VarExp(4,'a'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],0)

		n_res=NormExp([VarExp(8,'a'),VarExp(6,'b'),FuncExp(4,'f',[NormExp([VarExp(1,'x')],0)])],2)

		self.failUnless(n_res==n,'%s!=%s'%(n_res,n))

	#Tests the __sub__ method by subtracting a single variable
	def testSubVar(self):
		from iegen.ast import NormExp,VarExp,FuncExp

		n=NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)
		n=n-NormExp([VarExp(4,'a')],0)

		n_res=NormExp([VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)

		self.failUnless(n_res==n,'%s!=%s'%(n_res,n))

	#Tests the __sub__ method by subtracting multiple variables
	def testSubMultipleVars(self):
		from iegen.ast import NormExp,VarExp,FuncExp

		n=NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)
		n=n-NormExp([VarExp(4,'a'),VarExp(6,'b')],0)

		n_res=NormExp([FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)

		self.failUnless(n_res==n,'%s!=%s'%(n_res,n))

	#Tests the __sub__ method by subtracting a function
	def testSubFunc1(self):
		from iegen.ast import NormExp,VarExp,FuncExp

		n=NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)
		n=n-NormExp([FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],0)

		n_res=NormExp([VarExp(4,'a'),VarExp(6,'b')],2)

		self.failUnless(n_res==n,'%s!=%s'%(n_res,n))

	#Tests the __sub__ method by subtracting a function
	def testSubFunc2(self):
		from iegen.ast import NormExp,VarExp,FuncExp

		n=NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)
		n=n-NormExp([FuncExp(2,'f',[NormExp([VarExp(1,'y')],0)])],0)

		n_res=NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)]),FuncExp(-2,'f',[NormExp([VarExp(1,'y')],0)])],2)
		self.failUnless(n_res==n,'%s!=%s'%(n_res,n))

	#Tests the __sub__ method by subtracting all terms from the expression
	def testSubAll(self):
		from iegen.ast import NormExp,VarExp,FuncExp

		n=NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)
		n=n-NormExp([VarExp(4,'a'),VarExp(6,'b'),FuncExp(2,'f',[NormExp([VarExp(1,'x')],0)])],2)

		n_res=NormExp([],0)

		self.failUnless(n_res==n,'%s!=%s'%(n_res,n))

	#Tests the __cmp__ by making sure the NormExp terms are sorted properly
	def testSort(self):
		from iegen.ast import NormExp,FuncExp,VarExp

		n1=NormExp([VarExp(1,'a'),
		            VarExp(2,'a'),
		            VarExp(2,'b'),
		            VarExp(2,'c'),
		            VarExp(3,'c'),
		            FuncExp(1,'f',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(2,'f',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(3,'g',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(3,'h',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(4,'i',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(4,'i',[NormExp([VarExp(2,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(5,'j',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(5,'j',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(2,'f',[])],0)])],
		            6)

		n2=NormExp([FuncExp(1,'f',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(3,'g',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(2,'f',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            VarExp(2,'b'),
		            FuncExp(3,'h',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(5,'j',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(2,'f',[])],0)]),
		            VarExp(2,'c'),
		            FuncExp(4,'i',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            FuncExp(4,'i',[NormExp([VarExp(2,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            VarExp(3,'c'),
		            FuncExp(5,'j',[NormExp([VarExp(1,'a')],0),NormExp([FuncExp(1,'f',[])],0)]),
		            VarExp(2,'a'),
		            VarExp(1,'a')],
		            6)

		self.failUnless(n1==n2,'%s!=%s'%(n1,n2))
#-----------------------------------
