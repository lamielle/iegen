from unittest import TestCase
from nose.tools import raises

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
			from iegen import MapIR,IterationSpace,DataSpace,IndexArray,AccessRelation,Statement,DataDependence,RTRT,DataPermuteRTRT,IterPermuteRTRT,Set,Relation
		except Exception,e:
			self.fail("Importing classes from iegen failed: "+str(e))
#----------------------------------

#---------- Set Tests ----------
class SetTestCase(TestCase):

	#Tests that we can create a Set by specifying a set string
	def testSetString(self):
		from iegen import Set

		set=Set('{[a]:a>10}')
		set=Set(set_string='{[a]:a>10}')

	#Tests that we can create a Set by specifying a collection of PresSets
	def testSets(self):
		from iegen import Set
		from iegen.parser import PresParser

		set1=PresParser.parse_set('{[a]:a>10}')
		set2=PresParser.parse_set('{[b]:b>10}')

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

		Set('{[]}',[])
	@raises(ValueError)
	def testBothFail2(self):
		from iegen import Set

		Set(set_string='{[]}',sets=[])

	#Tests that all objects in the sets collection must 'look like' PresSets
	@raises(ValueError)
	def testNonPresSetFail(self):
		from iegen import Set
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]}')
		Set(sets=[set,"hello!"])

	#Tests that all objects in the sets collection must 'look like' PresSets
	def testLikePresSet(self):
		from iegen import Set
		from iegen.ast import VarTuple,Conjunction,Node
		from iegen.parser import PresParser

		class DummyPresSet(Node):
			def __init__(self):
				self.tuple_set=VarTuple([])
				self.conjunct=Conjunction([])
			def arity(self):
				return 0
			def apply_visitor(self,visitor):
				visitor.visitPresSet(self)

		set=PresParser.parse_set('{[]}')
		Set(sets=[set,DummyPresSet()])

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

		unioned=unioned.union(set1)
		unioned_res=Set(sets=[pset1,pset2,pset1])

		self.failUnless(unioned==unioned_res,'%s!=%s'%(unioned,unioned_res))

	#Tests that apply fails when the arity of the set does not match the input arity of the relation
	@raises(ValueError)
	def testApplyArityFail1(self):
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[b]->[b]}')
		applied=set.apply(relation)

	@raises(ValueError)
	def testApplyArityFail2(self):
		from iegen import Set,Relation

		set=Set('{[a,b,c]}')
		relation=Relation('{[a,b,c]->[e,f]}')
		applied=set.apply(relation)

	#Tests the apply operation
	def testApply(self):
		from iegen import Set,Relation

		set=Set('{[a]:1<=a and a<=10}')
		relation=Relation('{[d]->[e,f]:e=d && -10<=f and f<=0}')

		applied=set.apply(relation)
		applied_res=Set('{[e,f]: 1<=d and d<=10 && and e=d and -10<=f and f<=0 and a=d}')
		#Once simplification is implemented, this should be the result
		#applied_res=Set('{[e,f]: 1<=e and e<=10 && -10<=f and f<=0}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests the apply operation on a real-world use case from moldyn-FST.in
	def testApplyReal(self):
		from iegen import Set,Relation

		I_0=Set('{ [s1,i,s2] : s1=1 and s2=1 and 0 <= i and i <= (n_atom-1)  }').union(Set('{ [s1,ii,s2] : s1=2 and s2=1 and 0 <= ii and ii <= (n_inter-1)  }')).union(Set('{ [s1,ii,s2] : s1=2 and s2=2 and 0 <= ii  and ii <= (n_inter-1)  }'))
		iter_ssr=Relation('{ [ k, ii, j ] -> [ ii ] : k=2 }')

		I_0_applied=I_0.apply(iter_ssr)

		I_0_res=Set('{ [ii] : s1=1 and s2=1 and 0 <= i and i <= (n_atom-1) and k=2 and s1=k and ii=i and s2=j }').union(Set('{ [ii] : s1=2 and s2=1 and 0 <= ii and ii <= (n_inter-1) and s1=k and i=ii and s2=j and k=2 }')).union(Set('{ [ii] : s1=2 and s2=2 and 0 <= ii  and ii <= (n_inter-1) and s1=k and i=ii and s2=j and k=2 }'))
		#Once simplification is implemented, this should be the result
		#I_0_res=Set('{ [ii] : 0 <= ii and ii <= (n_atom-1) }').union(Set('{ [ii] : 0 <= ii and ii <= (n_inter-1) }')).union(Set('{ [ii] : 0 <= ii  and ii <= (n_inter-1) }'))

		self.failUnless(I_0_applied==I_0_res,'%s!=%s'%(I_0_applied,I_0_res))

		iter_reordering=Relation('{ [ in ] -> [ i ] : i=delta(in) }')
		I_0_applied.apply(iter_reordering)

		I_0_res=Set('{ [i] : s1=1 and s2=1 and 0 <= i and i <= (n_atom-1) and k=2 and s1=k and ii=i and s2=j and in=ii and i=delta(in) }').union(Set('{ [i] : s1=2 and s2=1 and 0 <= ii and ii <= (n_inter-1) and s1=k and i=ii and s2=j and k=2 and in=ii and i=delta(in) }')).union(Set('{ [i] : s1=2 and s2=2 and 0 <= ii  and ii <= (n_inter-1) and s1=k and i=ii and s2=j and k=2 and in=ii and i=delta(in) }'))
		#Once simplification is implemented, this should be the result
		#I_0_res=Set('{ [i] : 0 <= delta(i) and delta(i) <= (n_atom-1) }').union(Set('{ [ii] : 0 <= delta(i) and delta(i) <= (n_inter-1) }')).union(Set('{ [ii] : 0 <= delta(i)  and delta(i) <= (n_inter-1) }'))

		self.failUnless(I_0_applied==I_0_res,'%s!=%s'%(I_0_applied,I_0_res))

	#Tests the apply operation with equality constraints
	def testApplyEquality(self):
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[d]->[e,f]:e=d and f=d}')

		applied=set.apply(relation)
		applied_res=Relation('{[e,f]: a=d and e=d and f=d}')
		#Once simplification is implemented, this should be the result
		#applied_res=Relation('{[e,f]: e=f}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests that the apply operation doesn't choke on duplicate names
	def testApplyRename(self):
		from iegen import Set,Relation

		set=Set('{[a,b]:1<=a and a<=10 and 1<=b and b<=10}')
		relation=Relation('{[a,b]->[b,c]:-10<=a and a<=0}')

		applied=relation1.apply(relation2)
		applied_res=Relation('{[b,c]: -10<=a and a<=0 and 1<=a and a<=10 and 1<=b and b<=10 and a=a and b=b}')
		#Once simplification is implemented, this should be the result
		#applied_res=Relation('{[b,c]:1<=a and a<=10 and 1<=b and b<=10 and -10<=a and a<=0}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests the _get_rename_dict method
	def testGetRenameDict(self):
		from iegen import Set

		set=Set('{[a,b,c]:1<=a and a<=10}')

		rename=set._get_rename_dict(set.sets[0],'pre')
		rename_res={'a':'pre_in_a','b':'pre_in_b','c':'pre_out_c'}

		self.failUnless(rename==rename_res,'%s!=%s'%(rename,rename_res))

	#Tests the _get_unrename_dict method
	def testGetUnrenameDict(self):
		from iegen import Set 

		set=Set('{[a,b]:1<=a and a<=10}')

		unrename=set._get_unrename_dict(set.sets[0],'pre')
		unrename_res={'pre_in_a':'a','pre_in_b':'b'}

		self.failUnless(unrename==unrename_res,'%s!=%s'%(unrename,unrename_res))
#-------------------------------

#---------- Relation Tests ----------
class RelationTestCase(TestCase):

	#Tests that we can create a Relation by specifying a relation string
	def testRelationString(self):
		from iegen import Relation

		relation=Relation('{[a]->[b]:a>10}')
		relation=Relation(relation_string='{[a]->[b]:a>10}')

	#Tests that we can create a Relation by specifying a collection of PresRelations
	def testRelations(self):
		from iegen import Relation
		from iegen.parser import PresParser

		relation1=PresParser.parse_relation('{[a]->[b]:a>10}')
		relation2=PresParser.parse_relation('{[b]->[c]:b>10}')

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

		Relation('{[]->[]}',[])
	@raises(ValueError)
	def testBothFail2(self):
		from iegen import Relation

		Relation(relation_string='{[]->[]}',relations=[])

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
			def arity_in(self):
				return 0
			def arity_out(self):
				return 0
			def apply_visitor(self,visitor):
				visitor.visitPresRelation(self)

		relation=PresParser.parse_relation('{[]->[]}')
		Relation(relations=[relation,DummyPresRelation()])

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
		prelation2=PresParser.parse_relation('{[b]->[b]:b>10}')
		relation1=Relation(relations=[prelation1,prelation2])
		relation2=Relation(relations=[prelation2,prelation1])

		self.failUnless(relation1==relation2,'%s!=%s'%(relation1,relation2))

	#Tests the arity method
	def testArity(self):
		from iegen import Relation
		from iegen.util import lower_gen
		from string import lowercase

		for size in xrange(26):
			var_tuple=lowercase[:size]
			var_tuple='['+','.join(var_tuple)+']'
			relation=Relation('{'+var_tuple+'->'+var_tuple+'}')
			self.failUnless(relation.arity_in()==size,"Input arity of '%s'!=%d"%(relation,size))
			self.failUnless(relation.arity_out()==size,"Output arity of '%s'!=%d"%(relation,size))

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

	#Tests the union operation
	def testUnion(self):
		from iegen import Relation
		from iegen.parser import PresParser

		prelation1=PresParser.parse_relation('{[a]->[a]:a>10}')
		prelation2=PresParser.parse_relation('{[b]->[b]:b>10}')
		relation1=Relation('{[a]->[a]:a>10}')
		relation2=Relation('{[b]->[b]:b>10}')
		unioned=relation1.union(relation2)
		unioned_res=Relation(relations=[prelation1,prelation2])

		self.failUnless(unioned==unioned_res,'%s!=%s'%(unioned,unioned_res))

		unioned=unioned.union(relation1)
		unioned_res=Relation(relations=[prelation1,prelation2,prelation1])

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

	#Tests the compose operation
	def testCompose(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c]:1<=a and a<=10 and 1<=b and b<=10}')
		relation2=Relation('{[d]->[e,f]:-10<=d and d<=0}')

		composed=relation1.compose(relation2)
		composed_res=Relation('{[d]->[c]: -10<=d and d<=0 and 1<=a and a<=10 and 1<=b and b<=10 and a=e and b=f}')
		#Once simplification is implemented, this should be the result
		#composed_res=Relation('{[d]->[c]: -10<=d and d<=0}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests the compose operation on a real-world use case from moldyn-FST.in
	def testComposeReal(self):
		from iegen import Relation

		ar=Relation('{[ii,s]->[ar_out]:s=1 and ar_out=inter(ii)}')
		data_reordering=Relation('{[k]->[dr_out]:dr_out=sigma(k)}')

		ar_composed=data_reordering.compose(ar)
		ar_res=Relation('{[ii,s]->[dr_out]:s=1 and ar_out=inter(ii) and dr_out=sigma(k) and ar_out=k}')
		#Once simplification is implemented, this should be the result
		#ar_res=Relation('{[ii,s]->[dr_out]:s=1 and dr_out=sigma(inter(ii))}')

		self.failUnless(ar_composed==ar_res,'%s!=%s'%(ar_composed,ar_res))

	#Tests the compose operation with equality constraints
	def testComposeEquality(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c]:c=a}')
		relation2=Relation('{[d]->[e,f]:e=d and f=d}')

		composed=relation1.compose(relation2)
		composed_res=Relation('{[d]->[c]: a=e and b=f and e=d and f=d and c=a}')
		#Once simplification is implemented, this should be the result
		#composed_res=Relation('{[d]->[c]: d=c}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests that the compose operation doesn't choke on duplicate names
	def testComposeRename(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c]:1<=a and a<=10 and 1<=b and b<=10}')
		relation2=Relation('{[a]->[b,c]:-10<=a and a<=0}')

		composed=relation1.compose(relation2)
		composed_res=Relation('{[a]->[c]: -10<=a and a<=0 and 1<=a and a<=10 and 1<=b and b<=10 and a=b and b=c}')
		#Once simplification is implemented, this should be the result
		#composed_res=Relation('{[a]->[c]: -10<=a and a<=0}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests the _get_rename_dict method of Relation
	def testGetRenameDict(self):
		from iegen import Relation

		relation=Relation('{[a,b]->[c,d,e]:1<=a and a<=10}')

		rename=relation._get_rename_dict(relation.relations[0],'pre')
		rename_res={'a':'pre_in_a','b':'pre_in_b','c':'pre_out_c','d':'pre_out_d','e':'pre_out_e'}

		self.failUnless(rename==rename_res,'%s!=%s'%(rename,rename_res))

	#Tests the _get_unrename_dict method of Relation
	def testGetUnrenameDict(self):
		from iegen import Relation

		relation=Relation('{[a,b]->[c,d,e]:1<=a and a<=10}')

		unrename=relation._get_unrename_dict(relation.relations[0],'pre')
		unrename_res={'pre_in_a':'a','pre_in_b':'b','pre_out_c':'c','pre_out_d':'d','pre_out_e':'e'}

		self.failUnless(unrename==unrename_res,'%s!=%s'%(unrename,unrename_res))
#------------------------------------
