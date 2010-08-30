#Include the spmv computation specification
iegen.include('spmv_comp.spec')

#Define the desired transformations
spec.add_transformation(
   type=iegen.trans.IterPermuteTrans,
   name='cache_blocking',
   reordering_name='sigma',
   iter_sub_space_relation='{[c0,i,c1]->[i]}',
   target_data_arrays=['y','x'],
   erg_func_name='ERG_cacheblock',
   iter_space_trans=Relation('{[c0,i,c1]->[c0,j,c1] : j=sigma(i)}'))

spec.add_intertransopt(
    type=iegen.ito.PointerUpdate,
    name='ptrupdate',
    nests=[['row','sigma_inv'],['col','sigma_inv']])

#data permute on val using sigma

##CPACK data reordering
##The below performs a reordering of the interleaved data array
##based on the accesses in the ii loop.
#spec.add_transformation(
#    type=iegen.trans.DataPermuteTrans,
#    name='cpack',
#    reordering_name='sigma',
#    data_arrays=['data'],
#    iter_sub_space_relation='{[c0,s,c2,ii,x]->[ii] : c0=0 && c2=2}',
#    target_data_arrays=['data'],
#    erg_func_name='ERG_cpack')
#
##Loop alignment
##After the data reordering performed on the data array, it is
##necessary to align the 1st and third loops in the time loop
##because they used to be accessing the data array sequentially
##and are not accessing it through sigma.
##This is broken out into a transformation per statement.
##T1 is for the first loop.  T0 is for the statement that is not a loop.
##T2 is the loop that does NOT need realigned.
##T3 is the third loop.
#T0 = Relation('{[c0,s,c0,c0,c0]->[c0,s,c1,c0,c0]: c0=0 }')
#T1 = Relation('{[c0,s,c1,i,c0]->[c0,s,c1,j,c0]: c0=0 && c1=1 && j=sigma(i)}')
#T2 = Relation('{[c0, s, c2, ii, x] -> [c0, s, c2, ii, x] : c0=0 && c2=2}')
#T3 = Relation('{[c0,s,c3,i,x] -> [c0,s,c3,j,x] : c0=0 && c3=3 && j=sigma(i)}')
#
#spec.add_transformation(
#    type=iegen.trans.IterAlignTrans,
#    name='align',
#    iter_space_trans=T0.union(T1.union(T2.union(T3))) )
#
##Pointer update
##After the data reordering above, there will be uninterpreted function call
##nests of sigma(inter1()) and sigma(inter2()).  Apply pointer update to
##removed those.
#spec.add_intertransopt(
#    type=iegen.ito.PointerUpdate,
#    name='ptrupdate1',
#    nests=[['sigma','inter1'],['sigma','inter2']])
#
##Locality Grouping iteration permutation
##The below performs a reordering of the middle loop of the three
##nested loops based on the memory accesses in that middle loop.
##terminology: lexmin is an implementation of locality grouping.
#T0 = Relation('{[c0,s,c0,c0,c0]->[c0,s,c1,c0,c0]: c0=0 }')
#T1 = Relation('{[c0,s,c1,i,c0]->[c0,s,c1,i,c0]: c0=0 && c1=1 }')
#T2 = Relation('{[c0, s, c2, j, x] -> [c0, s, c2, e, x] : c0=0 && c2=2 && e = delta(j)}')
#T3 = Relation('{[c0,s,c3,i,x] -> [c0,s,c3,i,x] : c0=0 && c3=3 }')
#
#spec.add_transformation(
#    type=iegen.trans.IterPermuteTrans,
#    name='lexmin',
#    reordering_name='delta',
#    iter_sub_space_relation='{[x,s,c2,i,y]->[i]: c2=2}',
#    target_data_arrays=['data'],
#    erg_func_name='ERG_lexmin',
#    iter_space_trans=T0.union(T1.union(T2.union(T3))) )
#
##Pointer update
##After the data reordering above, there will be uninterpreted function call
##nests of sigma(inter1()) and sigma(inter2()).  Apply pointer update to
##removed those.
#spec.add_intertransopt(
#    type=iegen.ito.PointerUpdate,
#    name='ptrupdate2',
#    nests=[['sigma_inter1','delta_inv'],['sigma_inter2','delta_inv']])
