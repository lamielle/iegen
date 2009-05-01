# Script was originally written to show the naming bug #104.
# That bug is now fixed.  4/30/09, MMS

#!/usr/bin/env python

import iegen
from iegen import Set,Relation,Symbolic

import iegen.simplify

from iegen import IEGenObject
# None corresponds to stdout
IEGenObject.settings.outputs['debug'].append(None)


syms = [Symbolic("N"),Symbolic("T"),Symbolic("n_inter")]
iegen.simplify.register_inverse_pair('delta','delta_inv')

def ar_broken():
	a4_0=Relation('{[c0,s_out1,c1,j,c2]->[k]: c0=0 and c2=0 and k+-1inter1(j)=0 and -1c1+1=0}')

	#### DataPermuteTrans
	R_x0_x1 = Relation("{[k] -> [j] : j = sigma(k)}")

	a4_1 =  R_x0_x1.compose(a4_0)

	#### Loop Alignment
	T_I0_to_I1 = Relation('{[c0, s, c0, i, c0] -> [c0, s, c0, j, c0] : c0=0 && j=sigma(i)}').union( Relation('{[c0, s, c1, ii, x] -> [c0, s, c1, ii, x] : c0=0 && c1=1}') )

	a4_2 =  a4_1.compose( T_I0_to_I1.inverse() )

	#### IterPermuteTrans
	T_I1_to_I2 = Relation("{[c0,s1,c1,i,c2] -> [c3,s2,c4,j,c5] : s1=s2 && c0=0 && c1=0 && c2=0 && c3=0 && c4=0 && c5=0 && i=j}").union( Relation("{[c6,s3,c7,ii,x] -> [c8,s4,c9,j,y] : s3=s4 && j = delta(ii) && c6=0 && c8=0 && c7=1 && c9=1 && x=y }"))

	a4_3 =  a4_2.compose( T_I1_to_I2.inverse() )

	print a4_3

def ar_working():
	a4_0=Relation('{[c0,s_out1,c1,j,c2]->[k]: c0=0 and c2=0 and k+-1inter1(j)=0 and -1c1+1=0}')

	#### DataPermuteTrans
	R_x0_x1 = Relation("{[sigma_in] -> [sigma_out] : sigma_out = sigma(sigma_in)}")

	a4_1 =  R_x0_x1.compose(a4_0)

	#### Loop Alignment
	T_I0_to_I1 = Relation('{[c0, s, c0, i, c0] -> [c0, s, c0, j, c0] : c0=0 && j=sigma(i)}').union( Relation('{[c0, s, c1, ii, x] -> [c0, s, c1, ii, x] : c0=0 && c1=1}') )

	a4_2 =  a4_1.compose( T_I0_to_I1.inverse() )

	#### IterPermuteTrans
	T_I1_to_I2 = Relation("{[c0,s1,c1,i,c2] -> [c3,s2,c4,j,c5] : s1=s2 && c0=0 && c1=0 && c2=0 && c3=0 && c4=0 && c5=0 && i=j}").union( Relation("{[c6,s3,c7,ii,x] -> [c8,s4,c9,j,y] : s3=s4 && j = delta(ii) && c6=0 && c8=0 && c7=1 && c9=1 && x=y }"))

	a4_3 =  a4_2.compose( T_I1_to_I2.inverse() )

	print a4_3

def ar_recursion_bug():
	a4_0=Relation('{[s_out1,j]->[k]: k+-1inter1(j)=0}')

	#### DataPermuteTrans
	R_x0_x1 = Relation("{[sigma_in] -> [sigma_out] : sigma_out = sigma(sigma_in)}")

	a4_1 =  R_x0_x1.compose(a4_0)

	#### Loop Alignment
	T_I0_to_I1 = Relation('{[s,i] -> [s,j]: j=sigma(i)}')

	a4_2 =  a4_1.compose( T_I0_to_I1.inverse() )

	#### IterPermuteTrans
	T_I1_to_I2 = Relation("{[s3,ii]->[s4,j]: s3=s4 && j = delta(ii) }")

	a4_3 =  a4_2.compose( T_I1_to_I2.inverse() )

	print a4_3

def ar_testing():
	a4_0=Relation('{[s_out1,j]->[k]: k+-1inter1(j)=0}')

	#### DataPermuteTrans
	R_x0_x1 = Relation("{[sigma_in] -> [sigma_out] : sigma_out = sigma(sigma_in)}")

	a4_1 =  R_x0_x1.compose(a4_0)

	#### Loop Alignment
	T_I0_to_I1 = Relation('{[s,i] -> [s,j]: j=sigma(i)}')

	a4_2 =  a4_1.compose( T_I0_to_I1.inverse() )

	#### IterPermuteTrans
	T_I1_to_I2 = Relation("{[s,ii]->[s,j]: j = delta(ii) }")

	a4_3 =  a4_2.compose( T_I1_to_I2.inverse() )

	print a4_3

#ar_testing()
ar_broken()
ar_working()
ar_recursion_bug()
