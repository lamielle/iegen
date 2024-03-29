# Set and Relation operations needed for M2 example.
#
# See RTRTJournalShared/moldyn-FST-example.tex for corresponding writeup.
# Also see iegen/example/moldyn-FST.spec
#
# Need to keep in mind that the M2 example is not doing pointer update.  I want to keep 
# it that way so that we end up with some pretty deep nesting of UFS.


import cProfile
import pstats

import iegen
from iegen import Set
from iegen import Relation
from iegen import Symbolic

import iegen.simplify

#from iegen.ast.visitor import PrettyPrintVisitor


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
print S1_sched
#PrettyPrintVisitor().visit(S1_sched)


S1_full_I = S1_I.apply(S1_sched)
print S1_full_I

# S2
print "==== S2"
S2_I = Set("{[s,i]: 0<=s && s<T && 0<=i && i<n_inter}", syms)
print S2_I

S2_sched = Relation("{[s,i]->[c0,s,c1,j,c2]: c0=0 && c1=1 && c2=0 && i=j}")
print S2_sched
#PrettyPrintVisitor().visit(S2_sched)


S2_full_I = S2_I.apply(S2_sched)
print S2_full_I

# S3
print "==== S3"
S3_I = Set("{[s,i]: 0<=s && s<T && 0<=i && i<n_inter}", syms)
print S3_I

S3_sched = Relation("{[s,i]->[c0,s,c1,j,c2]: c0=1 && c1=1 && c2=1 && i=j}")
print S3_sched
#PrettyPrintVisitor().visit(S3_sched)


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
print a1
#PrettyPrintVisitor().visit(a1)
print "Modified a1, or a1_0"
#print '___START___'
#print 'a1:',a1
#print 'S1_sched:',S1_sched
#print 'S1_sched.inverse():',S1_sched.inverse()
a1_0 = a1.compose(S1_sched.inverse())
#print 'a1.compose(S1_sched.inverse()):',a1_0
#print '___END___'
print a1_0
#PrettyPrintVisitor().visit(a1_0)


# A4, access relation for S2, targets data array x
print "==== A4, access relation for S2"
a4 = Relation("{[s,i]->[k]: k=inter1(i)}")
print a4
#PrettyPrintVisitor().visit(a4)
print "Modified a4, or a4_0"
#print '___START___'
#print 'a4:',a1
#print 'S2_sched:',S1_sched
#print 'S2_sched.inverse():',S1_sched.inverse()
a4_0 = a4.compose(S2_sched.inverse())
#print 'a4.compose(S2_sched.inverse())',a4_0
#print '___END___'
print a4_0
#PrettyPrintVisitor().visit(a4_0)

# A8, access relation for S3, targets data array x
print "==== A8, access relation for S3"
a8 = Relation("{[s,i]->[k]: k=inter2(i)}")
print a8
#PrettyPrintVisitor().visit(a8)
print "Modified a8, or a8_0"
#print '___START___'
#print 'a8:',a1
#print 'S3_sched:',S1_sched
#print 'S3_sched.inverse():',S1_sched.inverse()
a8_0 = a8.compose(S2_sched.inverse())
#print 'a8.compose(S2_sched.inverse()):',a8_0
#print '___END___'
print a8_0
#PrettyPrintVisitor().visit(a8_0)



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

#print a1_0
#print a4_0
#print a8_0
all_ar = a1_0.union( a4_0 )
all_ar = a8_0.union( all_ar )
print "\t\tall_ar = "
print all_ar
#PrettyPrintVisitor().visit(all_ar)
print
#### PERFORMANCE PROBLEM: the following composition causes a noticable pause
print "\toutput:"
print "\t\tars of interest = inverse (iter_sub_space_relation compose (inverse all_ar))"
#print '___START___'
#print 'all_ar:',all_ar
#print 'all_ar.inverse():',all_ar.inverse()
#print 'iter_sub_space_relation:',iter_sub_space_relation
ars_of_interest = iter_sub_space_relation.compose( all_ar.inverse() ).inverse()
#print 'iter_sub_space_relation.compose( all_ar.inverse() ).inverse():',ars_of_interest
#print '___END___'
print "\t\tars of interest = " 
print ars_of_interest
#PrettyPrintVisitor().visit(ars_of_interest)

print
print
print "Update modified access relations based on automatically derived data reordering specification."
iegen.simplify.register_inverse_pair('sigma','sigma_inv')
R_x0_x1 = Relation("{[k] -> [j] : j = sigma(k)}")
print "\tdata reordering specification (R_x0_x1) = ", R_x0_x1
print
print "\ta1_1 = R_x0_x1 compose a1_0 = "
#print '___START___'
#print 'R_x0_x1:',R_x0_x1
#print 'a1_0:',a1_0
a1_1 = R_x0_x1.compose(a1_0)
#print 'R_x0_x1.compose(a1_0):',a1_1
#print '___END___'
print a1_1
#PrettyPrintVisitor().visit(a1_1)
print
print "\ta4_1 = R_x0_x1 compose a4_0 = "
#print '___START___'
#print 'R_x0_x1:',R_x0_x1
#print 'a4_0:',a4_0
a4_1 =  R_x0_x1.compose(a4_0)
#print 'R_x0_x1.compose(a4_0):',a4_1
#print '___END___'
print a4_1
#PrettyPrintVisitor().visit(a4_1)
print
print "\ta8_1 = R_x0_x1 compose a8_0 = "
#print '___START___'
#print 'R_x0_x1:',R_x0_x1
#print 'a8_0:',a8_0
a8_1 =  R_x0_x1.compose(a8_0)
#print 'R_x0_x1.compose(a8_0):',a8_1
#print '___END___'
print a8_1
#PrettyPrintVisitor().visit(a8_1)


#### Loop Alignment
print
print "==== Loop Alignment"
print "The transformation relation: "
T_I0_to_I1 = Relation('{[c0, s, c0, i, c0] -> [c0, s, c0, j, c0] : c0=0 && j=sigma(i)}')
T_I0_to_I1 = T_I0_to_I1.union( Relation('{[c0, s, c1, ii, x] -> [c0, s, c1, ii, x] : c0=0 && c1=1}') )
print "\tT_I0_to_I1 = "
print T_I0_to_I1
#PrettyPrintVisitor().visit(T_I0_to_I1)
print
print "Updating access relations due to T_I0_to_I1: "
print
print "\ta1_2  = a1_1 compose (inverse T_I0_to_I1)"
#print '___START___'
#print 'a1_1:',a1_1
#print 'T_I0_to_I1:',T_I0_to_I1
#print 'T_I0_to_I1.inverse():',T_I0_to_I1.inverse()
a1_2 =  a1_1.compose( T_I0_to_I1.inverse() )
#print 'a1_1.compose(T_I0_to_I1.inverse())',a1_2
#print '___END___'
print 'a1_2 =  a1_1.compose( T_I0_to_I1.inverse() ):'
print a1_1
print T_I0_to_I1
print a1_2
#PrettyPrintVisitor().visit(a1_2)
print
print "\ta4_2  = a4_1 compose (inverse T_I0_to_I1)"
#print '___START___'
#print 'a4_1:',a4_1
#print 'T_I0_to_I1:',T_I0_to_I1
#print 'T_I0_to_I1.inverse():',T_I0_to_I1.inverse()
a4_2 =  a4_1.compose( T_I0_to_I1.inverse() )
#print 'a4_1.compose(T_I0_to_I1.inverse()):',a4_2
#print '___END___'
print 'a4_2 =  a4_1.compose( T_I0_to_I1.inverse() ):'
print a4_1
print T_I0_to_I1
print a4_2
#PrettyPrintVisitor().visit(a4_2)
print
print "\ta8_2  = a8_1 compose (inverse T_I0_to_I1)"
#print '___START___'
#print 'a8_1:',a8_1
#print 'T_I0_to_I1:',T_I0_to_I1
#print 'T_I0_to_I1.inverse():',T_I0_to_I1.inverse()
a8_2 =  a8_1.compose( T_I0_to_I1.inverse() )
#print 'a8_1.compose(T_I0_to_I1.inverse()):',a8_2
#print '___END___'
print a8_2
#PrettyPrintVisitor().visit(a8_2)
print
print "Updating a data dependence: "
D_I0_to_I0 = Relation('{[c0,s,c0,i,c0] -> [c0,s,c1,ii,c0] : c0=0 && c1=1 && i=inter1(ii)}')
print "\tD_I0_to_I0 = "
print D_I0_to_I0
#PrettyPrintVisitor().visit(D_I0_to_I0)
print "Updating the data dependence due to the loop alignment transformation."
print "\tD_I1_to_I1 = T_I0_to_I1 compose ( D_I0_to_I0 compose (inverse T_I0_to_I1)"
#print '___START___'
#print 'T_I0_to_I1:',T_I0_to_I1
#print 'D_I0_to_I0:',D_I0_to_I0
D_I1_to_I1 = T_I0_to_I1.compose( D_I0_to_I0.compose( T_I0_to_I1.inverse() ) )
#print 'T_I0_to_I1.compose( D_I0_to_I0.compose( T_I0_to_I1.inverse() ) ):',D_I1_to_I1
#print '___END___'
print "\t           = "
print D_I1_to_I1
#PrettyPrintVisitor().visit(D_I1_to_I1)


#### IterPermuteTrans
iegen.simplify.register_inverse_pair('delta','delta_inv')
print
print "==== IterPermuteTrans"
T_I1_to_I2 = Relation("{[c0,s,c0,i,c0] -> [c0,s,c0,i,c0] : c0=0 }")
T_I1_to_I2 = T_I1_to_I2.union( Relation("{[c0,s,c1,ii,x] -> [c0,s,c1,j,x] : j = delta(ii) && c0=0  && c1=1 }"))
#related to bug #136
#T_I1_to_I2 = T_I1_to_I2.union( Relation("{[c0,s,c1,ii,x] -> [c7,s,c8,j,x] : j = delta(ii) && c0=0  && c1=1 }"))
print "T_I1_to_I2 = "
print T_I1_to_I2
#PrettyPrintVisitor().visit(T_I1_to_I2)

print
print "Computing ER_2, or access relation that is input to permutation alg"
print "\tAR = union over all access relations to x or fx"
AR = a1_2.union( a4_2.union( a8_2 ) )
print "\t\t= "
print AR
#PrettyPrintVisitor().visit(AR)

issr = Relation('{[c0, s, c1, ii, c2] -> [ ii ] : c1=1}')
print "\tissr = "
print issr
#PrettyPrintVisitor().visit(issr)
print
#print '___START___'
#print 'AR:',AR
#print 'issr:',issr
#print 'issr.inverse():',issr.inverse()
temp = AR.compose(issr.inverse())
#print 'AR.compose(issr.inverse()):',temp
#print '___END___'
print "\tAR compose (inverse issr)= "
print temp
#PrettyPrintVisitor().visit(temp)

print
print "Updating access relations due to T_I1_to_I2: "
print
print "\ta1_3  = a1_2 compose (inverse T_I1_to_I2)"
#print '___START___'
#print 'a1_2:',a1_2
#print 'T_I1_to_I2:',T_I1_to_I2
#print 'T_I1_to_I2.inverse():',T_I1_to_I2.inverse()
a1_3 =  a1_2.compose( T_I1_to_I2.inverse() )
#print 'a1_2.compose( T_I1_to_I2.inverse() ):',a1_3
#print '___END___'
print a1_3
#PrettyPrintVisitor().visit(a1_3)

print
print "\ta4_3  = a4_2 compose (inverse T_I1_to_I2)"
#print '___START___'
#print 'a4_2:',a4_2
#print 'T_I1_to_I2:',T_I1_to_I2
#print 'T_I1_to_I2.inverse():',T_I1_to_I2.inverse()
a4_3 =  a4_2.compose( T_I1_to_I2.inverse() )
#print 'a4_2.compose( T_I1_to_I2.inverse() ):',a4_3
#print '___END___'
print a4_3
#PrettyPrintVisitor().visit(a4_3)

print
print "\ta8_3  = a8_2 compose (inverse T_I1_to_I2)"
#print '___START___'
#print 'a8_2:',a8_2
#print 'T_I1_to_I2:',T_I1_to_I2
#print 'T_I1_to_I2.inverse():',T_I1_to_I2.inverse()
a8_3 =  a8_2.compose( T_I1_to_I2.inverse() )
#print 'a8_2.compose( T_I1_to_I2.inverse() ):',a8_3
#print '___END___'
print a8_3
#PrettyPrintVisitor().visit(a8_3)
print

print
print "Updating a data dependence: "
print "\tD_I1_to_I1 = "
print D_I1_to_I1
#PrettyPrintVisitor().visit(D_I1_to_I1)
print "Updating the data dependence due to the loop alignment transformation."
print "\tD_I2_to_I2 = T_I1_to_I2 compose ( D_I1_to_I1 compose (inverse T_I1_to_I2)"
#print '___START___'
#print 'T_I1_to_I2:',T_I1_to_I2
#print 'D_I1_to_I1:',D_I1_to_I1
D_I2_to_I2 = T_I1_to_I2.compose( D_I1_to_I1.compose( T_I1_to_I2.inverse() ) )
#print 'T_I1_to_I2.compose( D_I1_to_I1.compose( T_I1_to_I2.inverse() ) ):',D_I2_to_I2
#print '___END___'
print "\t           = "
print D_I2_to_I2
#PrettyPrintVisitor().visit(D_I2_to_I2)


##### SparseTileTrans 
#spec.add_transformation(
#    type=iegen.trans.SparseTileTrans,
#    name='fst',    # name used in IDG I think?
#    tilefunc_name='theta',  #? sparse tiling create a grouping function 
#    #tilefunc_in_arity=2,   #DON'T use, get arity from iter_sub_space_relation
#                            # out arity
#    #tilefunc_out_range='{[z] : 0<=z and z< nt}',
#    num_tile_symbol = 'nt',
#
#    # Mapping from full iteration space to sub space being tiled.
#    iter_sub_space_relation='{[x,s,y,i,z]->[y,i]}', # Tiling across inner loops
#
#    # Mapping from full iteration space to seed space.  Seed space should be 
#    # subset of subspace.
#    iter_seed_space_relation='{[x,s,c1,i,z]->[c1,i] : c1=1}', # Second inner loop
#
#    # Dependences in sub space that end in seed space (to_deps) and start 
#    # in seed space (from_deps).
#    # FIXME: Eventually we want to calculate this instead of having the user 
#    # specify it.
#    to_deps=Relation('{[c0,i,x] -> [c1,j,y] : c0=0 and c1=1 and i=sigma(inter1(delta_inv(j)))}').union(Relation('{[c0,i,x] -> [c1,j,y] : c0=0 and c1=1 and i=sigma(inter2(delta_inv(j)))}'))
#    from_deps=null,    # For M2 there is no third inner loop.
#
#    erg_func_name='ERG_fst',
#
#    iter_space_trans=Relation("{[x,s,y,i,z] -> [x,s,c0,t,y,i,z] : c0=0 and t=theta(y,i)}")
#
#    

iter_sub_space_relation=Relation('{[x,s,y,i,z]->[y,i]}')

iter_seed_space_relation=Relation('{[x,s,c1,i,z]->[c1,i] : c1=1}')

to_deps=Relation('{[c0,i,x] -> [c1,j,y] : c0=0 and c1=1 and i=sigma(inter1(delta_inv(j)))}').union(Relation('{[c0,i,x] -> [c1,j,y] : c0=0 and c1=1 and i=sigma(inter2(delta_inv(j)))}'))



## Creating the IDG nodes for SparseTileTrans
# See m2-idg-after-sparse-tile.pdf in paper.
# 1) For input need the dependences to and from the seed space.  Currently the
#    user is providing them so no set and/or relation operations are needed.
#    Will need "construct explicit relation" nodes and then the resulting ER 
#    spec nodes.  Will need inputs to the construct node.  For this example, 
#    will need sigma, inter1, inter2, and delta_inv nodes as input to 
#    construct node.    
# 
# 2) Then need an ERG node for full sparse tiling, which takes the created 
#    input nodes as input.
#
# 3) Then need an ER spec for the tiling function theta, which is generated 
#    by the full sparse tiling function.

tiled_sub_space = iter_sub_space_relation.apply(I2)


## Modifying the MapIR for SparseTileTrans
print "========\nModifying the MapIR due to sparse tiling transformation:"
#
#T_I2_to_I3 = Relation("{[c0,s,c0,i,c0] -> [c0,s,c0,t,c0,i,c0] : c0=0 && t=theta(0,i)}")
#T_I2_to_I3 = T_I2_to_I3.union( Relation("{[c0,s,c1,ii,x] -> [c0,s4,c0,t,c1,ii,x] : t = theta(1,ii) && c0=0 && c1=1 }"))
T_I2_to_I3 = Relation("{[c0,s,x,i,y] -> [c0,s,c0,t,x,i,y] : c0=0 && t=theta(x,i)}")

print "\tT_I2_to_I3 = ", T_I2_to_I3
print T_I2_to_I3

# Alan: When generating the code for the unified iteration spaces
# that result from these schedule changes, you will need to collect
# the non-affine constraints into a guard for the statement.
print
print "Modifying the scheduling function:"
S1_sched = Relation("{[s,i]->[c0,s,c0,i,c0] : c0=0}")
print "\tS1_sched = "
print S1_sched
print "\tT_I2_to_I3 compose S1_sched = "
print 'T_I2_to_I3:',T_I2_to_I3
print 'S1_sched:',S1_sched
S1_sched = T_I2_to_I3.compose(S1_sched)
print 'T_I2_to_I3.compose(S1_sched):',S1_sched
print S1_sched



# The access relations end up with that extra constraint involving the 
# iteration variable from the loops being tiled and theta.  
# When generating code, we will have to have logic that ignores this
# extra constraint.  If we had the equivalent of a gist operation we 
# could get rid of that constraint.
print
print "Updating access relations due to T_I2_to_I3: "
print
print "\ta1_4  = a1_3 compose (inverse T_I2_to_I3)"
#print '___START___'
#print 'a1_3:',a1_3
#print 'T_I2_to_I3:',T_I2_to_I3
#print 'T_I2_to_I3.inverse():',T_I2_to_I3.inverse()
a1_4 =  a1_3.compose( T_I2_to_I3.inverse() )
#print 'a1_3.compose( T_I2_to_I3.inverse() ):',a1_4
#print '___END___'
print a1_4
#PrettyPrintVisitor().visit(a1_4)

print
print "\ta4_4  = a4_3 compose (inverse T_I2_to_I3)"
a4_4 =  a4_3.compose( T_I2_to_I3.inverse() )
print a4_4
#PrettyPrintVisitor().visit(a4_4)

print
print "\ta8_4  = a8_3 compose (inverse T_I2_to_I3)"
a8_4 =  a8_3.compose( T_I2_to_I3.inverse() )
print a8_4
#PrettyPrintVisitor().visit(a8_4)
print

print
print "Updating the data dependences due to T_I2_to_I3:"
print "\tD_I2_to_I2 = "
print D_I2_to_I2
print "\t\tD_I3_to_I3 = T_I2_to_I3 compose ( D_I2_to_I2 compose (inverse T_I2_to_I3) ) ) ="
D_I3_to_I3 = T_I2_to_I3.compose( D_I2_to_I2.compose( T_I2_to_I3.inverse() ) )
print "\tD_I3_to_I3 = "
print D_I3_to_I3

##### SparseLoopOpt
# The goal of the sparse loop optimization is to get rid of any
# guards in the inner loop that involve UFS.
#spec.add_transformation(
#    type=iegen.trans.SparseLoopOpt,
#    name='sparseLoop',     # name used in IDG I think?
#)
#
# The sparse loop optimization doesn't need much specification because
# initially I think we should have it apply to all loops where there
# is a UFS constraint in the schedule.  Later we can specify individual loops
# for the transformation.  Is this going to be enough info or does user
# have to specify relation for each loop?
# The main questions are (1) which statement does the opt apply,
# (2) which constraint to remove from statement's schedule, 
# (3) relation for projecting out innermost loop from schedule, and
# (4) sparse loop relation with schedule output tuple vars as input
# vars and innermost loop var as an output tuple var.
# The access relations will stay the same so it is important to maintain
# tuple variable names (FIXME: this could be a problem).
#
# Assumption: All statements within a loop have been fused into one statement.
#   Only have one inner sparse loop.
#
# The SparseLoopOpt transformation should work as follows:
#   1) Iterate through all statements and find those with a UFS constraint
#      in the schedule.  For now let's focus on those where the UFS constraint
#      involves the innermost iterator variable.  If we find a case where 
#      this is not true, then assert.
#   2) 




###################### And some profiling at the end.
# And some profiling at the end.
cProfile.run('T_I2_to_I3.compose( D_I2_to_I2.compose( T_I2_to_I3.inverse() ) )','prof')
p = pstats.Stats('prof')
p.strip_dirs()
p.sort_stats('cumulative').print_stats(20)
p.sort_stats('time').print_stats(20)
p.print_callers(20)



##### SparseTileTrans OLD
## All of the below is how we were going to attempt to figure out the dependences to
## input to Sparse tiling.  Now we are just going to have the user provide them.
## Eventually we need to automate this.
#print
#print "==== SparseTileTrans"
#print "Data dependences to and from seed partitioning space."
#print "Will be computed in calc_input method"
#print "(See iegen/doc/sparse-tile-design.txt for algorithm)."
#print
#print "Input:"
#print "\tDirect data dependences:"
#D_1_2 = Relation("{[c0,s,c1,i,c2] -> [c0,s,c3,ii,c2] : i = inter1(ii) && c1=0 && c2=0 && c0=0 && c3=1}")
#D_1_2 = D_1_2.union(Relation("{[c0,s,c1,i,c2] -> [c0,s,c3,ii,c2] : i = inter2(ii) && c1=0 && c2=0 && c0=0 && c3=1}"))
#D_1_3 = D_1_2
#D_2_1 = Relation("{[c0,s,c1,ii,c0] -> [c0,s2,c0,i,c0] : s2 > s && i=inter1(ii) && c0=0 && c1=1}")
#D_2_1 = D_2_1.union(Relation("{[c0,s,c1,ii,c0] -> [c0,s2,c0,i,c0] : s2 > s && i = inter2(ii) && c0=0 && c1=1}"))
#print "\t\tD_1_2 = D_1_3 = "
#print D_1_2
##PrettyPrintVisitor().visit(D_1_2)
#print
#print "\t\tD_2_1 = "
#print D_2_1
##PrettyPrintVisitor().visit(D_2_1)
#print
#print "\tDirect data dependences modified by the previous transformations:"
#print
#print "\t\tD_1_2 = T_I0_to_I1 compose ( D_1_2 compose (inverse T_I0_to_I1) ) ) = "
##### some profiling to figure out why compose is so slow
##cProfile.run('T_I0_to_I1.compose( D_1_2.compose( T_I0_to_I1.inverse() ) )','prof')
##p = pstats.Stats('prof')
##p.strip_dirs()
##p.sort_stats('cumulative').print_stats(20)
##p.sort_stats('time').print_stats(20)
##p.print_callers(20)
#####
#
##print '___START___'
##print 'T_I0_to_I1:',T_I0_to_I1
##print 'T_I0_to_I1.inverse():',T_I0_to_I1.inverse()
##print 'D_1_2:',D_1_2
#D_1_2 = T_I0_to_I1.compose( D_1_2.compose( T_I0_to_I1.inverse() ) )
##print 'T_I0_to_I1.compose( D_1_2.compose( T_I0_to_I1.inverse() ) ):',D_1_2
##print '___END___'
#print D_1_2
##PrettyPrintVisitor().visit(D_1_2)
#print
#print "\t\tD_1_2 = T_I1_to_I2 compose ( D_1_2 compose (inverse T_I1_to_I2) ) ) ="
#D_1_2 = T_I1_to_I2.compose( D_1_2.compose( T_I1_to_I2.inverse() ) )
#print D_1_2
##PrettyPrintVisitor().visit(D_1_2)
#print
#print "\t\tD_1_3 = T_I0_to_I1 compose ( D_1_3 compose (inverse T_I0_to_I1) ) ) ="
#D_1_3 = T_I0_to_I1.compose( D_1_3.compose( T_I0_to_I1.inverse() ) )
#print D_1_3
##PrettyPrintVisitor().visit(D_1_3)
#print
#print "\t\tD_1_3 = T_I1_to_I2 compose ( D_1_3 compose (inverse T_I1_to_I2) ) ) ="
#D_1_3 = T_I1_to_I2.compose( D_1_3.compose( T_I1_to_I2.inverse() ) )
#print D_1_3
##PrettyPrintVisitor().visit(D_1_3)
#print
#print "\t\tfull_I = ", full_I
#iter_sub_space_relation = Relation("{[c0,s,x,i,y]->[x,i]}")
#iter_seed_space_relation = Relation("{[c0,s,c1,i,c2]->[i] : c1=1}")
#print
#print "\t\titer_sub_space_relation (issr) = "
#print iter_sub_space_relation
##PrettyPrintVisitor().visit(iter_sub_space_relation)
#print
#print "\t\titer_seed_space_relation (iseedsr) = "
#print iter_seed_space_relation
##PrettyPrintVisitor().visit(iter_seed_space_relation)
#print
#print "Algorithm:"
#print "\t\t# Dependences that exist within space being sparse tiled"
#D = D_1_3.union(D_1_2)
#print "\t\trelevant dependences = D_1_2 union D_1_3 = ",
#print D
##PrettyPrintVisitor().visit(D)
#print
#print "\t\tMake it so data dependence relations start and end in sparse tiling subspace"
#print "\t\t\tissr compose D ="
#print iter_sub_space_relation.compose(D)
##PrettyPrintVisitor().visit(iter_sub_space_relation.compose(D))
#print
#print "\t\tD_ST = inverse (issr compose (inverse (issr compose D)))"
##print '___START___'
##print 'iter_sub_space_relation:',iter_sub_space_relation
##print 'iter_sub_space_relation.inverse():',iter_sub_space_relation.inverse()
##print 'D:',D
#D_ST = iter_sub_space_relation.compose(iter_sub_space_relation.compose(D).inverse()).inverse()
##print 'iter_sub_space_relation.compose(iter_sub_space_relation.compose(D).inverse()).inverse():',D_ST
##print '___END___'
#print D_ST
##PrettyPrintVisitor().visit(D_ST)
#print
#print "\t\tNOTE: not doing verification that dependences in D_ST are not loop carried because I don't know how to iterate over the disjuntions or in and out tuples yet."
#print
#print "\t\t1) Count number of statements, for example count = 3"
#print "\t\t2) Compute D_ST_+"
#D_ST_0 = D_ST
#print "\t\t\tD_ST_0 = D_ST = "
#print D_ST_0
##PrettyPrintVisitor().visit(D_ST_0)
#print
#print "\t\t\tD_ST_0 compose D_ST = "
#print D_ST_0.compose(D_ST)
##PrettyPrintVisitor().visit(D_ST_0.compose(D_ST))
##print '___START___'
##print 'D_ST_0:',D_ST_0
##print 'D_ST:',D_ST
#D_ST_1 = D_ST_0.compose(D_ST).union(D_ST)
##print 'D_ST_0.compose(D_ST).union(D_ST):',D_ST_1
##print '___END___'
#print "\t\t\tD_ST_1 = (D_ST_0 compose D_ST) union D_ST = "
#print D_ST_1
##PrettyPrintVisitor().visit(D_ST_1)
#
#print "Output:"
#print "\tFROM_SS = "
#print "\tTO_SS = "
#
#print 

