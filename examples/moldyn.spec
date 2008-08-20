#!/usr/bin/env python

import iegen,iegen.util
from iegen import MapIR
from iegen import Symbolic,DataSpace,IndexArray
from iegen import Set,Relation
from iegen import Statement,AccessRelation

#Original Code:
#    for (ii=0; ii<n_inter; ii++) {
#        // simplified computations
#        fx[inter1[ii]] += x[inter1[ii]] - x[inter2[ii]];
#        fx[inter2[ii]] += x[inter1[ii]] - x[inter2[ii]];
#    }

#Create a new empty MapIR specification for simple moldyn
moldyn_spec=MapIR()

#Define the symbolic constants for the computation
moldyn_spec.symbolics['N']=Symbolic('N') #Number of atoms
moldyn_spec.symbolics['n_inter']=Symbolic('n_inter') #Number of interactions

#Define the data spaces for the computation
X_0=DataSpace(name='x',
              set=Set('{ [k] : 0 <= k && k <= (N-1) }'),
              is_index_array=False)
moldyn_spec.data_spaces['x']=X_0

FX_0=DataSpace(name='fx',
               set=Set('{ [k] : 0 <= k && k <= (N-1) }'),
               is_index_array=False)
moldyn_spec.data_spaces['fx']=FX_0

INTER1_0=DataSpace(
	name='inter1',
	set=Set('{ [k] : 0 <= k && k <= (n_inter-1) }'),
	is_index_array=True)
moldyn_spec.data_spaces['inter1']=INTER1_0

INTER2_0=DataSpace(
	name='inter2',
	set=Set('{ [k] : 0 <= k && k <= (n_inter-1) }'),
	is_index_array=True)
moldyn_spec.data_spaces['inter2']=INTER2_0

#Define the index arrays for the computation
inter1=IndexArray(data_space=INTER1_0,
                  is_permutation=False,
                  input_bounds=[Set('{ [k] : 0 <= k && k <= (n_inter-1) }')],
                  output_bounds=Set('{ [k] : 0 <= k && k <= (N-1) }'))
moldyn_spec.add_index_array(inter1)

inter2=IndexArray(data_space=INTER2_0,
                  is_permutation=False,
                  input_bounds=[Set('{ [k] : 0 <= k && k <= (n_inter-1) }')],
                  output_bounds=Set('{ [k] : 0 <= k && k <= (N-1) }'))
moldyn_spec.add_index_array(inter2)

#Define the statements for the computation
S1=Statement(statement='`a1 += `a2 - `a3;',
             iter_space=Set('{[ii] : 0 <= ii && ii <= (n_inter-1) }'),
             scatter=Relation('{[ii] -> [ii,j] : j=1}'))
moldyn_spec.add_statement(S1)

S2=Statement(statement='`a4 += `a5 - `a6;',
             iter_space=Set('{[ii] : 0 <= ii && ii <= (n_inter-1) }'),
             scatter=Relation('{[ii] -> [ii,j] : j=2}'))
moldyn_spec.add_statement(S2)

#Define the access relations for the statements
a1=AccessRelation(name='a1',
                  data_space=FX_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter1(ii) }'))
S1.add_access_relation(a1)

a2=AccessRelation(name='a2',
                  data_space=X_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter1(ii) }'))
S1.add_access_relation(a2)

a3=AccessRelation(name='a3',
                  data_space=X_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter2(ii) }'))
S1.add_access_relation(a3)

a4=AccessRelation(name='a4',
                  data_space=FX_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter1(ii) }'))
S2.add_access_relation(a4)

a5=AccessRelation(name='a5',
                  data_space=X_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter1(ii) }'))
S2.add_access_relation(a5)

a6=AccessRelation(name='a6',
                  data_space=X_0,
                  iter_to_data=Relation('{ [ii] -> [k] : k=inter2(ii) }'))
S2.add_access_relation(a6)

#Data Dependences
#    Only reduction dependences.  It is important to indicate that there are reduction dependences however, because that means each iteration needs to be executed atomically if the loop is being parallelized.

#XXX: What is the best way that this should be specified using the MapIR specification?

moldyn_spec.codegen()

#DataPermuteRTRT(
#	Relation('{ [ k ] -> [ sigma ] : sigma=sigma(k) }'),
#	(X_0,FX_0),
#	A_I0_to_X0,
#	Relation('{ [ ii, j ] -> [ ii ] }'),
#	'CPackHyper',
#	'IAG_Permute')
#
#IterPermuteRTRT(
#	Relation('{ [ i ] -> [ delta ] : delta=delta( i ) }'),
#	(I_0,),
#	A_I0_to_X0,
#	Relation('{ [ ii, j ] -> [ ii ] }'),
#	'LexMin',
#	'IAG_Permute')
