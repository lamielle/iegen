#Original Code:
#    for (i=0; i<n_inter; i++) {
#        // simplified computations
#        fx[inter1[i]] += x[inter1[i]] - x[inter2[i]];
#        fx[inter2[i]] += x[inter1[i]] - x[inter2[i]];
#    }

#Define the symbolic constants for the computation
spec.add_symbolic(name='N') #Number of atoms
spec.add_symbolic(name='n_inter') #Number of interactions between atoms

#Define the data arrays for the computation
spec.add_data_array(
    name='x',
    bounds='{[k]: 0<=k && k<N}')

spec.add_data_array(
    name='fx',
    bounds='{[k]: 0<=k && k<N}')

#Define the index arrays for the computation
spec.add_index_array(
    name='inter1',
    input_bounds='{[k]: 0<=k && k<n_inter}',
    output_bounds='{[k]: 0<=k && k<N}')

spec.add_index_array(
    name='inter2',
    input_bounds='{[k]: 0<=k && k<n_inter}',
    output_bounds='{[k]: 0<=k && k<N}')

#Define the statements for the computation
spec.add_statement(
    name='S1',
    text='fx[%(a1)s] += x[%(a2)s] - x[%(a3)s];',
    iter_space='{[i]: 0<=i && i<n_inter}',
    scatter='{[i]->[c0,i,c1]: c0=1 && c1=1}')

spec.add_statement(
    name='S2',
    text='fx[%(a4)s] += x[%(a5)s] - x[%(a6)s];',
    iter_space='{[i]: 0<=i && i<n_inter}',
    scatter='{[i]->[c0,i,c1]: c0=1 && c1=2}')

#Define the access relations for the statements
spec.add_access_relation(
    statement_name='S1',
    name='a1',
    data_array='fx',
    iter_to_data='{[i]->[k]: k=inter1(i)}')

spec.add_access_relation(
    statement_name='S1',
    name='a2',
    data_array='x',
    iter_to_data='{[i]->[k]: k=inter1(i)}')

spec.add_access_relation(
    statement_name='S1',
    name='a3',
    data_array='x',
    iter_to_data='{[i]->[k]: k=inter2(i)}')

spec.add_access_relation(
    statement_name='S2',
    name='a4',
    data_array='fx',
    iter_to_data='{[i]->[k]: k=inter2(i)}')

spec.add_access_relation(
    statement_name='S2',
    name='a5',
    data_array='x',
    iter_to_data='{[i]->[k]: k=inter1(i)}')

spec.add_access_relation(
    statement_name='S2',
    name='a6',
    data_array='x',
    iter_to_data='{[i]->[k]: k=inter2(i)}')

#Define the desired transformations
spec.add_transformation(
    type=iegen.trans.DataPermuteTrans,
    name='cpack1',
    reordering_name='sigma1',
    data_arrays=['x','fx'],
    iter_sub_space_relation='{[c0,i,c1]->[i]}',
    target_data_array='x',
    erg_func_name='ERG_cpack')

#spec.add_transformation(
#    type=iegen.trans.DataPermuteTrans,
#    name='cpack2',
#    reordering_name='sigma2',
#    data_arrays=['x','fx'],
#    iter_sub_space_relation='{[c0,i,c1]->[i]}',
#    target_data_array='x',
#    erg_func_name='ERG_cpack')

iter_reordering=None
#iter_reordering=IterPermuteTrans(
#                iter_reordering='{ [ i,x ] -> [ k,x ] : k = delta( i ) }',
##User doesn't specify?
##This is calculated in step 0
##               iteration_space=I_0,
##User doesn's specify?
##This is calculated in step 1a
##               access_relation=A_I_0_to_X_1,
#                iter_sub_space_relation='{ [ i, j ] -> [ i ] }',
#                erg_func_name='ERG_lexmin',
#                erg_type='ERG_Permute')

#Data Dependences
#    Only reduction dependences.  It is important to indicate that there are reduction dependences however, because that means each iteration needs to be executed atomically if the loop is being parallelized.

#XXX: What is the best way that this should be specified using the MapIR specification?
