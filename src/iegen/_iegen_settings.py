from __future__ import with_statement
import iegen

#---------- Settings related setup and definitions ----------

#---------- Settings class ----------
class IEGenSettings(object): pass
#------------------------------------

#---------- Global settings access ----------
iegen.settings=IEGenSettings()
#--------------------------------------------

#Define the possible output types.  Each tuple is:
#(output type name, short option string, default value
# 'quiet' value, 'verbose' value, help string)
iegen.settings.output_types=(
   ('code','-o',[],[],[None],'generated code'),
   ('progress','',[None],[],[None],'progress messages'),
   ('modified','',[],[],[None],'components as they are modified'),
   ('detail','',[],[],[None],'more detailed messages'),
   ('info','',[None],[],[None],'general information messages'),
   ('debug','',[],[],[],'debug messages'),
   ('operation','',[],[],[],'operations debugging messages'),
   ('error','',[None],[None],[None],'error messages'))

#Setup default outputs
outputs={}
for type,short,default,quiet,verbose,help in iegen.settings.output_types:
	outputs[type]=default
iegen.settings.outputs=outputs

#Debug is False by default
iegen.settings.debug=False

#Processing (simplification and checking) is disabled by default
iegen.settings.enable_processing=False

#---------- Printing methods -----
def print_gen(type,output=None):
	for dest in iegen.settings.outputs[type]:
		if dest is None:
			if output is None: print
			else: print output
		else:
			#Code is a special case as we don't want to append
			if 'code'==type:
				mode='w'
				print_progress("Writing generated code to file '%s'..."%(dest))
			else:
				mode='a'

			with file(dest,mode) as f:
				if output is None: print >>f
				else: print >>f,output

#Dynamically define printing methods based on output types
for type,short,default,quiet,verbose,help in iegen.settings.output_types:
	exec("def print_%s(output=None): print_gen('%s',output)"%(type,type))
#---------------------------------
#------------------------------------------------------------
