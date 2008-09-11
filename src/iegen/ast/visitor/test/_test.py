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
			from iegen.ast.visitor import DFVisitor,TransVisitor,RenameVisitor,SortVisitor,CheckVisitor,IsVarVisitor,IsSymbolicVarVisitor,IsTupleVarVisitor,FindFreeVarEqualityVisitor
		except Exception,e:
			self.fail("Importing classes from iegen.ast.visitor failed: "+str(e))
#----------------------------------

#---------- Depth First Visitor Tests ----------
#Test base visitor class
class DFVisitorTestCase(TestCase):

	#Test that 'self' is returned from the visit method
	def testReturnsSelf(self):
		from iegen.ast.visitor import DFVisitor
		from iegen import Set

		set=Set('{[]}')

		v=DFVisitor()

		self.failUnless(v.visit(set) is v,"visit() method does not return 'self'")
#-----------------------------------------------

#---------- Domain Matrix Translation Tests ----------
#Test translation visitor
class TransVisitorTestCase(TestCase):

	#Test that relations are not supported
	@raises(ValueError)
	def testRelationFailure(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Relation

		rel=Relation('{[]->[]}')
		TransVisitor([]).visit(rel)

	#Test that functions are not supported
	@raises(ValueError)
	def testFuncFailure(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[]:f(a)=1}')
		TransVisitor([]).visit(set)

	#Test that existential variables are not supported
	@raises(ValueError)
	def testExistentialFail(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[a]:a=1 && b=1}')
		TransVisitor([]).visit(set)

	#Make sure the result of the visiting is placed in the mat attribute
	def testResultPresent(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[]}')
		v=TransVisitor([]).visit(set)

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
			v=TransVisitor(params).visit(set)

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

		RenameVisitor({'a':"a'",'b':"b'",'c':"c'"}).visit(set)

		set_renamed=Set("{[a',b',c']: a'>=10 and b'<5 and c'=f(g(c'))}")

		self.failUnless(set==set_renamed,'%s!=%s'%(set,set_renamed))

	#Test that renaming in Sets works as expected with all variables
	def testRenameSetSome(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Set

		set=Set('{[a,b,c]:a>=10 and b<5 and c=f(g(c))}')

		RenameVisitor({'a':"a'",'c':"c'"}).visit(set)

		set_renamed=Set("{[a',b,c']: a'>=10 and b<5 and c'=f(g(c'))}")

		self.failUnless(set==set_renamed,'%s!=%s'%(set,set_renamed))

	#Test that renaming in Sets works as expected with all variables
	def testRenameSetOne(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Set

		set=Set('{[a,b,c]:a>=10 and b<5 and c=f(g(c))}')

		RenameVisitor({'a':"a'"}).visit(set)

		set_renamed=Set("{[a',b,c]: a'>=10 and b<5 and c=f(g(c))}")

		self.failUnless(set==set_renamed,'%s!=%s'%(set,set_renamed))

	#Test that renaming in Relations works as expected
	def testRenameRelationAll(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Relation

		relation=Relation('{[a,b,c]->[d,e,f]:a>=10 and b<5 and c=6 and d=5 and e>=4 and f=g(f)}')

		RenameVisitor({'a':"a'",'b':"b'",'c':"c'",'d':"d'",'e':"e'",'f':"f'"}).visit(relation)

		relation_renamed=Relation("{[a',b',c']->[d',e',f']:a'>=10 and b'<5 and c'=6 and d'=5 and e'>=4 and f'=g(f')}")

		self.failUnless(relation==relation_renamed,'%s!=%s'%(relation,relation_renamed))

	#Test that renaming in Relations works as expected
	def testRenameRelationSome(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Relation

		relation=Relation('{[a,b,c]->[d,e,f]:a>=10 and b<5 and c=6 and d=5 and e>=4 and f=g(f)}')

		RenameVisitor({'b':"b'",'c':"c'",'d':"d'",'f':"f'"}).visit(relation)

		relation_renamed=Relation("{[a,b',c']->[d',e,f']:a>=10 and b'<5 and c'=6 and d'=5 and e>=4 and f'=g(f')}")

		self.failUnless(relation==relation_renamed,'%s!=%s'%(relation,relation_renamed))

	#Test that renaming in Relations works as expected
	def testRenameRelationOne(self):
		from iegen.ast.visitor import RenameVisitor
		from iegen import Relation

		relation=Relation('{[a,b,c]->[d,e,f]:a>=10 and b<5 and c=6 and d=5 and e>=4 and f=g(f)}')

		RenameVisitor({'b':"b'",'f':"f'"}).visit(relation)

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

#---------- Var Visitor Tests ----------
#Test var visitor
class IsVarVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the is_var attribute
	def testResultPresent(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set

		set=Set('{[]}')
		v=IsVarVisitor('a').visit(set)
		self.failUnless(hasattr(v,'is_var'),"IsVarVisitor doesn't place result in 'is_var' property.")

	#Tests that vars in the Symbolics are searched
	def testSearchSymbolics(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation,Symbolic

		set=Set('{[]}',[Symbolic('n')])
		relation=Relation('{[]->[]}',[Symbolic('n')])

		self.failUnless(IsVarVisitor('n').visit(set).is_var,"'n' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('n').visit(relation).is_var,"'n' is not a var in %s"%relation)

	#Tests that vars in variable tuples are searched
	def testSearchVarTuple(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[a]->[b]}')

		self.failUnless(IsVarVisitor('a').visit(set).is_var,"'a' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('a').visit(relation).is_var,"'a' is not a var in %s"%relation)
		self.failUnless(IsVarVisitor('b').visit(relation).is_var,"'b' is not a var in %s"%relation)

	#Tests that vars in the constraints are searched
	def testSearchConstraints(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation

		set=Set('{[]: a>=10 and b=5}')
		relation=Relation('{[]->[]: a>=10 and b=5}')

		self.failUnless(IsVarVisitor('a').visit(set).is_var,"'a' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('b').visit(set).is_var,"'b' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('a').visit(relation).is_var,"'a' is not a var in %s"%relation)
		self.failUnless(IsVarVisitor('b').visit(relation).is_var,"'b' is not a var in %s"%relation)
#---------------------------------------

#---------- Symbolic Var Visitor Tests ----------
#Test var visitor
class IsSymbolicVarVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the is_symbolic_var attribute
	def testResultPresent(self):
		from iegen.ast.visitor import IsSymbolicVarVisitor
		from iegen import Set

		set=Set('{[]}')
		v=IsSymbolicVarVisitor('a').visit(set)
		self.failUnless(hasattr(v,'is_symbolic_var'),"IsSymbolicVarVisitor doesn't place result in 'is_symbolic_var' property.")

	#Tests that vars in the Symbolics are searched
	def testSearchSymbolics(self):
		from iegen.ast.visitor import IsSymbolicVarVisitor
		from iegen import Set,Relation,Symbolic

		set=Set('{[]}',[Symbolic('n')])
		relation=Relation('{[]->[]}',[Symbolic('n')])

		self.failUnless(IsSymbolicVarVisitor('n').visit(set).is_symbolic_var,"'n' is not a symbolic var in %s"%set)
		self.failUnless(IsSymbolicVarVisitor('n').visit(relation).is_symbolic_var,"'n' is not a symbolic var in %s"%relation)

	#Tests that vars in variable tuples are not searched
	def testNoSearchVarTuple(self):
		from iegen.ast.visitor import IsSymbolicVarVisitor
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[a]->[b]}')

		self.failIf(IsSymbolicVarVisitor('a').visit(set).is_symbolic_var,"'a' is a symbolic var in %s"%set)
		self.failIf(IsSymbolicVarVisitor('a').visit(relation).is_symbolic_var,"'a' is a symbolic var in %s"%relation)
		self.failIf(IsSymbolicVarVisitor('b').visit(relation).is_symbolic_var,"'b' is a symbolic var in %s"%relation)

	#Tests that vars in the constraints are not searched
	def testNoSearchConstraints(self):
		from iegen.ast.visitor import IsSymbolicVarVisitor
		from iegen import Set,Relation

		set=Set('{[]: a>=10 and b=5}')
		relation=Relation('{[]->[]: a>=10 and b=5}')

		self.failIf(IsSymbolicVarVisitor('a').visit(set).is_symbolic_var,"'a' is a symbolic var in %s"%set)
		self.failIf(IsSymbolicVarVisitor('b').visit(set).is_symbolic_var,"'b' is a symbolic var in %s"%set)
		self.failIf(IsSymbolicVarVisitor('a').visit(relation).is_symbolic_var,"'a' is a symbolic var in %s"%relation)
		self.failIf(IsSymbolicVarVisitor('b').visit(relation).is_symbolic_var,"'b' is a symbolic var in %s"%relation)
#---------------------------------------

#---------- Tuple Var Visitor Tests ----------
#Test var visitor
class IsTupleVarVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the is_tuple_var attribute
	def testResultPresent(self):
		from iegen.ast.visitor import IsTupleVarVisitor
		from iegen import Set

		set=Set('{[]}')
		v=IsTupleVarVisitor('a').visit(set)
		self.failUnless(hasattr(v,'is_tuple_var'),"IsTupleVarVisitor doesn't place result in 'is_tuple_var' property.")

	#Tests that vars in the Tuples are not searched
	def testNoSearchSymbolics(self):
		from iegen.ast.visitor import IsTupleVarVisitor
		from iegen import Set,Relation,Symbolic

		set=Set('{[]}',[Symbolic('n')])
		relation=Relation('{[]->[]}',[Symbolic('n')])

		self.failIf(IsTupleVarVisitor('n').visit(set).is_tuple_var,"'n' is a tuple var in %s"%set)
		self.failIf(IsTupleVarVisitor('n').visit(relation).is_tuple_var,"'n' is a tuple var in %s"%relation)

	#Tests that vars in variable tuples are searched
	def testSearchVarTuple(self):
		from iegen.ast.visitor import IsTupleVarVisitor
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[a]->[b]}')

		self.failUnless(IsTupleVarVisitor('a').visit(set).is_tuple_var,"'a' is a not tuple var in %s"%set)
		self.failUnless(IsTupleVarVisitor('a').visit(relation).is_tuple_var,"'a' is a not tuple var in %s"%relation)
		self.failUnless(IsTupleVarVisitor('b').visit(relation).is_tuple_var,"'b' is a not tuple var in %s"%relation)

	#Tests that vars in the constraints are not searched
	def testNoSearchConstraints(self):
		from iegen.ast.visitor import IsTupleVarVisitor
		from iegen import Set,Relation

		set=Set('{[]: a>=10 and b=5}')
		relation=Relation('{[]->[]: a>=10 and b=5}')

		self.failIf(IsTupleVarVisitor('a').visit(set).is_tuple_var,"'a' is a tuple var in %s"%set)
		self.failIf(IsTupleVarVisitor('b').visit(set).is_tuple_var,"'b' is a tuple var in %s"%set)
		self.failIf(IsTupleVarVisitor('a').visit(relation).is_tuple_var,"'a' is a tuple var in %s"%relation)
		self.failIf(IsTupleVarVisitor('b').visit(relation).is_tuple_var,"'b' is a tuple var in %s"%relation)
#---------------------------------------

#---------- Find Free Variable Equality Visitor ----------
class FindFreeVarEqualityVisitorTestCase(TestCase):

	#Tests that the visitor finds a simple equality
	def testFindSimpleSet(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[]:a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		equality_res=Equality(NormExp([VarExp(1,'a')],-5))

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor finds a simple equality
	def testFindSimpleRelation(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Relation
		from iegen.ast import Equality,NormExp,VarExp

		set=Relation('{[]->[]:a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		equality_res=Equality(NormExp([VarExp(1,'a')],-5))

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor finds an equality in a collection of equalities
	def testFindInCollection(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:b=5 and a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		equality_res=Equality(NormExp([VarExp(1,'b')],-5))

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor finds an equality in a collection of constraints
	def testFindInConstraints(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=5 and b>=5 and b=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		equality_res=Equality(NormExp([VarExp(1,'b')],-5))

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor finds an equality in a collection of constraints with symbolics
	def testFindInConstraintsWithSymbolic(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=5 and b>=5 and b=5}',[Symbolic('n')])

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		equality_res=Equality(NormExp([VarExp(1,'b')],-5))

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor does not find a free variable with a non-1 and non--1 coefficient
	def testFindCoefficientNeg1(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:-b=5 and b>=5 and a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		equality_res=Equality(NormExp([VarExp(-1,'b')],-5))

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor does not find any equalities
	def testNoFind1(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set

		set=Set('{[a]:a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		self.failUnless(None is equality,'%s is not None'%equality)

	#Tests that the visitor does not find any equalities
	def testNoFind2(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set,Symbolic

		set=Set('{[]:n=5}',[Symbolic('n')])

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		self.failUnless(None is equality,'%s is not None'%equality)

	#Tests that the visitor does not find an equality with func(a)=exp
	def testNoFindFuncEquality(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set

		set=Set('{[a]:f(b)=5 and b>=5 and a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		self.failUnless(None is equality,'%s is not None'%equality)

	#Tests that the visitor does not find an equality with func1(func2(a))=exp
	def testNoFindNestedFuncEquality(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set

		set=Set('{[a]:f(g(b))=5 and b>=5 and a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		self.failUnless(None is equality,'%s is not None'%equality)

	#Tests that the visitor does not find a free variable with a non-1 and non--1 coefficient
	def testNoFindCoefficient(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set

		set=Set('{[a]:5b=5 and b>=5 and a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).equality

		self.failUnless(None is equality,'%s is not None'%equality)
#---------------------------------------------------------
