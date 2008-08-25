from unittest import TestCase

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
			from iegen.util import run_tests,full_iter_space,define_properties,DimensionalityError,tuple_gen,lower_gen,upper_gen,parse_test,ast_equality_test,test_sets,test_relations
		except Exception,e:
			self.fail("Importing classes from iegen.util failed: "+str(e))
#----------------------------------
