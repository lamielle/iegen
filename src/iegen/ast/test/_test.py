from unittest import TestCase

#Test importing of iegen.ast
class ImportTestCase(TestCase):

	#Test simple importing of iegen.ast
	def testImport(self):
		try:
			import iegen.ast
		except Exception,e:
			self.fail("'import iegen.ast' failed: "+str(e))

	#Test simple importing of iegen.ast classes
	def testNameImport(self):
		try:
			from iegen.ast import Node,PresSet,PresSetUnion,PresRelation,PresRelationUnion,VarTuple,Conjunction,Constraint,Equality,Inequality,Expression,VarExp,FuncExp,NormExp
		except Exception,e:
			self.fail("Importing classes from iegen.ast failed: "+str(e))

class ASTTestCase(TestCase):

	def testSetRelation(self):
		from iegen.ast import PresSet,PresSetUnion,PresRelation,PresRelationUnion

	def testVarTuple(self):
		from iegen.ast import VarTuple

	def testConjunction(self):
		from iegen.ast import Conjunction

	def testConstraint(self):
		from iegen.ast import Equality,Inequality

	def testExpression(self):
		from iegen.ast import VarExp,FuncExp,NormExp

## Initial testing of the ast
#from ast import *
#
#root = PresSet(VarTuple(['a','b']),Conjunction([Inequality(NormExp([VarExp(1,'a')],-5))]))
#



#print
#print "========================= Testing equality of uninterp func ===="
##f = FuncExp('f',[VarExp('a'),IntExp(3),MulExp(IdExp('b'),IdExp('c'))])
##g = FuncExp('g',[IdExp('a'),IntExp(3),MulExp(IdExp('b'),IdExp('c'))])
##print "f= ", f
##print "g= ", g
##print "f==g should be false, f==g => ", f==g 
#
##g= FuncExp('f',[IdExp('a'),IntExp(3),MulExp(IdExp('b'),IdExp('c'))])
##print "f= ", f
##print "g= ", g
##print "f==g should be true, f==g => ", f==g
#
##g= FuncExp('f',[IdExp('a'),IntExp(3),MulExp(IdExp('c'),IdExp('b'))])
##print "f= ", f
##print "g= ", g
##print "f==g should be true, f==g => ", f==g
#
##g= FuncExp('f',[IdExp('a'),MulExp(IdExp('c'),IdExp('b'))])
##print "f= ", f
##print "g= ", g
##print "f==g should be false, f==g => ", f==g





