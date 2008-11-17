from __future__ import with_statement
import os.path
from cStringIO import StringIO
from iegen.ast import Node
import iegen,iegen.util,iegen.codegen

#Store the directory where the iegen module is located
iegen.base_dir=os.path.dirname(os.path.abspath(iegen.__file__))

#---------- MapIR class ----------
class MapIR(object):
	__slots__=('_symbolics','data_spaces','index_arrays','statements','full_iter_space','artt','mapir','sigma','ie_args')

	def __init__(self):
		self._symbolics={}
		self.data_spaces={}
		self.index_arrays=[]
		self.statements=[]
		self.full_iter_space=None

	#Adds the given symbolic to the dictionary of symbolic variables
	def add_symbolic(self,symbolic):
		self._symbolics[symbolic]=Symbolic(symbolic)

	#Returns a collection of instances of iegen.Symbolic
	def symbolics(self):
		return self._symbolics.values()

	#Adds the given index array to the collection of index arrays
	def add_index_array(self,index_array):
		self.index_arrays.append(index_array)

	#Adds the given statment to the collection of statements
	def add_statement(self,statement):
		self.statements.append(statement)

	#Generates a collection of pure data spaces (non-index-array data spaces)
	def pure_data_spaces(self):
		for data_space in self.data_spaces.values():
			if not data_space.is_index_array:
				yield data_space

	#---------- Main 'action' method ---------
	#This is the main interface that starts the whole code generation process
	#Given is a filled-in MapIR data structure
	#Code is generated based upon this data
	def codegen(self,data_reordering,iter_reordering,file_name=None):
		#Create a string buffer to hold the code that is generated
		code=StringIO()

		#Run code generation
		iegen.codegen.codegen(self,data_reordering,iter_reordering,code)

		#Write out the code to the given file if one was specified
		if file_name:
			print "Writing generated code to file '%s'..."%file_name
			with open(file_name,'w') as f:
				f.write(code.getvalue())

		#Return the generated code
		return code.getvalue()
	#-----------------------------------------

#---------------------------------

#---------- Symbolic class ----------
class Symbolic(Node):
	__slots__=('name',)

	def __init__(self,name):
		self.name=name

	def __repr__(self):
		#Use double quotes if this symbolic's name has a "'" in it
		if self.name.find("'")>=0:
			return 'Symbolic("%s")'%(self.name)
		else:
			return "Symbolic('%s')"%(self.name)

	def __str__(self):
		return self.name

	def __cmp__(self,other):
		if iegen.util.like_type(other,Symbolic):
			return cmp(self.name,other.name)
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	def apply_visitor(self,visitor):
		visitor.visitSymbolic(self)
#------------------------------------

#---------- DataSpace class ----------
class DataSpace(object):
	__slots__=('name','set','is_index_array')

	def __init__(self,name,set,is_index_array=False):
		self.name=name
		self.set=set
		self.is_index_array=is_index_array

	def __repr__(self):
		return 'DataSpace(%s,%s,%s)'%(self.name,self.set,self.is_index_array)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent
		return '''%sDataSpace:
%s|-name: %s
%s|-set: %s
%s|-is_index_array: %s'''%(spaces,spaces,self.name,spaces,self.set,spaces,self.is_index_array)
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
		if input_bounds.arity()!=self.data_space.set.arity():
			raise iegen.util.DimensionalityError("The dimensionality of all input bounds should match the dimensionality of index array's data space (%d).",self.data_space.set.arity())

		if 1!=self.output_bounds.arity():
			raise iegen.util.DimensionalityError('The dimensionality of the output bounds of the index array (%d) should be 1.'%self.output_bounds.arity_out())

	def _name(self):
		return self.data_space.name
	property(_name)

	def __repr__(self):
		return 'IndexArray(%s,%s,%s,%s)'%(repr(self.data_space),self.is_permutation,repr(self.input_bounds),repr(self.output_bounds))

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent
		return '''%sIndexArray
%s|-data_space:
%s
%s|-is_permutation: %s
%s|-input_bounds: %s
%s|-output_bounds: %s'''%(spaces,spaces,self.data_space._get_string(indent+5),spaces,self.is_permutation,spaces,self.input_bounds,spaces,self.output_bounds)
#--------------------------------------

#---------- Statement class ----------
class Statement(object):
	__slots__=('statement','iter_space','scatter','access_relations')

	def __init__(self,statement,iter_space,scatter,access_relations=None):
		self.statement=statement
		self.iter_space=iter_space
		self.scatter=scatter
		self.access_relations=[] if None is access_relations else access_relations

	def __repr__(self):
		return 'Statement(%s,%s,%s,%s)'%(self.statement,self.iter_space,self.scatter,self.access_relations)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		from cStringIO import StringIO

		if indent>0: indent+=1
		spaces=' '*indent
		dashes='-'*indent
		ar_string=StringIO()
		for access_relation in self.access_relations:
			print >>ar_string,access_relation._get_string(indent+5)
		ar_string=ar_string.getvalue()
		return '''Statement:
%s|-statement: %s
%s|-iter_space: %s
%s|-scatter: %s
%s|-access_relations:
%s'''%(spaces,self.statement,spaces,self.iter_space,spaces,self.scatter,spaces,ar_string)

	def add_access_relation(self,access_relation):
		#Checking
		if self.iter_space.arity()!=access_relation.iter_to_data.arity_in():
			raise iegen.util.DimensionalityError('The input arity of the access relation (%d) should be the arity of the iteration space (%d).'%(access_relation.iter_to_data.arity_in(),self.iter_space.arity()))

		self.access_relations.append(access_relation)
#-------------------------------------

#---------- AccessRelation class ----------
class AccessRelation(object):
	__slots__=('name','data_space','iter_to_data','iter_space')

	def __init__(self,name,data_space,iter_to_data,iter_space=None):
		self.name=name
		self.data_space=data_space
		self.iter_to_data=iter_to_data
		self.iter_space=iter_space

	def __repr__(self):
		return 'AccessRelation(%s,%s,%s,%s)'%(self.name,self.data_space,self.iter_to_data,self.iter_space)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent
		return '''%sAccessRelation:
%s|-name: %s
%s|-data_space:
%s
%s|-iter_to_data: %s
%s|-iter_space: %s'''%(spaces,spaces,self.name,spaces,self.data_space._get_string(indent+13),spaces,self.iter_to_data,spaces,self.iter_space)

		if self.data_space.set.arity()!=self.iter_to_data.arity_out():
			raise iegen.util.DimensionalityError('The output arity of the access relation (%d) should be the arity of the data space (%d).'%(self.iter_to_data.arity_out(),self.data_space.set.arity()))
#------------------------------------------

#---------- RTRT base class ----------
class RTRT(object):
	def __init__(self):
		raise NotImplementedException('RTRT is not an instantiable class.  One must create an instance of a sub class of RTRT')

	def calc_input(self):
		raise NotImplementedException('Subclasses of RTRT must implement calc_input')
	def calc_output(self):
		raise NotImplementedException('Subclasses of RTRT must implement calc_output')
	def calc_apply_reord(self):
		raise NotImplementedException('Subclasses of RTRT must implement calc_apply_reord')
	def calc_data_remaps(self):
		raise NotImplementedException('Subclasses of RTRT must implement calc_data_remaps')
#-------------------------------------

#---------- DataPermuteRTRT class ----------
class DataPermuteRTRT(RTRT):
	__slots__=('data_reordering','data_spaces','iter_sub_space_relation','target_data_space','iag_func_name')

	def __init__(self,data_reordering,data_spaces,iter_sub_space_relation,target_data_space,iag_func_name):
		self.data_reordering=data_reordering
		self.data_spaces=data_spaces
		self.iter_sub_space_relation=iter_sub_space_relation
		self.target_data_space=target_data_space
		self.iag_func_name=iag_func_name
#-------------------------------------------

#---------- IterPermuteRTRT class ----------
class IterPermuteRTRT(RTRT):
	__slots__=('iter_reordering','iter_space','access_relation','iter_sub_space_relation','iag_func_name','iag_type')

	def __init__(self,iter_reordering,iter_space,access_relation,iter_sub_space_relation,iag_func_name,iag_type):
		self.iter_reordering=iter_reordering
		self.iter_space=iter_space
		self.access_relation=access_relation
		self.iter_sub_space_relation=iter_sub_space_relation
		self.iag_func_name=iag_func_name
		self.iag_type=iag_type
#-------------------------------------------

#---------- Index Array Generator classes ----------
class IAGSpec(object):
	pass

class IAGPermute(IAGSpec):
	__slots__=('name','input','result')

	def __init__(self,name,input,result):
		self.name=name
		self.input=input
		self.result=result
#---------------------------------------------------

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
