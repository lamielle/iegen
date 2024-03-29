from unittest import TestCase
from iegen.lib.nose.tools import raises

#---------- Import Tests ----------
#Test importing of iegen.simplify
class ImportTestCase(TestCase):

	#Test simple importing of iegen.simplify
	def testImport(self):
		try:
			import iegen.simplify
		except Exception,e:
			self.fail("'import iegen.simplify' failed: "+str(e))

	#Test simple importing of iegen.simplify classes
	def testNameImport(self):
		try:
			#_simplify.py
			from iegen.simplify import simplify,register_rule,register_inverse_pair,unregister_inverse_pair,inverse_pairs
			#_rules.py
			from iegen.simplify import register_inverse_simplify_listener
		except Exception,e:
			self.fail("Importing classes from iegen.simplify failed: "+str(e))
#----------------------------------

#---------- Simplify Tests ----------
#Test simplification rules
#class SimplifyTestCase(TestCase):
#DISABLED: simplify no longer supported
#	#Test that simplify does not accept arguments other than Sets and Relations
#	@raises(ValueError)
#	def testNonFormulaFail1(self):
#		from iegen.simplify import simplify
#		simplify(1)
#	@raises(ValueError)
#	def testNonFormulaFail2(self):
#		from iegen.simplify import simplify
#		simplify('a')
#------------------------------------
