#---------- IEGenObject class ----------
class IEGenObject(object):
	__slots__=('settings',)

	class IEGenSettings(object): pass

	def __init__(self):
		self.settings=IEGenObject.IEGenSettings()

	#Helper method for debug printing
	#Will print only if self.settings.debug is True
	def debug_print(self,output):
		if self.settings.aether.debug: print output
#---------------------------------------
