from unittest import TestCase

#Test importing of iegen.pycloog
class ImportTestCase(TestCase):

	#Test simple importing of iegen.pycloog
	def testImport(self):
		try:
			import iegen.pycloog
		except Exception,e:
			self.fail("'import iegen.pycloog' failed: "+str(e))

	#Test simple importing of iegen.pycloog classes
	def testNameImport(self):
		try:
			from iegen.pycloog import Statement,Names,codegen
		except Exception,e:
			self.fail("Importing classes from iegen.pycloog failed: "+str(e))

class PYCLooGTestCase(TestCase):

	def testPYCLooGSimple(self):
		from iegen.pycloog import Statement,Names,codegen

		dom1=[[1, 1, 0,0, -1],
			  [1,-1, 0,1, 0],
			  [1, 0, 1,0, -1],
			  [1, 0,-1,1,0]]
		scat1=[[0,1,0,0,0,1]]
		dom2=[[1, 1, 0,0, -1],
			  [1,-1, 0,1, 0],
			  [1, 0, 1,0, -1],
			  [1, 0,-1,1,0]]
		scat2=[[0,1,0,0,0,2]]

		stmt1=Statement(dom1,scat1)
		stmt2=Statement(dom2,scat2)
		stmts=(stmt1,stmt2)
		names=Names(['i','j'],['n'])
		print codegen(stmts,names)
