#Define the symbolic constants for the computation
spec.add_symbolic(
    name='T',
    type='int %s',
    lower_bound=1) #Number of time steps
spec.add_symbolic(
    name='R',
    type='int %s',
    lower_bound=1) #Number of triangles
spec.add_symbolic(
    name='N',
    type='int %s',
    lower_bound=1) #Number of data values
#
#Define the data arrays for the computation
spec.add_data_array(
    name='data',
    type='double *%s',
    elem_size='sizeof(double)',
    bounds='{[k]: 0<=k and k<N}')
#
#Define the index arrays for the computation
spec.add_index_array(
    name='n1',
    type='int *%s',
    input_bounds='{[k]: 0<=k and k<R}',
    output_bounds='{[k]: 0<=k and k<N}')
#
#Define the statements for the computation
spec.add_statement(
    name='S1',
    text='...data[%(a1)s]...;',
    iter_space='''{[time,tri]:
                     0<=time and time<T and 0<=tri and tri<R}''',
    scatter='{[time,tri]->[c0,time,c1,tri,c0]: c0=0 and c1=1}')
#
#Define the access relations for the statements
spec.add_access_relation(
    statement_name='S1',
    name='a1',
    data_array='data',
    iter_to_data='{[time,tri]->[k]: k=n1(tri)}')
