#!/usr/bin/env python

from omega import OldSet,OldRelation

#Create a set with arity 2
#Variable names are 'a' and 'b'
s=OldSet(("a","b"))

#Get the variable objects for 'a' and 'b'
a=s["a"]
b=s["b"]

#Get a free variable called 'n'
n=s["n"]

#Create the formula 1<=a<=n AND 1<=b<=n and assign it to s
s.formula=( (a>=1) & (a<=n) & (b>=1) & (b<=n))
print "Original set:",s

#Specify the value of n
n=3
print "Value of n:",n

#Print the code for s
print "Code for original set:\n",s.code()

#Iterate through each of the tuples in the set s
print "Tuples in original set:",
for t in s:
	print t,
print

#Create a relation with input arity 2 and output arity 2
#The input and output variables are named as well
r=OldRelation(("a","b"),("ap","bp"))

#Get the input and output variables
a=r["a"]
b=r["b"]
ap=r["ap"]
bp=r["bp"]

#Assign the formular ap=2a and bp=2b to r
#This is a relation that scales by a factor of 2
r.formula=( (ap==2*a) & (bp==2*b) )
print "Scaling relation by a factor of 2:",r

#Apply the scaling relation to the set s
s.apply(r)
print "Scaled set:",s

print "Scaled set code:\n",s.code()

#Iterate through the tuples in the scaled set s
print "Tuples in scaled set:",
for t in s:
	print t,
print
