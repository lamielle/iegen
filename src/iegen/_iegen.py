import iegen,iegen.util
import os.path

#Store the directory where the iegen module is located
iegen.dir=os.path.dirname(os.path.abspath(iegen.__file__))

#---------- MapIR class ----------
class MapIR(object):
	__slots__=('symbolics','data_spaces','index_arrays','statements','full_iter_space')

	def __init__(self):
		self.symbolics={}
		self.data_spaces={}
		self.index_arrays=[]
		self.statements=[]
		self.full_iter_space=None

	#Adds the given index array to the collection of index arrays
	def add_index_array(self,index_array):
		self.index_arrays.append(index_array)

	#Adds the given statment to the collection of statements
	def add_statement(self,statement):
		self.statements.append(statement)

	#---------- Main 'action' method ---------
	#This is the main interface that starts the whole code generation process
	#Given is a filled-in MapIR data structure
	#Code is generated based upon this data
	def codegen(self):
		#Step 0) Calculate the full iteration space based on the iteration spaces of the statements
		self.full_iter_space=iegen.util.full_iter_space(self.statements)

		print mapir_space.full_iter
	#-----------------------------------------

#---------------------------------

#---------- Symbolic class ----------
class Symbolic(object):
	__slots__=('_name')

	def __init__(self,name):
		self.m_name=name

iegen.util.define_properties(Symbolic,('name',))
#------------------------------------

#---------- DataSpace class ----------
class DataSpace(object):
	__slots__=('name','set','is_index_array')

	def __init__(self,name,set,is_index_array=False):
		self.name=name
		self.set=set
		self.is_index_array=is_index_array
#-------------------------------------

#---------- IndexArray class ----------
class IndexArray(object):
	__slots__=('data_space','is_permutation','input_bounds','output_bounds')

	def __init__(self,data_space,is_permutation,input_bounds,output_bounds):
		self.data_space=data_space
		self.is_permutation=is_permutation
		self.input_bounds=input_bounds
		self.output_bounds=output_bounds

		#Checking
		for input_bound in self.input_bounds:
			if input_bound.arity()!=self.data_space.set.arity():
				raise iegen.util.DimensionalityError("The dimensionality of all input bounds should match the dimensionality of index array's data space (%d).",self.data_space.set.arity())

		if 1!=self.output_bounds.arity():
			raise iegen.util.DimensionalityError('The dimensionality of the output bounds of the index array (%d) should be 1.'%self.output_bounds.arity_out())
#--------------------------------------

#---------- Statement class ----------
class Statement(object):
	__slots__=('statement','iter_space','scatter','access_relations')

	def __init__(self,statement,iter_space,scatter):
		self.statement=statement
		self.iter_space=iter_space
		self.scatter=scatter
		self.access_relations=[]

	def add_access_relation(self,access_relation):
		#Checking
		if self.iter_space.set.arity()!=access_relation.iter_to_data.arity_in():
			raise iegen.util.DimensionalityError('The input arity of the access relation (%d) should be the arity of the iteration space (%d).'%(access_relation.iter_to_data.arity_in(),self.iter_space.set.arity()))

		self.access_relations.append(access_relation)
#-------------------------------------

#---------- AccessRelation class ----------
class AccessRelation(object):
	__slots__=('name','data_space','iter_to_data')

	def __init__(self,name,data_space,iter_to_data):
		self.name=name
		self.data_space=data_space
		self.iter_to_data=iter_to_data

		if self.data_space.set.arity()!=self.iter_to_data.arity_out():
			raise iegen.util.DimensionalityError('The output arity of the access relation (%d) should be the arity of the data space (%d).'%(self.iter_to_data.arity_out(),self.data_space.set.arity()))
#------------------------------------------

#---------- IterationSpace class ----------
class IterationSpace(object):
	__slots__=('_name','_spec')

	def __init__(self,name,spec):
		self.m_name=name
		self.m_spec=spec

iegen.util.define_properties(IterationSpace,('name','spec'))
#------------------------------------------

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
