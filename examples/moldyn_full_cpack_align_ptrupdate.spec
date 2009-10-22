#Include the moldyn computation specification
iegen.include('moldyn_full.spec')

#Define the desired transformations

#CPACK data reordering
#The below performs a reordering of the interleaved data array
#based on the accesses in the ii loop.
spec.add_transformation(
    type=iegen.trans.DataPermuteTrans,
    name='cpack',
    reordering_name='sigma',
    data_arrays=['data'],
    iter_sub_space_relation='{[c0,s,c2,ii,x]->[ii] : c0=0 && c2=2}',
    target_data_arrays=['data'],
    erg_func_name='ERG_cpack')

#Loop alignment
#After the data reordering performed on the data array, it is
#necessary to align the 1st and third loops in the time loop
#because they used to be accessing the data array sequentially 
#and are not accessing it through sigma.
#This is broken out into a transformation per statement.
#T0 is for the first loop.  T1 is for the statement that is not a loop.
#T2 is the loop that does NOT need realigned.
#T3 is the third loop.
T0 = Relation('{[c0,s,c0,i,c0]->[c0,s,c0,j,c0]: c0=0 && c2=2 && j=sigma(i)}')
T1 = Relation('{[c0,s,c1,c0,c0]->[c0,s,c1,c0,c0]: c0=0 && c1=1}')
T2 = Relation('{[c0, s, c2, ii, x] -> [c0, s, c2, ii, x] : c0=0 && c2=2}')
T3 = Relation('{[c0,s,c3,i,x] -> [c0,s,c3,j,x] : c0=0 && c3=3 && j=sigma(i)}')

spec.add_transformation(
    type=iegen.trans.IterAlignTrans,
    name='align',
    iter_space_trans=T0.union(T1.union(T2.union(T3))) )

#Pointer update
#After the data reordering above, there will be uninterpreted function call
#nests of sigma(inter1()) and sigma(inter2()).  Apply pointer update to
#removed those.
spec.add_intertransopt(
    type=iegen.ito.PointerUpdate,
    name='ptrupdate')
#    nests=[['sigma','inter1'],['sigma','inter2']])

