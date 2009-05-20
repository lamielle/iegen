# Set and Relation operations needed for M2 example.
# See RTRTJournalShared/moldyn-FST-example.tex for corresponding writeup.
# Also see iegen/example/moldyn-FST.spec

#import cProfile
#import pstats

import iegen
from iegen import Set
from iegen import Relation
from iegen import Symbolic

import iegen.simplify

from iegen.ast.visitor import PrettyPrintVisitor


#from iegen import IEGenObject
## None corresponds to stdout
#IEGenObject.settings.outputs['debug'].append(None)

##### Compose scheduling/scattering function for each statement
##### with the statement's original iteration space.
#iegen.simplify.registerInversePairs()

syms = [Symbolic("N"),Symbolic("T"), Symbolic("n_inter")]

# S1
print "==== S1"
S1_I = Set("{[s,i]: 0<=s && s<T && 0<=i && i<N}", syms)
print S1_I

S1_sched = Relation("{[s,i]->[c0,s,c1,j,c2]: c0=0 && c1=0 && c2=0 && i=j}")
#print S1_sched
PrettyPrintVisitor().visit(S1_sched)


S1_full_I = S1_I.apply(S1_sched)
print S1_full_I

# S2
print "==== S2"
S2_I = Set("{[s,i]: 0<=s && s<T && 0<=i && i<n_inter}", syms)
print S2_I

S2_sched = Relation("{[s,i]->[c0,s,c1,j,c2]: c0=0 && c1=1 && c2=0 && i=j}")
#print S2_sched
PrettyPrintVisitor().visit(S2_sched)


S2_full_I = S2_I.apply(S2_sched)
print S2_full_I

# S3
print "==== S3"
S3_I = Set("{[s,i]: 0<=s && s<T && 0<=i && i<n_inter}", syms)
print S3_I

S3_sched = Relation("{[s,i]->[c0,s,c1,j,c2]: c0=1 && c1=1 && c2=1 && i=j}")
#print S3_sched
PrettyPrintVisitor().visit(S3_sched)


S3_full_I = S3_I.apply(S3_sched)
print S3_full_I

# full iteration space
print "==== Full Iteration Space"
full_I = S1_full_I.union(S2_full_I.union(S3_full_I))
print full_I

#### Modifying the access relations so that their source is the 
#### full iteration space.

# A1, access relation for S1, targets data array x
print "==== A1, access relation for S1"
a1 = Relation("{[s,i]->[i] }")
#print a1
PrettyPrintVisitor().visit(a1)
print "Modified a1, or a1_0"
a1_0 = a1.compose(S1_sched.inverse())
#print a1_0
PrettyPrintVisitor().visit(a1_0)


# A4, access relation for S2, targets data array x
print "==== A4, access relation for S2"
a4 = Relation("{[s,i]->[k]: k=inter1(i)}")
#print a4
PrettyPrintVisitor().visit(a4)
print "Modified a4, or a4_0"
a4_0 = a4.compose(S2_sched.inverse())
#print a4_0
PrettyPrintVisitor().visit(a4_0)

# A8, access relation for S3, targets data array x
print "==== A8, access relation for S3"
a8 = Relation("{[s,i]->[k]: k=inter2(i)}")
#print a8
PrettyPrintVisitor().visit(a8)
print "Modified a8, or a8_0"
a8_0 = a8.compose(S2_sched.inverse())
#print a8_0
PrettyPrintVisitor().visit(a8_0)



#### DataPermuteTrans
print
print "==== DataPermuteTrans"

print "explicit relation specification generated by calc_input"
print "\tinput:"
print "\t\tall access relations that target data array x"
iter_sub_space_relation = Relation("{[c0,s,c1,i,c2]->[i] : c1=1}")
print "\t\titer_sub_space_relation = ", iter_sub_space_relation
print "\talgorithm:"
print "\t\tall_ar = union of all access relations"
all_ar = a1_0.union( a4_0.union( a8_0 ) )
print "\t\tall_ar = "
PrettyPrintVisitor().visit(all_ar)
print
#### PERFORMANCE PROBLEM: the following composition causes a noticable pause
print "\toutput:"
print "\t\tars of interest = inverse (iter_sub_space_relation compose (inverse all_ar))"
ars_of_interest = iter_sub_space_relation.compose( all_ar.inverse() ).inverse()
print "\t\tars of interest = " 
PrettyPrintVisitor().visit(ars_of_interest)

#cProfile.run('iter_sub_space_relation.compose( all_ar.inverse() ).inverse()','prof')
#p = pstats.Stats('prof')
#p.strip_dirs()
#p.sort_stats('cumulative').print_stats(20)
#p.sort_stats('time').print_stats(20)
#p.print_callers(20)
print
print
print "Update modified access relations based on automatically derived data reordering specification."
R_x0_x1 = Relation("{[k] -> [j] : j = sigma(k)}")
print "\tdata reordering specification (R_x0_x1) = ", R_x0_x1
print
print "\ta1_1 = R_x0_x1 compose a1_0 = "
a1_1 = R_x0_x1.compose(a1_0)
#print a1_1
PrettyPrintVisitor().visit(a1_1)
print
print "\ta4_1 = R_x0_x1 compose a4_0 = "
a4_1 =  R_x0_x1.compose(a4_0)
#print a4_1
PrettyPrintVisitor().visit(a4_1)
print
print "\ta8_1 = R_x0_x1 compose a8_0 = "
a8_1 =  R_x0_x1.compose(a8_0)
#print a8_1
PrettyPrintVisitor().visit(a8_1)


#### Loop Alignment
print
print "==== Loop Alignment"
print "The transformation relation: "
T_I0_to_I1 = Relation('{[c0, s, c0, i, c0] -> [c0, s, c0, j, c0] : c0=0 && j=sigma(i)}')
T_I0_to_I1 = T_I0_to_I1.union( Relation('{[c0, s, c1, ii, x] -> [c0, s, c1, ii, x] : c0=0 && c1=1}') )
print "\tT_I0_to_I1 = "
PrettyPrintVisitor().visit(T_I0_to_I1)
print
print "Updating access relations due to T_I0_to_I1: "
print
print "\ta1_2  = a1_1 compose (inverse T_I0_to_I1)"
a1_2 =  a1_1.compose( T_I0_to_I1.inverse() )
#print a1_2
PrettyPrintVisitor().visit(a1_2)
print
print "\ta4_2  = a4_1 compose (inverse T_I0_to_I1)"
a4_2 =  a4_1.compose( T_I0_to_I1.inverse() )
#print a4_2
PrettyPrintVisitor().visit(a4_2)
print
print "\ta8_2  = a8_1 compose (inverse T_I0_to_I1)"
a8_2 =  a8_1.compose( T_I0_to_I1.inverse() )
#print a8_2
PrettyPrintVisitor().visit(a8_2)
print
print "Updating a data dependence: "
D_I0_to_I0 = Relation('{[c0,s,c0,i,c0] -> [c0,s,c1,ii,c0] : c0=0 && c1=1 && i=inter1(ii)}')
print "\tD_I0_to_I0 = "
PrettyPrintVisitor().visit(D_I0_to_I0)
print "Updating the data dependence due to the loop alignment transformation."
print "\tD_I1_to_I1 = T_I0_to_I1 compose ( D_I0_to_I0 compose (inverse T_I0_to_I1)"
D_I1_to_I1 = T_I0_to_I1.compose( D_I0_to_I0.compose( T_I0_to_I1.inverse() ) )
print "\t           = "
PrettyPrintVisitor().visit(D_I1_to_I1)


#### IterPermuteTrans
iegen.simplify.register_inverse_pair('delta','delta_inv')
print
print "==== IterPermuteTrans"
T_I1_to_I2 = Relation("{[c0,s,c0,i,c0] -> [c0,s,c0,i,c0] : c0=0 }")
T_I1_to_I2 = T_I1_to_I2.union( Relation("{[c0,s,c1,ii,x] -> [c0,s,c1,j,x] : j = delta(ii) && c0=0  && c1=1 }"))
print "T_I1_to_I2 = "
PrettyPrintVisitor().visit(T_I1_to_I2)

print
print "Computing ER_2, or access relation that is input to permutation alg"
print "\tAR = union over all access relations to x or fx"
AR = a1_2.union( a4_2.union( a8_2 ) )
print "\t\t= "
PrettyPrintVisitor().visit(AR)

issr = Relation('{[c0, s, c1, ii, c2] -> [ ii ] : c1=1}')
print "\tissr = "
PrettyPrintVisitor().visit(issr)
print
temp = AR.compose(issr.inverse())
print "\tAR compose (inverse issr)= "
PrettyPrintVisitor().visit(temp)

print
print "Updating access relations due to T_I1_to_I2: "
print
print "\ta1_3  = a1_2 compose (inverse T_I1_to_I2)"
a1_3 =  a1_2.compose( T_I1_to_I2.inverse() )
#print a1_3
PrettyPrintVisitor().visit(a1_3)

print
print "\ta4_3  = a4_2 compose (inverse T_I1_to_I2)"
a4_3 =  a4_2.compose( T_I1_to_I2.inverse() )
#print a4_3
PrettyPrintVisitor().visit(a4_3)

print
print "\ta8_3  = a8_2 compose (inverse T_I1_to_I2)"
a8_3 =  a8_2.compose( T_I1_to_I2.inverse() )
#print a8_3
PrettyPrintVisitor().visit(a8_3)
print

print
print "Updating a data dependence: "
print "\tD_I1_to_I1 = "
PrettyPrintVisitor().visit(D_I1_to_I1)
print "Updating the data dependence due to the loop alignment transformation."
print "\tD_I2_to_I2 = T_I1_to_I2 compose ( D_I1_to_I1 compose (inverse T_I1_to_I2)"
D_I2_to_I2 = T_I1_to_I2.compose( D_I1_to_I1.compose( T_I1_to_I2.inverse() ) )
print "\t           = "
PrettyPrintVisitor().visit(D_I2_to_I2)

#### SparseTileTrans
print
print "==== SparseTileTrans"
print "Data dependences to and from seed partitioning space."
print "Will be computed in calc_input method"
print "(See iegen/doc/sparse-tile-design.txt for algorithm)."
print
print "Input:"
print "\tDirect data dependences:"
D_1_2 = Relation("{[c0,s,c1,i,c2] -> [c0,s,c3,ii,c2] : i = inter1(ii) && c1=0 && c2=0 && c0=0 && c3=1}")
D_1_2 = D_1_2.union(Relation("{[c0,s,c1,i,c2] -> [c0,s,c3,ii,c2] : i = inter2(ii) && c1=0 && c2=0 && c0=0 && c3=1}"))
D_1_3 = D_1_2
D_2_1 = Relation("{[c0,s,c1,ii,c0] -> [c0,s2,c0,i,c0] : s2 > s && i=inter1(ii) && c0=0 && c1=1}")
D_2_1 = D_2_1.union(Relation("{[c0,s,c1,ii,c0] -> [c0,s2,c0,i,c0] : s2 > s && i = inter2(ii) && c0=0 && c1=1}"))
print "\t\tD_1_2 = D_1_3 = "
PrettyPrintVisitor().visit(D_1_2)
print
print "\t\tD_2_1 = "
PrettyPrintVisitor().visit(D_2_1)
print
print "\tDirect data dependences modified by the previous transformations:"
print
print "\t\tD_1_2 = T_I0_to_I1 compose ( D_1_2 compose (inverse T_I0_to_I1) ) ) = "
D_1_2 = T_I0_to_I1.compose( D_1_2.compose( T_I0_to_I1.inverse() ) )
PrettyPrintVisitor().visit(D_1_2)
print
print "\t\tD_1_2 = T_I1_to_I2 compose ( D_1_2 compose (inverse T_I1_to_I2) ) ) ="
D_1_2 = T_I1_to_I2.compose( D_1_2.compose( T_I1_to_I2.inverse() ) )
PrettyPrintVisitor().visit(D_1_2)
print
print "\t\tD_1_3 = T_I0_to_I1 compose ( D_1_3 compose (inverse T_I0_to_I1) ) ) ="
D_1_3 = T_I0_to_I1.compose( D_1_3.compose( T_I0_to_I1.inverse() ) )
PrettyPrintVisitor().visit(D_1_3)
print
print "\t\tD_1_3 = T_I1_to_I2 compose ( D_1_3 compose (inverse T_I1_to_I2) ) ) ="
D_1_3 = T_I1_to_I2.compose( D_1_3.compose( T_I1_to_I2.inverse() ) )
PrettyPrintVisitor().visit(D_1_3)
print
print "\t\tfull_I = ", full_I
iter_sub_space_relation = Relation("{[c0,s,x,i,y]->[x,i]}")
iter_seed_space_relation = Relation("{[c0,s,c1,i,c2]->[i] : c1=1}")
print
print "\t\titer_sub_space_relation (issr) = "
PrettyPrintVisitor().visit(iter_sub_space_relation)
print
print "\t\titer_seed_space_relation (iseedsr) = "
PrettyPrintVisitor().visit(iter_seed_space_relation)
print
print "Algorithm:"
print "\t\t# Dependences that exist within space being sparse tiled"
D = D_1_3.union(D_1_2)
print "\t\trelevant dependences = D_1_2 union D_1_3 = ",
PrettyPrintVisitor().visit(D)
print
print "\t\tMake it so data dependence relations start and end in sparse tiling subspace"
print "\t\t\tissr compose D ="
PrettyPrintVisitor().visit(iter_sub_space_relation.compose(D))
print
print "\t\tD_ST = inverse (issr compose (inverse (issr compose D)))"
D_ST = iter_sub_space_relation.compose(iter_sub_space_relation.compose(D).inverse()).inverse()
PrettyPrintVisitor().visit(D_ST)
print
print "\t\tNOTE: not doing verification that dependences in D_ST are not loop carried because I don't know how to iterate over the disjuntions or in and out tuples yet."
print
print "\t\t1) Count number of statements, for example count = 3"
print "\t\t2) Compute D_ST_+"
D_ST_0 = D_ST
print "\t\t\tD_ST_0 = D_ST = "
PrettyPrintVisitor().visit(D_ST_0)
print
print "\t\t\tD_ST_0 compose D_ST = "
PrettyPrintVisitor().visit(D_ST_0.compose(D_ST))
D_ST_1 = D_ST_0.compose(D_ST).union(D_ST)
print "\t\t\tD_ST_1 = (D_ST_0 compose D_ST) union D_ST = "
PrettyPrintVisitor().visit(D_ST_1)

print "Output:"
print "\tFROM_SS = "
print "\tTO_SS = "

print 
print "========\nModifying the MapIR due to sparse tiling transformation:"

T_I2_to_I3 = Relation("{[c0,s,c0,i,c0] -> [c0,s,c0,t,c0,i,c0] : c0=0 && t=theta(0,i)}")
T_I2_to_I3 = T_I2_to_I3.union( Relation("{[c0,s,c1,ii,x] -> [c0,s4,c0,t,c1,ii,x] : t = theta(1,ii) && c0=0 && c1=1 }"))
print "\tT_I2_to_I3 = ", T_I2_to_I3
PrettyPrintVisitor().visit(T_I2_to_I3)
print
print "Modifying the scheduling function:"
S1_sched = Relation("{[s,i]->[c0,s,c0,i,c0] : c0=0}")
print "\tS1_sched = "
PrettyPrintVisitor().visit(S1_sched)
print "\tT_I2_to_I3 compose S1_sched = "
S1_sched = T_I2_to_I3.compose(S1_sched)
PrettyPrintVisitor().visit(S1_sched)


print
print "Updating access relations due to T_I2_to_I3: "
print
print "\ta1_4  = a1_3 compose (inverse T_I2_to_I3)"
a1_4 =  a1_3.compose( T_I2_to_I3.inverse() )
PrettyPrintVisitor().visit(a1_4)

print
print "\ta4_4  = a4_3 compose (inverse T_I2_to_I3)"
a4_4 =  a4_3.compose( T_I2_to_I3.inverse() )
PrettyPrintVisitor().visit(a4_4)

print
print "\ta8_4  = a8_3 compose (inverse T_I2_to_I3)"
a8_4 =  a8_3.compose( T_I2_to_I3.inverse() )
PrettyPrintVisitor().visit(a8_4)
print

print
print "Updating the data dependences due to T_I2_to_I3:"
print "\t\tD_1_2 = T_I2_to_I3 compose ( D_1_2 compose (inverse T_I2_to_I3) ) ) ="
D_1_2 = T_I2_to_I3.compose( D_1_2.compose( T_I2_to_I3.inverse() ) )
PrettyPrintVisitor().visit(D_1_2)
print
print "\t\tD_1_3 = T_I2_to_I3 compose ( D_1_3 compose (inverse T_I2_to_I3) ) ) ="
D_1_3 = T_I2_to_I3.compose( D_1_3.compose( T_I2_to_I3.inverse() ) )
PrettyPrintVisitor().visit(D_1_3)



