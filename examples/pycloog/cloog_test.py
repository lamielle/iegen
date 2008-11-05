#!/usr/bin/env python

from iegen import Set,Symbolic
from iegen.pycloog import Statement,codegen

s1_domain=Set('{[k,i,j]: 0<=k and k<=L and 0<=i and i<=M and 0<=j and j<=N}',[Symbolic('L'),Symbolic('M'),Symbolic('N')])
s2_domain=Set('{[k,i,j]: 0<=k and k<=L and 0<=i and i<=M and 0<=j and j<=N}',[Symbolic('L'),Symbolic('M'),Symbolic('N')])

s1=Statement(s1_domain)
s2=Statement(s2_domain)

print codegen([s1,s2])
