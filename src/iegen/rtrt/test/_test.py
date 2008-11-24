from unittest import TestCase

#---------- Import Tests ----------
#Test importing of iegen.rtrt
class ImportTestCase(TestCase):

	#Test simple importing of iegen.rtrt
	def testImport(self):
		try:
			import iegen.rtrt
		except Exception,e:
			self.fail("'import iegen.rtrt' failed: "+str(e))

	#Test simple importing of iegen.rtrt classes
	def testNameImport(self):
		try:
			from iegen.rtrt import RTRT,DataPermuteRTRT,DataEmbedRTRT,DataProjectRTRT,IterPermuteRTRT,IterEmbedRTRT,IterProjectRTRT
		except ImportError,e:
			self.fail('Importing classes from iegen.rtrt failed: '+str(e))
#----------------------------------
