#Original Code:
#for(int i=0; i<N; i++) {
#   res[i]+=data[n1[i]];
#   res[i]+=data[n2[i]];
#   res[i]+=data[n3[i]];
#   res[i]+=data[n4[i]];
#}

#Define the symbolic constants for the computation
spec.add_symbolic(
    name='N',
    type='int %s',
    lower_bound=1) #Number of tetrahedrons

#Define the data arrays for the computation
spec.add_data_array(
    name='data',
    type='double *%s',
    elem_size='sizeof(double)',
    bounds='{[k]: 0<=k && k<=N-1}')

spec.add_data_array(
    name='res',
    type='double *%s',
    elem_size='sizeof(double)',
    bounds='{[k]: 0<=k && k<=N-1}')

#Define the index arrays for the computation
spec.add_index_array(
    name='n1',
    type='int *%s',
    input_bounds='{[k]: 0<=k && k<=N-1}',
    output_bounds='{[k]: 0<=k && k<=N-1}')

spec.add_index_array(
    name='n2',
    type='int *%s',
    input_bounds='{[k]: 0<=k && k<=N-1}',
    output_bounds='{[k]: 0<=k && k<=N-1}')

spec.add_index_array(
    name='n3',
    type='int *%s',
    input_bounds='{[k]: 0<=k && k<=N-1}',
    output_bounds='{[k]: 0<=k && k<=N-1}')

spec.add_index_array(
    name='n4',
    type='int *%s',
    input_bounds='{[k]: 0<=k && k<=N-1}',
    output_bounds='{[k]: 0<=k && k<=N-1}')

#Define the statements for the computation
spec.add_statement(
    name='S1',
    text='res[%(a1)s]+=data[%(a2)s];',
    iter_space='{[i]: 0<=i && i<=N-1}',
    scatter='{[i]->[c0,i,c1]: c0=0 and c1=0}')

spec.add_statement(
    name='S2',
    text='res[%(a3)s]+=data[%(a4)s];',
    iter_space='{[i]: 0<=i && i<=N-1}',
    scatter='{[i]->[c0,i,c1]: c0=0 and c1=1}')

spec.add_statement(
    name='S3',
    text='res[%(a5)s]+=data[%(a6)s];',
    iter_space='{[i]: 0<=i && i<=N-1}',
    scatter='{[i]->[c0,i,c1]: c0=0 and c1=2}')

spec.add_statement(
    name='S4',
    text='res[%(a7)s]+=data[%(a8)s];',
    iter_space='{[i]: 0<=i && i<=N-1}',
    scatter='{[i]->[c0,i,c1]: c0=0 and c1=3}')

#Define the access relations for the statements
spec.add_access_relation(
    statement_name='S1',
    name='a1',
    data_array='res',
    iter_to_data='{[i]->[k]: k=i}')

spec.add_access_relation(
    statement_name='S1',
    name='a2',
    data_array='data',
    iter_to_data='{[i]->[k]: k=n1(i)}')

spec.add_access_relation(
    statement_name='S2',
    name='a3',
    data_array='res',
    iter_to_data='{[i]->[k]: k=i}')

spec.add_access_relation(
    statement_name='S2',
    name='a4',
    data_array='data',
    iter_to_data='{[i]->[k]: k=n2(i)}')

spec.add_access_relation(
    statement_name='S3',
    name='a5',
    data_array='res',
    iter_to_data='{[i]->[k]: k=i}')

spec.add_access_relation(
    statement_name='S3',
    name='a6',
    data_array='data',
    iter_to_data='{[i]->[k]: k=n3(i)}')

spec.add_access_relation(
    statement_name='S4',
    name='a7',
    data_array='res',
    iter_to_data='{[i]->[k]: k=i}')

spec.add_access_relation(
    statement_name='S4',
    name='a8',
    data_array='data',
    iter_to_data='{[i]->[k]: k=n4(i)}')
