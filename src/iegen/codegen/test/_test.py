from unittest import TestCase
from iegen.lib.nose.tools import raises

#---------- Import Tests ----------
#Test importing of iegen.codegen
class ImportTestCase(TestCase):

	#Test simple importing of iegen.codegen
	def testImport(self):
		try:
			import iegen.codegen
		except Exception,e:
			self.fail("'import iegen.codegen' failed: "+str(e))

	#Test simple importing of iegen.codegen classes
	def testNameImport(self):
		try:
			from iegen.codegen import full_iter_space,simplify
		except ImportError,e:
			self.fail('Importing classes from iegen.codegen failed: '+str(e))
#----------------------------------

#---------- Simplify Tests ----------
#Test simplification rules
class SimplifyTestCase(TestCase):

	#Test that simplify does not accept arguments other than Sets and Relations
	@raises(ValueError)
	def testNonFormulaFail1(self):
		from iegen.codegen import simplify
		simplify(1)
	@raises(ValueError)
	def testNonFormulaFail2(self):
		from iegen.codegen import simplify
		simplify('a')

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

		set=Relation('{[a]->[ap]: a=b and b=6 and ap=c and c=7}')

		set_res=Relation('{[a]->[ap]: a=6 and ap=7}')

		self.failUnless(set_res==set,'%s!=%s'%(set_res,set))

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
#------------------------------------