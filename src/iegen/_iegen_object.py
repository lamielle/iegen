#---------- IEGenObject class ----------
class IEGenObject(object):
	__slots__=('settings',)

	class IEGenSettings(object): pass
	settings=IEGenSettings()

	def __init__(self): pass

	#Helper method for debug printing
	#Will print only if self.settings.debug is True
	def debug_print(self,output):
		if self.settings.debug: print output

	#Static helper method for debug printing
	#Will print only if IEGenObject.settings.debug is True
	def debug_print(output):
		if IEGenObject.settings.debug: print output
	debug_print=staticmethod(debug_print)

	#Helper method for printing information messages
	#Will print only if self.settings.quiet is False
	def info_print(self,output):
		if not self.settings.quiet: print output

	#Static helper method for printing information messages
	#Will print only if IEGenObject.settings.quiet is False
	def info_print(output):
		if not IEGenObject.settings.quiet: print output
	info_print=staticmethod(info_print)
#---------------------------------------
