from unittest import TestCase
from nose.tools import raises

#---------- Import Tests ----------
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
#----------------------------------

#---------- Domain Matrix Translation Tests ----------
#Test translation visitor
class TransVisitorTestCase(TestCase):

	#Test that relations are not supported
	@raises(ValueError)
	def testRelationFailure(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Relation

		rel=Relation('{[]->[]}')
		v=TransVisitor([])
		v.visit(rel)

	#Test that relations are not supported
	@raises(ValueError)
	def testFuncFailure(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[]:f(a)=1}')
		v=TransVisitor([])
		v.visit(set)

	#Test that existential variables are not supported
	@raises(ValueError)
	def testExistentialFail(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[a]:a=1 && b=1}')
		v=TransVisitor([])
		v.visit(set)

	#Make sure the result of the visiting is placed in the mat attribute
	def testResultPresent(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[]}')
		v=TransVisitor([])
		v.visit(set)
		self.failUnless(hasattr(v,'mats'),"TransVisitor doesn't place result in 'mats' property.")

	set_tests=(('{[a]: a=n}',[[[0,1,-1,0]]],['n']),
	           ('{[a,b]: a=n && b=m}',[[[0,1,0,-1,0,0],
	                                   [0,0,1,0,-1,0]]],['n','m']),
	           ('{[a]: 0<a && a<n+1}',[[[1,1,0,-1],
	                              [1,-1,1,0]]],['n']),
	           ('{[a]: 1<=a && a<=n}',[[[1, 1,0,-1],
	                              [1,-1,1, 0]]],['n']),
	           ('{[a,b]: 0<a && a<n+1 && 0<b && b<n+1}',[[[1, 1, 0,0,-1],
	                                                   [1,-1, 0,1, 0],
	                                                   [1, 0, 1,0,-1],
	                                                   [1, 0,-1,1, 0]]],['n']),
	           ('{[a,b]: 1<=a && a<=n && 1<=b && b<=n}',[[[1, 1, 0,0,-1],
	                                                   [1,-1, 0,1, 0],
	                                                   [1, 0, 1,0,-1],
	                                                   [1, 0,-1,1, 0]]],['n']),
	           ('{[a,b]: 0<a && a<n+1 && 0<b && b<m+1}',[[[1, 1, 0,0,0,-1],
	                                                   [1,-1, 0,1,0, 0],
	                                                   [1, 0, 1,0,0,-1],
	                                                   [1, 0,-1,0,1, 0]]],['n','m']),
	           ('{[a,b]: 1<=a && a<=n && 1<=b && b<=m}',[[[1, 1, 0,0,0,-1],
	                                                   [1,-1, 0,1,0, 0],
	                                                   [1, 0, 1,0,0,-1],
	                                                   [1, 0,-1,0,1, 0]]],['n','m']))

	#Test that the sets in set_tests are translated properly
	def testTrans(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		for set_string,res_mats,params in self.set_tests:
			#Create a set from set string
			set=Set(set_string)

			#Visit the set
			v=TransVisitor(params)
			v.visit(set)

			#Sort the rows of the matricies
			for mat in v.mats:
				mat.sort()
			for res_mat in res_mats:
				res_mat.sort()

			#Make sure the translated matrix matches the result matrix
			self.failUnless(v.mats==res_mats,'%s!=%s'%(v.mats,res_mats))
#-----------------------------------------------------
