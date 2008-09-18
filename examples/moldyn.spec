#!/usr/bin/env python

import iegen,iegen.util
from iegen import MapIR
from iegen import Symbolic,DataSpace,IndexArray
from iegen import Set,Relation
from iegen import Statement,AccessRelation
from iegen import DataPermuteRTRT,IterPermuteRTRT

#Original Code:
#    for (ii=0; ii<n_inter; ii++) {
#        // simplified computations
#        fx[inter1[ii]] += x[inter1[ii]] - x[inter2[ii]];
#        fx[inter2[ii]] += x[inter1[ii]] - x[inter2[ii]];
#    }

#Create a new empty MapIR specification for simple moldyn
moldyn_spec=MapIR()

#Define the symbolic constants for the computation
moldyn_spec.add_symbolic('N') #Number of atoms
moldyn_spec.add_symbolic('n_inter') #Number of interactions
syms=moldyn_spec.symbolics()

#Define the data spaces for the computation
X_0=DataSpace(name='x',
              set=Set('{ [k] : 0 <= k && k <= (N-1) }',syms),
              is_index_array=False)
moldyn_spec.data_spaces['x']=X_0

FX_0=DataSpace(name='fx',
               set=Set('{ [k] : 0 <= k && k <= (N-1) }',syms),
               is_index_array=False)
moldyn_spec.data_spaces['fx']=FX_0

INTER1_0=DataSpace(
	name='inter1',
	set=Set('{ [k] : 0 <= k && k <= (n_inter-1) }',syms),
	is_index_array=True)
moldyn_spec.data_spaces['inter1']=INTER1_0

INTER2_0=DataSpace(
	name='inter2',
	set=Set('{ [k] : 0 <= k && k <= (n_inter-1) }',syms),
	is_index_array=True)
moldyn_spec.data_spaces['inter2']=INTER2_0

#Define the index arrays for the computation
inter1=IndexArray(data_space=INTER1_0,
                  is_permutation=False,
                  input_bounds=[Set('{ [k] : 0 <= k && k <= (n_inter-1) }',syms)],
                  output_bounds=Set('{ [k] : 0 <= k && k <= (N-1) }',syms))
moldyn_spec.add_index_array(inter1)

inter2=IndexArray(data_space=INTER2_0,
                  is_permutation=False,
                  input_bounds=[Set('{ [k] : 0 <= k && k <= (n_inter-1) }',syms)],
                  output_bounds=Set('{ [k] : 0 <= k && k <= (N-1) }',syms))
moldyn_spec.add_index_array(inter2)

#Define the statements for the computation
S1=Statement(statement='`a1 += `a2 - `a3;',
             iter_space=Set('{[ii] : 0 <= ii && ii <= (n_inter-1) }',syms),
             scatter=Relation('{[ii] -> [ii,j] : j=1}',syms))
moldyn_spec.add_statement(S1)

S2=Statement(statement='`a4 += `a5 - `a6;',
             iter_space=Set('{[ii] : 0 <= ii && ii <= (n_inter-1) }',syms),
             scatter=Relation('{[ii] -> [ii,j] : j=2}',syms))
moldyn_spec.add_statement(S2)

#Define the access relations for the statements
a1=AccessRelation(name='a1',
                  data_space=FX_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter1(ii) }',syms))
S1.add_access_relation(a1)

a2=AccessRelation(name='a2',
                  data_space=X_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter1(ii) }',syms))
S1.add_access_relation(a2)

a3=AccessRelation(name='a3',
                  data_space=X_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter2(ii) }',syms))
S1.add_access_relation(a3)

a4=AccessRelation(name='a4',
                  data_space=FX_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter1(ii) }',syms))
S2.add_access_relation(a4)

a5=AccessRelation(name='a5',
                  data_space=X_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter1(ii) }',syms))
S2.add_access_relation(a5)

a6=AccessRelation(name='a6',
                  data_space=X_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter2(ii) }',syms))
S2.add_access_relation(a6)


data_reordering=DataPermuteRTRT(
                data_reordering=Relation('{ [ k ] -> [ r ] : r=sigma( k ) }',syms),
                data_spaces=[X_0,FX_0],
                iter_sub_space_relation=Relation('{[ ii, j ] -> [ ii ] }',syms),
                target_data_space=X_0,
                iag_func_name='IAG_cpack')

iter_reordering=None
#iter_reordering=IterPermuteRTRT(
#                iter_reordering=Relation('{ [ i,x ] -> [ k,x ] : k = delta( i ) }',syms),
##User doesn't specify?
##This is calculated in step 0
##               iteration_space=I_0,
##User doesn's specify?
##This is calculated in step 1a
##               access_relation=A_I_0_to_X_1,
#                iter_sub_space_relation=Relation('{ [ ii, j ] -> [ ii ] }',syms),
#                iag_func_name='IAG_lexmin',
#                iag_type='IAG_Permute')

#Data Dependences
#    Only reduction dependences.  It is important to indicate that there are reduction dependences however, because that means each iteration needs to be executed atomically if the loop is being parallelized.

#XXX: What is the best way that this should be specified using the MapIR specification?

print moldyn_spec.codegen(data_reordering,iter_reordering,'test.c')
