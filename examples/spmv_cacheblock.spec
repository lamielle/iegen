#Include the spmv computation specification
iegen.include('spmv_comp.spec')

#Define the desired transformations

#Full Sparse Tiling

symbolics=[Symbolic('nz',lower_bound=1),Symbolic('ncb',lower_bound=1)]
T0 = Relation('{[c0,i,c0]->[c0,b,c0,r,c0,i,c0]: c0=0 and b=cb(i) and r=row(i)}',symbolics=symbolics)


spec.add_transformation(
    type=iegen.trans.CacheBlockTrans,
    name='cacheblock',    # name used in IDG
    grouping_name='cb',  # name of cache blocking created grouping function
    num_cb_name='ncb', #defines the name of the symbolic for the number of cache blocks

    # Mapping from full iteration space to sub space being cache blocked.
    iter_sub_space_relation=Relation('{[x,i,y]->[x,i]: y=0}',symbolics=symbolics), # Cache blocking non-zero loop

    #The name of the index array that maps non-zero ids to columns
    col_name='col',

    erg_func_name='ERG_cacheblock',

    iter_space_trans=T0 )
