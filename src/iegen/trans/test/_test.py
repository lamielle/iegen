from unittest import TestCase

#---------- Import Tests ----------
#Test importing of iegen.trans
class ImportTestCase(TestCase):

	#Test simple importing of iegen.trans
	def testImport(self):
		try:
			import iegen.trans
		except Exception,e:
			self.fail("'import iegen.trans' failed: "+str(e))

	#Test simple importing of iegen.trans classes
	def testNameImport(self):
		try:
			from iegen.trans import Transformation,DataPermuteTrans,DataEmbedTrans,DataProjectTrans,IterPermuteTrans,IterEmbedTrans,IterProjectTrans,SparseTileTrans,CacheBlockTrans,SparseLoopTrans
		except ImportError,e:
			self.fail('Importing classes from iegen.trans failed: '+str(e))
#----------------------------------
