#Include the example computation specification
iegen.include('example_comp.spec')
#
#CPACK data reordering
spec.add_transformation(
    type=iegen.trans.DataPermuteTrans,
    name='cpack',
    reordering_name='sigma',
    data_arrays=['data'],
    iter_sub_space_relation='{[c0,time,c1,tri,x]->[tri] : c0=0 && c1=1}',
    target_data_arrays=['data'],
    erg_func_name='EFG_cpack')
#
#Locality Grouping iteration permutation
spec.add_transformation(
    type=iegen.trans.IterPermuteTrans,
    name='lexmin',
    reordering_name='delta',
    iter_sub_space_relation='{[x,s,c1,i,y]->[i]: c1=1}',
    target_data_arrays=['data'],
    erg_func_name='ERG_lexmin',
    iter_space_trans=Relation('''{[c0,time,c1,tri,x]->[c0,time,c1,out,x]:
                                   c0=0 && c1=1 && out = delta(tri)}'''))
