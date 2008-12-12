#!/usr/bin/env python

from iegen import MapIR,Symbolic,DataArray,IndexArray,Statement,AccessRelation,Set,Relation
from iegen.trans import DataPermuteTrans,IterPermuteTrans

#Original Code:
#    for (i=0; i<n_inter; i++) {
#        // simplified computations
#        fx[inter1[i]] += x[inter1[i]] - x[inter2[i]];
#        fx[inter2[i]] += x[inter1[i]] - x[inter2[i]];
#    }

#Create a new empty MapIR specification for simple moldyn
moldyn_spec=MapIR()

#Define the symbolic constants for the computation
moldyn_spec.add_symbolic(Symbolic('N')) #Number of atoms
moldyn_spec.add_symbolic(Symbolic('n_inter')) #Number of interactions
syms=moldyn_spec.symbolics.values()

#Define the data arrays for the computation
moldyn_spec.add_data_array(DataArray(
    name='x',
    bounds=Set('{[k]: 0<=k && k<=N-1}',syms)))

moldyn_spec.add_data_array(DataArray(
    name='fx',
    bounds=Set('{[k]: 0<=k && k<=N-1}',syms)))

#Define the index arrays for the computation
moldyn_spec.add_index_array(IndexArray(
    name='inter1',
    input_bounds=Set('{[k]: 0<=k && k<=n_inter-1}',syms),
    output_bounds=Set('{[k]: 0<=k && k<=N-1}',syms)))

moldyn_spec.add_index_array(IndexArray(
    name='inter2',
    input_bounds=Set('{[k]: 0<=k && k<=n_inter-1}',syms),
    output_bounds=Set('{[k]: 0<=k && k<=N-1}',syms)))

#Define the statements for the computation
moldyn_spec.add_statement(Statement(
    name='S1',
    text='fx[%(a1)s] += x[%(a2)s] - x[%(a3)s];',
    iter_space=Set('{[i]: 0<=i && i<=n_inter-1}',syms),
    scatter=Relation('{[i]->[c0,i,c1]: c0=1 and c1=1}',syms)))

moldyn_spec.add_statement(Statement(
    name='S2',
    text='fx[%(a4)s] += x[%(a5)s] - x[%(a6)s];',
    iter_space=Set('{[i]: 0<=i && i<=n_inter-1}',syms),
    scatter=Relation('{[i]->[c0,i,c1]: c0=1 and c1=2}',syms)))

#Define the access relations for the statements
moldyn_spec.statements['S1'].add_access_relation(AccessRelation(
    name='a1',
    data_array=moldyn_spec.data_arrays['fx'],
    iter_to_data=Relation('{[i]->[k]: k=inter1(i)}',syms)))

moldyn_spec.statements['S1'].add_access_relation(AccessRelation(
    name='a2',
    data_array=moldyn_spec.data_arrays['x'],
    iter_to_data=Relation('{[i]->[k]: k=inter1(i)}',syms)))

moldyn_spec.statements['S1'].add_access_relation(AccessRelation(
    name='a3',
    data_array=moldyn_spec.data_arrays['x'],
    iter_to_data=Relation('{[i]->[k]: k=inter2(i)}',syms)))

moldyn_spec.statements['S2'].add_access_relation(AccessRelation(
    name='a4',
    data_array=moldyn_spec.data_arrays['x'],
    iter_to_data=Relation('{[i]->[k]: k=inter2(i)}',syms)))

moldyn_spec.statements['S2'].add_access_relation(AccessRelation(
    name='a5',
    data_array=moldyn_spec.data_arrays['x'],
    iter_to_data=Relation('{[i]->[k]: k=inter1(i)}',syms)))

moldyn_spec.statements['S2'].add_access_relation(AccessRelation(
    name='a6',
    data_array=moldyn_spec.data_arrays['x'],
    iter_to_data=Relation('{[i]->[k]: k=inter2(i)}',syms)))

#Define the desired transformations
moldyn_spec.add_transformation(DataPermuteTrans(
    name='cpack',
    data_reordering=Relation('{[k]->[r]: r=sigma(k)}',syms),
    data_arrays=[moldyn_spec.data_arrays['x'],moldyn_spec.data_arrays['fx']],
    iter_sub_space_relation=Relation('{[c0,i,c1]->[i]}',syms),
    target_data_array=moldyn_spec.data_arrays['x'],
    iag_func_name='IAG_cpack'))

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
#                iag_func_name='IAG_lexmin',
#                iag_type='IAG_Permute')

#Data Dependences
#    Only reduction dependences.  It is important to indicate that there are reduction dependences however, because that means each iteration needs to be executed atomically if the loop is being parallelized.

#XXX: What is the best way that this should be specified using the MapIR specification?

print moldyn_spec.codegen('test.c')
