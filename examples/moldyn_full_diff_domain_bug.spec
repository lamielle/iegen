spec.add_symbolic(name='n_moles')

spec.add_symbolic(name='n_tstep')

spec.add_symbolic(name='n_inter')

spec.add_data_array(
        name='x',
        bounds='{[k]: 0<=k && k<n_moles}',
        formal_decl='double data[][9]')

spec.add_data_array(
        name='fx',
        bounds='{[k]: 0<=k && k<n_moles}')

spec.add_data_array(
        name='vhx',
        bounds='{[k]: 0<=k && k<n_moles}')

######
#Line 276: x(i) += vhx(i) + fx(i); // ^jroelofs
######
spec.add_statement(
        name='s__0_tstep_0_i_0',
        text='x( %(a1)s ) += vhx( %(a2)s ) + fx( %(a3)s )',
        iter_space='{ [ tstep, i ] : 0 <= tstep && tstep < n_tstep && 0 <= i && i < n_moles }',
        scatter='{ [ tstep, i ]->[ c0, tstep, c1, i, c2 ] : c0=0 && c1=0 && c2=0 }')
spec.add_access_relation(
        statement_name='s__0_tstep_0_i_0',
        name='a1',
        data_array='x',
        iter_to_data='{ [ tstep, i ]->[ accessRelation1 ] : accessRelation1 = i }')
spec.add_access_relation(
        statement_name='s__0_tstep_0_i_0',
        name='a2',
        data_array='vhx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation2 ] : accessRelation2 = i }')
spec.add_access_relation(
        statement_name='s__0_tstep_0_i_0',
        name='a3',
        data_array='fx',
        iter_to_data='{ [ tstep, i ]->[ accessRelation3 ] : accessRelation3 = i }')



######
#Line 299: cutoffSquare = cutoffRadius*cutoffRadius ;
######  
spec.add_statement(        name='s__0_tstep_1',
        text='cutoffSquare = cutoffRadius * cutoffRadius',        
		iter_space='{ [tstep] : 0 <= tstep && tstep < n_tstep }',
		scatter='{ [ tstep ]->[ c0, tstep, c1, t0, c2 ] : c0=0 && c1=1 && t0=0 && c2=0 }')

