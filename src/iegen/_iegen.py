import iegen.util

class MapIR(object):
	__slots__=('_iterspaces','_dataspaces','_index_arrays')

	def __init__(self):
		self.m_iterspaces={}
		self.m_dataspaces={}
		self.m_index_arrays={}

util.define_properties('MapIR',('iterspaces','dataspaces','index_arrays'))

class IterationSpace(object):
	__slots__=('_name','_spec')

	def __init__(self,name,spec):
		self.m_name=name
		self.m_spec=spec

util.define_properties('IterationSpace',('name','spec'))

class DataSpace(object):
	__slots__=('_name','_spec','_is_index_array')

	def __init__(self,name,spec,is_index_array):
		self.m_name=name
		self.m_spec=spec
		self.m_is_index_array=is_index_array

util.define_properties('DataSpace',('name','spec','is_index_array'))

class IndexArray(object):
	__slots__=('_dataspace','_index_value_constraints')

	def __init__(self,dataspace,index_value_constraints):
		self.m_dataspace=dataspace
		self.m_index_value_constraints=index_value_constraints

		#Checking
		if self.m_index_value_constraints.arity_in()!=self.m_dataspace.arity():
			raise util.DimensionalityError('The dimensionality of the domain (%d) should match the dimensionality of the associated index array DataSpace (%d).'%(self.m_index_value_constraints.arity_in(),self.m_dataspace.arity())

		if 1!=self.m_index_value_constraints.arity_out():
        raise util.DimensionalityError('The dimensionality of the range of the index array (%d) should be 1.'%self.m_index_value_constraints.arity_out())

util.define_properties('IndexArray',('dataspace','index_value_constraints'))

class AccessRelation(object):
	__slots__=('_name','_iterspace','_dataspace','_iterspace_to_dataspace')

	def __init__(self,name,iterspace,dataspace,iterspace_to_dataspace):
		self.m_name=name
		self.m_iterspace=iterspace
		self.m_dataspace=dataspace
		self.m_iterspace_to_dataspace=iterspace_to_dataspace

		if self.m_iterspace.arity()!=self.m_iterspace_to_dataspace.arity_in():
			raise util.DimensionalityError('The input arity of the access relation (%d) should be the arity of the iteration space (%d).'%(self.m_iterspace_to_dataspace.arity_in(),self.m_iterspace.arity())

		if self.m_dataspace.arity()!=self.m_iterspace_to_dataspace.arity_out():
			raise util.DimensionalityError('The output arity of the access relation (%d) should be the arity of the data space (%d).'%(self.m_iterspace_to_dataspace.arity_out(),self.m_dataspace.arity())

util.define_properties('AccessRelation',('name','iterspace','dataspace','iterspace_to_dataspace'))

class DataDependence(object):
	__slots__=('_iterspace','_dataspace','_data_dependence')

	def __init__(self,iterspace,dataspace,data_dependence):
		self.m_iterspace=iterspace
		self.m_dataspace=dataspace
		self.m_data_dependence=data_dependence

util.define_properties('DataDependence',('iterspace','dataspace','data_dependence'))
		#Checking
		#Can we check that given the iteration space, data spaces, and access functions, the given data dependence is valid?  Is it overly conservative?  optimistic?

#-------------------------------------------------------------------        
#Transformation Specification:
#
#    All of the run-time reordering transformations (RTRTs) should derive from this base class.  For now just for conceptual organization.  We might need functionality or interface specifications later.
#
#    An IAGspec is different than an RTRT because an IAGspec is a specification of a library routine that takes hypergraphs as input and generates indexed permutations and/or groupings.  The IAGspec could eventually have pre and post conditions.  The RTRT needs to keep track of data and iteration spaces involved in the reordering, and the RTRT will be responsible for generating the code that generates the hypergraph data structures that will be passed to the IAG library routine at runtime.
#
#
#    class RTRT {
#    }
#
#    class DataPermuteRTRT extends RTRT {
#        // reordering specification
#        OmegaRelation data_reordering;
#
#        // DataSpaces that should all be permuted in the same way.
#        List<DataSpace> data_spaces;
#
#        // AccessRelation, mapping of iterations to data that
#        // needs to have hypergraph creation code generated
#        AccessRelation access_relation;
#
#        // Mapping of full iteration space to sub space of the 
#        // iteration space that inspector should 
#        // traverse when inspecting the access relation.
#        OmegaRelation iter_sub_space_relation;
#
#        // Generator for the index arrays that are represented 
#        // as uninterpreted functions 
#        // in the data reordering specification.
#        // For now ASSUMING there is only one.
#        // When DataPermuteRTRT is created don't have all the info needed
#        // for the IAGspec instance.  Instead, just store the name of the 
#        // IAG function and the IAGspec subclass (can you do this in python?).
#        //IAGspec index_array_generator;
#        String iag_func_name;
#        Type(?) iag_type;      
#
#        // Codifying correctness?  How should we codify things like
#        // the data space should be 1D?
#            - all data spaces being reordered should have the same bounds
#    }
#
#    class IterPermuteRTRT extends RTRT {
#        // reordering specification
#        OmegaRelation iter_reordering;
#
#        // Iteration space that inspector should traverse and also that
#        // is being reordered
#        IterSpace iter_space;
#
#        // AccessRelation, mapping of iterations to data that
#        // needs to have hypergraph creation code generated
#        AccessRelation access_relation;
#
#        // Mapping of full iteration space to sub space of the 
#        // iteration space that inspector should 
#        // traverse when inspecting the access relation.
#        OmegaRelation iter_sub_space_relation;
#
#        // Generator for the index arrays that are represented 
#        // as uninterpreted functions 
#        // in the iteration reordering specification.
#        // For now ASSUMING there is only one.
#        String iag_func_name;
#        Type(?) iag_type;
#
#        // Codifying correctness?  How should we codify things like
#        // the data space should be 1D?
#    }       
#
#
#    // Base class
#    // Index array generator specifications.
#    class IAGspec {
#    }
#
#
#    //      IAG_Permute - specification for an IAG that 
#    //          takes a hypergraph (and possibly use its dual) and 
#    //          creates an index array containing a 
#    //          permutation of either the nodes or hyperedges in 
#    //          the hypergraph.
#
#    class IAG_Permute extends IAGspec {
#        AccessRelation input;
#        String name;
#        IndexArray result;
#    }
#
#FIXME: MMS, 5/23/08, only need IAG_Permute to work on the first part of the moldyn-FST composed transformation, so the rest of this still needs thought out
#
#    //      IAG_Group - creates an index array that groups the space
#    //          used to access the index array.
#    //          Assuming for now that we are only applying these to iteration
#    //          spaces.
#    //      Don't want to make this abstract.  Instead, it can be used by
#    //      any grouping that does not inspect access relations or data
#    //      dependences.
#    class IAG_Group {
#        // return the space being grouped
#        IterSpace getInputIterSpace();
#
#        // return heuristic being used to perform the grouping
#        Heuristic getHeuristic();
#
#        // Return specification for the index array that will be the 
#        // result of the grouping.  Won't know name but will know 
#        // input and output constraints for the uninterpreted function.
#        // Is this something that the IAG should be able to compute from
#        // its various pieces of info, the input space being grouped,
#        // and the Heuristic info?  What do we really want here?
#        OmegaRelation getIndexArraySpec();
#
#        // might have these members in the base class, 
#        // but might just have this be an interface
#        IterSpace input;
#        Heuristic heuristic;
#        IndexArray result;
#    }
#
#    // uses data dependences in iteration space
#    class IAG_Wavefront : public IAG_Group {
#        // Wavefront needs the set of data dependences between the
#        // points in the input iteration space.
#        DataDeps input_dd;
#
#    }
#
#    // uses data dependences in iter space and a seed partitioning
#    // on a subspace of the iter space
#    class IAG_SparseTiling : public IAG_Group {
#        // take dependences, a mapping from iter to seed space 
#        // and a partitioning of the seed space
#        DataDeps input_dd;
#        OmegaRelation iter_space_to_seed_space;
#        IndexArray seed_partition;
#    }
#
#
#Initial assumptions:
#    -single iteration space, but different heuristics can operate on subspaces within that iteration space
#    -range of uninterpreted function symbol is single dimensional
#    -data and index arrays are only one dimensional when first specified?  what about later?
#    -a data space is either an index array or a data array but not both, not sure what being both would mean
