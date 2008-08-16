from unittest import TestCase

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
			from iegen.util import define_properties,DimensionalityError
		except Exception,e:
			self.fail("Importing classes from iegen.util failed: "+str(e))
