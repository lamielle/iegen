#!/usr/bin/env python

import omega

s=omega.OldSet(3)
s.name(1,"r")
s.name(2,"s")
s.name(3,"t")
print s
s=omega.OldSet("r")
print s
s=omega.OldSet(("r","s","t"))
print s

r=omega.OldRelation("a","b")
print r
r=omega.OldRelation(("a","b"),("c",))
print r

n=s["n"]
print n
n=s[("n",0)]
print n
f=s[("F",1,omega.TupleType.inp)]
print f
