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
		from iegen.ast import Node
		from iegen.parser import PresParser

		class DummyPresSet(Node):
			def __init__(self):
				self.set_tuple=None
				self.conjunct=None
			def arity(self):
				return 0

		set=PresParser.parse_set('{[]}')
		Set(sets=[set,DummyPresSet()])

	#Tests that we cannot create a set from two PresSets of differing arity
	@raises(ValueError)
	def testDiffArity(self):
		from iegen import Set
		from iegen.parser import PresParser

		set1=PresParser.parse_set('{[a]:a>10}')
		set2=PresParser.parse_set('{[a,b]:b>10}')
		Set(sets=[set1,set2])

	#Tests the __repr__ method
	def testRepr(self):
		from iegen import Set
		from iegen.ast import PresSet,VarTuple,Conjunction

		set_str="Set(sets=[PresSet(VarTuple(['a']),Conjunction([]))])"
		exec('set='+set_str)
		self.failUnless(repr(set)==set_str,'%s!=%s'%(repr(set),set_str))

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
		from iegen.ast import Node
		from iegen.parser import PresParser

		class DummyPresRelation(Node):
			def __init__(self):
				self.in_tuple=None
				self.out_tuple=None
				self.conjunct=None
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
#------------------------------------
