from unittest import TestCase

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
			from iegen.ast import Node,PresSet,PresSetUnion,PresRelation,PresRelationUnion,VarTuple,Conjunction,Constraint,Equality,Inequality,Expression,VarExp,FuncExp,NormExp
		except Exception,e:
			self.fail('Importing classes from iegen.ast failed: '+str(e))
#----------------------------------

#---------- PresSet Tests ----------
class SetTestCase(TestCase):

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp
		from iegen.util import test_sets

		for set_str,set_exp in test_sets:
			exec('new_set_exp=repr('+set_exp+')')
			self.failUnless(set_exp==new_set_exp,'%s!=%s'%(set_exp,new_set_exp))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp
		from iegen.util import test_sets

		for set_str,set_exp in test_sets:
			exec('new_set_exp1='+set_exp)
			exec('new_set_exp2='+set_exp)
			self.failUnless(new_set_exp1==new_set_exp2,'%s!=%s'%(new_set_exp1,new_set_exp2))
			new_set_exp1.set_tuple.id_list.append('asdfghjkl')
			self.failIf(new_set_exp1==new_set_exp2,'%s==%s'%(new_set_exp1,new_set_exp2))

	#Tests that the __cmp__ method doesn't use 'isinstance'
	#but instead checks for properties of the object
	def testCmpNoIsInstance(self):
		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp,Node
		from iegen.util import test_sets

		class DummyPresSet(Node):
			def __init__(self,set_tuple,conjunct):
				self.set_tuple=set_tuple
				self.conjunct=conjunct

		for set_str,set_exp in test_sets:
			exec('new_set_exp1='+set_exp)
			set_exp=set_exp.replace('PresSet','DummyPresSet')
			exec('new_set_exp2='+set_exp)
			self.failUnless(new_set_exp1==new_set_exp2,'%s!=%s'%(new_set_exp1,new_set_exp2))
			new_set_exp1.set_tuple.id_list.append('asdfghjkl')
			self.failIf(new_set_exp1==new_set_exp2,'%s==%s'%(new_set_exp1,new_set_exp2))

	#Tests for the arity method(s)
	def testArity(self):
		from iegen.ast import PresSet

		self.failUnless(hasattr(PresSet,'arity'),"PresSet has no 'arity' method.")

#---------- PresRelation Tests ----------
class RelationTestCase(TestCase):

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import PresRelation,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp
		from iegen.util import test_relations

		for rel_str,rel_exp in test_relations:
			exec('new_rel_exp=repr('+rel_exp+')')
			self.failUnless(rel_exp==new_rel_exp,'%s!=%s'%(rel_exp,new_rel_exp))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import PresRelation,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp
		from iegen.util import test_relations

		for rel_str,rel_exp in test_relations:
			exec('new_rel_exp1='+rel_exp)
			exec('new_rel_exp2='+rel_exp)
			self.failUnless(new_rel_exp1==new_rel_exp2,'%s!=%s'%(new_rel_exp1,new_rel_exp2))
			new_rel_exp1.in_tuple.id_list.append('asdfghjkl')
			self.failIf(new_rel_exp1==new_rel_exp2,'%s==%s'%(new_rel_exp1,new_rel_exp2))

	#Tests that the __cmp__ method doesn't use 'isinstance'
	#but instead checks for properties of the object
	def testCmpNoIsInstance(self):
		from iegen.ast import PresRelation,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp,Node
		from iegen.util import test_relations

		class DummyPresRelation(Node):
			def __init__(self,in_tuple,out_tuple,conjunct):
				self.in_tuple=in_tuple
				self.out_tuple=out_tuple
				self.conjunct=conjunct

		for rel_str,rel_exp in test_relations:
			exec('new_rel_exp1='+rel_exp)
			rel_exp=rel_exp.replace('PresRelation','DummyPresRelation')
			exec('new_rel_exp2='+rel_exp)
			self.failUnless(new_rel_exp1==new_rel_exp2,'%s!=%s'%(new_rel_exp1,new_rel_exp2))
			new_rel_exp1.in_tuple.id_list.append('asdfghjkl')
			self.failIf(new_rel_exp1==new_rel_exp2,'%s==%s'%(new_rel_exp1,new_rel_exp2))

	#Tests for the arity method(s)
	def testArity(self):
		from iegen.ast import PresRelation

		self.failUnless(hasattr(PresRelation,'arity_in'),"PresRelation has no 'arity_in' method.")
		self.failUnless(hasattr(PresRelation,'arity_out'),"PresRelation has no 'arity_out' method.")
#----------------------------------------

#---------- Conjunction Tests ----------
class ConjunctionTestCase(TestCase):

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import Conjunction,Inequality,VarExp

		cs="Conjunction([Inequality(VarExp(2,'c'))])"
		exec('c='+cs)

		self.failUnless(cs==repr(c),'%s!=%s'%(cs,repr(c)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp

		cs1="Conjunction([Equality(NormExp([VarExp(-5,'a')],-5))])"
		cs2="Conjunction([Equality(NormExp([VarExp(-5,'b')],-5))])"
		exec('c1a='+cs1)
		exec('c1b='+cs1)
		exec('c2='+cs2)

		self.failUnless(cs1==repr(c1a),'%s!=%s'%(cs1,repr(c1a)))
		self.failUnless(cs1==repr(c1b),'%s!=%s'%(cs1,repr(c1b)))
		self.failUnless(cs2==repr(c2),'%s!=%s'%(cs2,repr(c2)))
		self.failUnless(c1a==c1b,'%s!=%s'%(c1a,c1b))
		self.failIf(c1a==c2,'%s==%s'%(c1a,c2))

	#Tests that the __cmp__ method doesn't use 'isinstance'
	#but instead checks for properties of the object
	def testCmpNoIsInstance(self):
		from iegen.ast import Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp,Node
		from iegen.util import test_relations

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
#---------------------------------------

#---------- VarTuple Tests ----------
class VarTupleTestCase(TestCase):

	#Tests the __repr__ method
	def testRepr(self):
		from iegen.ast import VarTuple

		vs="VarTuple(['a', 'b', 'c'])"
		exec('v='+vs)

		self.failUnless(vs==repr(v),'%s!=%s'%(vs,repr(v)))

	#Validate VarTuple's __len__ method
	def testLen(self):
		from iegen.ast import VarTuple

		v1=VarTuple(['a'])
		v2=VarTuple(['a','b'])
		v3=VarTuple(['a','b','c'])

		self.failUnless(1==len(v1),'len(%s)!=1'%v1)
		self.failUnless(2==len(v2),'len(%s)!=2'%v2)
		self.failUnless(3==len(v3),'len(%s)!=3'%v3)

	def testConjunction(self):
		from iegen.ast import Conjunction,Inequality,VarExp

		cs="Conjunction([Inequality(VarExp(2,'c'))])"
		exec('c='+cs)

		self.failUnless(cs==repr(c),'%s!=%s'%(cs,repr(c)))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen.ast import Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp

		cs1="Conjunction([Equality(NormExp([VarExp(-5,'a')],-5))])"
		cs2="Conjunction([Equality(NormExp([VarExp(-5,'b')],-5))])"
		exec('c1a='+cs1)
		exec('c1b='+cs1)
		exec('c2='+cs2)

		self.failUnless(cs1==repr(c1a),'%s!=%s'%(cs1,repr(c1a)))
		self.failUnless(cs1==repr(c1b),'%s!=%s'%(cs1,repr(c1b)))
		self.failUnless(cs2==repr(c2),'%s!=%s'%(cs2,repr(c2)))
		self.failUnless(c1a==c1b,'%s!=%s'%(c1a,c1b))
		self.failIf(c1a==c2,'%s==%s'%(c1a,c2))

	#Tests that the __cmp__ method doesn't use 'isinstance'
	#but instead checks for properties of the object
	def testCmpNoIsInstance(self):
		from iegen.ast import Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp,Node
		from iegen.util import test_relations

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

#------------------------------------

#---------- Constraint Tests ----------
class ConstraintTestCase(TestCase):
	def testConstraint(self):
		from iegen.ast import Equality,Inequality,NormExp,FuncExp,VarExp

		cs1="Equality(NormExp([VarExp(1,'a')],1))"
		exec('c1='+cs1)
		cs2="Inequality(NormExp([FuncExp(1,'f',[VarExp(1,'b')])],1))"
		exec('c2='+cs2)

		self.failUnless(cs1==repr(c1),'%s!=%s'%(cs1,repr(c1)))
		self.failUnless(cs2==repr(c2),'%s!=%s'%(cs2,repr(c2)))
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

	def testVarExpRepr(self):
		from iegen.ast import VarExp

		for var_exp in self.var_exps:
			exec('v='+var_exp)

			#Test VarExp's repr function
			self.failUnless(repr(v)==var_exp,'%s!=%s'%(repr(v),var_exp))
			self.failUnless(str(v)==var_exp,'%s!=%s'%(str(v),var_exp))

	def testVarExpComp(self):
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

	def testVarExpMult(self):
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
	          "FuncExp(1,'f',[VarExp(1,'a')])",
	          "FuncExp(1,'f',[VarExp(1,'a'), VarExp(1,'a')])",
	          "FuncExp(1,'f',[VarExp(1,'a')])",
	          "FuncExp(1,'g',[VarExp(1,'a')])",
	          "FuncExp(1,'f',[VarExp(1,'a')])",
	          "FuncExp(2,'f',[VarExp(1,'a')])",
	          "FuncExp(2,'g',[VarExp(1,'a')])",
	          "FuncExp(3,'fog',[VarExp(1,'a')])",
	          "FuncExp(4,'rain',[VarExp(1,'a')])",
	          "FuncExp(42,'test',[VarExp(1,'a')])",
	          "FuncExp(-81,'z',[VarExp(1,'a')])",
	          "FuncExp(101,'x',[VarExp(1,'a')])",
	          "FuncExp(16,'wxyz',[VarExp(1,'a'), VarExp(2,'b')])")

	def testFuncExpRepr(self):
		from iegen.ast import FuncExp,VarExp

		for func_exp in self.func_exps:
			exec('f='+func_exp)

			#Test FuncExp's repr function
			self.failUnless(repr(f)==func_exp,'%s!=%s'%(repr(f),func_exp))
			self.failUnless(str(f)==func_exp,'%s!=%s'%(str(f),func_exp))

	def testFuncExpComp(self):
		from iegen.ast import FuncExp,VarExp

		for func_exp in self.func_exps:
			exec('f='+func_exp)

			#Test FuncExp's comparison operator
			self.failUnless(f==f,'%s!=%s'%(f,f))
			self.failIf(f!=f,'%s!=%s'%(f,f))

			for func_exp2 in [f2 for f2 in self.func_exps if f2!=func_exp]:
				exec('f2='+func_exp2)
				self.failUnless(f2!=f,'%s==%s'%(f2,f))
				self.failIf(f2==f,'%s==%s'%(f2,f))

	def testFuncExpMult(self):
		from iegen.ast import FuncExp,VarExp

		for func_exp in self.func_exps:
			exec('f='+func_exp)

			#Test FuncExp's multiplication operator
			coeff=f.coeff
			name=f.name
			exps=f.exp_list

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
	          "NormExp([VarExp(1,'a'), FuncExp(2,'f',[VarExp(1,'b')])],5)",
	          "NormExp([VarExp(1,'a'), FuncExp(2,'f',[VarExp(1,'b')])],5)",
	          "NormExp([VarExp(1,'b')],5)",
	          "NormExp([VarExp(1,'a')],6)")

	def testNormExpRepr(self):
		from iegen.ast import NormExp,FuncExp,VarExp

		for norm_exp in self.norm_exps:
			exec('n='+norm_exp)

			#Test NormExp's repr function
			self.failUnless(repr(n)==norm_exp,'%s!=%s'%(repr(n),norm_exp))
			self.failUnless(str(n)==norm_exp,'%s!=%s'%(str(n),norm_exp))

	def testNormExpComp(self):
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

	def testNormExpMult(self):
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

	def testNormExpAddConst(self):
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

	def testNormExpAddTermConst(self):
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

	def testNormExpSort(self):
		from iegen.ast import NormExp,FuncExp,VarExp

		n1=NormExp([VarExp(1,'a'),
		            VarExp(2,'a'),
		            VarExp(2,'b'),
		            VarExp(2,'c'),
		            VarExp(3,'c'),
		            FuncExp(1,'f',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            FuncExp(2,'f',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            FuncExp(3,'g',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            FuncExp(3,'h',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            FuncExp(4,'i',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            FuncExp(4,'i',[VarExp(2,'a'),FuncExp(1,'f',[])]),
		            FuncExp(5,'j',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            FuncExp(5,'j',[VarExp(1,'a'),FuncExp(2,'f',[])])],
		            6)

		n2=NormExp([FuncExp(1,'f',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            FuncExp(3,'g',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            FuncExp(2,'f',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            VarExp(2,'b'),
		            FuncExp(3,'h',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            FuncExp(5,'j',[VarExp(1,'a'),FuncExp(2,'f',[])]),
		            VarExp(2,'c'),
		            FuncExp(4,'i',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            FuncExp(4,'i',[VarExp(2,'a'),FuncExp(1,'f',[])]),
		            VarExp(3,'c'),
		            FuncExp(5,'j',[VarExp(1,'a'),FuncExp(1,'f',[])]),
		            VarExp(2,'a'),
		            VarExp(1,'a')],
		            6)

		self.failUnless(n1==n2,'%s!=%s'%(n1,n2))
#-----------------------------------
