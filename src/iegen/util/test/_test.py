from unittest import TestCase
from iegen.lib.nose.tools import raises

#---------- Import Tests ----------
#Test importing of iegen.util
class ImportTestCase(TestCase):

	#Test simple importing of iegen.util
	def testImport(self):
		try:
			import iegen.util
		except Exception,e:
			self.fail("'import iegen.util' failed: "+str(e))

	#Test simple importing of iegen.util classes
	def testNameImport(self):
		try:
			#_util.py
			from iegen.util import run_tests,sign,invert_dict,define_properties,get_basic_term,find_term,like_type,is_iterable,raise_objs_not_like_types,DimensionalityError,normalize_self,normalize_result,check
			#_test_util.py
			from iegen.util import tuple_gen,lower_gen,upper_gen,parse_test,ast_equality_test,test_sets,test_set_strings,test_relations,test_relation_strings
			#_simplify.py
			from iegen.util import simplify
		except Exception,e:
			self.fail("Importing classes from iegen.util failed: "+str(e))
#----------------------------------

#---------- Sign Tests ----------
class SignTestCase(TestCase):

	#Tests that sign(1)==1
	def testSign1(self):
		from iegen.util import sign
		self.failUnless(1==sign(1),'sign(1)!=1')

	#Tests that sign(-1)==-1
	def testSignNeg1(self):
		from iegen.util import sign
		self.failUnless(-1==sign(-1),'sign(-1)!=-1')

	#Tests that sign(0)==1
	def testSign0(self):
		from iegen.util import sign
		self.failUnless(1==sign(1),'sign(0)!=1')

	#Tests that sign(6)==1
	def testSign6(self):
		from iegen.util import sign
		self.failUnless(1==sign(6),'sign(6)!=1')

	#Tests that sign(-6)==-1
	def testSignNeg6(self):
		from iegen.util import sign
		self.failUnless(-1==sign(-6),'sign(-6)!=-1')
#--------------------------------

#---------- Simplify Tests ----------
#Test simplification rules
class SimplifyTestCase(TestCase):

	#Test that simplify does not accept arguments other than Sets and Relations
	@raises(ValueError)
	def testNonFormulaFail1(self):
		from iegen.util import simplify
		simplify(1)
	@raises(ValueError)
	def testNonFormulaFail2(self):
		from iegen.util import simplify
		simplify('a')
#------------------------------------
