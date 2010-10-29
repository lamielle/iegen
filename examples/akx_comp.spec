# ------------------------------------------------------------------------------
#    for(iter=0; iter<k; iter++) {
#      for(row=0; row<nrows; row++) {
#S0:     y[row]=0.0;
#      }
#      for(nzid=0; nzid<nnz; i++) {
#S1:     y[row[nzid]] += x[col[nzid]] * val[nzid];
#      }
#S2:   temp=x; x=y; y=temp;
#    }
# ------------------------------------------------------------------------------

#Number of non-zeros
spec.add_symbolic(name='k',type='int %s',lower_bound=1)
spec.add_symbolic(name='nnz',type='int %s',lower_bound=1)
spec.add_symbolic(name='nrows',type='int %s',lower_bound=1)
spec.add_symbolic(name='ncols',type='int %s',lower_bound=1)

spec.add_data_array(
        name='y',
        type='double * %s',
        elem_size='sizeof(double)',
        bounds='{[k]: 0<=k and k<nrows}')

spec.add_data_array(
        name='x',
        type='double * %s',
        elem_size='sizeof(double)',
        bounds='{[k]: 0<=k and k<ncols}')

spec.add_data_array(
        name='temp',
        type='double * %s',
        elem_size='sizeof(double)',
        bounds='{[k]: 0<=k and k<nrows}')

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

#    for(iter=0; iter<k; iter++) {
#      for(nzid=0; nzid<nnz; i++) {
#S0:     y[row[nzid]] += x[col[nzid]] * val[nzid];
#      }
#S1:   temp=x; x=y; y=temp;
#      for(row=0; row<nrows; row++) {
#S2:     y[row]=0.0;
#      }
#    }

spec.add_statement(
        name='zero_y',
        text='y[%(a4)s]=0.0;',
        iter_space='{[iter,row]: 0<=iter and iter<k and 0<=row and row<nrows}',
        scatter='{[iter,row]->[c0,iter,c0,row,c0]: c0=0}')
spec.add_access_relation(
        statement_name='zero_y',
        name='a4',
        data_array='y',
        iter_to_data='{[iter,row]->[ar]: ar=row}')

spec.add_statement(
        name='mul_sum',
        text='y[%(a1)s] += x[%(a2)s] * val[%(a3)s];',
        iter_space='{[iter,nzid]: 0<=iter and iter<k and 0<=nzid and nzid<nnz}',
        scatter='{[iter,nzid]->[c0,iter,c1,nzid,c0]: c0=0 and c1=1}')
spec.add_access_relation(
        statement_name='mul_sum',
        name='a1',
        data_array='y',
        iter_to_data='{[iter,nzid]->[ar]: ar=row(nzid)}')
spec.add_access_relation(
        statement_name='mul_sum',
        name='a2',
        data_array='x',
        iter_to_data='{[iter,nzid]->[ar]: ar=col(nzid)}')
spec.add_access_relation(
        statement_name='mul_sum',
        name='a3',
        data_array='val',
        iter_to_data='{[iter,nzid]->[ar]: ar=nzid}')

spec.add_statement(
        name='swap_vecs',
        text='temp=x; x=y; y=temp;',
        iter_space='{[iter]: 0<=iter and iter<k}',
        scatter='{[iter]->[c0,iter,c2,c0,c0]: c0=0 and c2=2}')
