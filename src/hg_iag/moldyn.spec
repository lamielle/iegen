#!/usr/bin/env python

from omega import Set,Relation
from iegen import IterationSpace,DataSpace,IndexArray,AccessRelation,Statement,DataPermuteRTRT,IterPermuteRTRT

#Code
#    for (ii=0; ii<n_inter; ii++) {
#        // simplified computations
#        fx[inter1[ii]] += x[inter1[ii]] - x[inter2[ii]]; 
#        fx[inter2[ii]] += x[inter1[ii]] - x[inter2[ii]]; 
#    }

#Iteration Space
I_0=IterationSpace('I_0',
    Set('{ [ii,stmt] : stmt=1 && 0 <= ii <= (n_inter-1)  }').union(Set('{ [ii,stmt] : stmt=2 && 0 <= ii <= (n_inter-1)  }')))

#Data Spaces
X_0=DataSpace('x',Set('{ [k] : 0 <= k <= (N-1) }'),False)
FX_0=DataSpace('fx',Set('{ [k] : 0 <= k <= (N-1) }'),False)
INTER1_0=DataSpace('inter1',Set('{ [k] : 0 <= k <= (n_inter-1) }'),True)
INTER2_0=DataSpace('inter2',Set('{ [k] : 0 <= k <= (n_inter-1) }'),True)

#Index Array Value Constraints
IA1_0=IndexArray(INTER1_0,Relation('{ [ii] -> [inter_func] : inter_func=inter1(i) && not (0 <= ii <= (n_inter-1)) || (0 <= inter1(i) <= (N-1)) }'))
IA2_0=IndexArray(INTER1_0,Relation('{ [ii] -> [inter_func] : inter_func=inter2(i) && not (0 <= ii <= (n_inter-1)) || (0 <= inter2(i) <= (N-1)) }'))

#Access Relations
STMT1_A1=AccessRelation('STMT1_A1',I_0,FX_0,Relation('{ [ii,1] -> [ inter_func ] : inter_func=inter1(ii) }'))
STMT1_A2=AccessRelation('STMT1_A2',I_0,X_0,Relation('{ [ii,1] -> [ inter_func ] : inter_func=inter1(ii) }'))
STMT1_A3=AccessRelation('STMT1_A3',I_0,X_0,Relation('{ [ii,1] -> [ inter_func ] : inter_func=inter2(ii) }'))

STMT2_A1=AccessRelation('STMT1_A1',I_0,FX_0,Relation('{ [ii,1] -> [ inter_func ] : inter_func=inter2(ii) }'))
STMT2_A2=AccessRelation('STMT1_A2',I_0,X_0,Relation('{ [ii,1] -> [ inter_func ] : inter_func=inter1(ii) }'))
STMT2_A3=AccessRelation('STMT1_A3',I_0,X_0,Relation('{ [ii,1] -> [ inter_func ] : inter_func=inter2(ii) }'))

STMT1=Statement('STMT1',(STMT1_A1,STMT1_A2,STMT1_A3))
STMT2=Statement('STMT2',(STMT2_A1,STMT2_A2,STMT2_A3))

A_I0_to_X0=AccessRelation('A_I0_to_X0',I_0,X_0,Relation('{ [ii,1] -> [ inter_func ] : inter_func=inter1(ii) }').union(Relation('{ [ii,2] -> [ inter_func ] : inter_func=inter2(ii) }')))
A_I0_to_FX0=AccessRelation('A_I0_to_FX0',I_0,FX_0,Relation('{ [ii,1] -> [ inter_func ] : inter_func=inter1(ii) }').union(Relation('{ [ii,2] -> [ inter_func ] : inter_func=inter2(ii)}')))

#Data Dependences
#    Only reduction dependences.  It is important to indicate that there are reduction dependences however, because that means each iteration needs to be executed atomically if the loop is being parallelized.

#What is the best way that this should be specified using the MapIR specification?


DataPermuteRTRT(
	Relation('{ [ k ] -> [ sigma ] : sigma=sigma(k) }'),
	(X_0,FX_0),
	A_I0_to_X0,
	Relation('{ [ ii, j ] -> [ ii ] }'),
	'CPackHyper',
	'IAG_Permute')

IterPermuteRTRT(
	Relation('{ [ i ] -> [ delta ] : delta=delta( i ) }'),
	(I_0,),
	A_I0_to_X0,
	Relation('{ [ ii, j ] -> [ ii ] }'),
	'LexMin',
	'IAG_Permute')

#------------------------------------------------------------
#Automatically Generating Straight-Forward Inspector/Executor
#------------------------------------------------------------
#
#Generating the composed inspector
#
#    1) DataPermuteRTRT
#        a) restrict access_relation to iteration subspace
#            input:
#                access_relation
#                iter_sub_space_relation
#
#            output:
#                access_relation_to_traverse = new AccessRelation
#                    name = access_relation.name
#                    iter_space = iter_sub_space_relation (     
#                                    [access_relation.iter_space] )
#                    data_space = access_relation.data_space
#                    iterspace_to_data =  inverse 
#                    ( iter_sub_space_relation compose (inverse access_relation))
#
#
#            For the example, output is the following:
#                access_relation_to_traverse = new AccessRelation
#                    name = "A_I0_to_X0"
#                    iter_space = { [ii] : 0 <= ii < n_inter  }
#                    data_space = X0                    
#                    iterspace_to_data := { [ii] -> [ inter1(ii) ] } 
#                                       union { [ii] -> [ inter2(ii) ] }
#
#
#        b) generate code that explicitly creates hypergraph representation of access relation at runtime.
#            input:
#                access_relation_to_traverse (artt)
#            output:
#                code
#                    // data index calc for each disjunct in access relation
#                    #define s1(i_1, ..., i_d) data_index = ...; \
#                        Hypergraph_ordered_insert_node([artt.name], \
#                        count,data_index); \
#                        count++;
#
#                    // initialize variables
#                    Hypergraph* [artt.name] = Hypergraph_ctor();
#                    int count=0;
#                    int data_index=0;
#                    int t1, ..., ;  // declare index variables omega will use
#
#                    // loop that traverses [artt.iter_space]
#                    for ...
#                        s1(i_1, ..., i_d);
#
#                    Hypergraph_finalize([argtt.name]);
#
#
#            For the example, output is the following:
#                    // this macro captures A_I0_to_X0, count, and data_index
#                    #define s1(t1) data_index = inter1[t1]; \
#                        Hypergraph_ordered_insert_node(A_I0_to_X0,count, \
#                        data_index); \
#                        data_index = inter2[t1]; \
#                        Hypergraph_ordered_insert_node(A_I0_to_X0,count, \
#                        data_index); \
#                        count++
#
#                    // initialize variables
#                    Hypergraph* A_I0_to_X0 = Hypergraph_ctor();
#                    int count=0;
#                    int data_index=0;
#
#                    // this specific example
#                    for(t1 = 0; t1 <= n_inter-1; t1++) {
#                        s1(t1);
#                    }
#
#                    Hypergraph_finalize(A_I0_to_X0);
#
#            algorithm:
#                1) use omega codegen to generate loop over iteration sub space
#                    codegen iter_sub_space;
#
#                2) generate a macro definition for the statement in the loop body from the relation_to_traverse
#                    a) for each conjunct in the DNF // seem omega lib docs
#                         -gen code that solves for the out variable, data_index, using the input iterator values
#                         -gen code that makes the following call:
#                            Hypergraph_ordered_insert_node( hgraph, iter_count, data_index )
#
#        c) Automatically generate the IndexArray specification for sigma
#            input:
#                DataPermuteRTRT instance
#                access_relation_to_traverse
#
#            output:
#                iag_spec = new IAG_Permute(
#                    String name = rtrt.iag_func_name
#                    AccessRelation input = access_relation_to_traverse
#                    IndexArray result = new IndexArray(
#                        data_space = [name of uninterp func in data_reordering],
#                                     [specification from data space in RTRT],
#                                     index array,
#                        index_value_constraints = { [k] -> [ uninterp(k) ] : 
#                            not [k has same bounds as data space] || 
#                            [uninterp(k) has same bounds as data space] }   
#                    )
#                )
#
#            Initial Assumptions:
#                -only one interpreted function in data reordering
#                -that uninterpreted function has a domain with dimensionality 1
#
#
#            For this example:
#                IAG_cpack = new IAG_Permute (
#                    String name = "CPackHyper"       // function name
#                    AccessRelation input = A_I0_to_X0
#                    IndexArray result = new IndexArray( 
#                        data_space = "sigma", X_0.spec, index array,
#                        index_value_constraints = { [k] -> [sigma(k)] : not (0 <= k <= (N-1)) || (0 <= sigma(k) <= (N-1)) }
#                    )
#
#                )        
#
#
#        d) generate code that passes hypergraph to IAG
#            input: 
#                iag_spec for sigma
#
#            output:
#                code
#                    [iag_spec.result.data_space.name] = malloc( ... );
#                    [iag_spec.name]( [iag_spec.input.name],
#                                     [iag_spec.result.data_space.name] );
#
#            For this example:
#                    int *sigma;
#                    MALLOC(sigma,int,N);
#                    CPackHyper( A_I0_to_X0, sigma );
#
#
#        e) generate code that does data reordering
#            input:
#                iag_spec for sigma
#                DataPermuteRTRT.data_spaces to be reordered
#
#            output:
#                code that reorders the specified data spaces with sigma
#                // one call to reorderArray for each data space being reordered
#                reorderArray((unsigned char*) [data_space.name], 
#                             sizeof([data_space.datatype]), 
#                             [data_space.num_elem],
#                             [iag_spec.name])
#
#            For this example:
#                reorderArray((unsigned char *)x, sizeof(double), NUM_NODES, sigma);
#                reorderArray((unsigned char *)fx, sizeof(double), NUM_NODES, sigma);
#
#
#        f) generate executor code for data reordering only
#        Note: eventually we want to generate the composed inspector/executor only, but for testing we need to be able to do each individually.
#
#            input:
#                DataPermuteRTRT.data_spaces
#
#
#            output:
#                // statement macros
#                #define s1(t1, ..., ) ...    
#
#                ...
#
#                // new executor loop
#                for ...
#
#            algorithm:
#                for each statement in computation
#                    for each data access
#                        if accessing array that was reordered
#                            modify array access relation as per DataPermuteRTRT.data_reordering specification
#
#                for each statement in computation
#                    generate macro code for statement
#
#                have omega generate code for transformed iteration space
#
#
#            output for this example:
#                #define e1(ii,g)    if ((g)==1) { \
#                    fx[sigma[inter1[ii]]] += x[sigma[inter1[ii]]]*0.1 \
#                             + x[sigma[inter2[ii]]]*0.3; \
#                } else { \
#                    fx[sigma[inter2[ii]]] += x[sigma[inter1[ii]]]*0.2  \
#                             + x[sigma[inter2[ii]]]*0.4; \
#                }
#
#                ...
#
#                // executor - execute the computation with modified arrays
#                for(t1 = 0; t1 <= n_inter-1; t1++) {
#                    e1(t1,1);
#                    e1(t1,2);
#                }
#
#    2) Modify iteration space and access functions based on previous transformation.
#
#        I1 := I0    // iteration space was not modified
#        X1 := X0    // same size
#        FX1 := FX0    // same size
#        A_I1_to_X1 = data_reordering(A_I0_to_X0) 
#                   = { [ii,1] -> [ sigma(inter1(ii)) ] } 
#                     union { [ii,1] -> [ sigma(inter2(ii)) ] }
#
#        A_I1_to_FX1 = data_reordering(A_I0_to_FX0)
#                    = { [ii,1] -> [ sigma(inter1(ii)) ] } 
#                      union { [ii,1] -> [ sigma(inter2(ii)) ] }
#
#    3) IterPermuteRTRT
#        a) restrict access_relation to iteration subspace (same as 1a above)
#
#            For the example, output is the following:
#                access_relation_to_traverse = new AccessRelation
#                    name = "A_I1_to_X1"
#                    iter_space = { [ii] : 0 <= ii < n_inter  }
#                    data_space = X1                    
#                    iterspace_to_data := { [ii] -> [ sigma(inter1(ii)) ] } 
#                                       union { [ii] -> [ sigma(inter2(ii)) ] }
#
#
#        b) generate code that explicitly creates hypergraph generate code that explicitly creates hypergraph representation of access relation at runtime. (same as 1b above)
#
#
#            For the example, output is the following:
#                    // this macro captures A_I1_to_X1, 
#                    // count, sigma, inter1, inter2, and data_index
#                    #define s2(t1) data_index = sigma[inter1[t1]]; \
#                        Hypergraph_ordered_insert_node(A_I1_to_X1,count, \
#                        data_index); \
#                        data_index = sigma[inter2[t1]]; \
#                        Hypergraph_ordered_insert_node(A_I1_to_X1,count, \
#                        data_index); \
#                        count++
#
#                    // initialize variables
#                    Hypergraph* A_I1_to_X1 = Hypergraph_ctor();
#                    int count=0;
#                    int data_index=0;
#
#                    // this specific example
#                    for(t1 = 0; t1 <= n_inter-1; t1++) {
#                        s2(t1);
#                    }
#
#                    Hypergraph_finalize(A_I1_to_X1);
#
#
#        c) Automatically generate the IndexArray specification for delta.
#        Should this algorithm be a method associated with IterPermuteRTRT?
#            input:
#                IterPermuteRTRT instance
#                access_relation_to_traverse
#
#            output: (almost the same as 1c, just replace data space with iteration space)
#                iag_spec = new IAG_Permute(
#                    String name = rtrt.iag_func_name
#                    AccessRelation input = access_relation_to_traverse
#                    IndexArray result = new IndexArray(
#                        data_space = [name of uninterp func in iter_reordering],
#                                     [rtrt.iter_space],
#                                     index array,
#                        index_value_constraints = { [k] -> [ uninterp(k) ] : 
#                            not [k has same bounds as rtrt.iter_space] || 
#                            [uninterp(k) has same bounds as rtrt.iter_space] }   
#                    )
#                )
#
#            Initial Assumptions:
#                -only one interpreted function in iteration reordering
#                -that uninterpreted function has a domain with dimensionality 1
#
#
#            For this example:
#                IAG_cpack = new IAG_Permute (
#                    String name = "LexMinHyper"       // function name
#                    AccessRelation input = A_I0_to_X0
#                    IndexArray result = new IndexArray( 
#                        data_space = "sigma", X_0.spec, index array,
#                        index_value_constraints = { [k] -> [sigma(k)] : not (0 <= k <= (N-1)) || (0 <= sigma(k) <= (N-1)) }
#                    )
#
#                )        
#
#
#        d) generate code that passes hypergraph to IAG
#            input: 
#                iag_spec for sigma
#
#            output:
#                code
#                    [iag_spec.result.data_space.name] = malloc( ... );
#                    [iag_spec.name]( [iag_spec.input.name],
#                                     [iag_spec.result.data_space.name] );
#
#            For this example:
#                    int *sigma;
#                    MALLOC(sigma,int,N);
#                    CPackHyper( A_I0_to_X0, sigma );
#
#
#        e) generate code that does data reordering
#            input:
#                iag_spec for sigma
#                DataPermuteRTRT.data_spaces to be reordered
#
#            output:
#                code that reorders the specified data spaces with sigma
#                // one call to reorderArray for each data space being reordered
#                reorderArray((unsigned char*) [data_space.name], 
#                             sizeof([data_space.datatype]), 
#                             [data_space.num_elem],
#                             [iag_spec.name])
#
#            For this example:
#                reorderArray((unsigned char *)x, sizeof(double), NUM_NODES, sigma);
#                reorderArray((unsigned char *)fx, sizeof(double), NUM_NODES, sigma);
#
#
#        f) generate executor code for data reordering only
#        Note: eventually we want to generate the composed inspector/executor only, but for testing we need to be able to do each individually.
#
#            input:
#                DataPermuteRTRT.data_spaces
#
#
#            output:
#                // statement macros
#                #define s1(t1, ..., ) ...    
#
#                ...
#
#                // new executor loop
#                for ...
#
#            algorithm:
#                for each statement in computation
#                    for each data access
#                        if accessing array that was reordered
#                            modify array access relation as per DataPermuteRTRT.data_reordering specification
#
#                for each statement in computation
#                    generate macro code for statement
#
#                have omega generate code for transformed iteration space
#
#
#            output for this example:
#                #define e1(ii,g)    if ((g)==1) { \
#                    fx[sigma[inter1[ii]]] += x[sigma[inter1[ii]]]*0.1 \
#                             + x[sigma[inter2[ii]]]*0.3; \
#                } else { \
#                    fx[sigma[inter2[ii]]] += x[sigma[inter1[ii]]]*0.2  \
#                             + x[sigma[inter2[ii]]]*0.4; \
#                }
#
#                ...
#
#                // executor - execute the computation with modified arrays
#                for(t1 = 0; t1 <= n_inter-1; t1++) {
#                    e1(t1,1);
#                    e1(t1,2);
#                }
