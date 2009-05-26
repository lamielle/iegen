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
			from iegen.codegen import do_calc
			from iegen.codegen import calc_initial_idg,calc_idg_deps,calc_er_spec_deps
			from iegen.codegen import calc_update_access_relations,calc_unupdate_access_relations,calc_access_relation_rename
			from iegen.codegen import calc_reorder_call,calc_erg_call
			from iegen.codegen import calc_full_iter_space,calc_bound_string,calc_lower_bound_string,calc_upper_bound_string,calc_size_string,calc_equality_value
			#_ito.py
			from iegen.codegen import do_ito
			#_gen.py
			from iegen.codegen import do_gen,gen_preamble,gen_index_array,gen_tuple_vars_decl
			#_gen_inspector.py
			from iegen.codegen import gen_inspector,gen_er_spec,gen_output_er_spec,gen_call
			#_gen_executor.py
			from iegen.codegen import gen_executor
			#_gen_main.py
			from iegen.codegen import gen_main
			#_program_ast.py
			from iegen.codegen import Program,Function,Statement,VarDecl
		except ImportError,e:
			self.fail('Importing classes from iegen.codegen failed: '+str(e))
#----------------------------------
