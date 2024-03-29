#Include the moldyn computation specification
iegen.include('moldyn_full.spec')

#Define the desired transformations
spec.add_transformation(
    type=iegen.trans.DataPermuteTrans,
    name='cpack',
    reordering_name='sigma',
    data_arrays=['data'],
    iter_sub_space_relation='{[c0,i,c2,ii,x]->[ii] : c0=0 && c2=2}',
    target_data_arrays=['data'],
    erg_func_name='ERG_cpack')
