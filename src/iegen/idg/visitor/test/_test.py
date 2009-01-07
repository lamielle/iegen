from unittest import TestCase

#---------- Import Tests ----------
#Test importing of iegen.idg.visitor
class ImportTestCase(TestCase):

	#Test simple importing of iegen.idg.visitor
	def testImport(self):
		try:
			import iegen.idg.visitor
		except Exception,e:
			self.fail("'import iegen.idg.visitor' failed: "+str(e))

	#Test simple importing of iegen.idg.visitor classes
	def testNameImport(self):
		try:
			from iegen.idg.visitor import TopoVisitor
		except ImportError,e:
			self.fail('Importing classes from iegen.idg.visitor failed: '+str(e))
#----------------------------------
