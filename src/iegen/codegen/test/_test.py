from unittest import TestCase

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
			#_codegen.py
			from iegen.codegen import calc_full_iter_space,get_bound_string,get_lower_bound_string,get_upper_bound_string
			#_program_ast.py
			from iegen.codegen import Program,Function,Statement
		except ImportError,e:
			self.fail('Importing classes from iegen.codegen failed: '+str(e))
#----------------------------------
