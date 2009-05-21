#Loop nest we are targeting:
#  for (s=0; s<T; s++) {
#  for (i=0; i<N; i++) {
#S1:     x[i] = fx[i] * 1.25;
#  }
#
#    for (i=0; i<n_inter; i++) {
#        // simplified computations
#S2:     fx[inter1[i]] += x[inter1[i]] - x[inter2[i]];
#S3:     fx[inter2[i]] += x[inter1[i]] - x[inter2[i]];
#    }
#  }

#Define the symbolic constants for the computation
spec.add_symbolic(name='T') #Number of time steps
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
    text='x[%(a1)s] = fx[%(a2)s] * 1.25;',
    iter_space='{[s,i]: 0<=s && s<T && 0<=i && i<N}',
    scatter='{[s,i]->[c0,s,c1,i,c2]: c0=0 && c1=0 && c2=0}')

spec.add_statement(
    name='S2',
    text='fx[%(a3)s] += x[%(a4)s] - x[%(a5)s];',
    iter_space='{[s,i]: 0<=s && s<T && 0<=i && i<n_inter}',
    scatter='{[s,i]->[c0,s,c1,i,c2]: c0=0 && c1=1 && c2=0}')

spec.add_statement(
    name='S3',
    text='fx[%(a6)s] += x[%(a7)s] - x[%(a8)s];',
    iter_space='{[s,i]: 0<=s && s<T && 0<=i && i<n_inter}',
    scatter='{[s,i]->[c0,s,c1,i,c2]: c0=0 && c1=1 && c2=1}')

#Define the access relations for the statements
spec.add_access_relation(
    statement_name='S1',
    name='a1',
    data_array='x',
    iter_to_data='{[s,i]->[i]}')

spec.add_access_relation(
    statement_name='S1',
    name='a2',
    data_array='fx',
    iter_to_data='{[s,i]->[i]}')

spec.add_access_relation(
    statement_name='S2',
    name='a3',
    data_array='fx',
    iter_to_data='{[s,i]->[k]: k=inter1(i)}')

spec.add_access_relation(
    statement_name='S2',
    name='a4',
    data_array='x',
    iter_to_data='{[s,i]->[k]: k=inter1(i)}')

spec.add_access_relation(
    statement_name='S2',
    name='a5',
    data_array='x',
    iter_to_data='{[s,i]->[k]: k=inter2(i)}')

spec.add_access_relation(
    statement_name='S3',
    name='a6',
    data_array='fx',
    iter_to_data='{[s,i]->[k]: k=inter2(i)}')

spec.add_access_relation(
    statement_name='S3',
    name='a7',
    data_array='x',
    iter_to_data='{[s,i]->[k]: k=inter1(i)}')

spec.add_access_relation(
    statement_name='S3',
    name='a8',
    data_array='x',
    iter_to_data='{[s,i]->[k]: k=inter2(i)}')

#Define the desired transformations
spec.add_transformation(
    type=iegen.trans.DataPermuteTrans,
    name='cpack',
    reordering_name='sigma',
    data_arrays=['x','fx'],
    iter_sub_space_relation='{[c0,s,c1,i,c2]->[i]: c1=1}',
    target_data_arrays=['x','fx'],
    erg_func_name='ERG_cpack')

spec.add_transformation(
    type=iegen.trans.IterAlignTrans,
    name='align',
    iter_space_trans=Relation('{[c0,s,c0,i,c0]->[c0,s,c0,j,c0]: c0=0 && j=sigma(i)}').union(Relation('{[c0, s, c1, ii, x] -> [c0, s, c1, ii, x] : c0=0 && c1=1}')))
