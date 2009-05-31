#Include the moldyn_fst computation specification
iegen.include('moldyn_simple_comp.spec')

#Define the desired transformations
spec.add_transformation(
    type=iegen.trans.DataPermuteTrans,
    name='cpack',
    reordering_name='sigma',
    data_arrays=['x','fx'],
    iter_sub_space_relation='{[c0,i,c1]->[i]}',
    target_data_arrays=['x','fx'],
    erg_func_name='ERG_cpack')
