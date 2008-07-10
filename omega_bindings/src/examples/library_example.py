#!/usr/bin/env python

from omega import OldSet,OldRelation

#S1 := { [t] | 1<=t<=n };
S1=OldSet(1)
S1.name(1,"t")
#S1=OldSet("t") or S1=OldSet(("t",))
t=S1["t"]
n=S1["n"]
S1.set_formula=((t-1>=0) & (n-t>=0))

#S2 := { [x] | (0<=x<=100 & Exists y s.t. (2n<=y<=x & y is odd)) | x=17 };
S2=OldSet(1)
S2.name(1,"x")
#S2=OldSet("x") or S2=OldSet(("x",))
x=S2["x"]
S2s_n=S2["n"]
y=S2[("y",-1)]
S2.set_formula=((x=17) | ((x>=0) & (100-x>=0) & Exists(y,((y-2n>=0) & (x-y>=0) & Stride(2,(y+1)))))

#R := { [i,j]->[i',j'] | 1<=i<=i'<=n & ~(F(i)=F(i')) & 1<=j,j'<=m };
R=OldRelation(2,2)
R.name_in(("i","j"))
R.name_in(("ip","jp"))
#R=OldRelation(("i","j"),("ip","jp")) or R=OldRelation("i","ip") for single dimensions
i=R["i"]
j=R["j"]
ip=R["ip"]
jp=R["jp"]
Rs_n=R["n"]
Rs_m=R["m"]
Rs_f_in=R[("F",1,inp)]
Rs_f_out=R[("F",1,out)]
#R.set_formula(
