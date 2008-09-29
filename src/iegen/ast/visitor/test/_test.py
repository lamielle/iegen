from unittest import TestCase
from iegen.lib.nose.tools import raises

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
			from iegen.ast.visitor import DFVisitor,TransVisitor,RenameVisitor,SortVisitor,CheckVisitor,IsVarVisitor,FindFreeVarEqualityVisitor,MergeExpTermsVisitor,RemoveEmptyConstraintsVisitor,RemoveFreeVarEqualityVisitor,RemoveDuplicateFormulasVisitor,RemoveSymbolicsVisitor
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
		TransVisitor().visit(rel)

	#Test that PresRelations are not supported
	@raises(ValueError)
	def testPresRelationFailure(self):
		from iegen.ast.visitor import TransVisitor
		from iegen.parser import PresParser

		rel=PresParser.parse_relation('{[]->[]}')
		TransVisitor().visit(rel)

	#Test that functions are not supported
	@raises(ValueError)
	def testFuncFailure(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[]:f(a)=1}')
		TransVisitor().visit(set)

	#Test that existential variables are not supported
	@raises(ValueError)
	def testExistentialFail(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=1}')
		set.sets[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],1)))
		TransVisitor().visit(set)

	#Make sure the result of the visiting is placed in the mat attribute
	def testResultPresent(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[]}')
		v=TransVisitor().visit(set)

		self.failUnless(hasattr(v,'mats'),"TransVisitor doesn't place result in the 'mats' property.")

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
		from iegen import Set,Symbolic

		for set_string,res_mats,params in self.set_tests:
			#Create a list of symbolics for the set
			symbolics=[Symbolic(param) for param in params]

			#Create a set from the set string
			set=Set(set_string,symbolics)

			#Visit the set
			v=TransVisitor().visit(set)

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

	#Make sure the results of the visiting are placed in the is_var, is_symbolic_var, is_constraint_var, and is_tuple_var attributes
	def testResultPresent(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set

		set=Set('{[]}')
		v=IsVarVisitor('a').visit(set)
		self.failUnless(hasattr(v,'is_var'),"IsVarVisitor doesn't place result in the 'is_var' property.")
		self.failUnless(hasattr(v,'is_symbolic_var'),"IsVarVisitor doesn't place result in the 'is_symbolic_var' property.")
		self.failUnless(hasattr(v,'is_constraint_var'),"IsVarVisitor doesn't place result in the 'is_constraint_var' property.")
		self.failUnless(hasattr(v,'is_tuple_var'),"IsVarVisitor doesn't place result in the 'is_tuple_var' property.")

	#Tests that vars in the Symbolics are searched
	def testIsVarSearchSymbolics(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation,Symbolic

		set=Set('{[]}')
		set.sets[0].symbolics.append(Symbolic('n'))

		relation=Relation('{[]->[]}')
		relation.relations[0].symbolics.append(Symbolic('n'))

		self.failUnless(IsVarVisitor('n').visit(set).is_var,"'n' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('n').visit(relation).is_var,"'n' is not a var in %s"%relation)

	#Tests that vars in variable tuples are searched
	def testIsVarSearchVarTuple(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[a]->[b]}')

		self.failUnless(IsVarVisitor('a').visit(set).is_var,"'a' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('a').visit(relation).is_var,"'a' is not a var in %s"%relation)
		self.failUnless(IsVarVisitor('b').visit(relation).is_var,"'b' is not a var in %s"%relation)

	#Tests that vars in the constraints are searched
	def testIsVarSearchConstraints(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[]}')
		set.sets[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.sets[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.relations[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		self.failUnless(IsVarVisitor('a').visit(set).is_var,"'a' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('b').visit(set).is_var,"'b' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('a').visit(relation).is_var,"'a' is not a var in %s"%relation)
		self.failUnless(IsVarVisitor('b').visit(relation).is_var,"'b' is not a var in %s"%relation)

	#Tests that vars in the Symbolics are searched
	def testIsSymSearchSymbolics(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation,Symbolic

		set=Set('{[]}')
		set.sets[0].symbolics.append(Symbolic('n'))

		relation=Relation('{[]->[]}')
		relation.relations[0].symbolics.append(Symbolic('n'))

		self.failUnless(IsVarVisitor('n').visit(set).is_symbolic_var,"'n' is not a symbolic var in %s"%set)
		self.failUnless(IsVarVisitor('n').visit(relation).is_symbolic_var,"'n' is not a symbolic var in %s"%relation)

	#Tests that vars in variable tuples are not searched
	def testIsSymNoSearchVarTuple(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[a]->[b]}')

		self.failIf(IsVarVisitor('a').visit(set).is_symbolic_var,"'a' is a symbolic var in %s"%set)
		self.failIf(IsVarVisitor('a').visit(relation).is_symbolic_var,"'a' is a symbolic var in %s"%relation)
		self.failIf(IsVarVisitor('b').visit(relation).is_symbolic_var,"'b' is a symbolic var in %s"%relation)

	#Tests that vars in the constraints are not searched
	def testIsSymNoSearchConstraints(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[]}')
		set.sets[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.sets[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.relations[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		self.failIf(IsVarVisitor('a').visit(set).is_symbolic_var,"'a' is a symbolic var in %s"%set)
		self.failIf(IsVarVisitor('b').visit(set).is_symbolic_var,"'b' is a symbolic var in %s"%set)
		self.failIf(IsVarVisitor('a').visit(relation).is_symbolic_var,"'a' is a symbolic var in %s"%relation)
		self.failIf(IsVarVisitor('b').visit(relation).is_symbolic_var,"'b' is a symbolic var in %s"%relation)

	#Tests that vars in the Symbolics are searched
	def testIsConstraintNoSearchSymbolics(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation,Symbolic

		set=Set('{[]}',[Symbolic('n')])
		set.sets[0].symbolics.append(Symbolic('n'))

		relation=Relation('{[]->[]}')
		relation.relations[0].symbolics.append(Symbolic('n'))

		self.failIf(IsVarVisitor('n').visit(set).is_constraint_var,"'n' is a constraint var in %s"%set)
		self.failIf(IsVarVisitor('n').visit(relation).is_constraint_var,"'n' is a constraint var in %s"%relation)

	#Tests that vars in variable tuples are not searched
	def testIsConstraintNoSearchVarTuple(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[a]->[b]}')

		self.failIf(IsVarVisitor('a').visit(set).is_constraint_var,"'a' is a constraint var in %s"%set)
		self.failIf(IsVarVisitor('a').visit(relation).is_constraint_var,"'a' is a constraint var in %s"%relation)
		self.failIf(IsVarVisitor('b').visit(relation).is_constraint_var,"'b' is a constraint var in %s"%relation)

	#Tests that vars in the constraints are not searched
	def testIsConstraintSearchConstraints(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[]}')
		set.sets[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.sets[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.relations[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		self.failUnless(IsVarVisitor('a').visit(set).is_constraint_var,"'a' is not a constraint var in %s"%set)
		self.failUnless(IsVarVisitor('b').visit(set).is_constraint_var,"'b' is not a constraint var in %s"%set)
		self.failUnless(IsVarVisitor('a').visit(relation).is_constraint_var,"'a' is not a constraint var in %s"%relation)
		self.failUnless(IsVarVisitor('b').visit(relation).is_constraint_var,"'b' is not a constraint var in %s"%relation)

	#Tests that vars in the Tuples are not searched
	def testIsTupleNoSearchSymbolics(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation,Symbolic

		set=Set('{[]}',[Symbolic('n')])
		set.sets[0].symbolics.append(Symbolic('n'))

		relation=Relation('{[]->[]}')
		relation.relations[0].symbolics.append(Symbolic('n'))

		self.failIf(IsVarVisitor('n').visit(set).is_tuple_var,"'n' is a tuple var in %s"%set)
		self.failIf(IsVarVisitor('n').visit(relation).is_tuple_var,"'n' is a tuple var in %s"%relation)

	#Tests that vars in variable tuples are searched
	def testIsTupleSearchVarTuple(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[a]->[b]}')

		self.failUnless(IsVarVisitor('a').visit(set).is_tuple_var,"'a' is a not tuple var in %s"%set)
		self.failUnless(IsVarVisitor('a').visit(relation).is_tuple_var,"'a' is a not tuple var in %s"%relation)
		self.failUnless(IsVarVisitor('b').visit(relation).is_tuple_var,"'b' is a not tuple var in %s"%relation)

	#Tests that vars in the constraints are not searched
	def testIsTupleNoSearchConstraints(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Set,Relation
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[]}')
		set.sets[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.sets[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.relations[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		self.failIf(IsVarVisitor('a').visit(set).is_tuple_var,"'a' is a tuple var in %s"%set)
		self.failIf(IsVarVisitor('b').visit(set).is_tuple_var,"'b' is a tuple var in %s"%set)
		self.failIf(IsVarVisitor('a').visit(relation).is_tuple_var,"'a' is a tuple var in %s"%relation)
		self.failIf(IsVarVisitor('b').visit(relation).is_tuple_var,"'b' is a tuple var in %s"%relation)
#---------------------------------------

#---------- Find Free Variable Equality Visitor ----------
class FindFreeVarEqualityVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the var_equality_tuple attribute
	def testResultPresent(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set

		set=Set('{[]}')
		v=FindFreeVarEqualityVisitor().visit(set)
		self.failUnless(hasattr(v,'var_equality_tuple'),"FindFreeVarEqualityVisitor doesn't place result in the 'var_equality_tuple' property.")

	#Tests that the visitor finds a simple equality
	def testFindSimpleSet(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[]}')
		set.sets[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'a')],-5)))

		equality=FindFreeVarEqualityVisitor().visit(set).var_equality_tuple

		eq=Equality(NormExp([VarExp(1,'a')],-5))
		var=eq.exp.terms[0]
		equality_res=(var,eq)

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor finds a simple equality
	def testFindSimpleRelation(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Relation
		from iegen.ast import Equality,NormExp,VarExp

		relation=Relation('{[]->[]:a=5}')
		relation.relations[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'a')],-5)))

		equality=FindFreeVarEqualityVisitor().visit(relation).var_equality_tuple

		eq=Equality(NormExp([VarExp(1,'a')],-5))
		var=eq.exp.terms[0]
		equality_res=(var,eq)

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor finds an equality in a collection of equalities
	def testFindInCollection(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=5}')
		set.sets[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],-5)))

		equality=FindFreeVarEqualityVisitor().visit(set).var_equality_tuple

		eq=Equality(NormExp([VarExp(1,'b')],-5))
		var=eq.exp.terms[0]
		equality_res=(var,eq)

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor finds an equality in a collection of constraints
	def testFindInConstraints(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a]:a=5}')
		set.sets[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],-5)))
		set.sets[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(1,'b')],-5)))

		equality=FindFreeVarEqualityVisitor().visit(set).var_equality_tuple

		eq=Equality(NormExp([VarExp(1,'b')],-5))
		var=eq.exp.terms[0]
		equality_res=(var,eq)

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor finds an equality in a collection of constraints with symbolics
	def testFindInConstraintsWithSymbolic(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a]:a=5}',[Symbolic('n')])
		set.sets[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(1,'b')],-5)))
		set.sets[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(1,'b')],-5)))

		equality=FindFreeVarEqualityVisitor().visit(set).var_equality_tuple

		eq=Equality(NormExp([VarExp(1,'b')],-5))
		var=eq.exp.terms[0]
		equality_res=(var,eq)

		self.failUnless(equality_res==equality,'%s!=%s'%(equality_res,equality))

	#Tests that the visitor does not find a free variable with a non-1 and non--1 coefficient
	def testFindCoefficientNeg1(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a]: a=5}')
		set.sets[0].conjunct.constraint_list.append(Equality(NormExp([VarExp(-6,'b')],5)))
		set.sets[0].conjunct.constraint_list.append(Inequality(NormExp([VarExp(1,'b')],-5)))

		equality=FindFreeVarEqualityVisitor().visit(set).var_equality_tuple

		self.failUnless(None is equality,'%s is not None'%equality)

	#Tests that the visitor does not find any equalities
	def testNoFind1(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set

		set=Set('{[a]:a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).var_equality_tuple

		self.failUnless(None is equality,'%s is not None'%equality)

	#Tests that the visitor does not find any equalities
	def testNoFind2(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set,Symbolic

		set=Set('{[]:n=5}',[Symbolic('n')])

		equality=FindFreeVarEqualityVisitor().visit(set).var_equality_tuple

		self.failUnless(None is equality,'%s is not None'%equality)

	#Tests that the visitor does not find an equality with func(a)=exp
	def testNoFindFuncEquality(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set

		set=Set('{[a]:f(b)=5 and b>=5 and a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).var_equality_tuple

		self.failUnless(None is equality,'%s is not None'%equality)

	#Tests that the visitor does not find an equality with func1(func2(a))=exp
	def testNoFindNestedFuncEquality(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set

		set=Set('{[a]:f(g(b))=5 and b>=5 and a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).var_equality_tuple

		self.failUnless(None is equality,'%s is not None'%equality)

	#Tests that the visitor does not find a free variable with a non-1 and non--1 coefficient
	def testNoFindCoefficient(self):
		from iegen.ast.visitor import FindFreeVarEqualityVisitor
		from iegen import Set

		set=Set('{[a]:5b=5 and b>=5 and a=5}')

		equality=FindFreeVarEqualityVisitor().visit(set).var_equality_tuple

		self.failUnless(None is equality,'%s is not None'%equality)
#---------------------------------------------------------

#---------- Merge Expression Terms Visitor ----------
class MergeExpTermsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the merged_terms attribute
	def testResultPresent(self):
		from iegen.ast.visitor import MergeExpTermsVisitor
		from iegen import Set

		set=Set('{[]}')
		v=MergeExpTermsVisitor().visit(set)
		self.failUnless(hasattr(v,'merged_terms'),"MergeExpTermsVisitor doesn't place result in the 'merged_terms' property.")

	#Tests that False is the result of not merging anything
	def testNoMerge(self):
		from iegen.ast.visitor import MergeExpTermsVisitor
		from iegen.ast import NormExp,VarExp,FuncExp

		e=NormExp([],0)
		e.terms=[VarExp(1,'a'),FuncExp(1,'f',[])]
		merged_terms=MergeExpTermsVisitor().visit(e).merged_terms
		e.terms.sort()

		e_res=NormExp([VarExp(1,'a'),FuncExp(1,'f',[])],0)

		self.failUnless(e_res==e,'%s!=%s'%(e_res,e))
		self.failUnless(False==merged_terms,'merged_terms!=False')

	#Tests that variables are merged
	def testMergeVars(self):
		from iegen.ast.visitor import MergeExpTermsVisitor
		from iegen.ast import NormExp,VarExp

		e=NormExp([],0)
		e.terms=[VarExp(1,'a'),VarExp(2,'a'),VarExp(3,'a')]
		merged_terms=MergeExpTermsVisitor().visit(e).merged_terms
		e.terms.sort()

		e_res=NormExp([VarExp(6,'a')],0)

		self.failUnless(e_res==e,'%s!=%s'%(e_res,e))
		self.failUnless(True==merged_terms,'merged_terms!=True')

	#Tests that multiple variables are merged
	def testMergeMultipleVars(self):
		from iegen.ast.visitor import MergeExpTermsVisitor
		from iegen.ast import NormExp,VarExp

		e=NormExp([],0)
		e.terms=[VarExp(1,'a'),VarExp(2,'a'),VarExp(3,'b'),VarExp(-1,'b')]
		merged_terms=MergeExpTermsVisitor().visit(e).merged_terms
		e.terms.sort()

		e_res=NormExp([VarExp(3,'a'),VarExp(2,'b')],0)

		self.failUnless(e_res==e,'%s!=%s'%(e_res,e))
		self.failUnless(True==merged_terms,'merged_terms!=True')

	#Tests that functions are merged
	def testMergeFunctions(self):
		from iegen.ast.visitor import MergeExpTermsVisitor
		from iegen.ast import NormExp,FuncExp

		e=NormExp([],0)
		e.terms=[FuncExp(1,'a',[]),FuncExp(2,'a',[]),FuncExp(3,'a',[])]
		merged_terms=MergeExpTermsVisitor().visit(e).merged_terms
		e.terms.sort()

		e_res=NormExp([FuncExp(6,'a',[])],0)

		self.failUnless(e_res==e,'%s!=%s'%(e_res,e))
		self.failUnless(True==merged_terms,'merged_terms!=True')

	#Tests that multiple functions are merged
	def testMergeMultipleFunctions(self):
		from iegen.ast.visitor import MergeExpTermsVisitor
		from iegen.ast import NormExp,FuncExp

		e=NormExp([],0)
		e.terms=[FuncExp(1,'a',[]),FuncExp(2,'a',[]),FuncExp(3,'b',[]),FuncExp(-1,'b',[])]
		merged_terms=MergeExpTermsVisitor().visit(e).merged_terms
		e.terms.sort()

		e_res=NormExp([FuncExp(3,'a',[]),FuncExp(2,'b',[])],0)

		self.failUnless(e_res==e,'%s!=%s'%(e_res,e))
		self.failUnless(True==merged_terms,'merged_terms!=True')

	#Tests that both vars and funcs are merged
	def testMergeAll(self):
		from iegen.ast.visitor import MergeExpTermsVisitor
		from iegen.ast import NormExp,VarExp,FuncExp

		e=NormExp([],0)
		e.terms=[VarExp(1,'a'),
               VarExp(2,'a'),
               VarExp(1,'b'),
               FuncExp(3,'b',[]),
               FuncExp(-1,'b',[NormExp([VarExp(1,'x')],0)]),
               FuncExp(-1,'b',[NormExp([VarExp(1,'x')],0)])]
		merged_terms=MergeExpTermsVisitor().visit(e).merged_terms
		e.terms.sort()

		e_res=NormExp([VarExp(3,'a'),
                     VarExp(1,'b'),
                     FuncExp(3,'b',[]),
                     FuncExp(-2,'b',[NormExp([VarExp(1,'x')],0)])],0)

		self.failUnless(e_res==e,'%s!=%s'%(e_res,e))
		self.failUnless(True==merged_terms,'merged_terms!=True')

	#Tests that terms within a function's arguments are merged
	def testMergeFuncArgs(self):
		from iegen.ast.visitor import MergeExpTermsVisitor
		from iegen.ast import NormExp,VarExp,FuncExp

		e=NormExp([FuncExp(1,'f',[NormExp([],0)])],0)
		e.terms[0].args[0].terms=[VarExp(1,'a'),VarExp(2,'a'),FuncExp(3,'b',[]),FuncExp(-1,'b',[])]
		merged_terms=MergeExpTermsVisitor().visit(e).merged_terms
		e.terms.sort()

		e_res=NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a'),FuncExp(2,'b',[])],0)])],0)

		self.failUnless(e_res==e,'%s!=%s'%(e_res,e))
		self.failUnless(True==merged_terms,'merged_terms!=True')
#----------------------------------------------------

#---------- Remove Empty Constraint Visitor ----------
class RemoveEmptyConstraintsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the removed_constraint
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveEmptyConstraintsVisitor
		from iegen import Set

		set=Set('{[]}')
		v=RemoveEmptyConstraintsVisitor().visit(set)
		self.failUnless(hasattr(v,'removed_constraint'),"RemoveEmptyConstraintsVisitor doesn't place result in the 'removed_constraint' property.")

	#Make sure non-empty Equalities are not removed
	def testNoRemoveEquality(self):
		from iegen.ast.visitor import RemoveEmptyConstraintsVisitor
		from iegen import Set

		set=Set('{[a]:a=6}')
		removed_constraint=RemoveEmptyConstraintsVisitor().visit(set).removed_constraint

		set_res=Set('{[a]:a=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==removed_constraint,'removed_constraint!=False')

	#Make sure empty Equalities are removed
	def testRemoveEquality(self):
		from iegen.ast.visitor import RemoveEmptyConstraintsVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp

		set=Set('{[a]:a=a}')
		i=Equality(NormExp([],0))
		i.exp=NormExp([],0)
		set.sets[0].conjunct.constraint_list=[i]
		removed_constraint=RemoveEmptyConstraintsVisitor().visit(set).removed_constraint

		set_res=Set('{[a]}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_constraint,'removed_constraint!=True')

	#Make sure non-empty Inequalities are not removed
	def testNoRemoveInequality(self):
		from iegen.ast.visitor import RemoveEmptyConstraintsVisitor
		from iegen import Set

		set=Set('{[a]:a>=6}')
		removed_constraint=RemoveEmptyConstraintsVisitor().visit(set).removed_constraint

		set_res=Set('{[a]:a>=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==removed_constraint,'removed_constraint!=False')

	#Make sure empty Inequalities are removed
	def testRemoveInequality(self):
		from iegen.ast.visitor import RemoveEmptyConstraintsVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp

		set=Set('{[a]}')
		i=Inequality(NormExp([],0))
		i.exp=NormExp([],0)
		set.sets[0].conjunct.constraint_list=[i]
		removed_constraint=RemoveEmptyConstraintsVisitor().visit(set).removed_constraint

		set_res=Set('{[a]}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_constraint,'removed_constraint!=True')
#-----------------------------------------------------

#---------- Remove Zero Coeff Visitor ----------
class RemoveZeroCoeffVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the removed_term attribute
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveZeroCoeffVisitor
		from iegen import Set

		set=Set('{[]}')
		v=RemoveZeroCoeffVisitor().visit(set)
		self.failUnless(hasattr(v,'removed_term'),"RemoveZeroCoeffVisitor doesn't place result in the 'removed_term' property.")

	#Make sure non-zero coefficient variables are not removed
	def testNoRemoveVar(self):
		from iegen.ast.visitor import RemoveZeroCoeffVisitor,SortVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=6}')
		eq=Equality(NormExp([],1))
		eq.exp.terms.append(VarExp(-1,'a'))
		set.sets[0].conjunct.constraint_list.append(eq)
		removed_term=RemoveZeroCoeffVisitor().visit(set).removed_term
		SortVisitor().visit(set)

		set_res=Set('{[a]:a=6 and a=1}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==removed_term,'removed_term!=False')

	#Make sure zero coefficient variables are removed
	def testRemoveVar(self):
		from iegen.ast.visitor import RemoveZeroCoeffVisitor,SortVisitor,RemoveEmptyConstraintsVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=6}')
		eq=Equality(NormExp([],0))
		eq.exp.terms.append(VarExp(0,'a'))
		set.sets[0].conjunct.constraint_list.append(eq)
		removed_term=RemoveZeroCoeffVisitor().visit(set).removed_term
		SortVisitor().visit(set)
		RemoveEmptyConstraintsVisitor().visit(set)

		set_res=Set('{[a]:a=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_term,'removed_term!=True')

	#Make sure non-zero coefficient functions are not removed
	def testNoRemoveFunc(self):
		from iegen.ast.visitor import RemoveZeroCoeffVisitor,SortVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp,FuncExp

		set=Set('{[a]:a=6}')
		eq=Equality(NormExp([],1))
		eq.exp.terms.append(FuncExp(-1,'a',[NormExp([VarExp(1,'x')],0)]))
		set.sets[0].conjunct.constraint_list.append(eq)
		removed_term=RemoveZeroCoeffVisitor().visit(set).removed_term
		SortVisitor().visit(set)

		set_res=Set('{[a]:a=6 and a(x)=1}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==removed_term,'removed_term!=False')

	#Make sure zero coefficient functions are removed
	def testRemoveFunc(self):
		from iegen.ast.visitor import RemoveZeroCoeffVisitor,SortVisitor,RemoveEmptyConstraintsVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,FuncExp

		set=Set('{[a]:a=6}')
		eq=Equality(NormExp([],0))
		eq.exp.terms.append(FuncExp(0,'a',[]))
		set.sets[0].conjunct.constraint_list.append(eq)
		removed_term=RemoveZeroCoeffVisitor().visit(set).removed_term
		SortVisitor().visit(set)
		RemoveEmptyConstraintsVisitor().visit(set)

		set_res=Set('{[a]:a=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_term,'removed_term!=True')
#-----------------------------------------------------

#---------- Remove Free Var Equality Visitor ----------
class RemoveFreeVarEqualityVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the changed attribute
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveFreeVarEqualityVisitor
		from iegen import Set

		set=Set('{[]}')
		v=RemoveFreeVarEqualityVisitor().visit(set)
		self.failUnless(hasattr(v,'changed'),"RemoveFreeVarEqualityVisitor doesn't place result in the 'changed' property.")

	#Test that equalities with free variables are removed and
	#replaced with their equivalent expression
	def testSimpleSet(self):
		from iegen import Set

		set=Set('{[a]: a=b and b=6}')

		set_res=Set('{[a]: a=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))

	#Simple free var equality test with a relation
	def testSimpleRelation(self):
		from iegen import Relation

		rel=Relation('{[a]->[ap]: a=b and b=6 and ap=c and c=7}')

		rel_res=Relation('{[a]->[ap]: a=6 and ap=7}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))

	#Tests for more complex 'chaining' equality constraints
	def testChaining(self):
		from iegen import Set

		set=Set('{[a]: a=b and b=c and c=d and d=6}')

		set_res=Set('{[a]: a=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))

	#Tests that symbolics are propogated along the equality chain
	def testSymbolic(self):
		from iegen import Set,Symbolic

		set=Set('{[a]: a=b and b=c and c=d and d=n}',[Symbolic('n')])

		set_res=Set('{[a]: a=n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))

	#Tests that inequality free variables are replaced
	def testInequality(self):
		from iegen import Set,Symbolic

		set=Set('{[a]: a>=b and b=c and c=d and d=n and a<=c}',[Symbolic('n')])

		set_res=Set('{[a]: a>=n and a<=n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))

	#Tests for multiple 'chains' of equalities
	def testMultiple(self):
		from iegen import Set,Symbolic

		set=Set('{[a,b]: a=c and c=d and d=n and b=e and e=f and f=m}',[Symbolic('n'),Symbolic('m')])

		set_res=Set('{[a,b]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))

	#Tests that free variables are replaced within a function
	def testFunction(self):
		from iegen import Set

		set=Set('{[a,b]: a=f(d) and b=c and c=d}')

		set_res=Set('{[a,b]: a=f(b)}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))

	#Tests that free variables are replaced within a nested set of functions
	def testFunctionNest(self):
		from iegen import Set

		set=Set('{[a,b]: a=f(g(h(d))) and b=c and c=d}')

		set_res=Set('{[a,b]: a=f(g(h(b)))}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))

	#Tests that free variables with a non-1 coefficient are replaced properly
	def testCoeff(self):
		from iegen import Set,Symbolic

		set=Set('{[a]: a=6b and b=2c and c=4n}',[Symbolic('n')])

		set_res=Set('{[a]: a=48n}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
#------------------------------------------------------

#---------- Remove Duplicate Formulas Visitor ----------
class RemoveDuplicateFormulasVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the changed attribute
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveDuplicateFormulasVisitor
		from iegen import Set

		set=Set('{[]}')
		v=RemoveDuplicateFormulasVisitor().visit(set)
		self.failUnless(hasattr(v,'removed_formula'),"RemoveDuplicateFormulasVisitor doesn't place result in the 'removed_formula' property.")

	#Tests that non-duplicated sets are not removed
	def testNoRemoveSet(self):
		from iegen.ast.visitor import RemoveDuplicateFormulasVisitor
		from iegen import Set
		from iegen.parser import PresParser

		set=Set('{[a]:a=5}')
		set.sets.append(PresParser.parse_set('{[b]:b=6}'))
		removed_formula=RemoveDuplicateFormulasVisitor().visit(set).removed_formula

		set_res=Set('{[a]:a=5}').union(Set('{[b]:b=6}'))

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==removed_formula,'removed_formula!=False')

	#Tests that duplicated sets are removed
	def testRemoveSet(self):
		from iegen.ast.visitor import RemoveDuplicateFormulasVisitor
		from iegen import Set
		from iegen.parser import PresParser

		set=Set('{[a]:a=5}')
		set.sets.append(PresParser.parse_set('{[a]:a=5}'))
		set.sets.append(PresParser.parse_set('{[b]:b=6}'))
		set.sets.append(PresParser.parse_set('{[b]:b=6}'))
		removed_formula=RemoveDuplicateFormulasVisitor().visit(set).removed_formula

		set_res=Set('{[a]:a=5}').union(Set('{[b]:b=6}'))

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_formula,'removed_formula!=True')

	#Tests that non-duplicated relations are not removed
	def testNoRemoveRelation(self):
		from iegen.ast.visitor import RemoveDuplicateFormulasVisitor
		from iegen import Relation
		from iegen.parser import PresParser

		relation=Relation('{[a]->[ap]:a=5}')
		relation.relations.append(PresParser.parse_relation('{[b]->[bp]:b=6}'))
		removed_formula=RemoveDuplicateFormulasVisitor().visit(relation).removed_formula

		relation_res=Relation('{[a]->[ap]:a=5}').union(Relation('{[b]->[bp]:b=6}'))

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(False==removed_formula,'removed_formula!=False')

	#Tests that duplicated relations are removed
	def testRemoveRelation(self):
		from iegen.ast.visitor import RemoveDuplicateFormulasVisitor
		from iegen import Relation
		from iegen.parser import PresParser

		relation=Relation('{[a]->[ap]:a=5}')
		relation.relations.append(PresParser.parse_relation('{[a]->[ap]:a=5}'))
		relation.relations.append(PresParser.parse_relation('{[b]->[bp]:b=6}'))
		relation.relations.append(PresParser.parse_relation('{[b]->[bp]:b=6}'))
		removed_formula=RemoveDuplicateFormulasVisitor().visit(relation).removed_formula

		relation_res=Relation('{[a]->[ap]:a=5}').union(Relation('{[b]->[bp]:b=6}'))

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(True==removed_formula,'removed_formula!=True')
#------------------------------------------------------

#---------- Remove Symbolics Visitor ----------
class RemoveSymbolicsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the removed_symbolic attribute
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveSymbolicsVisitor
		from iegen import Set

		set=Set('{[]}')
		v=RemoveSymbolicsVisitor().visit(set)
		self.failUnless(hasattr(v,'removed_symbolic'),"RemoveSymbolicsVisitor doesn't place result in the 'removed_symbolic' property.")

	#Tests that non duplicated and used symbolic variables are not removed from PresSets
	def testNoRemovePresSet(self):
		from iegen.ast.visitor import RemoveSymbolicsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]:a<=n}',[Symbolic('n')])
		removed_symbolic=RemoveSymbolicsVisitor().visit(set).removed_symbolic

		set_res=Set('{[a]:a<=n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==removed_symbolic,'removed_symbolic!=False')

	#Tests that duplicated symbolic variables are removed from PresSets
	def testRemoveDuplicatePresSet(self):
		from iegen.ast.visitor import RemoveSymbolicsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]:n<=a and a<=m}',[Symbolic('n'),Symbolic('m')])
		set.sets[0].symbolics.extend([Symbolic('n'),Symbolic('m')])
		removed_symbolic=RemoveSymbolicsVisitor().visit(set).removed_symbolic

		set_res=Set('{[a]:n<=a and a<=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_symbolic,'removed_symbolic!=True')

	#Tests that unused symbolic variables are removed from PresSets
	def testRemoveUnusedPresSet(self):
		from iegen.ast.visitor import RemoveSymbolicsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]:n<=a}',[Symbolic('n')])
		set.sets[0].symbolics.append(Symbolic('m'))
		removed_symbolic=RemoveSymbolicsVisitor().visit(set).removed_symbolic

		set_res=Set('{[a]:n<=a}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_symbolic,'removed_symbolic!=True')

	#Tests that both unused and duplicate symbolic variables are removed from PresSets
	def testRemoveDuplicateUnusedPresSet(self):
		from iegen.ast.visitor import RemoveSymbolicsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]:n<=a}',[Symbolic('n')])
		set.sets[0].symbolics.extend([Symbolic('m'),Symbolic('n'),Symbolic('m'),Symbolic('s')])
		removed_symbolic=RemoveSymbolicsVisitor().visit(set).removed_symbolic

		set_res=Set('{[a]:n<=a}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_symbolic,'removed_symbolic!=True')

	#Tests that non duplicated and used symbolic variables are not removed from PresRelations
	def testNoRemovePresRelation(self):
		from iegen.ast.visitor import RemoveSymbolicsVisitor
		from iegen import Relation,Symbolic

		relation=Relation('{[a]->[ap]:a<=n}',[Symbolic('n')])
		removed_symbolic=RemoveSymbolicsVisitor().visit(relation).removed_symbolic

		relation_res=Relation('{[a]->[ap]:a<=n}',[Symbolic('n')])

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(False==removed_symbolic,'removed_symbolic!=False')

	#Tests that duplicated symbolic variables are removed from PresRelations
	def testRemoveDuplicatePresRelation(self):
		from iegen.ast.visitor import RemoveSymbolicsVisitor
		from iegen import Relation,Symbolic

		relation=Relation('{[a]->[ap]:n<=a and a<=m}',[Symbolic('n'),Symbolic('n')])
		relation.relations[0].symbolics.extend([Symbolic('m'),Symbolic('m')])
		removed_symbolic=RemoveSymbolicsVisitor().visit(relation).removed_symbolic

		relation_res=Relation('{[a]->[ap]:n<=a and a<=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(True==removed_symbolic,'removed_symbolic!=True')

	#Tests that unused symbolic variables are removed from PresRelations
	def testRemoveUnusedPresRelation(self):
		from iegen.ast.visitor import RemoveSymbolicsVisitor
		from iegen import Relation,Symbolic

		relation=Relation('{[a]->[ap]:n<=a}',[Symbolic('n')])
		relation.relations[0].symbolics.append(Symbolic('m'))
		removed_symbolic=RemoveSymbolicsVisitor().visit(relation).removed_symbolic

		relation_res=Relation('{[a]->[ap]:n<=a}',[Symbolic('n')])

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(True==removed_symbolic,'removed_symbolic!=True')

	#Tests that both unused and duplicate symbolic variables are removed from PresRelations
	def testRemoveDuplicateUnusedPresRelation(self):
		from iegen.ast.visitor import RemoveSymbolicsVisitor
		from iegen import Relation,Symbolic

		relation=Relation('{[a]->[ap]:n<=a}',[Symbolic('n'),Symbolic('m')])
		relation.relations[0].symbolics.extend([Symbolic('n'),Symbolic('m'),Symbolic('s')])
		removed_symbolic=RemoveSymbolicsVisitor().visit(relation).removed_symbolic

		relation_res=Relation('{[a]->[ap]:n<=a}',[Symbolic('n')])

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(True==removed_symbolic,'removed_symbolic!=True')
#------------------------------------------------------
