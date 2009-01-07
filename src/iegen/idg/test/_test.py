from unittest import TestCase

#---------- Import Tests ----------
#Test importing of iegen.codegen
class ImportTestCase(TestCase):

	#Test simple importing of iegen.codegen
	def testImport(self):
		try:
			import iegen.idg
		except Exception,e:
			self.fail("'import iegen.idg' failed: "+str(e))

	#Test simple importing of iegen.codegen classes
	def testNameImport(self):
		try:
			from iegen.idg import IDGNode
		except ImportError,e:
			self.fail('Importing classes from iegen.idg failed: '+str(e))
#----------------------------------
