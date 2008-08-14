#!/usr/bin/env python

import omega

rel21=omega.OldRelation(2,1)
rel33=omega.OldRelation(3,3)

set1=omega.OldSet(1)
set1.name(1,"spam")
set4=omega.OldSet(4)
print set4
set4.name(("w","x","y","z"))
print set4
try:
	set4.name(("w","x","y","z","error"))
	print set4 #Shouldn't get here!
except RuntimeError,e:
	print "RuntimeError caught:",e

try:
	set1.name(2,"a")
except RuntimeError,e:
	print "RuntimeError caught:",e

try:
	rel21.name_in(-1,"b")
except RuntimeError,e:
	print "RuntimeError caught:",e

try:
	rel33.name_out(10,"z")
except RuntimeError,e:
	print "RuntimeError caught:",e

print "rel21 arities=("+str(rel21.arity_in())+","+str(rel21.arity_out())+")"
print "rel33 arities=("+str(rel33.arity_in())+","+str(rel33.arity_out())+")"
print "set1.arity()="+str(set1.arity())
print "set4.arity()="+str(set4.arity())

print rel21
rel21.name_in(("x","y"))
rel21.name_out(("z",))
print rel21
try:
	rel21.name_in(("x","y","error"))
except RuntimeError,e:
	print "RuntimeError caught:",e
try:
	rel21.name_out(("z","error"))
except RuntimeError,e:
	print "RuntimeError caught:",e

print rel21
print rel33
rel33.name_in(("w","x","y"))
rel33.name_out(("z","r","s"))
print rel33
print set1
print set4

print set4["w"]

#1<=t<=n ---> t-1>=0 AND n-t>=0
#AND(GEQ((1,t,-1)),GEQ((1,n,0),(-1,t,0)))
#(t-1>=0) &( n-t>=0)

#(0<=x<=100 AND (EXISTS y s.t. (2n<=y<=x AND y odd))) OR x=17


#Forumla
#|-And
#|-Or
#|-Not
#\-Declaration
#  |-Forall
#  \-Exists

#Expr
#|-GEQ
#|-EQ
#\-Stride

#Provide getitem for Declaration formulas



