# ------------------------------------------------------------------------------
#for (i=0; i<nnz; i++) {
#       y[row[i]] += x[col[i]] * val[i];
#}
# ------------------------------------------------------------------------------

#Number of non-zeros
spec.add_symbolic(name='nnz',type='int %s',lower_bound=1)
spec.add_symbolic(name='ncols',type='int %s',lower_bound=1)
spec.add_symbolic(name='nrows',type='int %s',lower_bound=1)

spec.add_data_array(
        name='y',
        type='double * %s',
        elem_size='sizeof(double)',
        bounds='{[k]: 0<=k && k<nrows}')

spec.add_data_array(
        name='x',
        type='double * %s',
        elem_size='sizeof(double)',
        bounds='{[k]: 0<=k && k<ncols}')

spec.add_data_array(
        name='val',
        type='double * %s',
        elem_size='sizeof(double)',
        bounds='{[k]: 0<=k && k<nnz}')

spec.add_index_array(
        name='row',
        type='int * %s',
        input_bounds='{[k]: 0<=k && k<nnz}',
        output_bounds='{[k]: 0<=k && k<nrows}')

spec.add_index_array(
        name='col',
        type='int * %s',
        input_bounds='{[k]: 0<=k && k<nnz}',
        output_bounds='{[k]: 0<=k && k<ncols}')

spec.add_statement(
        name='mul_sum',
        text='y[%(a1)s] += x[%(a2)s] * val[%(a3)s];',
        iter_space='{ [ i ] : 0 <= i && i < nnz}',
        scatter='{ [ i ]->[ c0, i, c0] : c0=0}')
spec.add_access_relation(
        statement_name='mul_sum',
        name='a1',
        data_array='y',
        iter_to_data='{ [i]->[ar] : ar = row(i) }')
spec.add_access_relation(
        statement_name='mul_sum',
        name='a2',
        data_array='x',
        iter_to_data='{ [i]->[ar] : ar = col(i) }')
spec.add_access_relation(
        statement_name='mul_sum',
        name='a3',
        data_array='val',
        iter_to_data='{ [i]->[ar] : ar = i }')
