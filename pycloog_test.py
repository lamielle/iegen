#!/usr/bin/env python

from ctypes import *
from iegen.pycloog import Statement,Names,codegen

dom1=[[1, 1, 0,0, -1],
     [1,-1, 0,1, 0],
     [1, 0, 1,0, -1],
     [1, 0,-1,1,0]]
scat1=[[0,1,0,0,0,1]]
dom2=[[1, 1, 0,0, -1],
     [1,-1, 0,1, 0],
     [1, 0, 1,0, -1],
     [1, 0,-1,1,0]]
scat2=[[0,1,0,0,0,2]]

stmt1=Statement(dom1,scat1)
stmt2=Statement(dom2,scat2)
stmts=(stmt1,stmt2)
names=Names(['i','j'],['n'])
codegen(stmts,names)
