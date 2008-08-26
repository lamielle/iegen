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
				self.set_tuple=VarTuple([])
				self.conjunct=Conjunction([])
			def arity(self):
				return 0

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
		from iegen.ast import PresSet,VarTuple,Conjunction

		set_str="Set(sets=[PresSet(VarTuple(['a']),Conjunction([]))])"
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
				self.in_tuple=VarTuple([])
				self.out_tuple=VarTuple([])
				self.conjunct=Conjunction([])
			def arity_in(self):
				return 0
			def arity_out(self):
				return 0

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
		from iegen.ast import PresRelation,VarTuple,Conjunction

		relation_str="Relation(relations=[PresRelation(VarTuple(['a']),VarTuple(['b']),Conjunction([]))])"
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

	#Tests the compose operation
	def testCompose(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c]:1<=a and a<=10 and 1<=b and b<=10}')
		relation2=Relation('{[a]->[b,c]:-10<=a and a<=0}')

		composed=relation1.compose(relation2)
		composed_res=Relation('{[a]->[c]: -10<=a and a<=0}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

#------------------------------------
