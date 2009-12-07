from unittest import TestCase
from iegen.lib.nose.tools import raises

#---------- Import Tests ----------
#Test importing of iegen
class ImportTestCase(TestCase):

	#Test simple importing of iegen
	def testImport(self):
		try:
			import iegen
		except Exception,e:
			self.fail("'import iegen' failed: "+str(e))

	#Test simple importing of iegen classes
	def testNameImport(self):
		try:
			from iegen import IEGenObject,MapIR,Symbolic,DataArray,IndexArray,AccessRelation,Statement,FunctionCallSpec,DataDependence,Set,Relation

			#SparseForumla related imports
			from iegen import SparseFormula,SparseSet,SparseRelation,SparseExpColumnType,TupleVarCol,SymbolicCol,FreeVarCol,ConstantCol,UFCall,SparseExp,SparseConstraint,SparseEquality,SparseInequality
		except Exception,e:
			self.fail("Importing classes from iegen failed: "+str(e))
#----------------------------------

#---------- Set Tests ----------
class SetTestCase(object):

	#Tests that we can create a Set by specifying a set string
	def testSetString(self):
		from iegen import Set

		set=Set('{[a]:a>10}')
		set=Set(set_string='{[a]:a>10}')

	#Tests that we can create a Set by specifying a set string and symbolic variables
	def testSetStringSymbolic(self):
		from iegen import Set,Symbolic

		set=Set('{[a]:a>10 and a<n}',[Symbolic('n')])
		set=Set(set_string='{[a]:a>10 and a<n}',symbolics=[Symbolic('n')])

	#Tests that we can create a Set by specifying a collection of PresSets
	def testSets(self):
		from iegen import Set
		from iegen.parser import PresParser

		set1=PresParser.parse_set('{[a]:a>10}')
		set2=PresParser.parse_set('{[b]:b>10}')

		set=Set(sets=[set1,set2])

	#Tests we cannot create a Set by specifying a collection of PresSets and Symbolics
	@raises(ValueError)
	def testSetsSymbolicFail(self):
		from iegen import Set,Symbolic
		from iegen.parser import PresParser

		set1=PresParser.parse_set('{[a]:a>10 and a<n}')
		set2=PresParser.parse_set('{[b]:b>10 and b<m}')

		set=Set(symbolics=[Symbolic('n'),Symbolic('m')],sets=[set1,set2])

	#Tests that we can create a Set by specifying a collection of PresSets that have Symbolics
	def testSetsWithSymbolics(self):
		from iegen import Set,Symbolic
		from iegen.parser import PresParser

		set1=PresParser.parse_set('{[a]:a>10 and a<n}',[Symbolic('n')])
		set2=PresParser.parse_set('{[b]:b>10 and b<m}',[Symbolic('m')])

		set=Set(sets=[set1,set2])

	#Tests that we must specify something to the Set constructor
	@raises(ValueError)
	def testEmptyFail(self):
		from iegen import Set

		Set()

	#Tests that we must have at least one item in the sets collection
	@raises(ValueError)
	def testEmptySetsFail(self):
		from iegen import Set

		Set(sets=[])

	#Tests that we cannot specify both a set string and a collection of sets
	@raises(ValueError)
	def testBothFail1(self):
		from iegen import Set

		Set('{[]}',[],[])
	@raises(ValueError)
	def testBothFail2(self):
		from iegen import Set

		Set(set_string='{[]}',sets=[])
	@raises(ValueError)
	def testBothFail3(self):
		from iegen import Set

		Set(set_string='{[]}',symbolics=[],sets=[])

	#Tests that all objects in the sets collection must 'look like' PresSets
	@raises(ValueError)
	def testNonPresSetFail(self):
		from iegen import Set
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]}')
		Set(sets=[set,'hello!'])

	#Tests that all objects in the sets collection must 'look like' PresSets
	def testLikePresSet(self):
		from iegen import Set
		from iegen.ast import VarTuple,Conjunction,Node
		from iegen.parser import PresParser

		class DummyPresSet(Node):
			def __init__(self):
				self.tuple_set=VarTuple([])
				self.conjunct=Conjunction([])
				self.symbolics=[]
			def arity(self):
				return 0
			def apply_visitor(self,visitor):
				visitor.visitPresSet(self)

		set=PresParser.parse_set('{[]}')
		Set(sets=[set,DummyPresSet()])

	#Tests that all objects in the symbolics collection must 'look like' Symbolics
	@raises(ValueError)
	def testNonSymbolicFail(self):
		from iegen import Set,Symbolic
		from iegen.parser import PresParser

		Set('{[]}',[Symbolic('n'),'m'])

	#Tests that all objects in the symbolics collection must 'look like' Symbolics
	def testLikeSymbolic(self):
		from iegen import Set
		from iegen.ast import VarTuple,Conjunction,Node
		from iegen.parser import PresParser

		class DummySymbolic(Node):
			def __init__(self,name):
				self.name=name
				self.type=None
				self.lower_bound=None
				self.upper_bound=None
			def apply_visitor(self,visitor):
				visitor.visitSymbolic(self)

		set=Set('{[]}',[DummySymbolic('n')])

	#Tests that we cannot create a set from two PresSets of differing arity
	@raises(ValueError)
	def testDiffArity(self):
		from iegen import Set
		from iegen.parser import PresParser

		pset1=PresParser.parse_set('{[a]:a>10}')
		pset2=PresParser.parse_set('{[a,b]:b>10}')
		Set(sets=[pset1,pset2])

	#Tests the __repr__ method
	def testRepr(self):
		from iegen import Set
		from iegen.ast import PresSet,VarTuple,Conjunction,VarExp

		set_str="Set(sets=[PresSet(VarTuple([VarExp(1,'a')]),Conjunction([]))])"
		exec('set='+set_str)
		self.failUnless(repr(set)==set_str,'%s!=%s'%(repr(set),set_str))

	#Tests the __str__ method
	def testStr(self):
		from iegen import Set,Symbolic
		from iegen.parser import PresParser

		set_str1='{[a]: -1a+5=0}'
		pset1=PresParser.parse_set(set_str1)

		set_str2='{[b]: -1b+6=0}'
		pset2=PresParser.parse_set(set_str2)

		set_str3='{[c]: -1c+7=0}'
		pset3=PresParser.parse_set(set_str3)

		set=Set(sets=[pset1])
		set_str='%s'%(set_str1)
		self.failUnless(str(set)==set_str,'%s!=%s'%(str(set),set_str))

		set=Set(sets=[pset1,pset2])
		set_str='{[a]: -1a+5=0} union {[a]: -1a+6=0}'
		self.failUnless(str(set)==set_str,'%s!=%s'%(str(set),set_str))

		set=Set(sets=[pset1,pset2,pset3])
		set_str='{[a]: -1a+5=0} union {[a]: -1a+6=0} union {[a]: -1a+7=0}'
		self.failUnless(str(set)==set_str,'%s!=%s'%(str(set),set_str))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen import Set

		set1=Set('{[]}')
		set2=Set('{[]}')
		set3=Set('{[a]}')

		self.failUnless(set1==set2,'%s!=%s'%(set1,set2))
		self.failIf(set1==set3,'%s==%s'%(set1,set3))

	#Tests that comparison still works when creating sets with differing order
	def testOrder(self):
		from iegen import Set
		from iegen.parser import PresParser

		pset1=PresParser.parse_set('{[a]:a>10}')
		pset2=PresParser.parse_set('{[b]:b>10}')
		set1=Set(sets=[pset1,pset2])
		set2=Set(sets=[pset2,pset1])

		self.failUnless(set1==set2,'%s!=%s'%(set1,set2))

	#Tests the arity method
	def testArity(self):
		from iegen import Set
		from iegen.util import lower_gen
		from string import lowercase

		for size in xrange(26):
			var_tuple=lowercase[:size]
			var_tuple='['+','.join(var_tuple)+']'
			set=Set('{'+var_tuple+'}')
			self.failUnless(set.arity()==size,"Arity of '%s'!=%d"%(set,size))

	#Tests that union does not allow sets of differing arity
	@raises(ValueError)
	def testUnionDiffArity(self):
		from iegen import Set

		set1=Set('{[]}')
		set2=Set('{[a]}')
		set1.union(set2)

	#Tests that union is not destructive
	def testUnionNonDestructive(self):
		from iegen import Set

		set1=Set('{[a]}')
		set2=Set('{[b]}')
		unioned=set1.union(set2)

		self.failIf(unioned is set1,'%s is %s'%(unioned,set1))
		self.failIf(unioned is set2,'%s is %s'%(unioned,set2))

	#Tests that union does not allow unioning with the same object
	@raises(ValueError)
	def testNoUnionSameObject(self):
		from iegen import Set

		set=Set('{[a]}')
		set.union(set)

	#Tests the union operation
	def testUnion(self):
		from iegen import Set
		from iegen.parser import PresParser

		pset1=PresParser.parse_set('{[a]:a>10}')
		pset2=PresParser.parse_set('{[b]:b>10}')
		set1=Set('{[a]:a>10}')
		set2=Set('{[b]:b>10}')
		unioned=set1.union(set2)
		unioned_res=Set(sets=[pset1,pset2])

		self.failUnless(unioned==unioned_res,'%s!=%s'%(unioned,unioned_res))

		pset1=PresParser.parse_set('{[a]:a>10}')
		pset2=PresParser.parse_set('{[b]:b>10}')
		pset3=PresParser.parse_set('{[b]:b>10}')
		set1=Set('{[a]:a>10}')
		set2=Set('{[b]:b>10}')
		unioned=unioned.union(set1)
		unioned_res=Set(sets=[pset1,pset2,pset3])

		self.failUnless(unioned==unioned_res,'%s!=%s'%(unioned,unioned_res))

	#Tests that the union operation standardizes names across all sets in the union
	def testUnionRename(self):
		from iegen import Set
		from iegen.parser import PresParser

		pset1=PresParser.parse_set('{[a]:a>10}')
		pset2=PresParser.parse_set('{[a]:a<5}')
		pset3=PresParser.parse_set('{[a]:a=7}')
		set1=Set('{[a]:a>10}')
		set2=Set('{[b]:b<5}')
		set3=Set('{[c]:c=7}')
		unioned=set1.union(set2).union(set3)
		unioned_res=Set(sets=[pset1,pset2,pset3])

		self.failUnless(unioned==unioned_res,'%s!=%s'%(unioned,unioned_res))

		pset1=PresParser.parse_set('{[a]:a>10}')
		pset2=PresParser.parse_set('{[a]:a<5}')
		pset3=PresParser.parse_set('{[a]:a=7}')
		set1=Set('{[a]:a>10}')
		set2=Set('{[b]:b<5}')
		set3=Set('{[c]:c=7}')
		unioned=unioned.union(set1)
		unioned_res=Set(sets=[pset1,pset2,pset3])

		self.failUnless(unioned==unioned_res,'%s!=%s'%(unioned,unioned_res))

	#Tests that apply is not destructive
	def testApplyNonDestructive(self):
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[a]->[b]}')
		applied=set.apply(relation)

		self.failIf(applied is set,'%s is %s'%(applied,set))

	#Tests that apply fails when the arity of the set does not match the input arity of the relation
	@raises(ValueError)
	def testApplyArityFail1(self):
		from iegen import Set,Relation

		set=Set('{[a,b]}')
		relation=Relation('{[b]->[b]}')
		applied=set.apply(relation)

	@raises(ValueError)
	def testApplyArityFail2(self):
		from iegen import Set,Relation

		set=Set('{[a,b,c]}')
		relation=Relation('{[a,b]->[e,f]}')
		applied=set.apply(relation)

	#Tests the apply operation
	def testApply(self):
		from iegen import Set,Relation

		set=Set('{[a]:1<=a and a<=10}')
		relation=Relation('{[d]->[e,f]:e=d && -10<=f and f<=0}')

		applied=set.apply(relation)

		applied_res=Set('{[e,f]: 1<=e and e<=10 && -10<=f and f<=0}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests the apply operation with equality constraints
	def testApplyEquality(self):
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[d]->[e,f]:e=d and f=d}')

		applied=set.apply(relation)

		applied_res=Set('{[e,f]: e=f}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests that the apply operation renames variables back
	def testApplyRenameBack(self):
		from iegen import Set,Relation

		set=Set('{[a]: a=5}')
		relation=Relation('{[b]->[b,f]: f=12}')

		applied=set.apply(relation)

		applied_res=Set('{[b0,f]: b0=5 and f=12}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests that the apply operation doesn't choke on duplicate names
	def testApplyRename1(self):
		from iegen import Set,Relation

		set=Set('{[a,b]:1<=a and a<=10 and 1<=b and b<=10}')
		relation=Relation('{[a,b]->[c,d]:-10<=a and a<=0 and c=6 and d>5}')

		applied=set.apply(relation)

		#TODO: Free var inequality bug #54 forces a1>=1
		applied_res=Set('{[c,d]: a1>=1 and c=6 and d>5}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests that the apply operation doesn't choke on duplicate names
	def testApplyRename2(self):
		from iegen import Set,Relation

		set=Set('{[a,b]:1<=a and a<=10 and 1<=b and b<=10}')
		relation=Relation('{[a,b]->[a,b]:-10<=a and a<=0 and b=6 and a>5}')

		applied=set.apply(relation)

		applied_res=Set('{[a0,b0]:1<=a0 and a0<=10 and -10<=a0 and a0<=0 and b0=6 and a0>5}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests the apply operation on a real-world use case from moldyn-FST.in
	def testApplyReal(self):
		from iegen import Set,Relation

		I_0=Set('{ [s1,i,s2] : s1=1 and s2=1 and 0 <= i and i <= (n_atom-1)  }')
		iter_ssr=Relation('{ [ k, ii, j ] -> [ ii ] : k=1 }')

		I_0_applied=I_0.apply(iter_ssr)

		I_0_res=Set('{ [ii0] : 0 <= ii0 and ii0 <= (n_atom-1) }')

		self.failUnless(I_0_applied==I_0_res,'%s!=%s'%(I_0_applied,I_0_res))

		iter_reordering=Relation('{ [ in ] -> [ i ] : in=i and i=delta(in) }')
		I_0_applied=I_0_applied.apply(iter_reordering)

		I_0_res=Set('{ [i] : i=delta(i) and 0 <= i and i <= (n_atom-1) }')

		self.failUnless(I_0_applied==I_0_res,'%s!=%s'%(I_0_applied,I_0_res))

	#Tests the apply operation on a real-world use case from moldyn-FST.in
	def testApplyRealUnion(self):
		from iegen import Set,Relation

		I_0=Set('{ [s1,i,s2] : s1=1 and s2=1 and 0 <= i and i <= (n_atom-1)  }').union(Set('{ [s1,i,s2] : s1=2 and s2=2 and 0 <= i and i <= (n_atom-2)  }')).union(Set('{ [s1,i,s2] : s1=3 and s2=3 and 0 <= i and i <= (n_atom-3)  }'))
		iter_ssr=Relation('{ [ k, ii, j ] -> [ ii ] : k=1 }').union(Relation('{ [ k, ii, j ] -> [ ii ] : k=2 }')).union(Relation('{ [ k, ii, j ] -> [ ii ] : k=3 }'))

		I_0_applied=I_0.apply(iter_ssr)

		I_0_res=Set('{ [ii0] : 0 <= ii0 and ii0 <= (n_atom-1) }').union(Set('{ [ii0] : 0 <= ii0 and ii0 <= (n_atom-2) }')).union(Set('{ [ii0] : 0 <= ii0 and ii0 <= (n_atom-3) }'))

		self.failUnless(I_0_applied==I_0_res,'%s!=%s'%(I_0_applied,I_0_res))

		iter_reordering=Relation('{ [ in ] -> [ i ] : i=delta(in) }')
		I_0_applied=I_0_applied.apply(iter_reordering)

		I_0_res=Set('{ [i] : i=delta(in) and 0 <= (n_atom-1) }').union(Set('{ [i] : i=delta(in) and 0 <= (n_atom-2) }')).union(Set('{ [i] : i=delta(in) and 0 <= (n_atom-3) }'))

		self.failUnless(I_0_applied==I_0_res,'%s!=%s'%(I_0_applied,I_0_res))

	#Tests a simple apply case
	def testApplyRenameBug(self):
		from iegen import Set,Relation

		s=Set('{[a]}').apply(Relation('{[b]->[c]: c=f(b)}'))
		s_res=Set('{[c]: c=f(b)}')

		self.failUnless(s==s_res,'%s!=%s'%(s,s_res))

	#Tests the _get_prefix_rename_dict method
	def testGetPrefixRenameDict(self):
		from iegen import Set

		set=Set('{[a,b,c]:1<=a and a<=10}')

		rename=set._get_prefix_rename_dict(set.sets[0],'pre')
		rename_res={'a':'pre_a','b':'pre_b','c':'pre_c'}

		self.failUnless(rename==rename_res,'%s!=%s'%(rename,rename_res))

	#Tests the _get_prefix_unrename_dict method
	def testGetPrefixUnrenameDict(self):
		from iegen import Set

		set=Set('{[a,b]:1<=a and a<=10}')

		unrename=set._get_prefix_unrename_dict(set.sets[0],'pre')
		unrename_res={'pre_a':'a','pre_b':'b'}

		self.failUnless(unrename==unrename_res,'%s!=%s'%(unrename,unrename_res))

	#Tests the _get_formula_rename_dict method
	def testGetFormulaRenameDict(self):
		from iegen import Set

		set1=Set('{[a_1,b_1]:1<=a_1 and a_1<=10}')
		set2=Set('{[b,c]}')
		rename=set1._get_formula_rename_dict(set1.sets[0],set2.sets[0])
		rename_res={'a_1':'b','b_1':'c'}

		self.failUnless(rename==rename_res,'%s!=%s'%(rename,rename_res))

	#Tests that the lower bound method fails when given variable names that aren't part of the tuple
	@raises(ValueError)
	def testLowerBoundNonTupleVarFail(self):
		from iegen import Set
		set=Set('{[a,b]: 1<=a and a<=10 and 1<=b and b<=10}')
		set.lower_bound('c')

	#Tests that the upper bound method fails when given variable names that aren't part of the tuple
	@raises(ValueError)
	def testUpperBoundNonTupleVarFail(self):
		from iegen import Set
		set=Set('{[a,b]: 1<=a and a<=10 and 1<=b and b<=10}')
		set.upper_bound('c')

	#Tests that the bounds method fails when given variable names that aren't part of the tuple
	@raises(ValueError)
	def testBoundsNonTupleVarFail(self):
		from iegen import Set
		set=Set('{[a,b]: 1<=a and a<=10 and 1<=b and b<=10}')
		set.bounds('c')

	#Tests that the proper upper and lower bounds are calculated for a 1d set
	def testBounds1D(self):
		from iegen import Set
		from iegen.ast import NormExp

		set=Set('{[a]: 1<=a and a<=10}')
		self.failUnless([NormExp([],1)]==set.lower_bound('a'),"The lower bound of 'a' is not 1")
		self.failUnless([NormExp([],10)]==set.upper_bound('a'),"The upper bound of 'a' is not 10")
		self.failUnless(([NormExp([],1)],[NormExp([],10)])==set.bounds('a'),"The bounds of 'a' are not (1,10)")

	#Tests that the proper upper and lower bounds are calculated for a 2d set
	def testBounds2D(self):
		from iegen import Set
		from iegen.ast import NormExp

		set=Set('{[a,b]: 5<=a and a<=20 and -10<=b and b<=0}')
		self.failUnless([NormExp([],5)]==set.lower_bound('a'),"The lower bound of 'a' is not 5 in set %s"%set)
		self.failUnless([NormExp([],20)]==set.upper_bound('a'),"The upper bound of 'a' is not 20")
		self.failUnless(([NormExp([],5)],[NormExp([],20)])==set.bounds('a'),"The bounds of 'a' are not (5,20)")
		self.failUnless([NormExp([],-10)]==set.lower_bound('b'),"The lower bound of 'b' is not -10")
		self.failUnless([NormExp([],0)]==set.upper_bound('b'),"The upper bound of 'b' is not 0")
		self.failUnless(([NormExp([],-10)],[NormExp([],0)])==set.bounds('b'),"The bounds of 'b' are not (-10,0)")

	#Tests that the proper upper and lower bounds are calculated for a 2d set with symbolics
	def testBoundsSymbolic(self):
		from iegen import Set,Symbolic
		from iegen.ast import NormExp,VarExp

		set=Set('{[a,b]: 5<=a and a<=n and m<=b and b<=0}',[Symbolic('n'),Symbolic('m')])
		self.failUnless([NormExp([],5)]==set.lower_bound('a'),"The lower bound of 'a' is not 5")
		self.failUnless([NormExp([VarExp(1,'n')],0)]==set.upper_bound('a'),"The upper bound of 'a' is not n")
		self.failUnless(([NormExp([],5)],[NormExp([VarExp(1,'n')],0)])==set.bounds('a'),"The bounds of 'a' are not (5,n)")
		self.failUnless([NormExp([VarExp(1,'m')],0)]==set.lower_bound('b'),"The lower bound of 'b' is not m")
		self.failUnless([NormExp([],0)]==set.upper_bound('b'),"The upper bound of 'b' is not 0")
		self.failUnless(([NormExp([VarExp(1,'m')],0)],[NormExp([],0)])==set.bounds('b'),"The bounds of 'b' are not (m,0)")

	#Tests that the proper upper and lower bounds are calculated for a 2d set with symbolics
	def testBoundsSymbolicMuliTerm(self):
		from iegen import Set,Symbolic
		from iegen.ast import NormExp,VarExp

		set=Set('{[a,b]: 5<=a and a<=n+m+10 and m-6<=b and b<=0}',[Symbolic('n'),Symbolic('m')])
		self.failUnless([NormExp([],5)]==set.lower_bound('a'),"The lower bound of 'a' is not 5")
		self.failUnless([NormExp([VarExp(1,'n'),VarExp(1,'m')],10)]==set.upper_bound('a'),"The upper bound of 'a' is not n+m+10")
		self.failUnless(([NormExp([],5)],[NormExp([VarExp(1,'n'),VarExp(1,'m')],10)])==set.bounds('a'),"The bounds of 'a' are not (5,n+m+10)")
		self.failUnless([NormExp([VarExp(1,'m')],-6)]==set.lower_bound('b'),"The lower bound of 'b' is not m-6")
		self.failUnless([NormExp([],0)]==set.upper_bound('b'),"The upper bound of 'b' is not 0")
		self.failUnless(([NormExp([VarExp(1,'m')],-6)],[NormExp([],0)])==set.bounds('b'),"The bounds of 'b' are not (m-6,0)")

	#Tests the is_tautology method
	def testIsTautology(self):
		from iegen import Set

		set=Set('{[a]}')
		self.failUnless(set.is_tautology(),'%s is not a tautology'%set)

		set=Set('{[a]: 5=5}')
		self.failUnless(set.is_tautology(),'%s is not a tautology'%set)

		set=Set('{[a]: 5=5}').union(Set('{[a]: 6=6}'))
		self.failUnless(set.is_tautology(),'%s is not a tautology'%set)

		set=Set('{[a]: 5=5}').union(Set('{[a]: 6=6}')).union(Set('{[a]: 3=3}'))
		self.failUnless(set.is_tautology(),'%s is not a tautology'%set)

		set=Set('{[a]: 5=0}')
		self.failIf(set.is_tautology(),'%s is a tautology'%set)

		set=Set('{[a]: 5=0}').union(Set('{[a]: 6=0}'))
		self.failIf(set.is_tautology(),'%s is a tautology'%set)

		set=Set('{[a]: 5=0}').union(Set('{[a]: 6=0}')).union(Set('{[a]: 7=0}'))
		self.failIf(set.is_tautology(),'%s is a tautology'%set)

		set=Set('{[a]: 5=0}').union(Set('{[a]: 5=5}'))
		self.failUnless(set.is_tautology(),'%s is not a tautology'%set)

	#Test the is_contradiction method
	def testIsContradiction(self):
		from iegen import Set

		set=Set('{[a]}')
		self.failIf(set.is_contradiction(),'%s is a contradiction'%set)

		set=Set('{[a]: 5=5}')
		self.failIf(set.is_contradiction(),'%s is a contradiction'%set)

		set=Set('{[a]: 5=5}').union(Set('{[a]: 6=6}'))
		self.failIf(set.is_contradiction(),'%s is a contradiction'%set)

		set=Set('{[a]: 5=5}').union(Set('{[a]: 6=6}')).union(Set('{[a]: 3=3}'))
		self.failIf(set.is_contradiction(),'%s is a contradiction'%set)

		set=Set('{[a]: 5=0}')
		self.failUnless(set.is_contradiction(),'%s is not a contradiction'%set)

		set=Set('{[a]: 5=0}').union(Set('{[a]: 6=0}'))
		self.failUnless(set.is_contradiction(),'%s is not a contradiction'%set)

		set=Set('{[a]: 5=0}').union(Set('{[a]: 6=0}')).union(Set('{[a]: 7=0}'))
		self.failUnless(set.is_contradiction(),'%s is not a contradiction'%set)

		set=Set('{[a]: 5=0}').union(Set('{[a]: 5=5}'))
		self.failIf(set.is_contradiction(),'%s is a contradiction'%set)

	def testVariables(self):
		from iegen import Set

		set=Set('{[a,b]: a=b}')
		res=['a','b']

		self.failUnless(res==set.variables(),'%s!=%s'%(res,set.variables()))

	def testFunctions(self):
		from iegen import Set

		set=Set('{[a,b]: a=f(b) and b=foo(a)}')
		res=['f','foo']

		self.failUnless(res==set.functions(),'%s!=%s'%(res,set.functions()))

	def testSymbolics(self):
		from iegen import Set,Symbolic

		set=Set('{[a,b]: a=f(n) and b=foo(a)}',[Symbolic('n')])
		res=['n']

		self.failUnless(res==set.symbolics(),'%s!=%s'%(res,set.symbolics()))
#-------------------------------

#---------- Relation Tests ----------
class RelationTestCase(object):

	#Tests that we can create a Relation by specifying a relation string
	def testRelationString(self):
		from iegen import Relation

		relation=Relation('{[a]->[b]:a>10}')
		relation=Relation(relation_string='{[a]->[b]:a>10}')

	#Tests that we can create a Relation by specifying a relation string and symbolic variables
	def testRelationStringSymbolic(self):
		from iegen import Relation,Symbolic

		relation=Relation('{[a]->[b]:a>10 and a<n}',[Symbolic('n')])
		relation=Relation(relation_string='{[a]->[b]:a>10 and a<n}',symbolics=[Symbolic('n')])

	#Tests that we can create a Relation by specifying a collection of PresRelations
	def testRelations(self):
		from iegen import Relation
		from iegen.parser import PresParser

		relation1=PresParser.parse_relation('{[a]->[b]:a>10}')
		relation2=PresParser.parse_relation('{[b]->[c]:b>10}')

		relation=Relation(relations=[relation1,relation2])

	#Tests that we cannot create a Relation by specifying a collection of PresRelations and Symbolics
	@raises(ValueError)
	def testRelationsSymbolicFail(self):
		from iegen import Relation,Symbolic
		from iegen.parser import PresParser

		relation1=PresParser.parse_relation('{[a]->[b]:a>10 and a<n}')
		relation2=PresParser.parse_relation('{[b]->[c]:b>10 and b<m}')

		relation=Relation(symbolics=[Symbolic('n'),Symbolic('m')],relations=[relation1,relation2])

	#Tests that we can create a Relation by specifying a collection of PresRelations that have Symbolics
	def testRelationsWhtSymbolics(self):
		from iegen import Relation,Symbolic
		from iegen.parser import PresParser

		relation1=PresParser.parse_relation('{[a]->[b]:a>10 and a<n}',[Symbolic('n')])
		relation2=PresParser.parse_relation('{[b]->[c]:b>10 and b<m}',[Symbolic('m')])

		relation=Relation(relations=[relation1,relation2])

	#Tests that we must specify something to the Relation constructor
	@raises(ValueError)
	def testEmptyFail(self):
		from iegen import Relation

		Relation()

	#Tests that we must have at least one item in the relations collection
	@raises(ValueError)
	def testEmptyRelationsFail(self):
		from iegen import Relation

		Relation(relations=[])

	#Tests that we cannot specify both a relation string and a collection of relations
	@raises(ValueError)
	def testBothFail1(self):
		from iegen import Relation

		Relation('{[]->[]}',[],[])
	@raises(ValueError)
	def testBothFail2(self):
		from iegen import Relation

		Relation(relation_string='{[]->[]}',relations=[])
	@raises(ValueError)
	def testBothFail3(self):
		from iegen import Relation

		Relation(relation_string='{[]->[]}',symbolics=[],relations=[])

	#Tests that all objects in the relations collection must 'look like' PresRelations
	@raises(ValueError)
	def testNonPresRelationFail(self):
		from iegen import Relation
		from iegen.parser import PresParser

		relation=PresParser.parse_relation('{[]->[]}')
		Relation(relations=[relation,"hello!"])

	#Tests that all objects in the relations collection must 'look like' PresRelations
	def testLikePresRelation(self):
		from iegen import Relation
		from iegen.ast import VarTuple,Conjunction,Node
		from iegen.parser import PresParser

		class DummyPresRelation(Node):
			def __init__(self):
				self.tuple_in=VarTuple([])
				self.tuple_out=VarTuple([])
				self.conjunct=Conjunction([])
				self.symbolics=[]
			def arity(self):
				return (0,0)
			def apply_visitor(self,visitor):
				visitor.visitPresRelation(self)

		relation=PresParser.parse_relation('{[]->[]}')
		Relation(relations=[relation,DummyPresRelation()])

	#Tests that all objects in the symbolics collection must 'look like' Symbolics
	@raises(ValueError)
	def testNonSymbolicFail(self):
		from iegen import Relation,Symbolic
		from iegen.parser import PresParser

		Relation('{[]->[]}',[Symbolic('n'),'m'])

	#Tests that all objects in the symbolics collection must 'look like' Symbolics
	def testLikeSymbolic(self):
		from iegen import Relation
		from iegen.ast import VarTuple,Conjunction,Node
		from iegen.parser import PresParser

		class DummySymbolic(Node):
			def __init__(self,name):
				self.name=name
				self.type=None
				self.lower_bound=None
				self.upper_bound=None
			def apply_visitor(self,visitor):
				visitor.visitSymbolic(self)

		relation=Relation('{[]->[]}',[DummySymbolic('n')])

	#Tests that we cannot create a relation from two PresRelations of differing arity
	@raises(ValueError)
	def testDiffInArity(self):
		from iegen import Relation
		from iegen.parser import PresParser

		relation1=PresParser.parse_relation('{[a]->[b]:a>10}')
		relation2=PresParser.parse_relation('{[a,b]->[b]:b>10}')
		Relation(relations=[relation1,relation2])
	@raises(ValueError)
	def testDiffOutArity(self):
		from iegen import Relation
		from iegen.parser import PresParser

		relation1=PresParser.parse_relation('{[a]->[b]:a>10}')
		relation2=PresParser.parse_relation('{[a]->[a,b]:b>10}')
		Relation(relations=[relation1,relation2])
	@raises(ValueError)
	def testDiffBothArity(self):
		from iegen import Relation
		from iegen.parser import PresParser

		relation1=PresParser.parse_relation('{[a]->[b]:a>10}')
		relation2=PresParser.parse_relation('{[a,b]->[a,b]:b>10}')
		Relation(relations=[relation1,relation2])

	#Tests the __repr__ method
	def testRepr(self):
		from iegen import Relation
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp

		relation_str="Relation(relations=[PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,'b')]),Conjunction([]))])"
		exec('relation='+relation_str)
		self.failUnless(repr(relation)==relation_str,'%s!=%s'%(repr(relation),relation_str))

	#Tests the __str__ method
	def testStr(self):
		from iegen import Relation,Symbolic
		from iegen.parser import PresParser

		relation_str1='{[a]->[ap]: -1a+5=0}'
		prelation1=PresParser.parse_relation(relation_str1)

		relation_str2='{[b]->[bp]: -1b+6=0}'
		prelation2=PresParser.parse_relation(relation_str2)

		relation_str3='{[c]->[cp]: -1c+7=0}'
		prelation3=PresParser.parse_relation(relation_str3)

		relation=Relation(relations=[prelation1])
		relation_str='%s'%(relation_str1)
		self.failUnless(str(relation)==relation_str,'%s!=%s'%(str(relation),relation_str))

		relation=Relation(relations=[prelation1,prelation2])
		relation_str='{[a]->[ap]: -1a+5=0} union {[a]->[ap]: -1a+6=0}'
		self.failUnless(str(relation)==relation_str,'%s!=%s'%(str(relation),relation_str))

		relation=Relation(relations=[prelation1,prelation2,prelation3])
		relation_str='{[a]->[ap]: -1a+5=0} union {[a]->[ap]: -1a+6=0} union {[a]->[ap]: -1a+7=0}'
		self.failUnless(str(relation)==relation_str,'%s!=%s'%(str(relation),relation_str))

	#Tests the __cmp__ method
	def testCmp(self):
		from iegen import Relation

		relation1=Relation('{[]->[]}')
		relation2=Relation('{[]->[]}')
		relation3=Relation('{[a]->[a]}')

		self.failUnless(relation1==relation2,'%s!=%s'%(relation1,relation2))
		self.failIf(relation1==relation3,'%s==%s'%(relation1,relation3))

	#Tests that comparison still works when creating sets with differing order
	def testOrder(self):
		from iegen import Relation
		from iegen.parser import PresParser

		prelation1=PresParser.parse_relation('{[a]->[a]:a>10}')
		prelation2=PresParser.parse_relation('{[b]->[b]:b>11}')
		relation1=Relation(relations=[prelation1,prelation2])

		prelation1=PresParser.parse_relation('{[a]->[a]:a>11}')
		prelation2=PresParser.parse_relation('{[b]->[b]:b>10}')
		relation2=Relation(relations=[prelation1,prelation2])

		self.failUnless(relation1==relation2,'%s!=%s'%(relation1,relation2))

	#Tests the arity_in, arity_out, and arity methods
	def testArity(self):
		from iegen import Relation
		from iegen.util import lower_gen
		from string import lowercase

		for size_in in xrange(10):
			for size_out in xrange(10):
				var_tuple_in=lowercase[:size_in]
				var_tuple_in='['+','.join(var_tuple_in)+']'
				var_tuple_out=[var+'p' for var in lowercase[:size_out]]
				var_tuple_out='['+','.join(var_tuple_out)+']'
				relation=Relation('{'+var_tuple_in+'->'+var_tuple_out+'}')
				self.failUnless(relation.arity_in()==size_in,"Input arity of '%s'!=%d"%(relation,size_in))
				self.failUnless(relation.arity_out()==size_out,"Output arity of '%s'!=%d"%(relation,size_out))
				self.failUnless(relation.arity()==(size_in,size_out),"Inpyut/Output arity of '%s'!=%s"%(relation,(size_in,size_out)))

	#Tests that union does not allow relations of differing arity
	@raises(ValueError)
	def testUnionDiffArity(self):
		from iegen import Relation

		relation1=Relation('{[]->[]}')
		relation2=Relation('{[a]->[a]}')
		relation1.union(relation2)

	#Tests that union is not destructive
	def testUnionNonDestructive(self):
		from iegen import Relation

		relation1=Relation('{[a]->[a]}')
		relation2=Relation('{[b]->[b]}')
		unioned=relation1.union(relation2)

		self.failIf(unioned is relation1,'%s is %s'%(unioned,relation1))
		self.failIf(unioned is relation2,'%s is %s'%(unioned,relation2))

	#Tests that union does not allow unioning with the same object
	@raises(ValueError)
	def testNoUnionSameObject(self):
		from iegen import Relation

		rel=Relation('{[a]->[a]}')
		rel.union(rel)

	#Tests the union operation
	def testUnion(self):
		from iegen import Relation
		from iegen.parser import PresParser

		prelation1=PresParser.parse_relation('{[a]->[a]:a>10}')
		prelation2=PresParser.parse_relation('{[b]->[b]:b>11}')
		relation1=Relation('{[a]->[a]:a>10}')
		relation2=Relation('{[b]->[b]:b>11}')
		unioned=relation1.union(relation2)
		unioned_res=Relation(relations=[prelation1,prelation2])

		self.failUnless(unioned==unioned_res,'%s!=%s'%(unioned,unioned_res))

		prelation1=PresParser.parse_relation('{[a]->[a]:a>10}')
		prelation2=PresParser.parse_relation('{[b]->[b]:b>11}')
		prelation3=PresParser.parse_relation('{[b]->[b]:b>11}')
		relation1=Relation('{[a]->[a]:a>10}')
		relation2=Relation('{[b]->[b]:b>11}')
		unioned=unioned.union(relation1)
		unioned_res=Relation(relations=[prelation1,prelation2,prelation3])

		self.failUnless(unioned==unioned_res,'%s!=%s'%(unioned,unioned_res))

	#Tests that the union operation standardizes names across all relations in the union
	def testUnionRename(self):
		from iegen import Relation
		from iegen.parser import PresParser

		prelation1=PresParser.parse_relation('{[a]->[ap]:a>10 and ap>20}')
		prelation2=PresParser.parse_relation('{[a]->[ap]:a<5 and ap<10}')
		prelation3=PresParser.parse_relation('{[a]->[ap]:a=7 and ap=14}')
		relation1=Relation('{[a]->[ap]:a>10 and ap>20}')
		relation2=Relation('{[b]->[bp]:b<5 and bp<10}')
		relation3=Relation('{[c]->[cp]:c=7 and cp=14}')
		unioned=relation1.union(relation2).union(relation3)
		unioned_res=Relation(relations=[prelation1,prelation2,prelation3])

		self.failUnless(unioned==unioned_res,'%s!=%s'%(unioned,unioned_res))

		prelation1=PresParser.parse_relation('{[a]->[ap]:a>10 and ap>20}')
		prelation2=PresParser.parse_relation('{[a]->[ap]:a<5 and ap<10}')
		prelation3=PresParser.parse_relation('{[a]->[ap]:a=7 and ap=14}')
		relation1=Relation('{[a]->[ap]:a>10 and ap>20}')
		relation2=Relation('{[b]->[bp]:b<5 and bp<10}')
		relation3=Relation('{[c]->[cp]:c=7 and cp=14}')
		unioned=unioned.union(relation1)
		unioned_res=Relation(relations=[prelation1,prelation2,prelation3])

		self.failUnless(unioned==unioned_res,'%s!=%s'%(unioned,unioned_res))

	#Tests the inverse operation
	def testInverse(self):
		from iegen import Relation
		from iegen.parser import PresParser

		relation=Relation('{[a,b]->[c,d]}')
		prelation=PresParser.parse_relation('{[c,d]->[a,b]}')

		inverse=relation.inverse()
		inverse_res=Relation(relations=[prelation])

		self.failUnless(inverse==inverse_res,'%s!=%s'%(inverse,inverse_res))

	#Tests the inverse operation with constraints
	def testInverseConstraints(self):
		from iegen import Relation
		from iegen.parser import PresParser

		relation=Relation('{[a,b]->[c,d]:a>=n && b<5 and c+d=15}')
		prelation=PresParser.parse_relation('{[c,d]->[a,b]:b<5 and a>=n && c+d=15}')

		inverse=relation.inverse()
		inverse_res=Relation(relations=[prelation])

		self.failUnless(inverse==inverse_res,'%s!=%s'%(inverse,inverse_res))

	#Tests that compose is not destructive
	def testComposeNonDestructive(self):
		from iegen import Relation

		relation1=Relation('{[a]->[a]}')
		relation2=Relation('{[b]->[b]}')
		composed=relation1.compose(relation2)

		self.failIf(composed is relation1,'%s is %s'%(composed,relation1))
		self.failIf(composed is relation2,'%s is %s'%(composed,relation2))

	#Tests that compose fails when the output arity of the second relation does not match the input arity of the first relation
	@raises(ValueError)
	def testComposeArityFail1(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c]}')
		relation2=Relation('{[b]->[b]}')
		composed=relation1.compose(relation2)

	@raises(ValueError)
	def testComposeArityFail2(self):
		from iegen import Relation

		relation1=Relation('{[]->[c]}')
		relation2=Relation('{[a,b,c,d]->[e]}')
		composed=relation1.compose(relation2)

	#Tests that compose can operate with the same object as both operands. 
	def testComposeSameObject(self):
		from iegen import Relation

		rel=Relation('{[a]->[a]}')
		composed=rel.compose(rel)

		composed_res=Relation('{[a2]->[a01]: a2=a01}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests the compose operation
	def testCompose(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c]:1<=a and a<=10 and 1<=b and b<=10}')
		relation2=Relation('{[d]->[e,f]:-10<=d and d<=0}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[d]->[c]: -10<=d and d<=0}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests the compose operation with equality constraints
	def testComposeEquality(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c]:c=a}')
		relation2=Relation('{[d]->[e,f]:e=d and f=d}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[d]->[c]: d=c}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests that variables are renamed back if there are no conflicts
	def testComposeRenameBack(self):
		from iegen import Relation

		relation1=Relation('{[a]->[b,c]: a=6 and b=7 and c>10}')
		relation2=Relation('{[i,j]->[k]: i>0 and j<-5 and k>3}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[i,j]->[b,c]: i>0 and j<-5 and b=7 and c>10}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests that variables are not renamed back if there are conflicts
	def testComposeNoRenameBack(self):
		from iegen import Relation

		relation1=Relation('{[a]->[b,c]: a=b and b=7 and c>10}')
		relation2=Relation('{[b,i]->[k]: i>0 and b<-5 and k>3 and b=k}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[b2,i2]->[b1,c1]: i2>0 and b2<-5 and b2>=4 and b1=7 and c1>10 and b2=b1}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests that mappings from a->a are treated as they should be
	#This is the main test case for bug #34
	def testInOutMapping(self):
		from iegen import Relation

		relation1=Relation('{[i]->[j]: j=f(i)}')
		relation2=Relation('{[a]->[a]}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[a]->[j]: j=f(a)}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests that the compose operation doesn't choke on duplicate names
	def testComposeRename1(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c]:1<=a and a<=10 and 1<=b and b<=10}')
		relation2=Relation('{[a]->[b,c]:-10<=a and a<=0}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[a2]->[c1]: -1a2>=0 and a2+10>=0}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests that the compose operation doesn't choke on duplicate names
	def testComposeRename2(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[b]:1<=a and a<=11 and 1<=b and b<=10}')
		relation2=Relation('{[a]->[a,b]:-10<=a and a<=0 and b=5}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[a2]->[b01]: a2+-1>=0 and -1a2>=0 and a2+10>=0 and -1a2+11>=0 and -1b01+5=0}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests that the compose operation doesn't choke on duplicate names
	def testComposeRename3(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[a]:1<=a and a<=10 and 1<=b and b<=10}')
		relation2=Relation('{[a]->[a,b]:-10<=a and a<=0 and b=5}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[a2]->[a01]: a2<=10 and a2<=0 and a2>=1 and a2>=-10 and a2=a01}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests the compose operation on a real-world use case from moldyn-FST.in
	def testComposeReal(self):
		from iegen import Relation

		ar=Relation('{[ii,s]->[ar_out]:s=1 and ar_out=inter(ii)}')
		data_reordering=Relation('{[k]->[dr_out]:dr_out=sigma(k)}')

		ar_composed=data_reordering.compose(ar)

		ar_res=Relation('{[ii,s]->[dr_out]:s=1 and dr_out=sigma(inter(ii))}')

		self.failUnless(ar_composed==ar_res,'%s!=%s'%(ar_composed,ar_res))

	#Tests the compose operation on a real-world use case from moldyn-FST.in
	def testComposeRealUnion(self):
		from iegen import Relation

		ar=Relation('{[ii,s]->[ar_out]:s=1 and ar_out=inter(ii)}').union(Relation('{[ii,s]->[ar_out]:s=2 and ar_out=inter(ii)}')).union(Relation('{[ii,s]->[ar_out]:s=3 and ar_out=inter(ii)}'))
		data_reordering=Relation('{[k]->[dr_out]:dr_out=sigma(k)}')

		ar_composed=data_reordering.compose(ar)

		ar_res=Relation('{[ii,s]->[dr_out]:s=1 and dr_out=sigma(inter(ii))}').union(Relation('{[ii,s]->[dr_out]:s=2 and dr_out=sigma(inter(ii))}')).union(Relation('{[ii,s]->[dr_out]:s=3 and dr_out=sigma(inter(ii))}'))

		self.failUnless(ar_composed==ar_res,'%s!=%s'%(ar_composed,ar_res))

	#Tests that Relation('{[c]->[d]: d=f(c)}').compose(Relation('{[a]->[b]}')) produces the correct result
	#This is bug #79
	def testComposeRenameBug(self):
		from iegen import Relation

		r=Relation('{[c]->[d]: d=f(c)}').compose(Relation('{[a]->[b]: a=b}'))
		r_res=Relation('{[a]->[d]: d=f(a)}')

		self.failUnless(r==r_res,'%s!=%s'%(r,r_res))

	#Tests that the inner tuple variables of a composition are renamed
	#This is a test to ensure that bug #124 was fixed
	def testComposeRenameInner(self):
		from iegen import Relation

		r=Relation('{[x]->[x,i]}').compose(Relation('{[c42]->[c4]: c42=0 and -1c4+1=0}'))
		r_res=Relation('{[c42]->[x0,i]: c42=0 and -1x0+1=0}')
		self.failUnless(r==r_res,'%s!=%s'%(r,r_res))

	#Tests the _get_prefix_rename_dict method of Relation
	def testGetPrefixRenameDict(self):
		from iegen import Relation

		relation=Relation('{[a,b]->[c,d,e]:1<=a and a<=10}')

		rename=relation._get_prefix_rename_dict(relation.relations[0],'pre')
		rename_res={'a':'pre_in_a','b':'pre_in_b','c':'pre_out_c','d':'pre_out_d','e':'pre_out_e'}

		self.failUnless(rename==rename_res,'%s!=%s'%(rename,rename_res))

	#Tests the _get_prefix_unrename_dict method of Relation
	def testGetPrefixUnrenameDict(self):
		from iegen import Relation

		relation=Relation('{[a,b]->[c,d,e]:1<=a and a<=10}')

		unrename=relation._get_prefix_unrename_dict(relation.relations[0],'pre')
		unrename_res={'pre_in_a':'a','pre_in_b':'b','pre_out_c':'c','pre_out_d':'d','pre_out_e':'e'}

		self.failUnless(unrename==unrename_res,'%s!=%s'%(unrename,unrename_res))

	#Tests the _get_formula_rename_dict method
	def testGetFormulaRenameDict(self):
		from iegen import Relation

		relation1=Relation('{[a_1,b_1]->[ap_1,bp_1]:1<=a_1 and a_1<=10}')
		relation2=Relation('{[b,c]->[bp,cp]}')
		rename=relation1._get_formula_rename_dict(relation1.relations[0],relation2.relations[0])
		rename_res={'a_1':'b','b_1':'c','ap_1':'bp','bp_1':'cp'}

		self.failUnless(rename==rename_res,'%s!=%s'%(rename,rename_res))

	#Tests the is_tautology method
	def testIsTautology(self):
		from iegen import Relation

		relation=Relation('{[a]->[ap]}')
		self.failUnless(relation.is_tautology(),'%s is not a tautology'%relation)

		relation=Relation('{[a]->[ap]: 5=5}')
		self.failUnless(relation.is_tautology(),'%s is not a tautology'%relation)

		relation=Relation('{[a]->[ap]: 5=5}').union(Relation('{[a]->[ap]: 6=6}'))
		self.failUnless(relation.is_tautology(),'%s is not a tautology'%relation)

		relation=Relation('{[a]->[ap]: 5=5}').union(Relation('{[a]->[ap]: 6=6}')).union(Relation('{[a]->[ap]: 3=3}'))
		self.failUnless(relation.is_tautology(),'%s is not a tautology'%relation)

		relation=Relation('{[a]->[ap]: 5=0}')
		self.failIf(relation.is_tautology(),'%s is a tautology'%relation)

		relation=Relation('{[a]->[ap]: 5=0}').union(Relation('{[a]->[ap]: 6=0}'))
		self.failIf(relation.is_tautology(),'%s is a tautology'%relation)

		relation=Relation('{[a]->[ap]: 5=0}').union(Relation('{[a]->[ap]: 6=0}')).union(Relation('{[a]->[ap]: 7=0}'))
		self.failIf(relation.is_tautology(),'%s is a tautology'%relation)

		relation=Relation('{[a]->[ap]: 5=0}').union(Relation('{[a]->[ap]: 5=5}'))
		self.failUnless(relation.is_tautology(),'%s is not a tautology'%relation)

	#Test the is_contradiction method
	def testIsContradiction(self):
		from iegen import Relation

		relation=Relation('{[a]->[ap]}')
		self.failIf(relation.is_contradiction(),'%s is a contradiction'%relation)

		relation=Relation('{[a]->[ap]: 5=5}')
		self.failIf(relation.is_contradiction(),'%s is a contradiction'%relation)

		relation=Relation('{[a]->[ap]: 5=5}').union(Relation('{[a]->[ap]: 6=6}'))
		self.failIf(relation.is_contradiction(),'%s is a contradiction'%relation)

		relation=Relation('{[a]->[ap]: 5=5}').union(Relation('{[a]->[ap]: 6=6}')).union(Relation('{[a]->[ap]: 3=3}'))
		self.failIf(relation.is_contradiction(),'%s is a contradiction'%relation)

		relation=Relation('{[a]->[ap]: 5=0}')
		self.failUnless(relation.is_contradiction(),'%s is not a contradiction'%relation)

		relation=Relation('{[a]->[ap]: 5=0}').union(Relation('{[a]->[ap]: 6=0}'))
		self.failUnless(relation.is_contradiction(),'%s is not a contradiction'%relation)

		relation=Relation('{[a]->[ap]: 5=0}').union(Relation('{[a]->[ap]: 6=0}')).union(Relation('{[a]->[ap]: 7=0}'))
		self.failUnless(relation.is_contradiction(),'%s is not a contradiction'%relation)

		relation=Relation('{[a]->[ap]: 5=0}').union(Relation('{[a]->[ap]: 5=5}'))
		self.failIf(relation.is_contradiction(),'%s is a contradiction'%relation)

	def testVariables(self):
		from iegen import Relation

		rel=Relation('{[a,b]->[ap,bp]: a=ap and b=bp}')
		res=['a','ap','b','bp']

		self.failUnless(res==rel.variables(),'%s!=%s'%(res,rel.variables()))

	def testFunctions(self):
		from iegen import Relation

		rel=Relation('{[a,b]->[ap,bp]: a=f(b) and b=foo(a)}')
		res=['f','foo']

		self.failUnless(res==rel.functions(),'%s!=%s'%(res,rel.functions()))

	def testSymbolics(self):
		from iegen import Relation,Symbolic

		rel=Relation('{[a,b]->[ap,bp]: a=f(n) and b=foo(a)}',[Symbolic('n')])
		res=['n']

		self.failUnless(res==rel.symbolics(),'%s!=%s'%(res,rel.symbolics()))
#------------------------------------

#---------- SparseSet Tests ----------
class SparseSetTestCase(TestCase):

	#Tests that we can create a very simple set
	def testCreation(self):
		from iegen import SparseSet

		SparseSet('{[a]}')

	#Tests that we can get the tuple variable names
	def testTupleVarNames(self):
		from iegen import SparseSet

		set=SparseSet('{[a,b,c]}')

		self.failUnless('a'==set.tuple_vars[0],"First tuple var is not 'a'")
		self.failUnless('b'==set.tuple_vars[1],"Second tuple var is not 'b'")
		self.failUnless('c'==set.tuple_vars[2],"Third tuple var is not 'c'")
		self.failUnless('a'==set.tuple_set[0],"First tuple var is not 'a'")
		self.failUnless('b'==set.tuple_set[1],"Second tuple var is not 'b'")
		self.failUnless('c'==set.tuple_set[2],"Third tuple var is not 'c'")

	#Tests that we can get the symbolics
	def testSymbolics(self):
		from iegen import SparseSet,Symbolic

		set=SparseSet('{[a,b,c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(Symbolic('m')==set.symbolics[0],"First symbolic is not 'm'")
		self.failUnless(Symbolic('n')==set.symbolics[1],"Second symbolic is not 'n'")

	#Tests that we can get the symbolic names
	def testSymbolicNames(self):
		from iegen import SparseSet,Symbolic

		set=SparseSet('{[a,b,c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless('m'==set.symbolic_names[0],"First symbolic is not 'm'")
		self.failUnless('n'==set.symbolic_names[1],"Second symbolic is not 'n'")

	#Tests that we can get the symbolic names
	def testArity(self):
		from iegen import SparseSet,Symbolic

		set=SparseSet('{[a,b,c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(3==set.arity(),"Set's arity is not 3")

	#Test the __str__ method
	def testStr(self):
		from iegen import SparseSet,Symbolic

		set_string='{[a,b]}'
		set=SparseSet(set_string)
		res_string='{[a,b]}'

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

		set_string='{[a,b]: a=10 and b=2n and a>=m}'
		set=SparseSet(set_string,[Symbolic('n'),Symbolic('m')])
		res_string='{[a,b]: a=10 and b=2n and a>=m | m,n}'

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

		set_string='{[a,b]: a=10 and b=2n and a>=m and a+b>=c}'
		set=SparseSet(set_string,[Symbolic('n'),Symbolic('m')])
		res_string='{[a,b]: a=10 and b=2n and a>=m and a+b>=c | m,n}'

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

	def testStrEmptyInequality1(self):
		from iegen import SparseSet

		set_string='{[a,b]: 0>=a+b}'

		set=SparseSet(set_string)

		res_string=set_string

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

	def testStrEmptyInequality2(self):
		from iegen import SparseSet

		set_string='{[a,b]: a+b>=0}'

		set=SparseSet(set_string)

		res_string=set_string

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

	#Test the __repr__ method
	def testRepr(self):
		from iegen import SparseSet,Symbolic

		set_string='{[a,b]: a=10 and b=2n and a>=m}'
		symbolics=[Symbolic('m'),Symbolic('n')]
		set=SparseSet(set_string,symbolics)
		res_string='{[a,b]: a=10 and b=2n and a>=m | m,n}'
		res_string='SparseSet("%s",%s)'%(res_string,repr(symbolics))

		self.failUnless(res_string==repr(set),'%s!=%s'%(repr(set),res_string))

		set_string='{[a,b]: a=10 and b=2n and a>=m and a+b>=c}'
		set=SparseSet(set_string,symbolics)
		res_string='{[a,b]: a=10 and b=2n and a>=m and a+b>=c | m,n}'
		res_string='SparseSet("%s",%s)'%(res_string,repr(symbolics))

		self.failUnless(res_string==repr(set),'%s!=%s'%(repr(set),res_string))

	def testDuplicateConstraint(self):
		from iegen import SparseSet

		set_string='{[a]: a=10 and a=10}'
		set=SparseSet(set_string)
		res_string=str(SparseSet('{[a]: a=10}'))

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

	def testSetEquality(self):
		from iegen import SparseSet

		set1_string='{[a,b]: a=10 and b>=0 and a>=0}'
		set2_string='{[c,d]: c=10 and d>=0 and c>=0}'
		set3_string='{[a,d]: a=10 and d>=0 and a>=0}'

		set1=SparseSet(set1_string)
		set2=SparseSet(set2_string)
		set3=SparseSet(set3_string)

		self.failUnless(set1==set2,'%s!=%s'%(set1,set2))
		self.failUnless(set1==set3,'%s!=%s'%(set1,set3))
		self.failUnless(set2==set3,'%s!=%s'%(set2,set3))

	def testCopy(self):
		from iegen import SparseSet,Symbolic

		set=SparseSet('{[a,b]: a=b and b=n}',symbolics=[Symbolic('n')])
		set_copy=set.copy()

		self.failIf(set_copy is set,'Copy returns same SparseSet instance')
		self.failUnless(set_copy==set,'%s!=%s'%(set_copy,set))

		set=SparseSet('{[a,b]: a=f(b) and b=n}',symbolics=[Symbolic('n')])
		set_copy=set.copy()

		self.failIf(set_copy is set,'Copy returns same SparseSet instance')
		self.failUnless(set_copy==set,'%s!=%s'%(set_copy,set))

	def testSimpleFunction(self):
		from iegen import SparseSet

		set_string='{[a,b]: b=f(a)}'

		set=SparseSet(set_string)
		res_string=str(set)

		self.failUnless(res_string==set_string,'%s!=%s'%(res_string,set_string))

	def testNestedFunction(self):
		from iegen import SparseSet

		set_string='{[a,b]: b=f(g(a))}'

		set=SparseSet(set_string)
		res_string=str(set)

		self.failUnless(res_string==set_string,'%s!=%s'%(res_string,set_string))

	def testTwoArgumentFunction(self):
		from iegen import SparseSet

		set_string='{[a,b,c]: c=f(a,b)}'

		set=SparseSet(set_string)
		res_string=str(set)

		self.failUnless(res_string==set_string,'%s!=%s'%(res_string,set_string))

	def testConstantArgumentFunction(self):
		from iegen import SparseSet

		set_string='{[a,b]: b=f(a,6)}'

		set=SparseSet(set_string)
		res_string=str(set)

		self.failUnless(res_string==set_string,'%s!=%s'%(res_string,set_string))

	#Tests that a frozen set cannot be cleared
	@raises(ValueError)
	def testClearFrozen(self):
		from iegen import SparseSet

		set1=SparseSet('{[a]: a=10}')

		set1.clear()

	def testClear(self):
		from iegen import SparseSet

		set1=SparseSet('{[a,b,c]: a=b and c>10}',freeze=False)

		self.failUnless(1==len(set1.disjunction),'Set does not have exactly one conjunction')
		self.failUnless(2==len(list(set1.disjunction.conjunctions)[0]),'Set conjunction does not have exactly two constraints')

		set1.clear()

		self.failUnless(0==len(set1.disjunction),'Set does not have exactly zero conjunctions')

	@raises(ValueError)
	def testModifyFrozen1(self):
		from iegen import SparseSet,SparseConjunction

		set1=SparseSet('{[a,b,c]}')
		set1.add_conjunction(SparseConjunction())

	@raises(ValueError)
	def testModifyFrozen2(self):
		from iegen import SparseSet,SparseDisjunction

		set1=SparseSet('{[a,b,c]}')
		set1.add_disjunction(SparseDisjunction())

	def testManualConstruction(self):
		from iegen import SparseSet

		set1=SparseSet('{[a,b,c]}',freeze=False)

		#Add conjunction a=b and b>=c
		set1.clear()
		set1.add_conjunction(set1.get_conjunction([set1.get_equality({set1.get_column('a'):1,set1.get_column('b'):-1}),set1.get_inequality({set1.get_column('b'):1,set1.get_column('c'):-1})]))
		set1.freeze()

		set_res=SparseSet('{[a,b,c]: a=b and b>=c}')

		self.failUnless(set1==set_res,'%s!=%s'%(set1,set_res))

	#----------------------------------------
	# Start operation tests

	#Tests that hash doesn't work on an unfrozen set
	@raises(ValueError)
	def testHashUnfrozen(self):
		from iegen import SparseSet

		hash(SparseSet('{[a,b]}',freeze=False))

	#Tests that equality doesn't work on an unfrozen set
	@raises(ValueError)
	def testEqualityUnfrozen1(self):
		from iegen import SparseSet

		SparseSet('{[a,b]}',freeze=False)==SparseSet('{[a,b]}')

	@raises(ValueError)
	def testEqualityUnfrozen2(self):
		from iegen import SparseSet

		SparseSet('{[a,b]}')==SparseSet('{[a,b]}',freeze=False)

	#Tests that union does not allow sets of differing arity
	@raises(ValueError)
	def testUnionDiffArity(self):
		from iegen import SparseSet

		set1=SparseSet('{[]}')
		set2=SparseSet('{[a]}')
		set1.union(set2)

	#Tests that union is not destructive
	def testUnionNonDestructive(self):
		from iegen import SparseSet

		set1=SparseSet('{[a]}')
		set2=SparseSet('{[b]}')
		unioned=set1.union(set2)

		self.failIf(unioned is set1,'%s is %s'%(unioned,set1))
		self.failIf(unioned is set2,'%s is %s'%(unioned,set2))

	#Tests that the union operation doesn't work on an unfrozen set
	@raises(ValueError)
	def testUnionUnfrozen1(self):
		from iegen import SparseSet

		set1=SparseSet('{[a,b]}',freeze=False)
		set2=SparseSet('{[c,d]}')

		set1.union(set2)

	@raises(ValueError)
	def testUnionUnfrozen2(self):
		from iegen import SparseSet

		set1=SparseSet('{[a,b]}')
		set2=SparseSet('{[c,d]}',freeze=False)

		set1.union(set2)

	#Tests the union operation
	def testUnionEmpty(self):
		from iegen import SparseSet

		set1=SparseSet('{[a,b]}')
		set2=SparseSet('{[c,d]}')

		set3=set1.union(set2)

		self.failUnless(1==len(set3.disjunction),'Unioned set should have exactly one conjunction')
		self.failUnless(set3==set1,'%s!=%s'%(set3,set1))
		self.failUnless(set2==set1,'%s!=%s'%(set2,set1))

	def testUnionConstraints(self):
		from iegen import SparseSet

		set1=SparseSet('{[a,b]: a=b}')
		set2=SparseSet('{[c,d]: c=10 and d=10}')

		set_union=set1.union(set2)

		res_union=SparseSet('{[a,b]}',freeze=False)
		res_union.clear()
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_column('b'):-1})]))
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_constant_column():-10}),res_union.get_equality({res_union.get_column('b'):1,res_union.get_constant_column():-10})]))
		res_union.freeze()

		self.failUnless(2==len(set_union.disjunction),'Unioned set should have exactly two conjunctions')
		self.failUnless(set_union==res_union,'%s!=%s'%(set_union,res_union))

		set1=SparseSet('{[a,b]: a=b}')
		set2=SparseSet('{[c,d]: c=d}')

		set_union=set1.union(set2)

		res_union=SparseSet('{[a,b]}',freeze=False)
		res_union.clear()
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_column('b'):-1})]))
		res_union.freeze()

		self.failUnless(1==len(set_union.disjunction),'Unioned set should have exactly one conjunction')
		self.failUnless(set_union==res_union,'%s!=%s'%(set_union,res_union))

	def testUnionStr(self):
		from iegen import SparseSet

		set1=SparseSet('{[a,b]: a=b}')
		set2=SparseSet('{[c,d]: c=10}')

		set_union=set1.union(set2)

		res_str='{[a,b]: a=b} union {[a,b]: a=10}'

		self.failUnless(res_str==str(set_union),'%s!=%s'%(str(set_union),res_str))

	#Tests that the apply operation doesn't work on unfrozen sets/relations
	@raises(ValueError)
	def testApplyUnfrozen1(self):
		from iegen import SparseSet,SparseRelation

		set=SparseSet('{[a,b]: a=b}',freeze=False)
		relation=SparseRelation('{[a]->[b]: b=10}')
		set.apply(relation)

	@raises(ValueError)
	def testApplyUnfrozen2(self):
		from iegen import SparseSet,SparseRelation

		set=SparseSet('{[a,b]: a=b}')
		relation=SparseRelation('{[a]->[b]: b=10}',freeze=False)
		set.apply(relation)

	#Tests that apply is not destructive
	def testApplyNonDestructive(self):
		from iegen import SparseSet,SparseRelation

		set=SparseSet('{[a]}')
		relation=SparseRelation('{[a]->[b]}')
		applied=set.apply(relation)

		self.failIf(applied is set,'%s is %s'%(applied,set))

	#Tests that apply fails when the arity of the set does not match the input arity of the relation
	@raises(ValueError)
	def testApplyArityFail1(self):
		from iegen import SparseSet,SparseRelation

		set=SparseSet('{[a,b]}')
		relation=SparseRelation('{[b]->[b]}')
		applied=set.apply(relation)

	@raises(ValueError)
	def testApplyArityFail2(self):
		from iegen import SparseSet,SparseRelation

		set=SparseSet('{[a,b,c]}')
		relation=SparseRelation('{[a,b]->[e,f]}')
		applied=set.apply(relation)

	#Tests the apply operation
	def testApply(self):
		from iegen import SparseSet,SparseRelation

		set=SparseSet('{[a]:1<=a and a<=10}')
		relation=SparseRelation('{[d]->[e,f]:e=d && -10<=f and f<=0}')

		applied=set.apply(relation)

		applied_res=SparseSet('{[e,f]: 1<=e and e<=10 && -10<=f and f<=0}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests that variable name collisions are handled
	def testApplyRename(self):
		from iegen import SparseSet,SparseRelation

		set=SparseSet('{[b,d]}')
		relation=SparseRelation('{[a,b]->[c,d]}')

		applied=set.apply(relation)

		applied_res=SparseSet('{[c,d]: b0=a and d0=b}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests the apply operation with equality constraints
	def testApplyEquality1(self):
		from iegen import SparseSet,SparseRelation

		set=SparseSet('{[a]}')
		relation=SparseRelation('{[d]->[e,f]:e=d and f=d}')

		applied=set.apply(relation)

		applied_res=SparseSet('{[e,f]: e=f}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	def testApplyEquality2(self):
		from iegen import SparseSet,SparseRelation

		set=SparseSet('{[a]: a=10}')
		relation=SparseRelation('{[b]->[c,d]: b=c and d=10}')

		applied=set.apply(relation)

		applied_res=SparseSet('{[c,d]: c=10 and d=10}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	# End operation tests
	#----------------------------------------
#-------------------------------------

#---------- SparseRelation Tests ----------
class SparseRelationTestCase(TestCase):

	#Tests that we can create a very simple relation
	def testCreation(self):
		from iegen import SparseRelation

		SparseRelation('{[a]->[b]}')

	#Tests that the names bijection is created correctly
	def testTupleVarNames(self):
		from iegen import SparseRelation

		rel=SparseRelation('{[a,b]->[c]}')

		self.failUnless(3==len(rel.tuple_vars),'The relation does not have 3 tuple vars')
		self.failUnless(2==len(rel.tuple_in),'The relation does not have 2 input tuple vars')
		self.failUnless(1==len(rel.tuple_out),'The relation does not have 1 output tuple var')

		self.failUnless('a'==rel.tuple_vars[0],"First tuple var is not 'a'")
		self.failUnless('b'==rel.tuple_vars[1],"Second tuple var is not 'b'")
		self.failUnless('c'==rel.tuple_vars[2],"Third tuple var is not 'c'")
		self.failUnless('a'==rel.tuple_in[0],"First in tuple var is not 'a'")
		self.failUnless('b'==rel.tuple_in[1],"Second in tuple var is not 'b'")
		self.failUnless('c'==rel.tuple_out[0],"First out tuple var is not 'c'")

	#Tests that we can get the symbolics
	def testSymbolics(self):
		from iegen import SparseRelation,Symbolic

		rel=SparseRelation('{[a,b]->[c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(Symbolic('m')==rel.symbolics[0],"First symbolic is not 'm'")
		self.failUnless(Symbolic('n')==rel.symbolics[1],"Second symbolic is not 'n'")

	#Tests that we can get the symbolic names
	def testSymbolicNames(self):
		from iegen import SparseRelation,Symbolic

		rel=SparseRelation('{[a,b]->[c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless('m'==rel.symbolic_names[0],"First symbolic is not 'm'")
		self.failUnless('n'==rel.symbolic_names[1],"Second symbolic is not 'n'")

	#Tests that we can get the symbolic names
	def testArity(self):
		from iegen import SparseRelation,Symbolic

		rel=SparseRelation('{[a,b]->[c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless((2,1)==rel.arity(),"Relation's arity is not (2,1)")
		self.failUnless(2==rel.arity_in(),"Relation's input arity is not 2")
		self.failUnless(1==rel.arity_out(),"Relation's output arity is not 1")

	#Test the __str__ method
	def testStr(self):
		from iegen import SparseRelation,Symbolic

		rel_string='{[a]->[b]}'
		rel=SparseRelation(rel_string)
		res_string='{[a]->[b]}'

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

		rel_string='{[a]->[b]: a=10 and b=2n and a>=m}'
		rel=SparseRelation(rel_string,[Symbolic('n'),Symbolic('m')])
		res_string='{[a]->[b]: a=10 and b=2n and a>=m | m,n}'

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

		rel_string='{[a]->[b]: a=10 and b=2n and a>=m and a+b>=c}'
		rel=SparseRelation(rel_string,[Symbolic('n'),Symbolic('m')])
		res_string='{[a]->[b]: a=10 and b=2n and a>=m and a+b>=c | m,n}'

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

	def testStrEmptyInequality1(self):
		from iegen import SparseRelation

		rel_string='{[a]->[b]: 0>=a+b}'

		rel=SparseRelation(rel_string)

		res_string=rel_string

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

	def testStrEmptyInequality2(self):
		from iegen import SparseRelation

		rel_string='{[a]->[b]: a+b>=0}'

		rel=SparseRelation(rel_string)

		res_string=rel_string

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

	#Test the __repr__ method
	def testRepr(self):
		from iegen import SparseRelation,Symbolic

		rel_string='{[a]->[b]: a=10 and b=2n and a>=m}'
		symbolics=[Symbolic('m'),Symbolic('n')]
		rel=SparseRelation(rel_string,symbolics)
		res_string='{[a]->[b]: a=10 and b=2n and a>=m | m,n}'
		res_string='SparseRelation("%s",%s)'%(res_string,repr(symbolics))

		self.failUnless(res_string==repr(rel),'%s!=%s'%(repr(rel),res_string))

		rel_string='{[a]->[b]: a=10 and b=2n and a>=m and a+b>=c}'
		rel=SparseRelation(rel_string,symbolics)
		res_string='{[a]->[b]: a=10 and b=2n and a>=m and a+b>=c | m,n}'
		res_string='SparseRelation("%s",%s)'%(res_string,repr(symbolics))

		self.failUnless(res_string==repr(rel),'%s!=%s'%(repr(rel),res_string))

	def testDuplicateConstraint(self):
		from iegen import SparseRelation

		rel_string='{[a]->[b]: a=10 and a=10}'
		rel=SparseRelation(rel_string)
		res_string=str(SparseRelation('{[a]->[b]: a=10}'))

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

	def testRelationEquality(self):
		from iegen import SparseRelation

		rel1_string='{[a]->[b]: a=10 and b>=0 and a>=0}'
		rel2_string='{[c]->[d]: c=10 and d>=0 and c>=0}'
		rel3_string='{[a]->[d]: a=10 and d>=0 and a>=0}'

		rel1=SparseRelation(rel1_string)
		rel2=SparseRelation(rel2_string)
		rel3=SparseRelation(rel3_string)

		self.failUnless(rel1==rel2,'%s!=%s'%(rel1,rel2))
		self.failUnless(rel1==rel3,'%s!=%s'%(rel1,rel3))
		self.failUnless(rel2==rel3,'%s!=%s'%(rel2,rel3))

	def testCopy(self):
		from iegen import SparseRelation,Symbolic

		rel=SparseRelation('{[a]->[b]: a=b and b=n}',symbolics=[Symbolic('n')])
		rel_copy=rel.copy()

		self.failIf(rel_copy is rel,'Copy returns same SparseRelation instance')
		self.failUnless(rel_copy==rel,'%s!=%s'%(rel_copy,rel))

		rel=SparseRelation('{[a]->[b]: a=f(b) and b=n}',symbolics=[Symbolic('n')])
		rel_copy=rel.copy()

		self.failIf(rel_copy is rel,'Copy returns same SparseRelation instance')
		self.failUnless(rel_copy==rel,'%s!=%s'%(rel_copy,rel))

	def testSimpleFunction(self):
		from iegen import SparseRelation

		rel_string='{[a]->[b]: b=f(a)}'

		rel=SparseRelation(rel_string)
		res_string=str(rel)

		self.failUnless(res_string==rel_string,'%s!=%s'%(res_string,rel_string))

	def testNestedFunction(self):
		from iegen import SparseRelation

		rel_string='{[a]->[b]: b=f(g(a))}'

		rel=SparseRelation(rel_string)
		res_string=str(rel)

		self.failUnless(res_string==rel_string,'%s!=%s'%(res_string,rel_string))

	def testTwoArgumentFunction(self):
		from iegen import SparseRelation

		rel_string='{[a,b]->[c]: c=f(a,b)}'

		rel=SparseRelation(rel_string)
		res_string=str(rel)

		self.failUnless(res_string==rel_string,'%s!=%s'%(res_string,rel_string))

	def testConstantArgumentFunction(self):
		from iegen import SparseRelation

		rel_string='{[a]->[b]: b=f(a,6)}'

		rel=SparseRelation(rel_string)
		res_string=str(rel)

		self.failUnless(res_string==rel_string,'%s!=%s'%(res_string,rel_string))

	#Tests that a frozen relation cannot be cleared
	@raises(ValueError)
	def testClearFrozen(self):
		from iegen import SparseRelation

		rel=SparseRelation('{[a]->[b]: a=10}')

		rel.clear()

	def testClear(self):
		from iegen import SparseRelation

		rel=SparseRelation('{[a]->[b,c]: a=b and c>10}',freeze=False)

		self.failUnless(1==len(rel.disjunction),'Relation does not have exactly one conjunction')
		self.failUnless(2==len(list(rel.disjunction.conjunctions)[0]),'Relation conjunction does not have exactly two constraints')

		rel.clear()

		self.failUnless(0==len(rel.disjunction),'Relation does not have exactly zero conjunctions')

	@raises(ValueError)
	def testModifyFrozen1(self):
		from iegen import SparseRelation,SparseConjunction

		rel=SparseRelation('{[a]->[b,c]}')
		rel.add_conjunction(SparseConjunction())

	@raises(ValueError)
	def testModifyFrozen2(self):
		from iegen import SparseRelation,SparseDisjunction

		rel=SparseRelation('{[a]->[b,c]}')
		rel.add_disjunction(SparseDisjunction())

	def testManualConstruction(self):
		from iegen import SparseRelation

		rel=SparseRelation('{[a]->[b,c]}',freeze=False)

		#Add conjunction a=b and b>=c
		rel.clear()
		rel.add_conjunction(rel.get_conjunction([rel.get_equality({rel.get_column('a'):1,rel.get_column('b'):-1}),rel.get_inequality({rel.get_column('b'):1,rel.get_column('c'):-1})]))
		rel.freeze()

		rel_res=SparseRelation('{[a]->[b,c]: a=b and b>=c}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	#----------------------------------------
	# Start operation tests

	#Tests that hash doesn't work on an unfrozen relation
	@raises(ValueError)
	def testHashUnfrozen(self):
		from iegen import SparseRelation

		hash(SparseRelation('{[a]->[b]}',freeze=False))

	#Tests that equality doesn't work on an unfrozen relation
	@raises(ValueError)
	def testEqualityUnfrozen1(self):
		from iegen import SparseRelation

		SparseRelation('{[a]->[b]}',freeze=False)==SparseRelation('{[a]->[b]}')

	@raises(ValueError)
	def testEqualityUnfrozen2(self):
		from iegen import SparseRelation

		SparseRelation('{[a]->[b]}')==SparseRelation('{[a]->[b]}',freeze=False)

	#Tests that union does not allow relations of differing arity
	@raises(ValueError)
	def testUnionDiffArity(self):
		from iegen import SparseRelation

		relation1=SparseRelation('{[]->[]}')
		relation2=SparseRelation('{[a]->[a]}')
		relation1.union(relation2)

	#Tests that union is not destructive
	def testUnionNonDestructive(self):
		from iegen import SparseRelation

		relation1=SparseRelation('{[a]->[a]}')
		relation2=SparseRelation('{[b]->[b]}')
		unioned=relation1.union(relation2)

		self.failIf(unioned is relation1,'%s is %s'%(unioned,relation1))
		self.failIf(unioned is relation2,'%s is %s'%(unioned,relation2))

	#Tests that the union operation doesn't work on an unfrozen relation
	@raises(ValueError)
	def testUnionUnfrozen1(self):
		from iegen import SparseRelation

		rel1=SparseRelation('{[a]->[b]}',freeze=False)
		rel2=SparseRelation('{[c]->[d]}')

		rel1.union(rel2)

	@raises(ValueError)
	def testUnionUnfrozen2(self):
		from iegen import SparseRelation

		rel1=SparseRelation('{[a]->[b]}')
		rel2=SparseRelation('{[c]->[d]}',freeze=False)

		rel1.union(rel2)

	#Tests the union operation
	def testUnionEmpty(self):
		from iegen import SparseRelation

		rel1=SparseRelation('{[a]->[b]}')
		rel2=SparseRelation('{[c]->[d]}')

		rel3=rel1.union(rel2)

		self.failUnless(1==len(rel3.disjunction),'Unioned relation should have exactly one conjunction')
		self.failUnless(rel3==rel1,'%s!=%s'%(rel3,rel1))
		self.failUnless(rel2==rel1,'%s!=%s'%(rel2,rel1))

	def testUnionConstraints(self):
		from iegen import SparseRelation

		rel1=SparseRelation('{[a]->[b]: a=b}')
		rel2=SparseRelation('{[c]->[d]: c=10 and d=10}')

		rel_union=rel1.union(rel2)

		res_union=SparseRelation('{[a]->[b]}',freeze=False)
		res_union.clear()
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_column('b'):-1})]))
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_constant_column():-10}),res_union.get_equality({res_union.get_column('b'):1,res_union.get_constant_column():-10})]))
		res_union.freeze()

		self.failUnless(2==len(rel_union.disjunction),'Unioned relation should have exactly two conjunctions')
		self.failUnless(rel_union==res_union,'%s!=%s'%(rel_union,res_union))

		rel1=SparseRelation('{[a]->[b]: a=b}')
		rel2=SparseRelation('{[c]->[d]: c=d}')

		rel_union=rel1.union(rel2)

		res_union=SparseRelation('{[a]->[b]}',freeze=False)
		res_union.clear()
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_column('b'):-1})]))
		res_union.freeze()

		self.failUnless(1==len(rel_union.disjunction),'Unioned relation should have exactly one conjunction')
		self.failUnless(rel_union==res_union,'%s!=%s'%(rel_union,res_union))

	def testUnionStr(self):
		from iegen import SparseRelation

		rel1=SparseRelation('{[a]->[b]: a=b}')
		rel2=SparseRelation('{[c]->[d]: c=10}')

		rel_union=rel1.union(rel2)

		res_str='{[a]->[b]: a=b} union {[a]->[b]: a=10}'

		self.failUnless(res_str==str(rel_union),'%s!=%s'%(str(rel_union),res_str))

	#Tests that the inverse operation doesn't work on an unfrozen relation
	@raises(ValueError)
	def testInverseUnfrozen(self):
		from iegen import SparseRelation

		SparseRelation('{[a]->[b]: a=b}',freeze=False).inverse()

	#Tests the inverse operation
	def testInverseEmpty(self):
		from iegen import SparseRelation

		inverse=SparseRelation('{[a,b]->[c,d]}').inverse()
		res_inverse=SparseRelation('{[c,d]->[a,b]}')

		self.failUnless(inverse==res_inverse,'%s!=%s'%(inverse,res_inverse))
		self.failUnless(str(inverse)==str(res_inverse),'%s!=%s'%(str(inverse),str(res_inverse)))

	#Tests the inverse operation with constraints
	def testInverseConstraints(self):
		from iegen import SparseRelation

		inverse=SparseRelation('{[a,b]->[c,d]:a>=n && b<5 and c+d=15}').inverse()
		res_inverse=SparseRelation('{[c,d]->[a,b]:b<5 and a>=n && c+d=15}')

		self.failUnless(inverse==res_inverse,'%s!=%s'%(inverse,res_inverse))
		self.failUnless(str(inverse)==str(res_inverse),'%s!=%s'%(str(inverse),str(res_inverse)))

	def testInverseArity(self):
		from iegen import SparseRelation

		rel=SparseRelation('{[a,b]->[c,d,e,f,g]}')
		inverse=rel.inverse()

		self.failUnless((2,5)==rel.arity(),'Arity of %s is not (2,5)'%(rel))
		self.failUnless((5,2)==inverse.arity(),'Arity of %s is not (5,2)'%(inverse))

	#Tests that the compose operation doesn't work on unfrozen relations
	@raises(ValueError)
	def testComposeUnfrozen1(self):
		from iegen import SparseRelation

		rel1=SparseRelation('{[a]->[b]: a=b}',freeze=False)
		rel2=SparseRelation('{[a]->[b]: b=10}')
		rel1.compose(rel2)

	@raises(ValueError)
	def testComposeUnfrozen2(self):
		from iegen import SparseRelation

		rel1=SparseRelation('{[a]->[b]: a=b}')
		rel2=SparseRelation('{[a]->[b]: b=10}',freeze=False)
		rel1.compose(rel2)

	#Tests that compose is not destructive
	def testComposeNonDestructive(self):
		from iegen import SparseRelation

		rel1=SparseRelation('{[a]->[a]}')
		rel2=SparseRelation('{[b]->[b]}')
		composed=rel1.compose(rel2)

		self.failIf(composed is rel1,'%s is %s'%(composed,rel1))
		self.failIf(composed is rel2,'%s is %s'%(composed,rel2))

	#Tests that compose fails when the output arity of the second relation does not match the input arity of the first relation
	@raises(ValueError)
	def testComposeArityFail1(self):
		from iegen import SparseRelation

		rel1=SparseRelation('{[a,b]->[c]}')
		rel2=SparseRelation('{[b]->[b]}')
		composed=rel1.compose(rel2)

	@raises(ValueError)
	def testComposeArityFail2(self):
		from iegen import SparseRelation

		rel1=SparseRelation('{[]->[c]}')
		rel2=SparseRelation('{[a,b,c,d]->[e]}')
		composed=rel1.compose(rel2)

	#Tests the compose operation
	def testCompose(self):
		from iegen import SparseRelation

		relation1=SparseRelation('{[a,b]->[c]:1<=a and a<=10 and 1<=b and b<=10}')
		relation2=SparseRelation('{[d]->[e,f]:-10<=d and d<=0}')

		composed=relation1.compose(relation2)

		composed_res=SparseRelation('{[d]->[c]: -10<=d and d<=0}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests that variable name collisions are handled
	def testComposeRename(self):
		from iegen import SparseRelation

		relation1=SparseRelation('{[a,b]->[c,d]}')
		relation2=SparseRelation('{[b,c]->[d,e]}')

		composed=relation1.compose(relation2)

		composed_res=SparseRelation('{[b,c]->[c0,d]: d0=a and e=b0}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests the compose operation with equality constraints
	def testComposeEquality1(self):
		from iegen import SparseRelation

		relation1=SparseRelation('{[a,b]->[c]:c=a}')
		relation2=SparseRelation('{[d]->[e,f]:e=d and f=d}')

		composed=relation1.compose(relation2)

		composed_res=SparseRelation('{[d]->[c]: d=c}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	def testComposeEquality2(self):
		from iegen import SparseRelation

		relation1=SparseRelation('{[a]->[b,c]: a=10}')
		relation2=SparseRelation('{[d,e]->[f]: f=10}')

		composed=relation2.compose(relation1)

		composed_res=SparseRelation('{[a]->[f]: a=10 and f=10}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	def testComposeEquality3(self):
		from iegen import SparseRelation

		relation1=SparseRelation('{[a]->[b,c]: a=10}')
		relation2=SparseRelation('{[d,e]->[f]: f=10}')

		composed=relation1.compose(relation2)

		composed_res=SparseRelation('{[d,e]->[b,c]}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	def testComposeEquality4(self):
		from iegen import SparseRelation

		relation1=SparseRelation('{[a]->[b,c]: a=10}')
		relation2=SparseRelation('{[c,d]->[e]: e=10}')

		composed=relation2.compose(relation1)

		composed_res=SparseRelation('{[a]->[e]: a=10 and e=10}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	def testComposeEquality5(self):
		from iegen import SparseRelation

		relation1=SparseRelation('{[a]->[b,c]: a=10}')
		relation2=SparseRelation('{[c,d]->[e]: e=10}')

		composed=relation1.compose(relation2)

		composed_res=SparseRelation('{[c,d]->[b,c0]}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	# End operation tests
	#----------------------------------------
#------------------------------------------
