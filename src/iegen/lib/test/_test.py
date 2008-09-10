from unittest import TestCase
from nose.tools import raises

#---------- Import Tests ----------
#Test importing of iegen.lib modules
class ImportTestCase(TestCase):

	#Test simple importing of iegen.lib
	def testImport(self):
		try:
			import iegen.lib
		except Exception,e:
			self.fail("'import iegen.lib' failed: "+str(e))

	#Test simple importing of iegen.lib.ply
	def testImportPLY(self):
		try:
			import iegen.lib.ply
		except Exception,e:
			self.fail("'import iegen.lib.ply' failed: "+str(e))

	#Test simple importing of iegen.ast.visitor classes
	def testNameImportPLY(self):
		try:
			from iegen.lib.ply import lex,yacc
		except Exception,e:
			self.fail("Importing classes from iegen.lib.ply failed: "+str(e))

	#Test simple importing of iegen.lib.nose
	def testImportNose(self):
		try:
			import iegen.lib.nose
		except Exception,e:
			self.fail("'import iegen.lib.nose' failed: "+str(e))

	#Test simple importing of iegen.ast.visitor classes
	def testNameImportNose(self):
		try:
			from iegen.lib.nose import DeprecatedTest,SkipTest,collector,main,run,run_exit,runmodule,with_setup

		except Exception,e:
			self.fail("Importing classes from iegen.lib.nose failed: "+str(e))

	#Test simple importing of iegen.lib.decorator
	def testImportDecorator(self):
		try:
			import iegen.lib.decorator
		except Exception,e:
			self.fail("'import iegen.lib.decorator' failed: "+str(e))

	#Test simple importing of iegen.ast.visitor classes
	def testNameImportDecorator(self):
		try:
			from iegen.lib.decorator import decorator,getinfo,new_wrapper
		except Exception,e:
			self.fail("Importing classes from iegen.lib.decorator failed: "+str(e))

	#Test simple importing of iegen.lib.coverage
	def testImportCoverage(self):
		try:
			import iegen.lib.coverage
		except Exception,e:
			self.fail("'import iegen.lib.coverage' failed: "+str(e))

	#Test simple importing of iegen.ast.visitor classes
	def testNameImportCoverage(self):
		try:
			from iegen.lib.coverage import start,stop,analysis,report
		except Exception,e:
			self.fail("Importing classes from iegen.lib.coverage failed: "+str(e))
#----------------------------------
