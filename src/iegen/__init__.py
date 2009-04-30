from _iegen_settings import *
from _iegen_object import *
from _iegen import *
from _set_relation import *
from _mapir import *

#for item in dir(_iegen):
#	exec("has_module=hasattr(%s,'__module__')"%item)
#	if has_module:
#		exec("print '%s.__module__=',%s.__module__"%(item,item))
#		exec("%s.__module__='iegen'"%item)
#		exec("print '%s.__module__=',%s.__module__"%(item,item))

#Append to sys.path so that the modules in lib are found
import os,os.path,sys

newpath=os.path.abspath(os.path.dirname(__file__))+os.sep+'lib'
sys.path=[newpath]+sys.path
