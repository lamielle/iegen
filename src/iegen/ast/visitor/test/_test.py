from unittest import TestCase
from nose.tools import assert_raises

#Test importing of iegen.ast.visitor
class ImportTestCase(TestCase):

	#Test simple importing of iegen.ast.visitor
	def testImport(self):
		try:
			import iegen.ast.visitor
		except Exception,e:
			self.fail("'import iegen.ast.visitor' failed: "+str(e))

	#Test simple importing of iegen.ast.visitor classes
	def testNameImport(self):
		try:
			from iegen.ast.visitor import DFVisitor,TransVisitor
		except Exception,e:
			self.fail("Importing classes from iegen.ast.visitor failed: "+str(e))

#Test translation visitor
class TransVisitorTestCase(TestCase):

	#Test that relations are not supported
	def testRelationFailure(self):
		from iegen.ast.visitor import TransVisitor
		from iegen.parser import PresParser

		rel=PresParser.parse_relation('{[]->[]}')
		v=TransVisitor([])
		assert_raises(ValueError,v.visit,rel)

	#Test that relations are not supported
	def testFuncFailure(self):
		from iegen.ast.visitor import TransVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]:f(a)=1}')
		v=TransVisitor([])
		assert_raises(ValueError,v.visit,set)

	#Test that existential variables are not supported
	def testExistentialFail(self):
		from iegen.ast.visitor import TransVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[a]:a=1 && b=1}')
		v=TransVisitor([])
		assert_raises(ValueError,v.visit,set)

	#Make sure the result of the visiting is placed in the mat property
	def testResultPresent(self):
		from iegen.ast.visitor import TransVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction

		set=PresSet(VarTuple([]),Conjunction([]))
		v=TransVisitor([])
		v.visit(set)
		self.failUnless(hasattr(v,'mat'),"TransVisitor doesn't place result in 'mat' property.")

	set_tests=(('{[a]: a=n}',[[0,1,-1,0]],['n']),
	           ('{[a,b]: a=n && b=m}',[[0,1,0,-1,0,0],
	                                   [0,0,1,0,-1,0]],['n','m']),
	           ('{[a]: 0<a && a<n+1}',[[1,1,0,-1],
	                              [1,-1,1,0]],['n']),
	           ('{[a]: 1<=a && a<=n}',[[1, 1,0,-1],
	                              [1,-1,1, 0]],['n']),
	           ('{[a,b]: 0<a && a<n+1 && 0<b && b<n+1}',[[1, 1, 0,0,-1],
	                                                   [1,-1, 0,1, 0],
	                                                   [1, 0, 1,0,-1],
	                                                   [1, 0,-1,1, 0]],['n']),
	           ('{[a,b]: 1<=a && a<=n && 1<=b && b<=n}',[[1, 1, 0,0,-1],
	                                                   [1,-1, 0,1, 0],
	                                                   [1, 0, 1,0,-1],
	                                                   [1, 0,-1,1, 0]],['n']),
	           ('{[a,b]: 0<a && a<n+1 && 0<b && b<m+1}',[[1, 1, 0,0,0,-1],
	                                                   [1,-1, 0,1,0, 0],
	                                                   [1, 0, 1,0,0,-1],
	                                                   [1, 0,-1,0,1, 0]],['n','m']),
	           ('{[a,b]: 1<=a && a<=n && 1<=b && b<=m}',[[1, 1, 0,0,0,-1],
	                                                   [1,-1, 0,1,0, 0],
	                                                   [1, 0, 1,0,0,-1],
	                                                   [1, 0,-1,0,1, 0]],['n','m']))
	#Test that the sets in set_tests are translated properly
	def testTrans(self):
		from iegen.ast.visitor import TransVisitor
		from iegen.parser import PresParser

		for set_test in self.set_tests:
			#Unpack the test tuple
			set_string=set_test[0]
			res_mat=set_test[1]
			params=set_test[2]

			#Create a set from set string
			set=PresParser.parse_set(set_string)

			#Visit the set
			v=TransVisitor(params)
			v.visit(set)

			#Make sure the translated matrix matches the result matrix
			self.failUnless(v.mat==res_mat,'%s!=%s'%(v.mat,res_mat))