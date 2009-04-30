import iegen

#---------- IEGenObject class ----------
class IEGenObject(object):
	__slots__=('settings',)

	settings=iegen.settings

	def __init__(self): pass

	#Custom hash function
	#IEGenObjects hashes are the hash of the string class_name+str(object)
	def __hash__(self):
		return hash(self.__class__.__name__+str(self))

	#Dynamically define printing methods based on output types
	for type,short,default,quiet,verbose,help in iegen.settings.output_types:
		exec("def print_%s(self,output=None): from iegen import print_gen; print_gen('%s',output)"%(type,type))
#---------------------------------------
