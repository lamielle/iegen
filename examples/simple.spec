#Computation
#for(int i=0; i<N; i++)
#{
#  data[i]=data[index[i]];
#}

spec.add_symbolic(name='N')

spec.add_data_array(
     name='data',
     bounds='{[i]: 0<=i and i<=N}')

spec.add_index_array(
     name='index',
     input_bounds='{[i]: 0<=i and i<=N}',
     output_bounds='{[i]: 0<=i and i<=N}')

spec.add_statement(
    name='S1',
    text='data[%(a1)s]=data[%(a2)s];',
    iter_space='{[i]: 0<=i and i<=N}',
    scatter='{[i]->[c0,i,c1]: c0=0 && c1=0}')

spec.add_access_relation(
    statement_name='S1',
    name='a1',
    data_array='data',
    iter_to_data='{[i]->[ip]: ip=i}')

spec.add_access_relation(
    statement_name='S1',
    name='a2',
    data_array='data',
    iter_to_data='{[i]->[ip]: ip=index(i)}')
