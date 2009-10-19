#Include the moldyn computation specification
iegen.include('moldyn_full.spec')

#Define the desired transformations
spec.add_transformation(
    type=iegen.trans.DataPermuteTrans,
    name='cpack',
    reordering_name='sigma',
    data_arrays=['data'],
    iter_sub_space_relation='{[c0,s,c2,ii,x]->[ii] : c0=0 && c2=2}',
    target_data_arrays=['data'],
    erg_func_name='ERG_cpack')

T1 = Relation('{[c0,s,c2,ii,c0]->[c0,s,c0,j,c0]: c0=0 && c2=2 && j=sigma(ii)}')
T2 = Relation('{[c0, s, y, i, x] -> [c0, s, y, i, x] : c0=0 && y<2}')
T3 = Relation('{[c0,s,y,i,x] -> [c0,s,y,i,x] : c0=0 && y>2}')

spec.add_transformation(
    type=iegen.trans.IterAlignTrans,
    name='align',
    iter_space_trans=T1.union(T2.union(T3)) )
