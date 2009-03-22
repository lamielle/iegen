#!/usr/bin/env python

import iegen,iegen.trans

#from iegen import MapIR,IndexArray,Statement,AccessRelation,Set,Relation
#from iegen.trans import DataPermuteTrans,IterPermuteTrans

#Original Code:
#for(int i=0; i<N; i++) {
#   res[i]+=data[n1[i]]
#   res[i]+=data[n2[i]]
#   res[i]+=data[n3[i]]
#   res[i]+=data[n4[i]]
#}

#Create a new empty MapIR specification for simple tetra
tetra_spec=iegen.MapIR()

#Define the symbolic constants for the computation
tetra_spec.add_symbolic(name='N') #Number of tetrahedrons

#Define the data arrays for the computation
tetra_spec.add_data_array(
    name='data',
    bounds='{[k]: 0<=k && k<=N-1}')

tetra_spec.add_data_array(
    name='res',
    bounds='{[k]: 0<=k && k<=N-1}')

#Define the index arrays for the computation
tetra_spec.add_index_array(
    name='n1',
    input_bounds='{[k]: 0<=k && k<=N-1}',
    output_bounds='{[k]: 0<=k && k<=N-1}')

tetra_spec.add_index_array(
    name='n2',
    input_bounds='{[k]: 0<=k && k<=N-1}',
    output_bounds='{[k]: 0<=k && k<=N-1}')

tetra_spec.add_index_array(
    name='n3',
    input_bounds='{[k]: 0<=k && k<=N-1}',
    output_bounds='{[k]: 0<=k && k<=N-1}')

tetra_spec.add_index_array(
    name='n4',
    input_bounds='{[k]: 0<=k && k<=N-1}',
    output_bounds='{[k]: 0<=k && k<=N-1}')

#Define the statements for the computation
tetra_spec.add_statement(
    name='S1',
    text='res[%(a1)s]+=data[%(a2)s];',
    iter_space='{[i]: 0<=i && i<=N-1}',
    scatter='{[i]->[c0,i,c1]: c1=1}')

tetra_spec.add_statement(
    name='S2',
    text='res[%(a3)s]+=data[%(a4)s];',
    iter_space='{[i]: 0<=i && i<=N-1}',
    scatter='{[i]->[c0,i,c1]: c1=2}')

tetra_spec.add_statement(
    name='S3',
    text='res[%(a5)s]+=data[%(a6)s];',
    iter_space='{[i]: 0<=i && i<=N-1}',
    scatter='{[i]->[c0,i,c1]: c1=3}')

tetra_spec.add_statement(
    name='S4',
    text='res[%(a7)s]+=data[%(a8)s];',
    iter_space='{[i]: 0<=i && i<=N-1}',
    scatter='{[i]->[c0,i,c1]: c1=4}')

#Define the access relations for the statements
tetra_spec.add_access_relation(
    statement_name='S1',
    name='a1',
    data_array='res',
    iter_to_data='{[i]->[k]: k=i}')

tetra_spec.add_access_relation(
    statement_name='S1',
    name='a2',
    data_array='data',
    iter_to_data='{[i]->[k]: k=n1(i)}')

tetra_spec.add_access_relation(
    statement_name='S2',
    name='a3',
    data_array='res',
    iter_to_data='{[i]->[k]: k=i}')

tetra_spec.add_access_relation(
    statement_name='S2',
    name='a4',
    data_array='data',
    iter_to_data='{[i]->[k]: k=n2(i)}')

tetra_spec.add_access_relation(
    statement_name='S3',
    name='a5',
    data_array='res',
    iter_to_data='{[i]->[k]: k=i}')

tetra_spec.add_access_relation(
    statement_name='S3',
    name='a6',
    data_array='data',
    iter_to_data='{[i]->[k]: k=n3(i)}')

tetra_spec.add_access_relation(
    statement_name='S4',
    name='a7',
    data_array='res',
    iter_to_data='{[i]->[k]: k=i}')

tetra_spec.add_access_relation(
    statement_name='S4',
    name='a8',
    data_array='data',
    iter_to_data='{[i]->[k]: k=n4(i)}')

#Define the desired transformations
tetra_spec.add_transformation(
    iegen.trans.DataPermuteTrans,
    name='cpack',
    reordering_name='sigma',
    data_arrays=['data'],
    iter_sub_space_relation='{[c0,i,c1]->[i]}',
    target_data_array='data',
    erg_func_name='ERG_cpack')

iter_reordering=None
#iter_reordering=IterPermuteTrans(
#                iter_reordering=iegen.Relation('{ [ i,x ] -> [ k,x ] : k = delta( i ) }',syms),
##User doesn't specify?
##This is calculated in step 0
##               iteration_space=I_0,
##User doesn's specify?
##This is calculated in step 1a
##               access_relation=A_I_0_to_X_1,
#                iter_sub_space_relation=iegen.Relation('{ [ i, j ] -> [ i ] }',syms),
#                erg_func_name='ERG_lexmin',
#                erg_type='ERG_Permute')

#Data Dependences
#    Only reduction dependences.  It is important to indicate that there are reduction dependences however, because that means each iteration needs to be executed atomically if the loop is being parallelized.

#XXX: What is the best way that this should be specified using the MapIR specification?

print tetra_spec.codegen('test.c')
