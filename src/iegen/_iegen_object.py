#---------- IEGenObject class ----------
class IEGenObject(object):
	__slots__=('settings',)

	class IEGenSettings(object): pass
	settings=IEGenSettings()

	def __init__(self): pass

	#Helper method for debug printing
	#Will print only if self.settings.debug is True
	def debug_print(self,output=None):
		if self.settings.debug:
			if None is output: print
			else: print output

	#Static helper method for debug printing
	#Will print only if IEGenObject.settings.debug is True
	def debug_print(output=None):
		if IEGenObject.settings.debug:
			if None is output: print
			else: print output
	debug_print=staticmethod(debug_print)

	#Helper method for printing information messages
	#Will print only if self.settings.quiet is False
	def info_print(self,output=None):
		if not self.settings.quiet:
			if None is output: print
			else: print output

	#Static helper method for printing information messages
	#Will print only if IEGenObject.settings.quiet is False
	def info_print(output=None):
		if not IEGenObject.settings.quiet:
			if None is output: print
			else: print output
	info_print=staticmethod(info_print)
#---------------------------------------
