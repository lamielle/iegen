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
			from iegen.ast.visitor import DFVisitor,UniqueTupleVarsVisitor,SparseTransVisitor,IsVarVisitor
		except Exception,e:
			self.fail("Importing classes from iegen.ast.visitor failed: "+str(e))
#----------------------------------

#---------- Depth First Visitor Tests ----------
#Test base visitor class
class DFVisitorTestCase(TestCase):

	#Test that 'self' is returned from the visit method
	def testReturnsSelf(self):
		from iegen.ast.visitor import DFVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]}')

		v=DFVisitor()

		self.failUnless(v.visit(set) is v,"visit() method does not return 'self'")
#-----------------------------------------------

#---------- Unique Tuple Vars Visitor ----------
class UniqueTupleVarsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]}')
		v=UniqueTupleVarsVisitor().visit(set)
		self.failUnless(hasattr(v,'changed'),"UniqueTupleVarsVisitor doesn't place result in the 'changed' property.")

#DISABLED: This test no longer works after AST changes
#	#Make sure the visitor doesn't do anything to empty Sets
#	def testEmptySet(self):
#		from iegen.ast.visitor import UniqueTupleVarsVisitor
#		from iegen.ast import PresSet,VarTuple,Conjunction
#		from iegen import Set
#
#		set=PresSet(VarTuple([]),Conjunction([]))
#
#		changed=UniqueTupleVarsVisitor().visit(set).changed
#		set_res=Set('{[]}')
#
#		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
#		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor doesn't do anything to empty Relations
	def testEmptyRelation(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction
		from iegen.parser import PresParser

		rel=PresRelation(VarTuple([]),VarTuple([]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		rel_res=PresParser.parse_relation('{[]->[]}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor doesn't do anything to a Set this visitor doesn't apply to
	def testNoChangeSet(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction,VarExp
		from iegen.parser import PresParser

		set=PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'b')]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(set).changed
		set_res=PresParser.parse_set('{[a,b]}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor doesn't do anything to a Relation this visitor doesn't apply to
	def testNoChangeRelation(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen.parser import PresParser

		rel=PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,'b')]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		rel_res=PresParser.parse_relation('{[a]->[b]}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(False==changed,'changed!=False')

	#Make sure the visitor renames variables in Sets for simple cases
	def testRenameSetSimple(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction,VarExp
		from iegen.parser import PresParser

		set=PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'a')]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(set).changed
		set_res=PresParser.parse_set('{[a,a0]:a=a0}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor renames variables in Relations for simple cases
	def testRenameRelationSimple1(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen.parser import PresParser

		rel=PresRelation(VarTuple([VarExp(1,'a'),VarExp(1,'a')]),VarTuple([]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		rel_res=PresParser.parse_relation('{[a,a0]->[]: a=a0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor renames variables in Relations for simple cases
	def testRenameRelationSimple2(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen.parser import PresParser

		rel=PresRelation(VarTuple([]),VarTuple([VarExp(1,'a'),VarExp(1,'a')]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		rel_res=PresParser.parse_relation('{[]->[a,a0]: a=a0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor renames variables in Relations for simple cases
	def testRenameRelationSimple3(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen.parser import PresParser

		rel=PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,'a')]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		rel_res=PresParser.parse_relation('{[a]->[a0]: a=a0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles renaming positions properly
	def testRenameSetPos(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction,VarExp
		from iegen.parser import PresParser

		set=PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c'),VarExp(1,'b')]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(set).changed
		set_res=PresParser.parse_set('{[a,b,c,b0]:b=b0}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles renaming positions properly
	def testRenameRelationPos(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen.parser import PresParser

		rel=PresRelation(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c'),VarExp(1,'d')]),VarTuple([VarExp(1,'e'),VarExp(1,'f'),VarExp(1,'g'),VarExp(1,'c')]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		rel_res=PresParser.parse_relation('{[a,b,c,d]->[e,f,g,c0]: c=c0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles multiple renamings
	def testMultipleRenameSet(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction,VarExp
		from iegen.parser import PresParser

		set=PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c'),VarExp(1,'d'),VarExp(1,'c'),VarExp(1,'a'),VarExp(1,'b')]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(set).changed
		set_res=PresParser.parse_set('{[a,b,c,d,c0,a0,b0]: c=c0 and a=a0 and b=b0 }')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles renaming positions properly
	def testMultipleRenameRelation(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,VarExp
		from iegen.parser import PresParser

		rel=PresRelation(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'c'),VarExp(1,'c')]),VarTuple([VarExp(1,'d'),VarExp(1,'e'),VarExp(1,'a'),VarExp(1,'d')]),Conjunction([]))

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		rel_res=PresParser.parse_relation('{[a,b,c,c0]->[d,e,a0,d0]: c=c0 and a=a0 and d=d0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles renaming with extra constraints
	def testRenameWithConstraintSet(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,NormExp,VarExp,FuncExp
		from iegen.parser import PresParser

		set=PresSet(VarTuple([VarExp(1,'a'),VarExp(1,'b'),VarExp(1,'a')]),Conjunction([Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([VarExp(1,'a')],0)])],0))]))

		changed=UniqueTupleVarsVisitor().visit(set).changed
		set_res=PresParser.parse_set('{[a,b,a0]: b=f(a) and a=a0}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))
		self.failUnless(True==changed,'changed!=True')

	#Make sure the visitor handles renaming with extra constraints
	def testRenameWithConstraintRelation(self):
		from iegen.ast.visitor import UniqueTupleVarsVisitor
		from iegen.ast import PresRelation,VarTuple,Conjunction,Equality,NormExp,VarExp,FuncExp
		from iegen.parser import PresParser

		rel=PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,'b'),VarExp(1,'a')]),Conjunction([Equality(NormExp([VarExp(1,'b'),FuncExp(-1,'f',[NormExp([VarExp(1,'a')],0)])],0))]))

		changed=UniqueTupleVarsVisitor().visit(rel).changed
		rel_res=PresParser.parse_relation('{[a]->[b,a0]: b=f(a) and a=a0}')

		self.failUnless(rel_res==rel,'%s!=%s'%(rel_res,rel))
		self.failUnless(True==changed,'changed!=True')
#--------------------------------------------------

#---------- Collect Vars Visitor ----------
class CollectVarsVisitorTestCase(TestCase):

	#Make sure the result of the visiting is placed in the proper attribute
	def testResultPresent(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[a]}')
		v=CollectVarsVisitor().visit(set)
		self.failUnless(hasattr(v,'vars'),"CollectVarsVisitor doesn't place result in the 'vars' property.")

	def testNoVarsSet(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]}')
		v=CollectVarsVisitor().visit(set)
		res=[]

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testNoVarsRelation(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen.parser import PresParser

		rel=PresParser.parse_relation('{[]->[]}')
		v=CollectVarsVisitor().visit(rel)
		res=[]

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testOneVarSet(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Symbolic
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[a]: a=n}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(set)
		res=['a']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testOneVarRelation(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Symbolic
		from iegen.parser import PresParser

		rel=PresParser.parse_relation('{[a]->[]: a=n}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(rel)
		res=['a']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testTwoVarsSet(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Symbolic
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[a,b]: a=1 and b=m}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(set)
		res=['a','b']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

		set=PresParser.parse_set('{[b,a]: a=1 and b=m}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(set)
		res=['a','b']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testTwoVarsRelation(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Symbolic
		from iegen.parser import PresParser

		rel=PresParser.parse_relation('{[a]->[b]: a=1 and b=n}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(rel)
		res=['a','b']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

		rel=PresParser.parse_relation('{[b]->[a]: a=1 and b=n}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(rel)
		res=['a','b']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testTwoVarsSet(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[a,b,c]: a=1 and b=c}')
		v=CollectVarsVisitor().visit(set)
		res=['a','b','c']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

		set=PresParser.parse_set('{[a,c,b]: a=1 and b=c}')
		v=CollectVarsVisitor().visit(set)
		res=['a','b','c']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testThreeVarsRelation(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen import Symbolic
		from iegen.parser import PresParser

		rel=PresParser.parse_relation('{[a]->[b,c]: a=1 and b=c}')
		v=CollectVarsVisitor().visit(rel)
		res=['a','b','c']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

		rel=PresParser.parse_relation('{[a,b]->[c]: a=1 and b=n}',[Symbolic('n')])
		v=CollectVarsVisitor().visit(rel)
		res=['a','b','c']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

#DISABLED: union is no longer supported for ASTs
#	def testVarsAcrossUnionSet(self):
#		from iegen.ast.visitor import CollectVarsVisitor
#		from iegen import Set,Symbolic
#
#		set=Set('{[a,b]: a=1}').union(Set('{[a,b]: c=10}'))
#		v=CollectVarsVisitor().visit(set)
#		res=['a','b']
#
#		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))
#
#	def testVarsAcrossUnionRelation(self):
#		from iegen.ast.visitor import CollectVarsVisitor
#		from iegen import Relation
#
#		rel=Relation('{[a]->[d]: a=1}').union(Relation('{[a]->[d]: c=10}'))
#		v=CollectVarsVisitor().visit(rel)
#		res=['a','d']
#
#		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))
#
#	def testCollectFreeVar(self):
#		from iegen.ast.visitor import CollectVarsVisitor
#		from iegen.ast import Equality,NormExp,VarExp
#		from iegen import Relation
#
#		rel=Relation('{[a]->[d]: a=1}').union(Relation('{[a]->[d]: c=10}'))
#		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],10)))
#		v=CollectVarsVisitor(all_vars=True).visit(rel)
#		res=['a','b','d']
#
#		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))
#
#	def testCollectFreeVars(self):
#		from iegen.ast.visitor import CollectVarsVisitor
#		from iegen.ast import Equality,NormExp,VarExp
#		from iegen import Relation
#
#		rel=Relation('{[a]->[d]: a=1}').union(Relation('{[a]->[d]: c=10}'))
#		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],10)))
#		rel.relations[1].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c')],10)))
#		v=CollectVarsVisitor(all_vars=True).visit(rel)
#		res=['a','b','c','d']
#
#		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))
#
#	def testCollectSymbolic(self):
#		from iegen.ast.visitor import CollectVarsVisitor
#		from iegen.ast import Equality,NormExp,VarExp
#		from iegen import Relation,Symbolic
#
#		rel=Relation('{[a]->[d]: a=n}',[Symbolic('n')]).union(Relation('{[a]->[d]: c=10}'))
#		rel.relations[0].conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],10)))
#		rel.relations[1].conjunct.constraints.append(Equality(NormExp([VarExp(1,'c')],10)))
#		v=CollectVarsVisitor(all_vars=True).visit(rel)
#		res=['a','b','c','d','n']
#
#		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))

	def testCollectTwice(self):
		from iegen.ast.visitor import CollectVarsVisitor
		from iegen.ast import Equality,NormExp,VarExp
		from iegen.parser import PresParser
		from iegen import Symbolic

		rel=PresParser.parse_relation('{[a]->[b]: a=n}',[Symbolic('n')])
		v=CollectVarsVisitor(all_vars=True).visit(rel)
		rel=PresParser.parse_relation('{[c]->[d]: c=n}',[Symbolic('n')])
		v.visit(rel)
		res=['a','b','c','d','n']

		self.failUnless(res==v.vars,'%s!=%s'%(res,v.vars))
#--------------------------------------------

#---------- Var Visitor Tests ----------
#Test var visitor
class IsVarVisitorTestCase(TestCase):

	#Make sure the results of the visiting are placed in the is_var, is_symbolic_var, is_constraint_var, and is_tuple_var attributes
	def testResultPresent(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]}')
		v=IsVarVisitor('a').visit(set)
		self.failUnless(hasattr(v,'is_var'),"IsVarVisitor doesn't place result in the 'is_var' property.")
		self.failUnless(hasattr(v,'is_symbolic_var'),"IsVarVisitor doesn't place result in the 'is_symbolic_var' property.")
		self.failUnless(hasattr(v,'is_constraint_var'),"IsVarVisitor doesn't place result in the 'is_constraint_var' property.")
		self.failUnless(hasattr(v,'is_tuple_var'),"IsVarVisitor doesn't place result in the 'is_tuple_var' property.")

	#Tests that vars in the Symbolics are searched
	def testIsVarSearchSymbolics(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Symbolic
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]}')
		set.symbolics.append(Symbolic('n'))

		relation=PresParser.parse_relation('{[]->[]}')
		relation.symbolics.append(Symbolic('n'))

		self.failUnless(IsVarVisitor('n').visit(set).is_var,"'n' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('n').visit(relation).is_var,"'n' is not a var in %s"%relation)

	#Tests that vars in variable tuples are searched
	def testIsVarSearchVarTuple(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[a]}')
		relation=PresParser.parse_relation('{[a]->[b]}')

		self.failUnless(IsVarVisitor('a').visit(set).is_var,"'a' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('a').visit(relation).is_var,"'a' is not a var in %s"%relation)
		self.failUnless(IsVarVisitor('b').visit(relation).is_var,"'b' is not a var in %s"%relation)

	#Tests that vars in the constraints are searched
	def testIsVarSearchConstraints(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen.parser import PresParser
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=PresParser.parse_set('{[]}')
		set.conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=PresParser.parse_relation('{[]->[]}')
		relation.conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		self.failUnless(IsVarVisitor('a').visit(set).is_var,"'a' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('b').visit(set).is_var,"'b' is not a var in %s"%set)
		self.failUnless(IsVarVisitor('a').visit(relation).is_var,"'a' is not a var in %s"%relation)
		self.failUnless(IsVarVisitor('b').visit(relation).is_var,"'b' is not a var in %s"%relation)

	#Tests that vars in the Symbolics are searched
	def testIsSymSearchSymbolics(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Symbolic
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]}')
		set.symbolics.append(Symbolic('n'))

		relation=PresParser.parse_relation('{[]->[]}')
		relation.symbolics.append(Symbolic('n'))

		self.failUnless(IsVarVisitor('n').visit(set).is_symbolic_var,"'n' is not a symbolic var in %s"%set)
		self.failUnless(IsVarVisitor('n').visit(relation).is_symbolic_var,"'n' is not a symbolic var in %s"%relation)

	#Tests that vars in variable tuples are not searched
	def testIsSymNoSearchVarTuple(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[a]}')
		relation=PresParser.parse_relation('{[a]->[b]}')

		self.failIf(IsVarVisitor('a').visit(set).is_symbolic_var,"'a' is a symbolic var in %s"%set)
		self.failIf(IsVarVisitor('a').visit(relation).is_symbolic_var,"'a' is a symbolic var in %s"%relation)
		self.failIf(IsVarVisitor('b').visit(relation).is_symbolic_var,"'b' is a symbolic var in %s"%relation)

	#Tests that vars in the constraints are not searched
	def testIsSymNoSearchConstraints(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen.parser import PresParser
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=PresParser.parse_set('{[]}')
		set.conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=PresParser.parse_relation('{[]->[]}')
		relation.conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		self.failIf(IsVarVisitor('a').visit(set).is_symbolic_var,"'a' is a symbolic var in %s"%set)
		self.failIf(IsVarVisitor('b').visit(set).is_symbolic_var,"'b' is a symbolic var in %s"%set)
		self.failIf(IsVarVisitor('a').visit(relation).is_symbolic_var,"'a' is a symbolic var in %s"%relation)
		self.failIf(IsVarVisitor('b').visit(relation).is_symbolic_var,"'b' is a symbolic var in %s"%relation)

	#Tests that vars in the Symbolics are searched
	def testIsConstraintNoSearchSymbolics(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Symbolic
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]}',[Symbolic('n')])
		set.symbolics.append(Symbolic('n'))

		relation=PresParser.parse_relation('{[]->[]}')
		relation.symbolics.append(Symbolic('n'))

		self.failIf(IsVarVisitor('n').visit(set).is_constraint_var,"'n' is a constraint var in %s"%set)
		self.failIf(IsVarVisitor('n').visit(relation).is_constraint_var,"'n' is a constraint var in %s"%relation)

	#Tests that vars in variable tuples are not searched
	def testIsConstraintNoSearchVarTuple(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[a]}')
		relation=PresParser.parse_relation('{[a]->[b]}')

		self.failIf(IsVarVisitor('a').visit(set).is_constraint_var,"'a' is a constraint var in %s"%set)
		self.failIf(IsVarVisitor('a').visit(relation).is_constraint_var,"'a' is a constraint var in %s"%relation)
		self.failIf(IsVarVisitor('b').visit(relation).is_constraint_var,"'b' is a constraint var in %s"%relation)

	#Tests that vars in the constraints are not searched
	def testIsConstraintSearchConstraints(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen.parser import PresParser
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=PresParser.parse_set('{[]}')
		set.conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=PresParser.parse_relation('{[]->[]}')
		relation.conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		self.failUnless(IsVarVisitor('a').visit(set).is_constraint_var,"'a' is not a constraint var in %s"%set)
		self.failUnless(IsVarVisitor('b').visit(set).is_constraint_var,"'b' is not a constraint var in %s"%set)
		self.failUnless(IsVarVisitor('a').visit(relation).is_constraint_var,"'a' is not a constraint var in %s"%relation)
		self.failUnless(IsVarVisitor('b').visit(relation).is_constraint_var,"'b' is not a constraint var in %s"%relation)

	#Tests that vars in the Tuples are not searched
	def testIsTupleNoSearchSymbolics(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen import Symbolic
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[]}',[Symbolic('n')])
		set.symbolics.append(Symbolic('n'))

		relation=PresParser.parse_relation('{[]->[]}')
		relation.symbolics.append(Symbolic('n'))

		self.failIf(IsVarVisitor('n').visit(set).is_tuple_var,"'n' is a tuple var in %s"%set)
		self.failIf(IsVarVisitor('n').visit(relation).is_tuple_var,"'n' is a tuple var in %s"%relation)

	#Tests that vars in variable tuples are searched
	def testIsTupleSearchVarTuple(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen.parser import PresParser

		set=PresParser.parse_set('{[a]}')
		relation=PresParser.parse_relation('{[a]->[b]}')

		self.failUnless(IsVarVisitor('a').visit(set).is_tuple_var,"'a' is a not tuple var in %s"%set)
		self.failUnless(IsVarVisitor('a').visit(relation).is_tuple_var,"'a' is a not tuple var in %s"%relation)
		self.failUnless(IsVarVisitor('b').visit(relation).is_tuple_var,"'b' is a not tuple var in %s"%relation)

	#Tests that vars in the constraints are not searched
	def testIsTupleNoSearchConstraints(self):
		from iegen.ast.visitor import IsVarVisitor
		from iegen.parser import PresParser
		from iegen.ast import Equality,Inequality,NormExp,VarExp

		set=PresParser.parse_set('{[]}')
		set.conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		set.conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		relation=PresParser.parse_relation('{[]->[]}')
		relation.conjunct.constraints.append(Equality(NormExp([VarExp(1,'b')],1)))
		relation.conjunct.constraints.append(Inequality(NormExp([VarExp(-1,'a')],10)))

		self.failIf(IsVarVisitor('a').visit(set).is_tuple_var,"'a' is a tuple var in %s"%set)
		self.failIf(IsVarVisitor('b').visit(set).is_tuple_var,"'b' is a tuple var in %s"%set)
		self.failIf(IsVarVisitor('a').visit(relation).is_tuple_var,"'a' is a tuple var in %s"%relation)
		self.failIf(IsVarVisitor('b').visit(relation).is_tuple_var,"'b' is a tuple var in %s"%relation)
#---------------------------------------
