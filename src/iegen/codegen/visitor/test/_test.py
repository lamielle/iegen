from unittest import TestCase

#---------- Import Tests ----------
#Test importing of iegen.codegen.visitor
class ImportTestCase(TestCase):

	#Test simple importing of iegen.codegen.visitor
	def testImport(self):
		try:
			import iegen.codegen.visitor
		except Exception,e:
			self.fail("'import iegen.codegen.visitor' failed: "+str(e))

	#Test simple importing of iegen.codegen.visitor classes
	def testNameImport(self):
		try:
			from iegen.codegen.visitor import DFVisitor,CPrintVisitor
		except ImportError,e:
			self.fail('Importing classes from iegen.codegen.visitor failed: '+str(e))
#----------------------------------
