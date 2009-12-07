from unittest import TestCase
from iegen.lib.nose.tools import raises
from iegen.simplify import simplify

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
			from iegen.ast.visitor import DFVisitor,TransVisitor,RenameVisitor,SortVisitor,CheckVisitor,IsVarVisitor,FindConstraintVisitor,FindFreeVarConstraintVisitor,MergeExpTermsVisitor,RemoveEmptyConstraintsVisitor,RemoveFreeVarConstraintVisitor,RemoveDuplicateFormulasVisitor,RemoveDuplicateConstraintsVisitor,RemoveSymbolicsVisitor,CollectBoundsVisitor,ValueStringVisitor,RemoveTautologiesVisitor,RemoveContradictionsVisitor,FindFunctionsVisitor,CollectSymbolicsVisitor,CollectVarsVisitor,RemoveFreeVarFunctionVisitor,UniqueTupleVarsVisitor,SparseTransVisitor
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

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set,Relation

		set=Set('{[]}')
		v=TransVisitor([]).visit(set)

		self.failUnless(hasattr(v,'mats'),"TransVisitor doesn't place result in the 'mats' property when visiting a Set.")

		rel=Relation('{[]->[]}')
		v=TransVisitor([]).visit(rel)

		self.failUnless(hasattr(v,'mat'),"TransVisitor doesn't place result in the 'mat' property when visiting a Relation.")

	#Test that sets are supported
	def testNoSetFailure(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[]}')
		TransVisitor([]).visit(set)

	#Test that relations are supported
	def testNoRelationFailure(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Relation

		rel=Relation('{[]->[]}')
		TransVisitor([]).visit(rel)

	#Test that functions are not supported
	@raises(ValueError)
	def testFuncFailureSet(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[]:f(a)=1}')
		TransVisitor([]).visit(set)

	#Test that functions are not supported
	@raises(ValueError)
	def testFuncFailureRel(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Relation

		rel=Relation('{[]->[]:f(a)=1}')
		TransVisitor([]).visit(rel)

	#Test that existential variables are not supported
	@raises(ValueError)
	def testExistentialFail(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=1}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		TransVisitor([]).visit(set)

	#Test that translation of unions of PresSets is supported
	def testSetUnion(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set

		set=Set('{[a]: a=1}').union(Set('{[a]: a=2}'))
		mats=TransVisitor([]).visit(set).mats

		self.failUnless(2==len(mats),'Translation of two conjunctions in a Set did not produce two matrices')

	#Test that translation of unions of PresRelations is not supported
	@raises(ValueError)
	def testRelationUnion(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Relation

		rel=Relation('{[a]->[b]: a=1}').union(Relation('{[a]->[b]: a=2}'))
		TransVisitor([]).visit(rel)

	#Tests that all paramaters must be specified in the constructor
	@raises(ValueError)
	def testMissingParameter(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]:a=1 and a<n}',[Symbolic('n')])
		TransVisitor(['m']).visit(set)

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
	                                                      [1, 0,-1,0,1, 0]]],['n','m']),
	           ('{[s,i]: 0<=s && s<T && 0<=i && i<n_inter}',[[[1,1,0,0,0,0],
	                                                          [1,-1,0,1,0,-1],
	                                                          [1,0,1,0,0,0],
	                                                          [1,0,-1,0,1,-1]]],['T','n_inter']),
	           ('{[s,i]: 0<=s && s<T && 0<=i && i<n_inter}',[[[1,1,0,0,0,0,0],
	                                                          [1,-1,0,1,0,0,-1],
	                                                          [1,0,1,0,0,0,0],
	                                                          [1,0,-1,0,0,1,-1]]],['T','N','n_inter']),
	           ('{[s,i]: 0<=s && s<T && 0<=i && i<n_inter}',[[[1,1,0,0,0,0,0],
	                                                          [1,-1,0,1,0,0,-1],
	                                                          [1,0,1,0,0,0,0],
	                                                          [1,0,-1,0,1,0,-1]]],['T','n_inter','N']))

	#Test that the sets in set_tests are translated properly
	def testTransSet(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Set,Symbolic

		for set_string,res_mats,params in self.set_tests:
			#Create a list of symbolics for the set
			symbolics=[Symbolic(param) for param in params]

			#Create a set from the set string
			set=Set(set_string,symbolics)

			#Visit the set
			v=TransVisitor(params).visit(set)

			#Sort the rows of the matricies
			for mat in v.mats:
				mat.sort()
			for res_mat in res_mats:
				res_mat.sort()

			#Make sure the translated matrix matches the result matrix
			self.failUnless(v.mats==res_mats,'%s!=%s'%(v.mats,res_mats))


	rel_tests=(('{[i]->[c0,i,c1]: c0=1 and c1=2}',[[0,-1,0,0,0,0,1],
	                                               [0,0,-1,0,1,0,0],
	                                               [0,0,0,-1,0,0,2]],['n']),
	           ('{[i]->[c0,i,c1]: c0=1 and c1=2}',[[0,-1,0,0,0,0,0,1],
	                                               [0,0,-1,0,1,0,0,0],
	                                               [0,0,0,-1,0,0,0,2]],['n','m']),
	           ('{[s,i]->[c0,s,c1,i,c2]: c0=0 && c1=1 && c2=2}',[[0,1,0,0,0,0,0,0,0,0],
	                                                             [0,0,-1,0,0,0,1,0,0,0],
	                                                             [0,0,0,-1,0,0,0,0,0,1],
	                                                             [0,0,0,0,-1,0,0,1,0,0],
	                                                             [0,0,0,0,0,-1,0,0,0,2]],['T']),
	           ('{[s,i]->[c0,s,c1,i,c2]: c0=0 && c1=1 && c2=2}',[[0,1,0,0,0,0,0,0,0,0,0,0],
	                                                             [0,0,-1,0,0,0,1,0,0,0,0,0],
	                                                             [0,0,0,-1,0,0,0,0,0,0,0,1],
	                                                             [0,0,0,0,-1,0,0,1,0,0,0,0],
	                                                             [0,0,0,0,0,-1,0,0,0,0,0,2]],['T','N','n_inter']))

	#Test that the sets in set_tests are translated properly
	def testTransRel(self):
		from iegen.ast.visitor import TransVisitor
		from iegen import Relation,Symbolic

		for rel_string,res_mat,params in self.rel_tests:
			#Create a relation from the relation string
			rel=Relation(rel_string)

			#Visit the relation
			v=TransVisitor(params).visit(rel)

			#Sort the rows of the matricies
			v.mat.sort()
			res_mat.sort()

			#Make sure the translated matrix matches the result matrix
			self.failUnless(v.mat==res_mat,'%s!=%s'%(v.mat,res_mat))
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

	#Tests that the arguments to functions are not sorted
	#This ensures that bug #129 is actually fixed
	def testDontSortFunctionArgs(self):
		from iegen.ast import NormExp,VarExp,FuncExp
		from iegen.ast.visitor import SortVisitor

		func=FuncExp(1,'f',[NormExp([],1), NormExp([VarExp(1,'ii')],0)])
		SortVisitor().visit(func)

		func_res=FuncExp(1,'f',[])
		func_res.args=[NormExp([],1), NormExp([VarExp(1,'ii')],0)]

		self.failUnless(func==func_res,'%s!=%s'%(func,func_res))
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
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

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
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

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
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

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
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		self.failIf(IsVarVisitor('a').visit(set).is_tuple_var,"'a' is a tuple var in %s"%set)
		self.failIf(IsVarVisitor('b').visit(set).is_tuple_var,"'b' is a tuple var in %s"%set)
		self.failIf(IsVarVisitor('a').visit(relation).is_tuple_var,"'a' is a tuple var in %s"%relation)
		self.failIf(IsVarVisitor('b').visit(relation).is_tuple_var,"'b' is a tuple var in %s"%relation)
#---------------------------------------

#---------- Find Constraint Visitor ----------
class FindConstraintVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,Inequality

		set=Set('{[]}')
		v=FindConstraintVisitor(Equality,'a').visit(set)
		self.failUnless(hasattr(v,'var_constraints'),"FindConstraintVisitor(Equality,'a') doesn't place result in the 'var_constraints' property.")

		set=Set('{[]}')
		v=FindConstraintVisitor(Inequality,'a').visit(set)
		self.failUnless(hasattr(v,'var_constraints'),"FindConstraintVisitor(Inequality,'a') doesn't place result in the 'var_constraints' property.")

	#Tests that the visitor only accepts Equality and Inequality as the constraint type parameter
	@raises(ValueError)
	def testConstraintTypeIntFail(self):
		from iegen.ast.visitor import FindConstraintVisitor
		FindConstraintVisitor(6,'a')
	@raises(ValueError)
	def testConstraintTypeStringFail(self):
		from iegen.ast.visitor import FindConstraintVisitor
		FindConstraintVisitor('fail!','a')
	@raises(ValueError)
	def testConstraintTypeConjunctionFail(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen.ast import Conjunction
		FindConstraintVisitor(Conjunction,'a')

	#Tests that the visitor finds a tuple var equality
	def testFindTupleVarSetEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=5}')
		equalities=FindConstraintVisitor(Equality,'a').visit(set).var_constraints

		eq=Equality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(-1,'a')
		equalities_res=[(var,eq)]

		self.failUnless(equalities_res==equalities,'%s!=%s'%(equalities_res,equalities))

	#Tests that the visitor finds a free var equality
	def testFindFreeVarSetEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))

		equalities=FindConstraintVisitor(Equality,'a').visit(set).var_constraints

		eq=Equality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(-1,'a')
		equalities_res=[(var,eq)]

		self.failUnless(equalities_res==equalities,'%s!=%s'%(equalities_res,equalities))

	#Tests that the visitor finds a tuple var inequality
	def testFindTupleVarSetIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a]:a>=5}')
		inequalities=FindConstraintVisitor(Inequality,'a').visit(set).var_constraints

		ineq=Inequality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(1,'a')
		inequalities_res=[(var,ineq)]

		self.failUnless(inequalities_res==inequalities,'%s!=%s'%(inequalities_res,inequalities))

	#Tests that the visitor finds a free var inequality
	def testFindFreeVarSetIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[]}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))

		inequalities=FindConstraintVisitor(Inequality,'a').visit(set).var_constraints

		ineq=Inequality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(1,'a')
		inequalities_res=[(var,ineq)]

		self.failUnless(inequalities_res==inequalities,'%s!=%s'%(inequalities_res,inequalities))

	#Tests that the visitor finds a tuple var equality
	def testFindTupleVarRelationEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Relation
		from iegen.ast import Equality,NormExp,VarExp

		relation=Relation('{[a]->[b]:a=5}')
		equalities=FindConstraintVisitor(Equality,'a').visit(relation).var_constraints

		eq=Equality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(-1,'a')
		equalities_res=[(var,eq)]

		self.failUnless(equalities_res==equalities,'%s!=%s'%(equalities_res,equalities))

	#Tests that the visitor finds a simple equality
	def testFindFreeVarRelationEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Relation
		from iegen.ast import Equality,NormExp,VarExp

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))

		equalities=FindConstraintVisitor(Equality,'a').visit(relation).var_constraints

		eq=Equality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(-1,'a')
		equalities_res=[(var,eq)]

		self.failUnless(equalities_res==equalities,'%s!=%s'%(equalities_res,equalities))

	#Tests that the visitor finds a tuple var inequality
	def testFindTupleVarRelationIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Relation
		from iegen.ast import Inequality,NormExp,VarExp

		relation=Relation('{[a]->[b]:a>=5}')
		inequalities=FindConstraintVisitor(Inequality,'a').visit(relation).var_constraints

		ineq=Inequality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(1,'a')
		inequalities_res=[(var,ineq)]

		self.failUnless(inequalities_res==inequalities,'%s!=%s'%(inequalities_res,inequalities))

	#Tests that the visitor finds a simple inequality
	def testFindFreeVarRelationIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Relation
		from iegen.ast import Inequality,NormExp,VarExp

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))

		inequalities=FindConstraintVisitor(Inequality,'a').visit(relation).var_constraints

		ineq=Inequality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(1,'a')
		inequalities_res=[(var,ineq)]

		self.failUnless(inequalities_res==inequalities,'%s!=%s'%(inequalities_res,inequalities))

	#Tests that the visitor finds an equality in a collection of equalities
	def testFindInCollectionEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a,b,c,d]:a=5 and b=5 and c=5 and d=5}')
		equalities=FindConstraintVisitor(Equality,'d').visit(set).var_constraints

		eq=Equality(NormExp([VarExp(1,'d')],-5))
		var=VarExp(-1,'d')
		equalities_res=[(var,eq)]

		self.failUnless(equalities_res==equalities,'%s!=%s'%(equalities_res,equalities))

	#Tests that the visitor finds an inequality in a collection of inequalities
	def testFindInCollectionIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a,b,c,d]:a>=5 and b>=5 and c>=5 and d>=5}')
		inequalities=FindConstraintVisitor(Inequality,'d').visit(set).var_constraints

		ineq=Inequality(NormExp([VarExp(1,'d')],-5))
		var=VarExp(1,'d')
		inequalities_res=[(var,ineq)]

		self.failUnless(inequalities_res==inequalities,'%s!=%s'%(inequalities_res,inequalities))

	#Tests that the visitor finds an equality in a collection of constraints
	def testFindInConstraintsEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a,b]:a=5 and b=6 and b>=5}')
		equalities=FindConstraintVisitor(Equality,'b').visit(set).var_constraints

		eq=Equality(NormExp([VarExp(1,'b')],-6))
		var=VarExp(-1,'b')
		equalities_res=[(var,eq)]

		self.failUnless(equalities_res==equalities,'%s!=%s'%(equalities_res,equalities))

	#Tests that the visitor finds an inequality in a collection of constraints
	def testFindInConstraintsIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a,b]:a>=5 and b=6 and b>=6}')
		inequalities=FindConstraintVisitor(Inequality,'b').visit(set).var_constraints

		ineq=Inequality(NormExp([VarExp(1,'b')],-6))
		var=VarExp(1,'b')
		inequalities_res=[(var,ineq)]

		self.failUnless(inequalities_res==inequalities,'%s!=%s'%(inequalities_res,inequalities))

	#Tests that the visitor finds an equality in a collection of constraints with symbolics
	def testFindInConstraintsWithSymbolicEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a,b]:a=5 and b=6 and b>=5}',[Symbolic('n')])
		equalities=FindConstraintVisitor(Equality,'b').visit(set).var_constraints

		eq=Equality(NormExp([VarExp(1,'b')],-6))
		var=VarExp(-1,'b')
		equalities_res=[(var,eq)]

		self.failUnless(equalities_res==equalities,'%s!=%s'%(equalities_res,equalities))

	#Tests that the visitor finds an inequality in a collection of constraints with symbolics
	def testFindInConstraintsWithSymbolicIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a,b]:a>=5 and b=6 and b>=6}',[Symbolic('n')])
		inequalities=FindConstraintVisitor(Inequality,'b').visit(set).var_constraints

		ineq=Inequality(NormExp([VarExp(1,'b')],-6))
		var=VarExp(1,'b')
		inequalities_res=[(var,ineq)]

		self.failUnless(inequalities_res==inequalities,'%s!=%s'%(inequalities_res,inequalities))

	#Tests that the visitor finds an equality with multiple free variables
	def testFindMultipleFreeVarEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a,b,c]:a=5 and a=n and b=c+5}',[Symbolic('n')])
		equalities=FindConstraintVisitor(Equality,'c').visit(set).var_constraints

		eq=Equality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],-5))
		var=VarExp(1,'c')
		equalities_res=[(var,eq)]

		self.failUnless(equalities_res==equalities,'%s!=%s'%(equalities_res,equalities))

	#Tests that the visitor finds an inequality with multiple free variables
	def testFindMultipleFreeVarIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a,b,c]:a>=5 and a>=n and b>=c+5}',[Symbolic('n')])
		inequalities=FindConstraintVisitor(Inequality,'b').visit(set).var_constraints

		ineq=Inequality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],-5))
		var=VarExp(1,'b')
		inequalities_res=[(var,ineq)]

		self.failUnless(inequalities_res==inequalities,'%s!=%s'%(inequalities_res,inequalities))

	#Tests that multiple equalities are found for a variable
	def testFindMultipleEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a,b]: a=5 and b=6 and a=7}')
		equalities=FindConstraintVisitor(Equality,'a').visit(set).var_constraints

		eq1=Equality(NormExp([VarExp(-1,'a')],5))
		eq2=Equality(NormExp([VarExp(-1,'a')],7))
		var=VarExp(-1,'a')
		equalities_res=[(var,eq1),(var,eq2)]

		self.failUnless(equalities_res==equalities,'%s!=%s'%(equalities_res,equalities))

	#Tests that multiple inequalities are found for a variable
	def testFindMultipleIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a,b]: a>=5 and b>=6 and a>=7}')
		inequalities=FindConstraintVisitor(Inequality,'a').visit(set).var_constraints

		ineq1=Inequality(NormExp([VarExp(1,'a')],-7))
		ineq2=Inequality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(1,'a')
		inequalities_res=[(var,ineq1),(var,ineq2)]

		self.failUnless(inequalities_res==inequalities,'%s!=%s'%(inequalities_res,inequalities))

	#Tests that the visitor does not find a free variable with a non-1 and non--1 coefficient
	def testNoFindCoefficientEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a,b]: a=5 and 6b=5 and 5b=5}')
		equalities=FindConstraintVisitor(Equality,'b').visit(set).var_constraints
		self.failUnless([]==equalities,'%s!=[]'%equalities)

	#Tests that the visitor does not find a free variable with a non-1 and non--1 coefficient
	def testNoFindCoefficientNeg1Ineq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a,b]: a>=5 and 6b>=5 and 5b>=5}')
		inequalities=FindConstraintVisitor(Inequality,'b').visit(set).var_constraints
		self.failUnless([]==inequalities,'%s!=[]'%inequalities)

	#Tests that the visitor does not find an equality with func(a)=exp
	def testNoFindFuncEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality

		set=Set('{[a,b]:f(b)=5 and a=5}')
		equalities=FindConstraintVisitor(Equality,'b').visit(set).var_constraints
		self.failUnless([]==equalities,'%s!=[]'%equalities)

	#Tests that the visitor does not find an inequality with func(a)=exp
	def testNoFindFuncIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality

		set=Set('{[a,b]:f(b)>=5 and a>=5}')
		inequalities=FindConstraintVisitor(Inequality,'b').visit(set).var_constraints
		self.failUnless([]==inequalities,'%s!=[]'%inequalities)

	#Tests that the visitor does not find an equality with func1(func2(a))=exp
	def testNoFindNestedFuncEq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality

		set=Set('{[a,b]:f(g(b))=5 and a=5}')
		equalities=FindConstraintVisitor(Equality,'b').visit(set).var_constraints
		self.failUnless([]==equalities,'%s!=[]'%equalities)

	#Tests that the visitor does not find an inequality with func1(func2(a))=exp
	def testNoFindNestedFuncIneq(self):
		from iegen.ast.visitor import FindConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality

		set=Set('{[a,b]:f(g(b))>=5 and a=5}')
		inequalities=FindConstraintVisitor(Inequality,'b').visit(set).var_constraints
		self.failUnless([]==inequalities,'%s!=[]'%inequalities)
#---------------------------------------------------------

#---------- Find Free Variable Constraint Visitor ----------
class FindFreeVarConstraintVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,Inequality

		set=Set('{[]}')
		v=FindFreeVarConstraintVisitor(Equality).visit(set)
		self.failUnless(hasattr(v,'var_constraint_tuple'),"FindFreeVarConstraintVisitor(Equality) doesn't place result in the 'var_constraint_tuple' property.")

		set=Set('{[]}')
		v=FindFreeVarConstraintVisitor(Inequality).visit(set)
		self.failUnless(hasattr(v,'var_constraint_tuple'),"FindFreeVarConstraintVisitor(Inequality) doesn't place result in the 'var_constraint_tuple' property.")

	#Tests that the visitor only accepts Equality and Inequality as the constraint type parameter
	@raises(ValueError)
	def testConstraintTypeIntFail(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		FindFreeVarConstraintVisitor(6)
	@raises(ValueError)
	def testConstraintTypeStringFail(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		FindFreeVarConstraintVisitor('fail!')
	@raises(ValueError)
	def testConstraintTypeConjunctionFail(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen.ast import Conjunction
		FindFreeVarConstraintVisitor(Conjunction)

	#Tests that the visitor finds a simple equality
	def testFindSimpleSetEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		eq=Equality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(-1,'a')
		equality_res=(var,eq)

		self.failUnless(equality_res==equality_tuple,'%s!=%s'%(equality_res,equality_tuple))

	#Tests that the visitor finds a simple inequality
	def testFindSimpleSetIneq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[]}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		ineq=Inequality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(1,'a')
		inequality_res=(var,ineq)

		self.failUnless(inequality_res==inequality_tuple,'%s!=%s'%(inequality_res,inequality_tuple))

	#Tests that the visitor finds a simple equality
	def testFindSimpleRelationEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Relation
		from iegen.ast import Equality,NormExp,VarExp

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(relation).var_constraint_tuple

		eq=Equality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(-1,'a')
		equality_res=(var,eq)

		self.failUnless(equality_res==equality_tuple,'%s!=%s'%(equality_res,equality_tuple))

	#Tests that the visitor finds a simple inequality
	def testFindSimpleRelationIneq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Relation
		from iegen.ast import Inequality,NormExp,VarExp

		relation=Relation('{[]->[]}')
		relation.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(relation).var_constraint_tuple

		ineq=Inequality(NormExp([VarExp(1,'a')],-5))
		var=VarExp(1,'a')
		inequality_res=(var,ineq)

		self.failUnless(inequality_res==inequality_tuple,'%s!=%s'%(inequality_res,inequality_tuple))

	#Tests that the visitor finds an equality in a collection of equalities
	def testFindInCollectionEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a,b,c]:a=5 and b=5 and c=5}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'d')],-5)))

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		eq=Equality(NormExp([VarExp(1,'d')],-5))
		var=VarExp(-1,'d')
		equality_res=(var,eq)

		self.failUnless(equality_res==equality_tuple,'%s!=%s'%(equality_res,equality_tuple))

	#Tests that the visitor finds an inequality in a collection of inequalities
	def testFindInCollectionIneq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a,b,c]:a>=5 and b>=5 and c>=5}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'d')],-5)))

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		ineq=Inequality(NormExp([VarExp(1,'d')],-5))
		var=VarExp(1,'d')
		inequality_res=(var,ineq)

		self.failUnless(inequality_res==inequality_tuple,'%s!=%s'%(inequality_res,inequality_tuple))

	#Tests that the visitor finds an equality in a collection of constraints
	def testFindInConstraintsEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a]:a=5}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],-5)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b')],-5)))

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		eq=Equality(NormExp([VarExp(1,'b')],-5))
		var=VarExp(-1,'b')
		equality_res=(var,eq)

		self.failUnless(equality_res==equality_tuple,'%s!=%s'%(equality_res,equality_tuple))

	#Tests that the visitor finds an inequality in a collection of constraints
	def testFindInConstraintsIneq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a]:a>=5}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],-5)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b')],-5)))

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		ineq=Inequality(NormExp([VarExp(1,'b')],-5))
		var=VarExp(1,'b')
		inequality_res=(var,ineq)

		self.failUnless(inequality_res==inequality_tuple,'%s!=%s'%(inequality_res,inequality_tuple))

	#Tests that the visitor finds an equality in a collection of constraints with symbolics
	def testFindInConstraintsWithSymbolicEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a]:a=5}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],-5)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b')],-5)))

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		eq=Equality(NormExp([VarExp(1,'b')],-5))
		var=VarExp(-1,'b')
		equality_res=(var,eq)

		self.failUnless(equality_res==equality_tuple,'%s!=%s'%(equality_res,equality_tuple))

	#Tests that the visitor finds an inequality in a collection of constraints with symbolics
	def testFindInConstraintsWithSymbolicIneq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a]:a>=5}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],-5)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b')],-5)))

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		ineq=Inequality(NormExp([VarExp(1,'b')],-5))
		var=VarExp(1,'b')
		inequality_res=(var,ineq)

		self.failUnless(inequality_res==inequality_tuple,'%s!=%s'%(inequality_res,inequality_tuple))

	#Tests that the visitor finds an equality with multiple free variables
	def testFindMultipleFreeVarEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=5 and a=n}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],-5)))

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		eq=Equality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],-5))
		var=VarExp(1,'c')
		equality_res=(var,eq)

		self.failUnless(equality_res==equality_tuple,'%s!=%s'%(equality_res,equality_tuple))

	#Tests that the visitor finds an inequality with multiple free variables
	def testFindMultipleFreeVarIneq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a]:a>=5 and a>=n}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],-5)))

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		ineq=Inequality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],-5))
		var=VarExp(1,'b')
		inequality_res=(var,ineq)

		self.failUnless(inequality_res==inequality_tuple,'%s!=%s'%(inequality_res,inequality_tuple))

	#Tests that the visitor finds an equality with one free var and one tuple var
	def testFindFreeTupleVarEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=5 and a=n}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],-5)))

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		eq=Equality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],-5))
		var=VarExp(1,'b')
		equality_res=(var,eq)

		self.failUnless(equality_res==equality_tuple,'%s!=%s'%(equality_res,equality_tuple))

	#Tests that the visitor finds an inequality with one free var and one tuple var
	def testFindFreeTupleVarIneq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a]:a>=5 and a>=n}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],-5)))

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		ineq=Inequality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],-5))
		var=VarExp(-1,'b')
		inequality_res=(var,ineq)

		self.failUnless(inequality_res==inequality_tuple,'%s!=%s'%(inequality_res,inequality_tuple))

	#Tests that the visitor finds an equality with one free variable and one function
	def testFindFunctionEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp,FuncExp

		set=Set('{[a]:a=5 and a=n}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(1,'f',[NormExp([VarExp(1,'c')],0)])],-5)))

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		eq=Equality(NormExp([VarExp(1,'b'),FuncExp(1,'f',[NormExp([VarExp(1,'c')],0)])],-5))
		var=VarExp(-1,'b')
		equality_res=(var,eq)

		self.failUnless(equality_res==equality_tuple,'%s!=%s'%(equality_res,equality_tuple))

	#Tests that the visitor finds an inequality with one free variable and one function
	def testFindFunctionIneq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp,FuncExp

		set=Set('{[a]:a>=5 and a>=n}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b'),FuncExp(1,'f',[NormExp([VarExp(1,'c')],0)])],-5)))

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		ineq=Inequality(NormExp([VarExp(1,'b'),FuncExp(1,'f',[NormExp([VarExp(1,'c')],0)])],-5))
		var=VarExp(1,'b')
		inequality_res=(var,ineq)

		self.failUnless(inequality_res==inequality_tuple,'%s!=%s'%(inequality_res,inequality_tuple))

	#Tests that the visitor finds an equality with a free variable with a negative coefficient
	def testFindNeg1Eq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]:a=5 and a=n}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(-1,'b')],5)))

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		eq=Equality(NormExp([VarExp(-1,'b')],5))
		var=VarExp(-1,'b')
		equality_res=(var,eq)

		self.failUnless(equality_res==equality_tuple,'%s!=%s'%(equality_res,equality_tuple))

	#Tests that the visitor finds an inequality with a free variable with a negative coefficient
	def testFindNeg1Ineq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a]:a>=5 and a>=n}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'b')],5)))

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		ineq=Inequality(NormExp([VarExp(-1,'b')],5))
		var=VarExp(-1,'b')
		inequality_res=(var,ineq)

		self.failUnless(inequality_res==inequality_tuple,'%s!=%s'%(inequality_res,inequality_tuple))

	#Tests that the visitor does not find a free variable with a non-1 and non--1 coefficient
	def testNoFindCoefficientEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]: a=5}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(-6,'b')],5)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(5,'b')],-5)))

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		self.failUnless(None is equality_tuple,'%s is not None'%equality_tuple)

	#Tests that the visitor does not find a free variable with a non-1 and non--1 coefficient
	def testNoFindCoefficientNeg1Ineq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a]: a>=5}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-6,'b')],5)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(5,'b')],-5)))

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		self.failUnless(None is inequality_tuple,'%s is not None'%inequality_tuple)

	#Tests that the visitor does not find any equalities that don't have a free variable
	def testNoFind1Eq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality

		set=Set('{[a]:a=5}')

		equality=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		self.failUnless(None is equality,'%s is not None'%equality)

	#Tests that the visitor does not find any inequalities that don't have a free variable
	def testNoFind1Ineq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality

		set=Set('{[a]:a>=5}')

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		self.failUnless(None is inequality_tuple,'%s is not None'%inequality_tuple)

	#Tests that the visitor does not find any equalities involving only symbolics
	def testNoFind2Eq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality

		set=Set('{[]:n=5}',[Symbolic('n')])

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		self.failUnless(None is equality_tuple,'%s is not None'%equality_tuple)

	#Tests that the visitor does not find any inequalities involving only symbolics
	def testNoFind2Ineq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality

		set=Set('{[]:n>=5}',[Symbolic('n')])

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		self.failUnless(None is inequality_tuple,'%s is not None'%inequality_tuple)

	#Tests that the visitor does not find an equality with func(a)=exp
	def testNoFindFuncEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality

		set=Set('{[a]:f(b)=5 and a=5}')

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		self.failUnless(None is equality_tuple,'%s is not None'%equality_tuple)

	#Tests that the visitor does not find an inequality with func(a)=exp
	def testNoFindFuncIneq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality

		set=Set('{[a]:f(b)>=5 and a>=5}')

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		self.failUnless(None is inequality_tuple,'%s is not None'%inequality_tuple)

	#Tests that the visitor does not find an equality with func1(func2(a))=exp
	def testNoFindNestedFuncEq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality

		set=Set('{[a]:f(g(b))=5 and a=5}')

		equality_tuple=FindFreeVarConstraintVisitor(Equality).visit(set).var_constraint_tuple

		self.failUnless(None is equality_tuple,'%s is not None'%equality_tuple)

	#Tests that the visitor does not find an inequality with func1(func2(a))=exp
	def testNoFindNestedFuncIneq(self):
		from iegen.ast.visitor import FindFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Inequality

		set=Set('{[a]:f(g(b))>=5 and a=5}')

		inequality_tuple=FindFreeVarConstraintVisitor(Inequality).visit(set).var_constraint_tuple

		self.failUnless(None is inequality_tuple,'%s is not None'%inequality_tuple)
#---------------------------------------------------------

#---------- Merge Expression Terms Visitor ----------
class MergeExpTermsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
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

	#Make sure the result of the visiting is placed in the proper attribute
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
		set.sets[0].conjunct.constraints=[i]
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
		set.sets[0].conjunct.constraints=[i]
		removed_constraint=RemoveEmptyConstraintsVisitor().visit(set).removed_constraint

		set_res=Set('{[a]}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_constraint,'removed_constraint!=True')
#-----------------------------------------------------

#---------- Remove Zero Coeff Visitor ----------
class RemoveZeroCoeffVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
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
		set.sets[0].conjunct.constraints.append(eq)
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
		set.sets[0].conjunct.constraints.append(eq)
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
		set.sets[0].conjunct.constraints.append(eq)
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
		set.sets[0].conjunct.constraints.append(eq)
		removed_term=RemoveZeroCoeffVisitor().visit(set).removed_term
		SortVisitor().visit(set)
		RemoveEmptyConstraintsVisitor().visit(set)

		set_res=Set('{[a]:a=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_term,'removed_term!=True')
#-----------------------------------------------------

#---------- Remove Free Var Constraint Visitor ----------
class RemoveFreeVarConstraintVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor
		from iegen import Set
		from iegen.ast import Equality,Inequality

		set=Set('{[]}')
		v=RemoveFreeVarConstraintVisitor(Equality).visit(set)
		self.failUnless(hasattr(v,'changed'),"RemoveFreeVarConstraintVisitor doesn't place result in the 'changed' property.")

		set=Set('{[]}')
		v=RemoveFreeVarConstraintVisitor(Inequality).visit(set)
		self.failUnless(hasattr(v,'changed'),"RemoveFreeVarConstraintVisitor doesn't place result in the 'changed' property.")


	#Tests that the visitor only accepts Equality and Inequality as the constraint type parameter
	@raises(ValueError)
	def testConstraintTypeIntFail(self):
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor
		RemoveFreeVarConstraintVisitor(6)
	@raises(ValueError)
	def testConstraintTypeStringFail(self):
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor
		RemoveFreeVarConstraintVisitor('fail!')
	@raises(ValueError)
	def testConstraintTypeConjunctionFail(self):
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor
		from iegen.ast import Conjunction
		RemoveFreeVarConstraintVisitor(Conjunction)

	#Test that equalities with free variables are removed and
	#replaced with their equivalent expression
	def testSimpleSetEq(self):
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor,SortVisitor

		set=Set('{[a]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],-6)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed
		SortVisitor().visit(set)

		set_res=Set('{[a]: a=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Test that inequalities with free variables are removed and
	#replaced with their equivalent expression
	def testSimpleSetIneq(self):
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a]}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b')],-6)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed

		set_res=Set('{[a]: a>=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Simple free var equality test with a relation
	def testSimpleRelationEq(self):
		from iegen import Relation
		from iegen.ast import Equality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor,SortVisitor

		rel=Relation('{[a]->[ap]}')
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'ap'),VarExp(-1,'c')],0)))
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],-6)))
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c')],-7)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(rel).changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(rel).changed and changed
		SortVisitor().visit(rel)

		rel_res=Relation('{[a]->[ap]: a=6 and ap=7}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Simple free var inequality test with a relation
	def testSimpleRelationIneq(self):
		from iegen import Relation
		from iegen.ast import Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		rel=Relation('{[a]->[ap]}')
		rel.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'c')],-7)))
		rel.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		rel.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'ap'),VarExp(-1,'c')],0)))
		rel.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b')],-6)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(rel).changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(rel).changed and changed

		rel_res=Relation('{[a]->[ap]: a>=6 and ap>=7}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Tests for more complex 'chaining' equality constraints
	def testChainingEq(self):
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor,SortVisitor

		set=Set('{[a]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'d')],-6)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed
		SortVisitor().visit(set)

		set_res=Set('{[a]: a=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests for more complex 'chaining' inequality constraints
	def testChainingIneq(self):
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a]}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'d')],-6)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed and changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed and changed

		set_res=Set('{[a]: a>=6}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that symbolics are propogated along the equality chain
	def testSymbolicEq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'d'),VarExp(-1,'n')],0)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed

		set_res=Set('{[a]: a=n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that symbolics are propogated along the equality chain
	def testSymbolicIneq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'d'),VarExp(-1,'n')],0)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed and changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed and changed

		set_res=Set('{[a]: a>=n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that inequality free variables are replaced
	def testInequalityEq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Equality,Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor,SortVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a'),VarExp(1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'d'),VarExp(-1,'n')],0)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed
		SortVisitor().visit(set)

		set_res=Set('{[a]: a>=n and a<=n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that equality free variables are not replaced
	def testEqualityIneq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Equality,Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor,SortVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'d'),VarExp(-1,'n')],0)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed and changed
		SortVisitor().visit(set)

		set_res=Set('{[a]}')
		set_res.sets[0].symbolics=[Symbolic('n')]
		set_res.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set_res.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-1,'c')],0)))
		set_res.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b'),VarExp(-1,'n')],0)))
		SortVisitor().visit(set_res)

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests for multiple 'chains' of equalities
	def testMultipleEq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor,SortVisitor

		set=Set('{[a,b]}')
		set.sets[0].symbolics=[Symbolic('n'),Symbolic('m')]
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'d'),VarExp(-1,'n')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),VarExp(-1,'e')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'e'),VarExp(-1,'f')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'f'),VarExp(-1,'m')],0)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed
		SortVisitor().visit(set)

		set_res=Set('{[a,b]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests for multiple 'chains' of equalities
	def testMultipleIneq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor,SortVisitor

		set=Set('{[a,b]}')
		set.sets[0].symbolics=[Symbolic('n'),Symbolic('m')]
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'d'),VarExp(-1,'n')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b'),VarExp(-1,'e')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'e'),VarExp(-1,'f')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'f'),VarExp(-1,'m')],0)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed and changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed and changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed and changed
		SortVisitor().visit(set)

		set_res=Set('{[a,b]: a>=n and b>=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that free variables are replaced within a function
	def testFunctionEq(self):
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp,FuncExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a,b]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([VarExp(1,'d')],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed

		set_res=Set('{[a,b]: a=f(b)}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that free variables are not replaced within a function
	def testFunctionIneq(self):
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp,FuncExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor,SortVisitor

		set=Set('{[a,b]}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([VarExp(1,'d')],0)])],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed and changed
		SortVisitor().visit(set)

		set_res=Set('{[a,b]: a>=f(d) and b>=d}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Tests that free variables are replaced within a nested set of functions
	def testFunctionNestEq(self):
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp,FuncExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a,b]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([FuncExp(1,'h',[NormExp([VarExp(1,'b')],0)])],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed

		set_res=Set('{[a,b]: a=f(g(h(b)))}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that free variables are not replaced within a nested set of functions
	def testFunctionNestIneq(self):
		from copy import deepcopy
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp,FuncExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a,b]}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'c'),VarExp(-1,'d')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([FuncExp(1,'h',[NormExp([VarExp(1,'b')],0)])],0)])],0)])],0)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed

		set_res=Set('{[a,b]: a>=f(g(h(b))) and b>=d}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that free variables with a non-1/non--1 coefficient are replaced properly
	def testCoeffEq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-6,'b')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),VarExp(-2,'c')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),VarExp(-4,'n')],0)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed and changed

		set_res=Set('{[a]: a=48n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that free variables with a non-1/non--1 coefficient are replaced properly
	def testCoeffIneq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-6,'b')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'b'),VarExp(-2,'c')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'c'),VarExp(-4,'n')],0)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed
		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed and changed

		set_res=Set('{[a]: a>=48n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that free variables with a non-1/non-1 coefficient are not found for replacement
	def testNon1CoeffEq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor,SortVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),VarExp(-6,'b')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(4,'b'),VarExp(-2,'c')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(5,'c'),VarExp(-4,'n')],0)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed
		SortVisitor().visit(set)

		set_res=Set('{[a]: a=6b and 4b=2c and 5c=4n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Tests that free variables with a non-1/non-1 coefficient are not found for replacement
	def testNon1CoeffIneq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-6,'b')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(5,'c'),VarExp(-4,'n')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(4,'b'),VarExp(-2,'c')],0)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed

		set_res=Set('{[a]: a>=6b and 4b>=2c and 5c>=4n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Tests that expressions with mutiple tuple variables are replaced properly
	def testMultipleTupleVarEq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Equality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(2,'a'),VarExp(3,'b'),VarExp(4,'n'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(4,'c'),],-6)))

		changed=RemoveFreeVarConstraintVisitor(Equality).visit(set).changed

		set_res=Set('{[a]: 8a+12b+16n=6}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that expressions with mutiple tuple variables are replaced properly
	def testMultipleTupleVarIneq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(2,'a'),VarExp(3,'b'),VarExp(4,'n'),VarExp(-1,'c')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(4,'c'),],-6)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed

		set_res=Set('{[a]: 8a+12b+16n>=6}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Tests that free variables on the 'wrong' side of an inequality are not replaced
	#IE:  a>=b and b<=c does not imply a<=c or a>=c
	def testWrongSideIneq(self):
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp
		from iegen.ast.visitor import RemoveFreeVarConstraintVisitor

		set=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'c'),VarExp(-1,'b')],0)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'n'),VarExp(-1,'b')],0)))

		changed=RemoveFreeVarConstraintVisitor(Inequality).visit(set).changed

		set_res=Set('{[a]}')
		set.sets[0].symbolics=[Symbolic('n')]
		set_res.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a'),VarExp(-1,'b')],0)))
		set_res.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'c'),VarExp(-1,'b')],0)))
		set_res.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'n'),VarExp(-1,'b')],0)))

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')
#------------------------------------------------------

#---------- Remove Duplicate Formulas Visitor ----------
class RemoveDuplicateFormulasVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
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
		set.sets.append(PresParser.parse_set('{[a]:a=6}'))
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
		set.sets.append(PresParser.parse_set('{[a]:a=6}'))
		set.sets.append(PresParser.parse_set('{[a]:a=6}'))
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
		relation.relations.append(PresParser.parse_relation('{[a]->[ap]:a=6}'))
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
		relation.relations.append(PresParser.parse_relation('{[a]->[ap]:a=6}'))
		relation.relations.append(PresParser.parse_relation('{[a]->[ap]:a=6}'))
		removed_formula=RemoveDuplicateFormulasVisitor().visit(relation).removed_formula

		relation_res=Relation('{[a]->[ap]:a=5}').union(Relation('{[b]->[bp]:b=6}'))

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(True==removed_formula,'removed_formula!=True')
#------------------------------------------------------

#---------- Remove Duplicate Constraints Visitor ----------
class RemoveDuplicateConstraintsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveDuplicateConstraintsVisitor
		from iegen import Set

		set=Set('{[]}')
		v=RemoveDuplicateConstraintsVisitor().visit(set)
		self.failUnless(hasattr(v,'removed_constraint'),"RemoveDuplicateConstraintsVisitor doesn't place result in the 'removed_constraint' property.")

	#Tests that duplicated equality constraints are removed from sets
	def testRemoveEqualitySet(self):
		from iegen.ast.visitor import RemoveDuplicateConstraintsVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp,VarExp

		set=Set('{[a]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))
		removed_constraint=RemoveDuplicateConstraintsVisitor().visit(set).removed_constraint

		set_res=Set('{[a]:a=5}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_constraint,'removed_constraint!=True')

	#Tests that duplicated equality constraints are removed from relations
	def testRemoveEqualityRelation(self):
		from iegen.ast.visitor import RemoveDuplicateConstraintsVisitor
		from iegen import Relation
		from iegen.ast import Equality,NormExp,VarExp

		relation=Relation('{[a]->[ap]}')
		relation.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))
		relation.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))
		removed_constraint=RemoveDuplicateConstraintsVisitor().visit(relation).removed_constraint

		relation_res=Relation('{[a]->[ap]:a=5}')

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(True==removed_constraint,'removed_constraint!=True')

	#Tests that duplicated equality constraints are removed from sets
	def testRemoveInequalitySet(self):
		from iegen.ast.visitor import RemoveDuplicateConstraintsVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a]}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))
		removed_constraint=RemoveDuplicateConstraintsVisitor().visit(set).removed_constraint

		set_res=Set('{[a]:a>=5}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_constraint,'removed_constraint!=True')

	#Tests that duplicated equality constraints are removed from relations
	def testRemoveInequalityRelation(self):
		from iegen.ast.visitor import RemoveDuplicateConstraintsVisitor
		from iegen import Relation
		from iegen.ast import Inequality,NormExp,VarExp

		relation=Relation('{[a]->[ap]}')
		relation.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))
		relation.relations[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))
		removed_constraint=RemoveDuplicateConstraintsVisitor().visit(relation).removed_constraint

		relation_res=Relation('{[a]->[ap]:a>=5}')

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(True==removed_constraint,'removed_constraint!=True')

	#Tests that duplicated equality constraints are removed without removing other constraints
	def testRemoveConstraintOthers(self):
		from iegen.ast.visitor import RemoveDuplicateConstraintsVisitor
		from iegen import Set
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a]: a>=10}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))
		removed_constraint=RemoveDuplicateConstraintsVisitor().visit(set).removed_constraint

		set_res=Set('{[a]:a>=5 and a=5 and a>=10}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_constraint,'removed_constraint!=True')

	#Tests that duplicated equality constraints are removed without removing other constraints
	def testRemoveConstraintSymbolics(self):
		from iegen.ast.visitor import RemoveDuplicateConstraintsVisitor,SortVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=Set('{[a]: a>=10 and a<=n}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([VarExp(1,'a')],-5)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a')],-5)))
		removed_constraint=RemoveDuplicateConstraintsVisitor().visit(set).removed_constraint
		SortVisitor().visit(set)

		set_res=Set('{[a]:a>=5 and a=5 and a>=10 and a<=n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_constraint,'removed_constraint!=True')
#----------------------------------------------------------

#---------- Remove Symbolics Visitor ----------
class RemoveSymbolicsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
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

	#Tests that symbolics that are only used as input to a function are not removed
	def testNoRemoveFunctionInput(self):
		from iegen.ast.visitor import RemoveSymbolicsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]:a<=f(n)}',[Symbolic('n')])
		removed_symbolic=RemoveSymbolicsVisitor().visit(set).removed_symbolic

		set_res=Set('{[a]:a<=f(n)}',[Symbolic('n')])

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

#---------- Collect Bounds Visitor ----------
class CollectBoundsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import CollectBoundsVisitor
		from iegen import Set

		set=Set('{[]}')
		v=CollectBoundsVisitor('a').visit(set)
		self.failUnless(hasattr(v,'bounds'),"RemoveSymbolicsVisitor doesn't place result in the 'bounds' property.")

	#Tests that an empty set produces no bounds on 'a'
	def testNoBounds1(self):
		from iegen.ast.visitor import CollectBoundsVisitor
		from iegen import Set

		set=Set('{[]}')
		bounds=CollectBoundsVisitor('a').visit(set).bounds
		self.failUnless(([],[])==bounds,'Bounds not empty')

	#Tests that a set with bounds on 'a' produces no bounds on 'b'
	def testNoBounds2(self):
		from iegen.ast.visitor import CollectBoundsVisitor
		from iegen import Set

		set=Set('{[a]:0<=a and a<=10}')
		bounds=CollectBoundsVisitor('b').visit(set).bounds
		self.failUnless(([],[])==bounds,'Bounds not empty')

	#Tests that the bounds are found for a set with one variable
	def testOneVarBounds(self):
		from iegen.ast.visitor import CollectBoundsVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a]:0<=a and a<=10}')
		bounds=CollectBoundsVisitor('a').visit(set).bounds

		lb_exp=NormExp([],0)
		lb_ineq=Inequality(NormExp([VarExp(1,'a')],0)+lb_exp)
		ub_exp=NormExp([],10)
		ub_ineq=Inequality(NormExp([VarExp(-1,'a')],0)+ub_exp)
		bounds_res=([(1,lb_exp,lb_ineq)],[(1,ub_exp,ub_ineq)])

		self.failUnless(bounds_res==bounds,'Incorrect bounds: %s!=%s'%(bounds_res,bounds))

	#Tests that the bounds are found for a set with one variable and multiple upper and lower bounds
	def testMultipleBounds1(self):
		from iegen.ast.visitor import CollectBoundsVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a]:0<=a and a<=10 and -5<=a and a<=20}')
		bounds=CollectBoundsVisitor('a').visit(set).bounds

		lb_exp1=NormExp([],0)
		lb_ineq1=Inequality(NormExp([VarExp(1,'a')],0)-lb_exp1)
		lb_exp2=NormExp([],-5)
		lb_ineq2=Inequality(NormExp([VarExp(1,'a')],0)-lb_exp2)
		ub_exp1=NormExp([],10)
		ub_ineq1=Inequality(NormExp([VarExp(-1,'a')],0)+ub_exp1)
		ub_exp2=NormExp([],20)
		ub_ineq2=Inequality(NormExp([VarExp(-1,'a')],0)+ub_exp2)
		bounds_res=([(1,lb_exp1,lb_ineq1),(1,lb_exp2,lb_ineq2)],[(1,ub_exp1,ub_ineq1),(1,ub_exp2,ub_ineq2)])

		self.failUnless(bounds_res==bounds,'Incorrect bounds: %s!=%s'%(bounds_res,bounds))

	#Tests that the bounds are found for a set with two variables and multiple upper and lower bounds
	def testMultipleBounds2(self):
		from iegen.ast.visitor import CollectBoundsVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a,b]:0<=5a and a<=10 and a<=20 and b>=16 and b<=5}')
		bounds=CollectBoundsVisitor('a').visit(set).bounds

		lb_exp=NormExp([],0)
		lb_ineq=Inequality(NormExp([VarExp(5,'a')],0)-lb_exp)
		ub_exp1=NormExp([],10)
		ub_ineq1=Inequality(NormExp([VarExp(-1,'a')],0)+ub_exp1)
		ub_exp2=NormExp([],20)
		ub_ineq2=Inequality(NormExp([VarExp(-1,'a')],0)+ub_exp2)
		bounds_res=([(5,lb_exp,lb_ineq)],[(1,ub_exp1,ub_ineq1),(1,ub_exp2,ub_ineq2)])

		self.failUnless(bounds_res==bounds,'Incorrect bounds: %s!=%s'%(bounds_res,bounds))

		bounds=CollectBoundsVisitor('b').visit(set).bounds

		lb_exp=NormExp([],16)
		lb_ineq=Inequality(NormExp([VarExp(1,'b')],0)-lb_exp)
		ub_exp=NormExp([],5)
		ub_ineq=Inequality(NormExp([VarExp(-1,'b')],0)+ub_exp)
		bounds_res=([(1,lb_exp,lb_ineq)],[(1,ub_exp,ub_ineq)])

		self.failUnless(bounds_res==bounds,'Incorrect bounds: %s!=%s'%(bounds_res,bounds))

	#Tests that bounds are found with symbolics involved
	def testSymbolicBounds(self):
		from iegen.ast.visitor import CollectBoundsVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp,VarExp

		set=Set('{[a,b]:n+m<=3a and a<=2n+5 and a<=20 and 3b>=16 and b<=m-1}',[Symbolic('n'),Symbolic('m')])
		bounds=CollectBoundsVisitor('a').visit(set).bounds

		lb_exp=NormExp([VarExp(1,'n'),VarExp(1,'m')],0)
		lb_ineq=Inequality(NormExp([VarExp(3,'a')],0)-lb_exp)
		ub_exp1=NormExp([VarExp(2,'n')],5)
		ub_ineq1=Inequality(NormExp([VarExp(-1,'a')],0)+ub_exp1)
		ub_exp2=NormExp([],20)
		ub_ineq2=Inequality(NormExp([VarExp(-1,'a')],0)+ub_exp2)
		bounds_res=([(3,lb_exp,lb_ineq)],[(1,ub_exp1,ub_ineq1),(1,ub_exp2,ub_ineq2)])

		self.failUnless(bounds_res==bounds,'Incorrect bounds: %s!=%s'%(bounds_res,bounds))

		bounds=CollectBoundsVisitor('b').visit(set).bounds

		lb_exp=NormExp([],16)
		lb_ineq=Inequality(NormExp([VarExp(3,'b')],0)-lb_exp)
		ub_exp=NormExp([VarExp(1,'m')],-1)
		ub_ineq=Inequality(NormExp([VarExp(-1,'b')],0)+ub_exp)
		bounds_res=([(3,lb_exp,lb_ineq)],[(1,ub_exp,ub_ineq)])

		self.failUnless(bounds_res==bounds,'Incorrect bounds: %s!=%s'%(bounds_res,bounds))
#--------------------------------------------

#---------- Value String Visitor ----------
class ValueStringVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp

		exp=NormExp([],0)
		v=ValueStringVisitor().visit(exp)
		self.failUnless(hasattr(v,'value'),"ValueStringVisitor doesn't place result in the 'value' property.")

	#Tests that the visitor accepts NormExp, VarExp, and FuncExp for visiting
	def testVisitingAccept(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,VarExp,FuncExp

		ne=NormExp([],0)
		ve=VarExp(0,'a')
		fe=FuncExp(0,'f',[])

		ValueStringVisitor().visit(ne)
		ValueStringVisitor().visit(ve)
		ValueStringVisitor().visit(fe)

	#Tests that other types of nodes are not accepted for visiting
	@raises(ValueError)
	def testVisitingRejectSet(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen import Set
		ValueStringVisitor().visit(Set('{[]}'))
	@raises(ValueError)
	def testVisitingRejectRelation(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen import Relation
		ValueStringVisitor().visit(Relation('{[]->[]}'))
	@raises(ValueError)
	def testVisitingRejectPresSet(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction
		ValueStringVisitor().visit(PresSet(VarTuple([]),Conjunction([]),[]))
	@raises(ValueError)
	def testVisitingRejectPresRelation(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction
		ValueStringVisitor().visit(PresRelation(VarTuple([]),VarTuple([]),Conjunction([]),[]))

	#Tests that the proper string is returned for a single variable
	def testVisitVarExp(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import VarExp

		value=ValueStringVisitor().visit(VarExp(3,'a')).value
		value_res='3a'
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with a constant
	def testVisitNormExpConstant(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,VarExp

		value=ValueStringVisitor().visit(NormExp([],-5)).value
		value_res='-5'
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with one variable
	def testVisitNormExpOneVar(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,VarExp

		value=ValueStringVisitor().visit(NormExp([VarExp(3,'a')],0)).value
		value_res='3a'
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with one variable and a constant
	def testVisitNormExpOneVarConstant(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,VarExp

		value=ValueStringVisitor().visit(NormExp([VarExp(3,'a')],7)).value
		value_res='3a+7'
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with two variables
	def testVisitNormExpTwoVars(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,VarExp

		value=ValueStringVisitor().visit(NormExp([VarExp(3,'a'),VarExp(5,'b')],0)).value
		value_res='3a+5b'
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with two variables and a constant
	def testVisitNormExpTwoVarsConstant(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,VarExp

		value=ValueStringVisitor().visit(NormExp([VarExp(3,'a'),VarExp(5,'b')],9)).value
		value_res='3a+5b+9'
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with three variables
	def testVisitNormExpThreeVars(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,VarExp

		value=ValueStringVisitor().visit(NormExp([VarExp(3,'a'),VarExp(5,'b'),VarExp(7,'c')],0)).value
		value_res='3a+5b+7c'
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with three variables and a constant
	def testVisitNormExpThreeVarsConstant(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,VarExp

		value=ValueStringVisitor().visit(NormExp([VarExp(3,'a'),VarExp(5,'b'),VarExp(7,'c')],11)).value
		value_res='3a+5b+7c+11'
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#----- Explicit Relation lookup tests -----

	#Tests that the proper string is returned for single function
	def testVisitFuncExpER(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='ER_out_given_in(f_ER,3a)'

		value=ValueStringVisitor().visit(FuncExp(1,'f',[NormExp([VarExp(3,'a')],0)])).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

		value=ValueStringVisitor(False).visit(FuncExp(1,'f',[NormExp([VarExp(3,'a')],0)])).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with one function
	def testVisitNormExpOneFuncER(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='ER_out_given_in(f_ER,3a)'

		value=ValueStringVisitor().visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],0)])],0)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

		value=ValueStringVisitor(False).visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],0)])],0)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with one function and a constant
	def testVisitNormExpOneFuncConstantER(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='ER_out_given_in(f_ER,3a)+5'

		value=ValueStringVisitor().visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],0)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

		value=ValueStringVisitor(False).visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],0)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with one function (with a constant term in its arguments) and a constant
	def testVisitNormExpOneFuncConstArgConstantER(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='ER_out_given_in(f_ER,3a+2)+5'

		value=ValueStringVisitor().visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],2)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

		value=ValueStringVisitor(False).visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],2)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with two function (with constant terms in their arguments) and a constant
	def testVisitNormExpTwoFuncConstArgConstantER(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='ER_out_given_in(f_ER,3a+2)+ER_out_given_in(g_ER,4b+3)+5'

		value=ValueStringVisitor().visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],2)]),FuncExp(1,'g',[NormExp([VarExp(4,'b')],3)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

		value=ValueStringVisitor(False).visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],2)]),FuncExp(1,'g',[NormExp([VarExp(4,'b')],3)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with mutiple terms
	def testVisitNormExpTermsER(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='9c+ER_out_given_in(f_ER,3a+2)+ER_out_given_in(g_ER,4b+3)+5'

		value=ValueStringVisitor().visit(NormExp([VarExp(9,'c'),FuncExp(1,'f',[NormExp([VarExp(3,'a')],2)]),FuncExp(1,'g',[NormExp([VarExp(4,'b')],3)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

		value=ValueStringVisitor(False).visit(NormExp([VarExp(9,'c'),FuncExp(1,'f',[NormExp([VarExp(3,'a')],2)]),FuncExp(1,'g',[NormExp([VarExp(4,'b')],3)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#----- Raw index array tests -----

	#Tests that the proper string is returned for single function
	def testVisitFuncExpRaw(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='f[3a]'

		value=ValueStringVisitor(True).visit(FuncExp(1,'f',[NormExp([VarExp(3,'a')],0)])).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with one function
	def testVisitNormExpOneFuncRaw(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='f[3a]'

		value=ValueStringVisitor(True).visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],0)])],0)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with one function and a constant
	def testVisitNormExpOneFuncConstantRaw(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='f[3a]+5'

		value=ValueStringVisitor(True).visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],0)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with one function (with a constant term in its arguments) and a constant
	def testVisitNormExpOneFuncConstArgConstantRaw(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='f[3a+2]+5'

		value=ValueStringVisitor(True).visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],2)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with two function (with constant terms in their arguments) and a constant
	def testVisitNormExpTwoFuncConstArgConstantRaw(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='f[3a+2]+g[4b+3]+5'

		value=ValueStringVisitor(True).visit(NormExp([FuncExp(1,'f',[NormExp([VarExp(3,'a')],2)]),FuncExp(1,'g',[NormExp([VarExp(4,'b')],3)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))

	#Tests that the proper string is returned for an expression with mutiple terms
	def testVisitNormExpTermsRaw(self):
		from iegen.ast.visitor import ValueStringVisitor
		from iegen.ast import NormExp,FuncExp,VarExp

		value_res='9c+f[3a+2]+g[4b+3]+5'

		value=ValueStringVisitor(True).visit(NormExp([VarExp(9,'c'),FuncExp(1,'f',[NormExp([VarExp(3,'a')],2)]),FuncExp(1,'g',[NormExp([VarExp(4,'b')],3)])],5)).value
		self.failUnless(value_res==value,'%s!=%s'%(value_res,value))
#------------------------------------------

#---------- Remove Tautologies Visitor ----------
class RemoveTautologiesVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveTautologiesVisitor
		from iegen import Set

		set=Set('{[a]}')
		v=RemoveTautologiesVisitor().visit(set)
		self.failUnless(hasattr(v,'removed_tautology'),"RemoveTautologiesVisitor doesn't place result in the 'removed_tautology' property.")

	#Tests that equality tautologies are removed from a set
	def testRemoveEqualitySet(self):
		from iegen.ast.visitor import RemoveTautologiesVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp

		set=Set('{[a]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([],0)))

		removed_tautology=RemoveTautologiesVisitor().visit(set).removed_tautology

		set_res=Set('{[a]}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_tautology,'removed_tautology!=True')

	#Tests that equality tautologies are removed from a relation
	def testRemoveEqualityRelation(self):
		from iegen.ast.visitor import RemoveTautologiesVisitor
		from iegen import Relation
		from iegen.ast import Equality,NormExp

		relation=Relation('{[a]->[ap]}')
		relation.relations[0].conjunct.constraints.append(Equality(NormExp([],0)))

		removed_tautology=RemoveTautologiesVisitor().visit(relation).removed_tautology

		relation_res=Relation('{[a]->[ap]}')

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(True==removed_tautology,'removed_tautology!=True')

	#Tests that inequality tautologies are removed from a set
	def testRemoveInequalitySet(self):
		from iegen.ast.visitor import RemoveTautologiesVisitor
		from iegen import Set
		from iegen.ast import Inequality,NormExp

		set=Set('{[a]}')
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([],1)))

		removed_tautology=RemoveTautologiesVisitor().visit(set).removed_tautology

		set_res=Set('{[a]}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_tautology,'removed_tautology!=True')

	#Tests that equality tautologies are removed from a relation
	def testRemoveInequalityRelation(self):
		from iegen.ast.visitor import RemoveTautologiesVisitor
		from iegen import Relation
		from iegen.ast import Inequality,NormExp

		relation=Relation('{[a]->[ap]}')
		relation.relations[0].conjunct.constraints.append(Inequality(NormExp([],1)))

		removed_tautology=RemoveTautologiesVisitor().visit(relation).removed_tautology

		relation_res=Relation('{[a]->[ap]}')

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(True==removed_tautology,'removed_tautology!=True')

	#Tests that inequality tautologies are removed from a set
	def testRemoveOthers(self):
		from iegen.ast.visitor import RemoveTautologiesVisitor
		from iegen import Set,Symbolic
		from iegen.ast import Inequality,NormExp

		set=Set('{[a]: a=10 and a<=n}',[Symbolic('n')])
		set.sets[0].conjunct.constraints.append(Inequality(NormExp([],1)))

		removed_tautology=RemoveTautologiesVisitor().visit(set).removed_tautology

		set_res=Set('{[a]: a=10 and a<=n}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_tautology,'removed_tautology!=True')
#------------------------------------------------

#---------- Remove Contradictions Visitor ----------
class RemoveContradictionsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveContradictionsVisitor
		from iegen import Set

		set=Set('{[a]}')
		v=RemoveContradictionsVisitor().visit(set)
		self.failUnless(hasattr(v,'removed_contradiction'),"RemoveContradictionsVisitor doesn't place result in the 'removed_contradiction' property.")

	#Tests that contradictions are removed from sets def testRemoveSet(self):
	def testRemoveSet(self):
		from iegen.ast.visitor import RemoveContradictionsVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp

		set=Set('{[a]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([],2)))

		removed_contradiction=RemoveContradictionsVisitor().visit(set).removed_contradiction

		set_res=Set('{[a]: 1=0}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_contradiction,'removed_contradiction!=True')

	#Tests that contradictions are removed from sets
	def testRemoveRelation(self):
		from iegen.ast.visitor import RemoveContradictionsVisitor
		from iegen import Relation
		from iegen.ast import Inequality,NormExp

		relation=Relation('{[a]->[ap]}')
		relation.relations[0].conjunct.constraints.append(Inequality(NormExp([],-1)))

		removed_contradiction=RemoveContradictionsVisitor().visit(relation).removed_contradiction

		relation_res=Relation('{[a]->[ap]: 1=0}')

		self.failUnless(relation_res==relation,'%s!=%s'%(relation_res,relation))
		self.failUnless(True==removed_contradiction,'removed_contradiction!=True')

	#Tests that whole contradictions in a union are removed
	def testRemoveOthers(self):
		from iegen.ast.visitor import RemoveContradictionsVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp

		set=Set('{[a]:a=10}')
		set2=Set('{[a]}')
		set2.sets[0].conjunct.constraints.append(Equality(NormExp([],1)))
		set.sets.append(set2)

		removed_contradiction=RemoveContradictionsVisitor().visit(set).removed_contradiction

		set_res=Set('{[a]: a=10}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_contradiction,'removed_contradiction!=True')

	#Tests that all contradictions are removed and just a single remains with a variable tuple and contradictory constraint
	def testRemoveAll(self):
		from iegen.ast.visitor import RemoveContradictionsVisitor
		from iegen import Set
		from iegen.ast import Equality,NormExp

		set=Set('{[a,b]:b=0}').union(Set('{[a,b]:b=1}')).union(Set('{[a,b]:b=2}'))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([],1)))
		set.sets[1].conjunct.constraints.append(Equality(NormExp([],1)))
		set.sets[2].conjunct.constraints.append(Equality(NormExp([],1)))

		removed_contradiction=RemoveContradictionsVisitor().visit(set).removed_contradiction

		set_res=Set('{[a,b]:1=0}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==removed_contradiction,'removed_contradiction!=True')

#---------------------------------------------------

#---------- Find Functions Visitor ----------
class FindFunctionsTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import FindFunctionsVisitor
		from iegen import Set

		set=Set('{[a]}')
		v=FindFunctionsVisitor().visit(set)
		self.failUnless(hasattr(v,'functions'),"FindFunctionsVisitor doesn't place result in the 'functions' property.")

	def testNoFunctions(self):
		from iegen.ast.visitor import FindFunctionsVisitor
		from iegen import Set

		set=Set('{[]}')
		v=FindFunctionsVisitor().visit(set)

		self.failUnless([]==v.functions,'Functions found in a set with no functions: %s'%(v.functions))

	def testOneFunction(self):
		from iegen.ast.visitor import FindFunctionsVisitor
		from iegen import Set

		set=Set('{[a]: a=f(6)}')
		v=FindFunctionsVisitor().visit(set)
		res=['f']

		self.failUnless(res==v.functions,'%s!=%s'%(res,v.functions))

	def testTwoFunctionsSet(self):
		from iegen.ast.visitor import FindFunctionsVisitor
		from iegen import Set

		set=Set('{[a,b]: a=f(b) and b=g(a)}')
		v=FindFunctionsVisitor().visit(set)
		res=['f','g']

		self.failUnless(res==v.functions,'%s!=%s'%(res,v.functions))

	def testTwoFunctionsRelation(self):
		from iegen.ast.visitor import FindFunctionsVisitor
		from iegen import Relation

		rel=Relation('{[a]->[b]: a=f(b) and b=g(a)}')
		v=FindFunctionsVisitor().visit(rel)
		res=['f','g']

		self.failUnless(res==v.functions,'%s!=%s'%(res,v.functions))

	def testDuplicateFunctions(self):
		from iegen.ast.visitor import FindFunctionsVisitor
		from iegen import Set

		set=Set('{[a]: a=f(6) and a=f(5)}')
		v=FindFunctionsVisitor().visit(set)
		res=['f']

		self.failUnless(res==v.functions,'%s!=%s'%(res,v.functions))

	def testThreeFunctions(self):
		from iegen.ast.visitor import FindFunctionsVisitor
		from iegen import Set

		set=Set('{[a,b,c]: a=f(b) and b=g(a) and c=h(a)}')
		v=FindFunctionsVisitor().visit(set)
		res=['f','g','h']

		self.failUnless(res==v.functions,'%s!=%s'%(res,v.functions))

	def testNestedFunctions(self):
		from iegen.ast.visitor import FindFunctionsVisitor
		from iegen import Set

		set=Set('{[a,b,c]: a=f(g(h(b))) and b=g(a) and c=h(a)}')
		v=FindFunctionsVisitor().visit(set)
		res=['f','g','h']

		self.failUnless(res==v.functions,'%s!=%s'%(res,v.functions))

	def testSetUnion(self):
		from iegen.ast.visitor import FindFunctionsVisitor
		from iegen import Set

		set=Set('{[a,b,c]: a=f(g(h(b))) and b=g(a) and c=h(a)}').union(Set('{[a,d,e]: a=test(b) and a=h(4)}'))
		v=FindFunctionsVisitor().visit(set)
		res=['f','g','h','test']

		self.failUnless(res==v.functions,'%s!=%s'%(res,v.functions))
#--------------------------------------------

#---------- Collect Symbolics Visitor ----------
class CollectSymbolicsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import CollectSymbolicsVisitor
		from iegen import Set

		set=Set('{[a]}')
		v=CollectSymbolicsVisitor().visit(set)
		self.failUnless(hasattr(v,'symbolics'),"CollectSymbolicsVisitor doesn't place result in the 'symbolics' property.")

	def testNoSymbolics(self):
		from iegen.ast.visitor import CollectSymbolicsVisitor
		from iegen import Set

		set=Set('{[a]}')
		v=CollectSymbolicsVisitor().visit(set)
		res=[]

		self.failUnless(res==v.symbolics,'%s!=%s'%(res,v.symbolics))

	def testOneSymbolic(self):
		from iegen.ast.visitor import CollectSymbolicsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]: n=1}',[Symbolic('n')])
		v=CollectSymbolicsVisitor().visit(set)
		res=['n']

		self.failUnless(res==v.symbolics,'%s!=%s'%(res,v.symbolics))

	def testTwoSymbolicsSet(self):
		from iegen.ast.visitor import CollectSymbolicsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]: n=1 and m=2}',[Symbolic('n'),Symbolic('m')])
		v=CollectSymbolicsVisitor().visit(set)
		res=['m','n']

		self.failUnless(res==v.symbolics,'%s!=%s'%(res,v.symbolics))

	def testTwoSymbolicsRelation(self):
		from iegen.ast.visitor import CollectSymbolicsVisitor
		from iegen import Relation,Symbolic

		rel=Relation('{[a]->[ap]: n=1 and m=2}',[Symbolic('n'),Symbolic('m')])
		v=CollectSymbolicsVisitor().visit(rel)
		res=['m','n']

		self.failUnless(res==v.symbolics,'%s!=%s'%(res,v.symbolics))

	def testSymbolicsAcrossUnion(self):
		from iegen.ast.visitor import CollectSymbolicsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]: n=1}',[Symbolic('n'),Symbolic('m')]).union(Set('{[c]: j=10}',[Symbolic('j')]))
		v=CollectSymbolicsVisitor().visit(set)
		res=['j','n']

		self.failUnless(res==v.symbolics,'%s!=%s'%(res,v.symbolics))
#--------------------------------------------

#---------- Collect Vars Visitor ----------
class CollectVarsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Set

		set=Set('{[a]}')
		v=CollectVarsVisitor().visit(set)
		self.failUnless(hasattr(v,'vars'),"CollectVarsVisitor doesn't place result in the 'vars' property.")

	def testNoVarsSet(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Set

		set=Set('{[]}')
		v=CollectVarsVisitor().visit(set)
		res=[]

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testNoVarsRelation(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Relation

		rel=Relation('{[]->[]}')
		v=CollectVarsVisitor().visit(rel)
		res=[]

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testOneVarSet(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]: a=n}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(set)
		res=['a']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testOneVarRelation(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Relation,Symbolic

		rel=Relation('{[a]->[]: a=n}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(rel)
		res=['a']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testTwoVarsSet(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a,b]: a=1 and b=m}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(set)
		res=['a','b']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

		set=Set('{[b,a]: a=1 and b=m}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(set)
		res=['a','b']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testTwoVarsRelation(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Relation,Symbolic

		rel=Relation('{[a]->[b]: a=1 and b=n}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(rel)
		res=['a','b']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

		rel=Relation('{[b]->[a]: a=1 and b=n}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(rel)
		res=['a','b']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testTwoVarsSet(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Set

		set=Set('{[a,b,c]: a=1 and b=c}')
		v=CollectVarsVisitor().visit(set)
		res=['a','b','c']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

		set=Set('{[a,c,b]: a=1 and b=c}')
		v=CollectVarsVisitor().visit(set)
		res=['a','b','c']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testThreeVarsRelation(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Relation,Symbolic

		rel=Relation('{[a]->[b,c]: a=1 and b=c}')
		v=CollectVarsVisitor().visit(rel)
		res=['a','b','c']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

		rel=Relation('{[a,b]->[c]: a=1 and b=n}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(rel)
		res=['a','b','c']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testVarsAcrossUnionSet(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Set,Symbolic

		set=Set('{[a,b]: a=1}').union(Set('{[a,b]: c=10}'))
		v=CollectVarsVisitor().visit(set)
		res=['a','b']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testVarsAcrossUnionRelation(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Relation

		rel=Relation('{[a]->[d]: a=1}').union(Relation('{[a]->[d]: c=10}'))
		v=CollectVarsVisitor().visit(rel)
		res=['a','d']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testCollectFreeVar(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen.ast import Equality,NormExp,VarExp
		from iegen import Relation

		rel=Relation('{[a]->[d]: a=1}').union(Relation('{[a]->[d]: c=10}'))
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],10)))
		v=CollectVarsVisitor(all_vars=True).visit(rel)
		res=['a','b','d']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testCollectFreeVars(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen.ast import Equality,NormExp,VarExp
		from iegen import Relation

		rel=Relation('{[a]->[d]: a=1}').union(Relation('{[a]->[d]: c=10}'))
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],10)))
		rel.relations[1].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c')],10)))
		v=CollectVarsVisitor(all_vars=True).visit(rel)
		res=['a','b','c','d']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testCollectSymbolic(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen.ast import Equality,NormExp,VarExp
		from iegen import Relation,Symbolic

		rel=Relation('{[a]->[d]: a=n}',[Symbolic('n')]).union(Relation('{[a]->[d]: c=10}'))
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],10)))
		rel.relations[1].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c')],10)))
		v=CollectVarsVisitor(all_vars=True).visit(rel)
		res=['a','b','c','d','n']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testCollectTwice(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen.ast import Equality,NormExp,VarExp
		from iegen import Relation,Symbolic

		rel=Relation('{[a]->[b]: a=n}',[Symbolic('n')])
		v=CollectVarsVisitor(all_vars=True).visit(rel)
		rel=Relation('{[c]->[d]: c=n}',[Symbolic('n')])
		v.visit(rel)
		res=['a','b','c','d','n']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))
#--------------------------------------------

#---------- Remove Free Var Function Visitor ----------
class RemoveFreeVarFunctionVisitor(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set

		set=Set('{[]}')
		v=RemoveFreeVarFunctionVisitor({}).visit(set)
		self.failUnless(hasattr(v,'changed'),"RemoveFreeVarFunctionVisitor doesn't place result in the 'changed' property.")

	#Tests that this visitor doesn't die when given something other than a Set/Relation/PresSet/PresRelation
	#This tests that bug #89 is fixed
	def testAcceptOtherObjects(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen.ast import VarExp, NormExp, FuncExp,Equality,Inequality,Conjunction

		varexp=VarExp(1,'a')
		funcexp=FuncExp(1,'f',[NormExp([VarExp(1,'b')],0)])
		normexp=NormExp([VarExp(1,'c')],10)
		equality=Equality(NormExp([VarExp(1,'d')],10))
		inequality=Inequality(NormExp([VarExp(1,'e')],10))
		conjunction=Conjunction([Inequality(NormExp([VarExp(1,'f')],10))])
		equality2=Equality(NormExp([VarExp(1,'b'),FuncExp(1,'f',[NormExp([VarExp(1,'c')],0)])],-5))

		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(varexp).changed
		self.failUnless(False==changed,'changed!=False')
		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(funcexp).changed
		self.failUnless(False==changed,'changed!=False')
		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(normexp).changed
		self.failUnless(False==changed,'changed!=False')
		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(equality).changed
		self.failUnless(False==changed,'changed!=False')
		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(inequality).changed
		self.failUnless(False==changed,'changed!=False')
		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(conjunction).changed
		self.failUnless(False==changed,'changed!=False')
		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(equality2).changed
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor doesn't do anything in 'normal' situations
	def testNothingToDoSet(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set,Symbolic

		set=Set('{[a,b]: 10<=a and a<=n and b>n and b<22}',[Symbolic('n')])

		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(set).changed
		set_res=Set('{[a,b]: 10<=a and a<=n and b>n and b<22}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor doesn't do anything in 'normal' situations
	def testNothingToDoRelation(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Relation,Symbolic

		rel=Relation('{[a,b]->[ap,bp]: 10<=a and a<=n and b>n and b<22}',[Symbolic('n')])

		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(rel).changed
		rel_res=Relation('{[a,b]->[ap,bp]: 10<=a and a<=n and b>n and b<22}',[Symbolic('n')])

		self.failUnless(rel==rel,'%s!=%s'%(rel,rel))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor doesn't simplify when the function name isn't given
	def testFunctionNotGiven(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set

		set=Set('{[a]: a=f(b)}')

		changed=RemoveFreeVarFunctionVisitor({}).visit(set).changed
		set_res=Set('{[a]: a=f(b)}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

		set=Set('{[a]: a=f(b)}')

		changed=RemoveFreeVarFunctionVisitor({'g':'g_inv','g_inv':'g'}).visit(set).changed
		set_res=Set('{[a]: a=f(b)}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor simplifies a simple case
	def testSimplifySimple1(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set

		set=Set('{[a,b]: a=f(c) and b=g(c)}')

		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(set).changed
		simplify(set)
		set_res=Set('{[a,b]: b=g(f_inv(a))}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor simplifies a simple case
	def testSimplifySimple2(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set

		set=Set('{[a]: a=f(c) and a<=c}')

		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(set).changed
		simplify(set)
		set_res=Set('{[a]: a<=f_inv(a)}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor simplifies a simple case
	def testSimplifySimpleCoeff(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set

		set=Set('{[a,b]: 5a=f(c) and b=g(c)}')

		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(set).changed
		simplify(set)
		set_res=Set('{[a,b]: b=g(f_inv(5a))}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor doesn't simplify functions that aren't given
	def testSimplifyOnlyGiven1(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set

		set=Set('{[a,b]: a=f(d) and b=g(d) and a<=d}')

		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(set).changed
		simplify(set)
		set_res=Set('{[a,b]: b=g(f_inv(a)) and a<=f_inv(a)}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor doesn't simplify functions that aren't given
	def testSimplifyOnlyGiven2(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set

		set=Set('{[a,b,c]: a=f(d) and b=g(d) and a<=c+d}')

		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c]: b=g(f_inv(a)) and a<=c+f_inv(a)}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor simplifies all functions that are given
	def testSimplifyAllGiven(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set

		set=Set('{[a,b,c]: a=f(d) and b=g(e) and a<=d and c<=e}')

		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f','g':'g_inv','g_inv':'g'}).visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c]: a<=f_inv(a) and c<=g_inv(b)}')
		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor doesn't simplify functions that aren't given
	def testSimplifyWithSymbolic(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set,Symbolic

		set=Set('{[a]: a=f(c) and a+n<=c}',[Symbolic('n')])

		changed=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'}).visit(set).changed
		simplify(set)
		set_res=Set('{[a]: a+n<=f_inv(a)}',[Symbolic('n')])

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor saves the names of the functions that were used
	def testSimplifyFuncNames(self):
		from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
		from iegen import Set

		set=Set('{[a,b]: a=f(c) and b=g(c)}')

		v=RemoveFreeVarFunctionVisitor({'f':'f_inv','f_inv':'f'})
		changed=v.visit(set).changed
		simplify(set)
		set_res=Set('{[a,b]: b=g(f_inv(a))}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')
		self.failUnless('f'==v.func_name,'v.func_name!=f')
		self.failUnless('f_inv'==v.func_inv_name,'v.func_inv_name!=f_inv')
#--------------------------------------------------------

#---------- Unique Tuple Vars Visitor ----------
class UniqueTupleVarsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen import Set

		set=Set('{[]}')
		v=UniqueTupleVarsVisitor().visit(set)
		self.failUnless(hasattr(v,'changed'),"UniqueTupleVarsVisitor doesn't place result in the 'changed' property.")

	#Make sure the visitor doesn't do anything to empty Sets
	def testEmptySet(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction
		from iegen import Set

		set=Set(sets=[PresSet(VarTuple([]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(set).changed
		set_res=Set('{[]}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor doesn't do anything to empty Relations
	def testEmptyRelation(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction
		from iegen import Relation

		rel=Relation(relations=[PresRelation(VarTuple([]),VarTuple([]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		rel_res=Relation('{[]->[]}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor doesn't do anything to a Set this visitor doesn't apply to
	def testNoChangeSet(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction,VarExp
		from iegen import Set

		set=Set(sets=[PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'b')]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(set).changed
		set_res=Set('{[a,b]}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor doesn't do anything to a Relation this visitor doesn't apply to
	def testNoChangeRelation(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen import Relation

		rel=Relation(relations=[PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,'b')]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		rel_res=Relation('{[a]->[b]}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor renames variables in Sets for simple cases
	def testRenameSetSimple(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction,VarExp
		from iegen import Set

		set=Set(sets=[PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'a')]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,a0]:a=a0}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor renames variables in Relations for simple cases
	def testRenameRelationSimple1(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen import Relation

		rel=Relation(relations=[PresRelation(VarTuple([VarExp(1,'a'),VarExp(1,'a')]),VarTuple([]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		simplify(rel)
		rel_res=Relation('{[a,a0]->[]: a=a0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor renames variables in Relations for simple cases
	def testRenameRelationSimple2(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen import Relation

		rel=Relation(relations=[PresRelation(VarTuple([]),VarTuple([VarExp(1,'a'),VarExp(1,'a')]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		simplify(rel)
		rel_res=Relation('{[]->[a,a0]: a=a0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor renames variables in Relations for simple cases
	def testRenameRelationSimple3(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen import Relation

		rel=Relation(relations=[PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,'a')]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		simplify(rel)
		rel_res=Relation('{[a]->[a0]: a=a0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles renaming positions properly
	def testRenameSetPos(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction,VarExp
		from iegen import Set

		set=Set(sets=[PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c'),VarExp(1,'b')]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c,b0]:b=b0}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles renaming positions properly
	def testRenameRelationPos(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen import Relation

		rel=Relation(relations=[PresRelation(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c'),VarExp(1,'d')]),VarTuple([VarExp(1,'e'),VarExp(1,'f'),VarExp(1,'g'),VarExp(1,'c')]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		simplify(rel)
		rel_res=Relation('{[a,b,c,d]->[e,f,g,c0]: c=c0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles multiple renamings
	def testMultipleRenameSet(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction,VarExp
		from iegen import Set

		set=Set(sets=[PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c'),VarExp(1,'d'),VarExp(1,'c'),VarExp(1,'a'),VarExp(1,'b')]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c,d,c0,a0,b0]: a=a0 and b=b0 and c=c0}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles renaming positions properly
	def testMultipleRenameRelation(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen import Relation

		rel=Relation(relations=[PresRelation(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c'),VarExp(1,'c')]),VarTuple([VarExp(1,'d'),VarExp(1,'e'),VarExp(1,'a'),VarExp(1,'d')]),Conjunction([]))])

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		simplify(rel)
		rel_res=Relation('{[a,b,c,c0]->[d,e,a0,d0]: a=a0 and c=c0 and d=d0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles renaming with extra constraints
	def testRenameWithConstraintSet(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,NormExp,VarExp,FuncExp
		from iegen import Set

		set=Set(sets=[PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'a')]),Conjunction([Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([VarExp(1,'a')],0)])],0))]))])

		changed=UniqueTupleVarsVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,a0]: a=a0 and b=f(a)}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles renaming with extra constraints
	def testRenameWithConstraintRelation(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,Equality,NormExp,VarExp,FuncExp
		from iegen import Relation

		rel=Relation(relations=[PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,'b'),VarExp(1,'a')]),Conjunction([Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([VarExp(1,'a')],0)])],0))]))])

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		simplify(rel)
		rel_res=Relation('{[a]->[b,a0]: a=a0 and b=f(a)}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')
#--------------------------------------------------

#---------- Remove Equal Function Visitor ----------
class RemoveEqualFunctionVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen import Set

		set=Set('{[]}')
		v=RemoveEqualFunctionVisitor().visit(set)
		self.failUnless(hasattr(v,'changed'),"RemoveEqualFunctionVisitor doesn't place result in the 'changed' property.")

	#Make sure the visitor doesn't do anything to empty Sets
	def testEmptySet(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen import Set

		set=Set('{[]}')

		changed=RemoveEqualFunctionVisitor().visit(set).changed
		set_res=Set('{[]}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor doesn't do anything to empty Relations
	def testEmptyRelation(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen import Relation

		rel=Relation('{[]->[]}')

		changed=RemoveEqualFunctionVisitor().visit(rel).changed
		rel_res=Relation('{[]->[]}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(False==changed,'changed!=False')

	#Test that the equal variable cannot have a non-1 coefficient
	def testSetNon1Coeff(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Set

		set=Set('{[a,b,c]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([VarExp(1,'c')],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(2,'a'),FuncExp(-1,'f',[NormExp([VarExp(1,'c')],0)])],0)))

		changed=RemoveEqualFunctionVisitor().visit(set).changed
		set_res=Set('{[a,b,c]: 2a=f(c) and b=f(c)}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Test that the equality constraint cannot have a constant
	def testSetNoConst(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Set

		set=Set('{[a,b,c]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([VarExp(1,'c')],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([VarExp(1,'c')],0)])],5)))

		changed=RemoveEqualFunctionVisitor().visit(set).changed
		set_res=Set('{[a,b,c]: a+5=f(c) and b=f(c)}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Test a simple case for Sets
	def testSetSimple(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Set

		set=Set('{[a,b,c]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([VarExp(1,'c')],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([VarExp(1,'c')],0)])],0)))

		changed=RemoveEqualFunctionVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c]: a=b}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Test a simple case for Relations
	def testRelationSimple(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Relation

		rel=Relation('{[a,b]->[c]}')
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([VarExp(1,'c')],0)])],0)))
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([VarExp(1,'c')],0)])],0)))

		changed=RemoveEqualFunctionVisitor().visit(rel).changed
		simplify(rel)
		rel_res=Relation('{[a,b]->[c]:a=b}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Test a nested function case for Sets
	def testSetNested(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Set

		set=Set('{[a,b,c]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'c')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'c')],0)])],0)])],0)))

		changed=RemoveEqualFunctionVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c]: a=b}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Test a nested function case for Relations
	def testRelationNested(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Relation

		rel=Relation('{[a,b]->[c]}')
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'c')],0)])],0)])],0)))
		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'c')],0)])],0)])],0)))

		changed=RemoveEqualFunctionVisitor().visit(rel).changed
		simplify(rel)
		rel_res=Relation('{[a,b]->[c]: a=b}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Test that more than two constraints are able to be replaced
	def testSetReplaceThree(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Set

		set=Set('{[a,b,c,d]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'d')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'d')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'d')],0)])],0)])],0)))

		changed=RemoveEqualFunctionVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c,d]: a=b and a=c}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Test that more than two constraints are able to be replaced
	def testSetReplaceFour(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Set

		set=Set('{[a,b,c,d,e]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'d'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))

		changed=RemoveEqualFunctionVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c,d,e]: a=b and a=c and a=d}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Test that functions that are not equal are not replaced
	def testSetNotEqual(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Set

		set=Set('{[a,b,c,d,e]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),FuncExp(-1,'f',[NormExp([FuncExp(1,'s',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'d'),FuncExp(-1,'f',[NormExp([FuncExp(1,'r',[NormExp([VarExp(1,'e')],0)])],0)])],0)))

		changed=RemoveEqualFunctionVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c,d,e]: a=b and c=f(s(e)) and d=f(r(e))}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Test that equality constraints with multiple terms are not replaced
	def testSetMultipleTerms(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Set

		set=Set('{[a,b,c,d,e]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),VarExp(1,'a'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'d'),FuncExp(-1,'g',[NormExp([FuncExp(1,'f',[NormExp([VarExp(1,'e')],0)])],0)])],0)))

		changed=RemoveEqualFunctionVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c,d,e]: a=b and c+a=f(g(e)) and d=g(f(e))}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Test that multiple different function values are replaced
	def testSetReplaceDifferent(self):
		from iegen.ast.visitor import RemoveEqualFunctionVisitor
		from iegen.ast import Equality,VarExp,FuncExp,NormExp
		from iegen import Set

		set=Set('{[a,b,c,d,e]}')
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'a'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c'),FuncExp(-1,'g',[NormExp([FuncExp(1,'f',[NormExp([VarExp(1,'e')],0)])],0)])],0)))
		set.sets[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'d'),FuncExp(-1,'g',[NormExp([FuncExp(1,'f',[NormExp([VarExp(1,'e')],0)])],0)])],0)))

		changed=RemoveEqualFunctionVisitor().visit(set).changed
		simplify(set)
		set_res=Set('{[a,b,c,d,e]: a=b and c=d}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')
#---------------------------------------------------
