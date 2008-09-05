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
			from iegen.ast.visitor import DFVisitor,TransVisitor,RenameVisitor,SortVisitor,CheckVisitor
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

	#Test that functions are not supported
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

#---------- Renaming Visitor Tests ----------
#Test renaming visitor
class RenameVisitorTestCase(TestCase):

	#Test that renaming in Sets works as expected with all variables
	def testRenameSetAll(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Set

		set=Set('{[a,b,c]:a>=10 and b<5 and c=f(g(c))}')

		v=RenameVisitor({'a':"a'",'b':"b'",'c':"c'"})

		v.visit(set)

		set_renamed=Set("{[a',b',c']: a'>=10 and b'<5 and c'=f(g(c'))}")

		self.failUnless(set==set_renamed,'%s!=%s'%(set,set_renamed))

	#Test that renaming in Sets works as expected with all variables
	def testRenameSetSome(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Set

		set=Set('{[a,b,c]:a>=10 and b<5 and c=f(g(c))}')

		v=RenameVisitor({'a':"a'",'c':"c'"})

		v.visit(set)

		set_renamed=Set("{[a',b,c']: a'>=10 and b<5 and c'=f(g(c'))}")

		self.failUnless(set==set_renamed,'%s!=%s'%(set,set_renamed))

	#Test that renaming in Sets works as expected with all variables
	def testRenameSetOne(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Set

		set=Set('{[a,b,c]:a>=10 and b<5 and c=f(g(c))}')

		v=RenameVisitor({'a':"a'"})

		v.visit(set)

		set_renamed=Set("{[a',b,c]: a'>=10 and b<5 and c=f(g(c))}")

		self.failUnless(set==set_renamed,'%s!=%s'%(set,set_renamed))

	#Test that renaming in Relations works as expected
	def testRenameRelationAll(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Relation

		relation=Relation('{[a,b,c]->[d,e,f]:a>=10 and b<5 and c=6 and d=5 and e>=4 and f=g(f)}')

		v=RenameVisitor({'a':"a'",'b':"b'",'c':"c'",'d':"d'",'e':"e'",'f':"f'"})

		v.visit(relation)

		relation_renamed=Relation("{[a',b',c']->[d',e',f']:a'>=10 and b'<5 and c'=6 and d'=5 and e'>=4 and f'=g(f')}")

		self.failUnless(relation==relation_renamed,'%s!=%s'%(relation,relation_renamed))

	#Test that renaming in Relations works as expected
	def testRenameRelationSome(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Relation

		relation=Relation('{[a,b,c]->[d,e,f]:a>=10 and b<5 and c=6 and d=5 and e>=4 and f=g(f)}')

		v=RenameVisitor({'b':"b'",'c':"c'",'d':"d'",'f':"f'"})

		v.visit(relation)

		relation_renamed=Relation("{[a,b',c']->[d',e,f']:a>=10 and b'<5 and c'=6 and d'=5 and e>=4 and f'=g(f')}")

		self.failUnless(relation==relation_renamed,'%s!=%s'%(relation,relation_renamed))

	#Test that renaming in Relations works as expected
	def testRenameRelationOne(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Relation

		relation=Relation('{[a,b,c]->[d,e,f]:a>=10 and b<5 and c=6 and d=5 and e>=4 and f=g(f)}')

		v=RenameVisitor({'b':"b'",'f':"f'"})

		v.visit(relation)

		relation_renamed=Relation("{[a,b',c]->[d,e,f']:a>=10 and b'<5 and c=6 and d=5 and e>=4 and f'=g(f')}")

		self.failUnless(relation==relation_renamed,'%s!=%s'%(relation,relation_renamed))
#--------------------------------------------

#---------- Sort Visitor Tests ----------
#Test sort visitor
class SortVisitorTestCase(TestCase):

	#Tests that the _set_largest_exp method of Equality is called following sorting all of the lists in the Set/Relation object
	#BUG FIX:
	#This tests a subtle bug in which the largest expression of the Equality was selected first
	#followed by sorting the list of terms in this expression
	#Since the terms' order may change, it is possible that the largest expression was not selected after all
	def testSortChooseLargestExpLast(self):
		from iegen import Set
		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,NormExp,VarExp
		from iegen.ast.visitor import RenameVisitor,SortVisitor

		unrename={'form1_s2': 's2', 'form1_s1': 's1', 'form2_in_k': 'k', 'form2_in_j': 'j'}

		set=Set(sets=[PresSet(VarTuple([]),Conjunction([Equality(NormExp([VarExp(-1,'form2_in_k'), VarExp(1,'form1_s1')],0)), Equality(NormExp([VarExp(-1,'form2_in_j'), VarExp(1,'form1_s2')],0))]))])

		RenameVisitor(unrename).visit(set)
		SortVisitor().visit(set)

		set_res=Set('{[]: k=s1 and j=s2}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))
#----------------------------------------
