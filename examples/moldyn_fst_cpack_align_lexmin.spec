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

spec.add_transformation(
    type=iegen.trans.IterPermuteTrans,
    name='lexmin',
    reordering_name='delta',
    iter_sub_space_relation='{[c0,s,c1,i,c2]->[i]: c1=1}',
    target_data_arrays=['x','fx'],
    erg_func_name='ERG_lexmin',
    iter_space_trans=Relation("{[c0,s1,c1,i,c2] -> [c3,s2,c4,j,c5] : s1=s2 && c0=0 && c1=0 && c2=0 && c3=0 && c4=0 && c5=0 && i=j}").union(Relation("{[c6,s3,c7,ii,x] -> [c8,s4,c9,j,y] : s3=s4 && j = delta(ii) && c6=0 && c8=0 && c7=1 && c9=1 && x=y }")))

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
#    iteration reordering // permuting the ii loop
#        IterPermuteRTRT
#            iter_reordering = { [ s,x,i,y ] -> [ s,x,k,y ] : k = delta( i )  && x=2 }
#            access_relation = A_I_0_to_X_1
#            erg_func_name = LexMin
#            erg_type = ERG_Permute
#
#    iteration reordering: FST
#	seedpart = ERG_Group	// not an RTRT so no reordering occurs
#		iter_sub_space_relation = { [ s,x,i,y ] -> [ i ] : x=2 }
#		erg_name = "Block"
#		num_groups = num_blocks
#		ia_name = "part"
#
#        SparseTileRTRT
#            iter_reordering = { [ s,x,i,y ] -> [ s,v,t,x,i,y ] : v=1 && x=1 && y=1 && t=theta(x,i) }
#                union { [ s,x,ii,y ] -> [ s,v,t,x,ii,y ] : v=1 && x=2 && 1<=y && y<=2 && t=theta(x,ii) }
#                // split because of different y's
#
#            // seed partition the ii loop
#            iter_space_to_seed_space = { [ s,x,i,y ] -> [ i ] : x=2 }
#
#            // only inspect the dependences within one s iteration
#            // essentially this relation computes the arity of the tiling
#            // function itself
#            iter_sub_space_relation = { [ s,x,i,y ] -> [ x,i ] }
#
#            seed_part_gen = seedpart
#            erg_func_name = FST
#
#    iteration reordering: tilepack

#Data Dependences
#(eventually should be automatically calculated, but for now computing by hand)
#(only direct dependences for now and those not carried by s loop)
#D1    s1:x[i] to s2:x[inter1[ii]]:
#        { [s,z,i,j] -> [s,y,ii,k] : z=1 && j=1 && y=2 && k=1
#                                    && i=inter1(ii) }
#D2    s1:x[i] to s3:x[inter1[ii]]:
#        { [s,z,i,j] -> [s,y,ii,k] : z=1 && j=1 && y=2 && k=2
#                                    && i=inter1(ii) }
#D3    s1:x[i] to s2:x[inter2[ii]]:
#        { [s,z,i,j] -> [s,y,ii,k] : z=1 && j=1 && y=2 && k=1
#                                    && i=inter2(ii) }
#
#D4    s1:x[i] to s3:x[inter2[ii]]:
#        { [s,z,i,j] -> [s,y,ii,k] : z=1 && j=1 && y=2 && k=2
#                                    && i=inter2(ii) }

#    Reduction dependences in ii loop.  It is important to indicate that there are reduction dependences however, because that means each iteration needs to be executed atomically if the loop is being parallelized.
#    FIXME: how will we indicate reduction dependences?
#XXX: What is the best way that this should be specified using the MapIR specification?