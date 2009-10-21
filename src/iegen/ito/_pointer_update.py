from iegen.ito import InterTransOpt

#---------- PointerUpdate class ----------
class PointerUpdate(InterTransOpt):

	def __init__(self,name):
		InterTransOpt.__init__(self,name)

	def __repr__(self):
		return 'PointerUpdate(%s)'%(self.name)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent

		return '''%sPointerUpdate:
%s|-name: %s'''%(spaces,spaces,self.name)


	def apply(self,mapir):
		print "PointerUpdate.apply does not do anything yet!"	
#-------------------------------------------
