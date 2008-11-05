#!/usr/bin/env python

from iegen import Set,Symbolic
from iegen.pycloog import Statement,codegen

s1_domain=Set('{[k,i,j]: 0<=k and k<=L and 0<=i and i<=M and 0<=j and j<=N}',[Symbolic('L'),Symbolic('M'),Symbolic('N')])
s2_domain=Set('{[k,i,j]: 0<=k and k<=L and 0<=i and i<=M and 0<=j and j<=N}',[Symbolic('L'),Symbolic('M'),Symbolic('N')])

s1_scatter=Set('{[p1,p2,p3,k,i,j,L,M,N]: p1=0 and p2=0 and p3=0}')
s2_scatter=Set('{[p1,p2,p3,k,i,j,L,M,N]: p1=0 and p2=0 and p3=0}')

s1=Statement(s1_domain,s1_scatter)
s2=Statement(s2_domain,s2_scatter)

print codegen([s1,s2])

s1_domain=Set('{[i,j]: 1<=i and i<=N and 1<=j and j<=N}',[Symbolic('N')])
s2_domain=Set('{[i,j]: 1<=i and i<=N and 1<=j and j<=N}',[Symbolic('N')])

s1_scatter=Set('{[c0,i1,c1,i2,c2,i,j,N]: c0=0 and i1=i and c1=0 and i2=j and c2=0}')
s1_scatter=Set('{[c0,i1,c1,i2,c2,i,j,N]: c0=1 and i1=0 and c1=0 and i2=0 and c2=0}')
s2_scatter=Set('{[c0,i1,c1,i2,c2,i,j,N]: c0=0 and i1=i and c1=1 and i2=j and c2=0}')
s2_scatter=Set('{[c0,i1,c1,i2,c2,i,j,N]: c0=i and i1=0 and c1=0 and i2=0 and c2=0}')

s1=Statement(s1_domain,s1_scatter)
s2=Statement(s2_domain,s2_scatter)

for row in s1.scatter:
	print row
#[[0, 0, -1, 0, 0, 0, 1, 0, 0, 0],
# [0, 0, 0, 0, 1, 0, 0, -1, 0, 0],
# [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
# [0, 0, 0, -1, 0, 0, 0, 0, 0, 1]]

#[[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
# [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],

print codegen([s1,s2])
