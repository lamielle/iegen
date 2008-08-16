import iegen,iegen.util

import os.path

#Store the directory where the iegen module is located
iegen.dir=os.path.dirname(os.path.abspath(iegen.__file__))

#---------- MapIR class ----------
class MapIR(object):
	__slots__=('_iterspaces','_dataspaces','_index_arrays')

	def __init__(self):
		self.m_iterspaces={}
		self.m_dataspaces={}
		self.m_index_arrays={}

iegen.util.define_properties(MapIR,('iterspaces','dataspaces','index_arrays'))
#---------------------------------

#---------- IterationSpace class ----------
class IterationSpace(object):
	__slots__=('_name','_spec')

	def __init__(self,name,spec):
		self.m_name=name
		self.m_spec=spec

iegen.util.define_properties(IterationSpace,('name','spec'))
#------------------------------------------

#---------- DataSpace class ----------
class DataSpace(object):
	__slots__=('_name','_spec','_is_index_array')

	def __init__(self,name,spec,is_index_array):
		self.m_name=name
		self.m_spec=spec
		self.m_is_index_array=is_index_array

iegen.util.define_properties(DataSpace,('name','spec','is_index_array'))
#-------------------------------------

#---------- IndexArray class ----------
class IndexArray(object):
	__slots__=('_dataspace','_index_value_constraints')

	def __init__(self,dataspace,index_value_constraints):
		self.m_dataspace=dataspace
		self.m_index_value_constraints=index_value_constraints

		#Checking
		if self.m_index_value_constraints.arity_in()!=self.m_dataspace.m_spec.arity():
			raise iegen.util.DimensionalityError('The dimensionality of the domain (%d) should match the dimensionality of the associated index array DataSpace (%d).'%(self.m_index_value_constraints.arity_in(),self.m_dataspace.m_spec.arity()))

		if 1!=self.m_index_value_constraints.arity_out():
			raise iegen.util.DimensionalityError('The dimensionality of the range of the index array (%d) should be 1.'%self.m_index_value_constraints.arity_out())

iegen.util.define_properties(IndexArray,('dataspace','index_value_constraints'))
#--------------------------------------

#---------- AccessRelation class ----------
class AccessRelation(object):
	__slots__=('_name','_iterspace','_dataspace','_iterspace_to_dataspace')

	def __init__(self,name,iterspace,dataspace,iterspace_to_dataspace):
		self.m_name=name
		self.m_iterspace=iterspace
		self.m_dataspace=dataspace
		self.m_iterspace_to_dataspace=iterspace_to_dataspace

		if self.m_iterspace.m_spec.arity()!=self.m_iterspace_to_dataspace.arity_in():
			raise iegen.util.DimensionalityError('The input arity of the access relation (%d) should be the arity of the iteration space (%d).'%(self.m_iterspace_to_dataspace.arity_in(),self.m_iterspace.m_spec.arity()))

		if self.m_dataspace.m_spec.arity()!=self.m_iterspace_to_dataspace.arity_out():
			raise iegen.util.DimensionalityError('The output arity of the access relation (%d) should be the arity of the data space (%d).'%(self.m_iterspace_to_dataspace.arity_out(),self.m_dataspace.m_spec.arity()))

iegen.util.define_properties(AccessRelation,('name','iterspace','dataspace','iterspace_to_dataspace'))
#------------------------------------------

#---------- Statement class ----------
class Statement(object):
	__slots__=('_name','_access_relations')

	def __init__(self,name,access_relations):
		self.m_name=name
		self.m_access_relations=access_relations

iegen.util.define_properties(Statement,('name','access_relations'))
#-------------------------------------

#---------- DataDependence class ----------
class DataDependence(object):
	__slots__=('_iterspace','_dataspace','_data_dependence')

	def __init__(self,iterspace,dataspace,data_dependence):
		self.m_iterspace=iterspace
		self.m_dataspace=dataspace
		self.m_data_dependence=data_dependence

		#Checking
		#Can we check that given the iteration space, data spaces, and access functions, the given data dependence is valid?  Is it overly conservative?  optimistic?

iegen.util.define_properties(DataDependence,('iterspace','dataspace','data_dependence'))
#------------------------------------------

#---------- RTRT base class ----------
class RTRT(object):
	pass
#-------------------------------------

#---------- DataPermuteRTRT class ----------
class DataPermuteRTRT(RTRT):
	__slots__=('_data_reordering','_data_spaces','_access_relation','_iter_sub_space_relation','_iag_func_name','_iag_type')

	def __init__(self,data_reordering,data_spaces,access_relation,iter_sub_space_relation,iag_func_name,iag_type):
		m_data_reordering=data_reordering
		m_data_spaces=data_spaces
		m_access_relation=access_relation
		m_iter_sub_space_relation=iter_sub_space_relation
		m_iag_func_name=iag_func_name
		m_iag_type=iag_type

iegen.util.define_properties(DataPermuteRTRT,('data_reordering','data_spaces','access_relation','iter_sub_space_relation','iag_func_name','iag_type'))
#-------------------------------------------

#---------- IterPermuteRTRT class ----------
class IterPermuteRTRT(RTRT):
	__slots__=('_iter_reordering','_iter_space','_access_relation','_iter_sub_space_relation','_iag_func_name','_iag_type')

	def __init__(self,iter_reordering,iter_spaces,access_relation,iter_sub_space_relation,iag_func_name,iag_type):
		m_iter_reordering=iter_reordering
		m_iter_spaces=iter_spaces
		m_access_relation=access_relation
		m_iter_sub_space_relation=iter_sub_space_relation
		m_iag_func_name=iag_func_name
		m_iag_type=iag_type

iegen.util.define_properties(IterPermuteRTRT,('iter_reordering','iter_space','access_relation','iter_sub_space_relation','iag_func_name','iag_type'))
#-------------------------------------------

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
