#!/usr/bin/env python

from __future__ import with_statement
from omega import OldSet,OldRelation

#Build the set {1<=a,b<=4}
s=OldSet(("a","b"))
a=s["a"]
b=s["b"]
with s: s.formula=((1<=a)&(a<=4)&(1<=b)&(b<=4))

print "OldSet before scale:",s

#Create a scaling transformation (factor 3)
scale3=OldRelation.scale(2,3)

#Apply the scaling transformation to the set
print "OldSet before scale:",
for t in s: print t,
print
s.apply(scale3)
print
print "OldSet after scale:",s
print "OldSet after scale:",
for t in s: print t,
print

#Create a new set {1<=a,b,<=4}
s=OldSet(("a","b"))
with s: s.formula=((1<=a)&(a<=4)&(1<=b)&(b<=4))
print
print "OldSet before skew: ",s

#Create a skewing transformation (skew right by a factor of 1)
#skew(transformation dimension (arity), skew dimension, base dimension, skew factor)
skew1=OldRelation.skew(2,2,1,1)

#Apply the skewing transformation to the set
print "OldSet before skew:",
for t in s: print t,
print
s.apply(skew1)
print
print "OldSet after skew: ",s
print "OldSet after skew:",
for t in s: print t,
print

