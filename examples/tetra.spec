#!/usr/bin/env python

from iegen import MapIR,Symbolic,DataArray,IndexArray,Statement,AccessRelation,Set,Relation
from iegen.trans import DataPermuteTrans,IterPermuteTrans

#Original Code:
#for(int i=0; i<N; i++) {
#   res[i]+=data[n1[i]]
#   res[i]+=data[n2[i]]
#   res[i]+=data[n3[i]]
#   res[i]+=data[n4[i]]
#}

#Create a new empty MapIR specification for simple tetra
tetra_spec=MapIR()

#Define the symbolic constants for the computation
tetra_spec.add_symbolic(Symbolic('N')) #Number of tetrahedrons
syms=tetra_spec.get_symbolics()

#Define the data arrays for the computation
tetra_spec.add_data_array(DataArray(
    name='data',
    bounds=Set('{[k]: 0<=k && k<=N-1}',syms)))

tetra_spec.add_data_array(DataArray(
    name='res',
    bounds=Set('{[k]: 0<=k && k<=N-1}',syms)))

#Define the index arrays for the computation
tetra_spec.add_index_array(IndexArray(
    name='n1',
    input_bounds=Set('{[k]: 0<=k && k<=N-1}',syms),
    output_bounds=Set('{[k]: 0<=k && k<=N-1}',syms)))

tetra_spec.add_index_array(IndexArray(
    name='n2',
    input_bounds=Set('{[k]: 0<=k && k<=N-1}',syms),
    output_bounds=Set('{[k]: 0<=k && k<=N-1}',syms)))

tetra_spec.add_index_array(IndexArray(
    name='n3',
    input_bounds=Set('{[k]: 0<=k && k<=N-1}',syms),
    output_bounds=Set('{[k]: 0<=k && k<=N-1}',syms)))

tetra_spec.add_index_array(IndexArray(
    name='n4',
    input_bounds=Set('{[k]: 0<=k && k<=N-1}',syms),
    output_bounds=Set('{[k]: 0<=k && k<=N-1}',syms)))

#Define the statements for the computation
tetra_spec.add_statement(Statement(
    name='S1',
    text='res[%(a1)s]+=data[%(a2)s];',
    iter_space=Set('{[i]: 0<=i && i<=N-1}',syms),
    scatter=Relation('{[i]->[c0,i,c1]: c1=1}',syms)))

tetra_spec.add_statement(Statement(
    name='S2',
    text='res[%(a3)s]+=data[%(a4)s];',
    iter_space=Set('{[i]: 0<=i && i<=N-1}',syms),
    scatter=Relation('{[i]->[c0,i,c1]: c1=2}',syms)))

tetra_spec.add_statement(Statement(
    name='S3',
    text='res[%(a5)s]+=data[%(a6)s];',
    iter_space=Set('{[i]: 0<=i && i<=N-1}',syms),
    scatter=Relation('{[i]->[c0,i,c1]: c1=3}',syms)))

tetra_spec.add_statement(Statement(
    name='S4',
    text='res[%(a7)s]+=data[%(a8)s];',
    iter_space=Set('{[i]: 0<=i && i<=N-1}',syms),
    scatter=Relation('{[i]->[c0,i,c1]: c1=4}',syms)))

#Define the access relations for the statements
tetra_spec.statements['S1'].add_access_relation(AccessRelation(
    name='a1',
    data_array=tetra_spec.data_arrays['res'],
    iter_to_data=Relation('{[i]->[k]: k=i}',syms)))

tetra_spec.statements['S1'].add_access_relation(AccessRelation(
    name='a2',
    data_array=tetra_spec.data_arrays['data'],
    iter_to_data=Relation('{[i]->[k]: k=n1(i)}',syms)))

tetra_spec.statements['S2'].add_access_relation(AccessRelation(
    name='a3',
    data_array=tetra_spec.data_arrays['res'],
    iter_to_data=Relation('{[i]->[k]: k=i}',syms)))

tetra_spec.statements['S2'].add_access_relation(AccessRelation(
    name='a4',
    data_array=tetra_spec.data_arrays['data'],
    iter_to_data=Relation('{[i]->[k]: k=n2(i)}',syms)))

tetra_spec.statements['S3'].add_access_relation(AccessRelation(
    name='a5',
    data_array=tetra_spec.data_arrays['res'],
    iter_to_data=Relation('{[i]->[k]: k=i}',syms)))

tetra_spec.statements['S3'].add_access_relation(AccessRelation(
    name='a6',
    data_array=tetra_spec.data_arrays['data'],
    iter_to_data=Relation('{[i]->[k]: k=n3(i)}',syms)))

tetra_spec.statements['S4'].add_access_relation(AccessRelation(
    name='a7',
    data_array=tetra_spec.data_arrays['res'],
    iter_to_data=Relation('{[i]->[k]: k=i}',syms)))

tetra_spec.statements['S4'].add_access_relation(AccessRelation(
    name='a8',
    data_array=tetra_spec.data_arrays['data'],
    iter_to_data=Relation('{[i]->[k]: k=n4(i)}',syms)))

#Define the desired transformations
tetra_spec.add_transformation(DataPermuteTrans(
    name='cpack',
    reordering_name='sigma',
    data_arrays=[tetra_spec.data_arrays['data']],
    iter_sub_space_relation=Relation('{[c0,i,c1]->[i]}',syms),
    target_data_array=tetra_spec.data_arrays['data'],
    erg_func_name='ERG_cpack'))

iter_reordering=None
#iter_reordering=IterPermuteTrans(
#                iter_reordering=Relation('{ [ i,x ] -> [ k,x ] : k = delta( i ) }',syms),
##User doesn't specify?
##This is calculated in step 0
##               iteration_space=I_0,
##User doesn's specify?
##This is calculated in step 1a
##               access_relation=A_I_0_to_X_1,
#                iter_sub_space_relation=Relation('{ [ i, j ] -> [ i ] }',syms),
#                erg_func_name='ERG_lexmin',
#                erg_type='ERG_Permute')

#Data Dependences
#    Only reduction dependences.  It is important to indicate that there are reduction dependences however, because that means each iteration needs to be executed atomically if the loop is being parallelized.

#XXX: What is the best way that this should be specified using the MapIR specification?

print tetra_spec.codegen('test.c')
