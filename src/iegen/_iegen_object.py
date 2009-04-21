#---------- IEGenObject class ----------
class IEGenObject(object):
	__slots__=('settings',)

	#Defines the possible output types.  Each tuple is:
	#(output type name, short option string, default value
	# 'quiet' value, 'verbose' value, help string)
	output_types=(
	   ('code','-o',[],[],[None],'generated code'),
	   ('progress','',[None],[],[None],'progress messages'),
	   ('modified','',[],[],[None],'components as they are modified'),
	   ('detail','',[],[],[None],'more detailed messages'),
	   ('info','',[None],[],[None],'general information messages'),
	   ('debug','',[],[],[],'debug messages'),
	   ('error','',[None],[None],[None],'error messages'))

	class IEGenSettings(object): pass
	settings=IEGenSettings()

	def __init__(self): pass

	#Custom hash function
	#IEGenObjects hashes are the hash of the string class_name+str(object)
	def __hash__(self):
		return hash(self.__class__.__name__+str(self))

	#Setup default outputs
	outputs={}
	for type,short,default,quiet,verbose,help in output_types:
		outputs[type]=default
	settings.outputs=outputs

	#Debug is False by default
	settings.debug=False

	#Dynamically define printing methods based on output types
	for type,short,default,quiet,verbose,help in output_types:
		exec("def print_%s(self,output=None): from iegen import print_gen; print_gen('%s',output)"%(type,type))
#---------------------------------------
