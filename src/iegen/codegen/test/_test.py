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
			from iegen.codegen import codegen
			#_calc.py
			from iegen.codegen import do_calc,calc_full_iter_space,,calc_size_string
			#_ito.py
			from iegen.codegen import do_ito
			#_gen.py
			from iegen.codegen import do_gen,gen_preamble
			#_gen_inspector.py
			from iegen.codegen import gen_inspector
			#_gen_executor.py
			from iegen.codegen import gen_executor
			#_gen_main.py
			from iegen.codegen import gen_main
			#_program_ast.py
			from iegen.codegen import Program,Function,Statement,VarDecl
		except ImportError,e:
			self.fail('Importing classes from iegen.codegen failed: '+str(e))
#----------------------------------
