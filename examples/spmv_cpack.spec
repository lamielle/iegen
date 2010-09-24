#Include the spmv computation specification
iegen.include('spmv_comp.spec')

#Define the desired transformations
spec.add_transformation(
    type=iegen.trans.DataPermuteTrans,
    name='cpack',
    reordering_name='sigma',
    data_arrays=['x'],
    iter_sub_space_relation='{[c0,i,c0]-> [i]:c0=0}',
    target_data_arrays=['x'],
    erg_func_name='ERG_cpack')
