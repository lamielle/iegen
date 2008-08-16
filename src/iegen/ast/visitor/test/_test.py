from unittest import TestCase

#Test importing of iegen.ast.visitor
class ImportTestCase(TestCase):

	#Test simple importing of iegen.ast.visitor
	def testImport(self):
		try:
			import iegen.ast.visitor
		except Exception,e:
			self.fail("'import iegen.ast.visitor' failed: "+str(e))

	#Test simple importing of iegen.ast.visitor classes
	def testNameImport(self):
		try:
			from iegen.ast.visitor import DFVisitor,TransVisitor
		except Exception,e:
			self.fail("Importing classes from iegen.ast.visitor failed: "+str(e))
