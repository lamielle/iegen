# ------------------------------------------------------------------------------
#    for(iter=0; iter<k; iter++) {
#      for(nzid=0; nzid<nnz; i++) {
#S0:     x[iter][row[nzid]] += x[iter-1][col[nzid]] * val[nzid];
#      }
#    }
# ------------------------------------------------------------------------------

#Number of non-zeros
spec.add_symbolic(name='k',type='int %s',lower_bound=1)
spec.add_symbolic(name='nnz',type='int %s',lower_bound=1)
spec.add_symbolic(name='nrows',type='int %s',lower_bound=1)
spec.add_symbolic(name='ncols',type='int %s',lower_bound=1)

spec.add_data_array(
        name='x',
        type='double ** %s',
        elem_size='sizeof(double)',
        bounds='{[iter,c]: 0<=iter and iter<k and 0<=c and c<ncols}')

spec.add_data_array(
        name='val',
        type='double * %s',
        elem_size='sizeof(double)',
        bounds='{[k]: 0<=k and k<nnz}')

spec.add_index_array(
        name='row',
        type='int * %s',
        input_bounds='{[k]: 0<=k and k<nnz}',
        output_bounds='{[k]: 0<=k and k<nrows}')

spec.add_index_array(
        name='col',
        type='int * %s',
        input_bounds='{[k]: 0<=k and k<nnz}',
        output_bounds='{[k]: 0<=k and k<ncols}')

spec.add_statement(
        name='mul_sum',
        text='x[%(a1)s] += x[%(a2)s] * val[%(a3)s];',
        iter_space='{[iter,nzid]: 0<=iter and iter<k and 0<=nzid and nzid<nnz}',
        scatter='{[iter,nzid]->[c0,iter,c0,nzid,c0]: c0=0}')
spec.add_access_relation(
        statement_name='mul_sum',
        name='a1',
        data_array='x',
        iter_to_data='{[iter,nzid]->[ar1,ar2]: ar1=iter and ar2=row(nzid)}')
spec.add_access_relation(
        statement_name='mul_sum',
        name='a2',
        data_array='x',
        iter_to_data='{[iter,nzid]->[ar1,ar2]: ar1=iter-1 and ar2=col(nzid)}')
spec.add_access_relation(
        statement_name='mul_sum',
        name='a3',
        data_array='val',
        iter_to_data='{[iter,nzid]->[ar]: ar=nzid}')
