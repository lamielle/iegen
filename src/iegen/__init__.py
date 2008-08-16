from _iegen import *

#Append to sys.path so that the modules in lib are found
import os,os.path,sys

newpath=os.path.abspath(os.path.dirname(__file__))+os.sep+'lib'
sys.path=[newpath]+sys.path
