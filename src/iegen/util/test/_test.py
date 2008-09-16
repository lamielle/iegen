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
			from iegen.util import run_tests,invert_dict,define_properties,get_basic_term,find_term,like_type,is_iterable,raise_objs_not_like_types,DimensionalityError,normalize_self,normalize_result,check
			from iegen.util import tuple_gen,lower_gen,upper_gen,parse_test,ast_equality_test,test_sets,test_set_strings,test_relations,test_relation_strings
		except Exception,e:
			self.fail("Importing classes from iegen.util failed: "+str(e))
#----------------------------------
