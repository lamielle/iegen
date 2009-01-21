from __future__ import with_statement
import os.path
from cStringIO import StringIO
from iegen.ast import Node
import iegen,iegen.util,iegen.codegen
from iegen.idg import IDG

#Store the directory where the iegen module is located
iegen.base_dir=os.path.dirname(os.path.abspath(iegen.__file__))

#---------- MapIR class ----------
class MapIR(object):
	__slots__=('symbolics','data_arrays','index_arrays','er_specs','statements','transformations','full_iter_space','idg')

	def __init__(self):
		self.symbolics={}
		self.data_arrays={}
		self.index_arrays={}
		self.er_specs={}
		self.statements={}
		self.transformations=[]
		self.idg=IDG()

	#---------- Symbolics ----------
	#Returns the symbolics that are present in the MapIR
	def get_symbolics(self): return self.symbolics.values()

	#Adds the given symbolic to the dictionary of symbolic variables
	def add_symbolic(self,symbolic):
		print "Adding symbolic '%s'"%symbolic.name
		self.symbolics[symbolic.name]=symbolic
	#-------------------------------

	#---------- Data Arrays ----------
	#Returns the data arrays that are present in the MapIR
	def get_data_arrays(self): return self.data_arrays.values()

	#Adds the given data array to the dictionary of data arrays
	def add_data_array(self,data_array):
		print "Adding data array '%s'"%data_array.name
		self.data_arrays[data_array.name]=data_array
	#---------------------------------

	#---------- ERSpecs ----------
	#Returns the ERSpecs that are present in the MapIR
	def get_er_specs(self): return self.er_specs.values()

	#Adds the given ERSpec to the collection of ERSpecs
	def add_er_spec(self,er_spec):
		print "Adding ERSpec '%s'"%er_spec.name
		self.er_specs[er_spec.name]=er_spec
	#-----------------------------

	#---------- Index Arrays ----------
	#Returns the index arrays that are present in the MapIR
	def get_index_arrays(self): return self.index_arrays.values()

	#Adds the given index array to the collection of index arrays
	def add_index_array(self,index_array):
		print "Adding index array '%s'"%index_array.name
		self.index_arrays[index_array.name]=index_array
		self.er_specs[index_array.name]=index_array
	#----------------------------------

	#---------- Statements ----------
	#Returns the statements that are present in the MapIR
	def get_statements(self): return self.statements.values()

	#Adds the given statement to the collection of statements
	def add_statement(self,statement):
		print "Adding statement '%s'"%statement.name
		self.statements[statement.name]=statement
	#--------------------------------

	#---------- Transformations ----------
	#Adds the given transformation to the sequence of transformations
	#Transformations are not stored as a dictionary as
	#the ordering is important
	def add_transformation(self,transformation):
		print "Adding transformation '%s'"%transformation.name
		self.transformations.append(transformation)
	#-------------------------------------

	#---------- Main 'action' method ---------
	#This is the main interface that starts the whole code generation process
	#Given is a filled-in MapIR data structure
	#Code is generated based upon this data
	def codegen(self,file_name=None):

		print "Running code generation..."

		#Create a string buffer to hold the code that is generated
		code=StringIO()

		#Run code generation
		iegen.codegen.codegen(self,code)

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

#---------- DataArray class ----------
class DataArray(object):
	__slots__=('name','bounds')

	def __init__(self,name,bounds):
		self.name=name
		self.bounds=bounds

	def __repr__(self):
		return 'DataArray(%s,%s)'%(self.name,self.bounds)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent
		return '''%sDataArray:
%s|-name: %s
%s|-bounds: %s'''%(spaces,spaces,self.name,spaces,self.bounds)
#-------------------------------------

#---------- ERSpec class ----------
class ERSpec(object):
	__slots__=('name','input_bounds','output_bounds','relation','_is_function','_is_permutation','is_inverse','created')

	def __init__(self,name,input_bounds,output_bounds,relation,is_function=False,is_permutation=False,is_inverse=False):
		self.name=name
		self.input_bounds=input_bounds
		self.output_bounds=output_bounds
		self.relation=relation
		self.is_function=is_function
		self.is_permutation=is_permutation
		self.is_inverse=is_inverse
		self.created=False

	def _get_is_function(self): return self._is_function
	def _set_is_function(self,is_function):
		if not is_function: self.is_permutation=False
		self._is_function=is_function
	is_function=property(_get_is_function,_set_is_function)

	def _get_is_permutation(self): return self._is_permutation
	def _set_is_permutation(self,is_permutation):
		if is_permutation: self.is_function=True
		self._is_permutation=is_permutation
	is_permutation=property(_get_is_permutation,_set_is_permutation)

	def __repr__(self):
		return 'ERSpec(%s,%s,%s,%s,%s,%s,%s,%s)'%(self.name,repr(self.input_bounds),repr(self.output_bounds),repr(self.relation),self.is_function,self.is_permutation,self.is_inverse,self.created)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent
		return '''%sERSpec:
%s|-name: %s
%s|-input_bounds: %s
%s|-output_bounds: %s
%s|-relation: %s
%s|-is_function: %s
%s|-permuatation: %s'''%(spaces,spaces,self.name,spaces,self.input_bounds,spaces,self.output_bounds,spaces,self.relation,spaces,self.is_function,spaces,self.is_permutation)

	#Returns all symbolics in each Set/Relation that this ERSpec contains
	def symbolics(self):
		return list(set(self.input_bounds.symbolics()+self.output_bounds.symbolics()+self.relation.symbolics()))

	#Returns the names of all functions in the constraints of each Set/Relation that this ERSpec contains
	def functions(self):
		return list(set(self.input_bounds.functions()+self.output_bounds.functions()+self.relation.functions()))
#----------------------------------

#---------- IndexArray class ----------
class IndexArray(ERSpec):

	def __init__(self,name,input_bounds,output_bounds):
		ERSpec.__init__(self,name,input_bounds,output_bounds,True,False)

		#Checking
		if 1!=self.output_bounds.arity():
			raise iegen.util.DimensionalityError('The dimensionality of the output bounds of the index array (%d) should be 1.'%self.output_bounds.arity_out())

	def __repr__(self):
		return 'IndexArray(%s,%s,%s,%s)'%(self,name,repr(self.input_bounds),repr(self.output_bounds),repr(self.relation))

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent
		return '''%sIndexArray:
%s|-name: %s
%s|-input_bounds: %s
%s|-output_bounds: %s
%s|-relation: %s'''%(spaces,spaces,self.name,spaces,self.input_bounds,spaces,self.output_bounds,spaces,self.relation)
#--------------------------------------

#---------- Statement class ----------
class Statement(object):
	__slots__=('name','text','iter_space','scatter','access_relations')

	def __init__(self,name,text,iter_space,scatter,access_relations=None):
		self.name=name
		self.text=text
		self.iter_space=iter_space
		self.scatter=scatter
		self.access_relations={} if None is access_relations else access_relations

		#Make sure the arity of the iteration space is the same as the input arity of the scattering funcion
		if self.iter_space.arity()!=self.scatter.arity_in():
			raise ValueError('Input arity of scattering function must be equal to arity of iteration space.')

	def __repr__(self):
		return 'Statement(%s,%s,%s,%s,%s)'%(self.name,self.text,self.iter_space,self.scatter,self.access_relations)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		from cStringIO import StringIO

		if indent>0: indent+=1
		spaces=' '*indent
		dashes='-'*indent
		ar_string=StringIO()
		for access_relation in self.get_access_relations():
			print >>ar_string,access_relation._get_string(indent+5)
		ar_string=ar_string.getvalue()
		return '''Statement:
%s|-name: %s
%s|-text: %s
%s|-iter_space: %s
%s|-scatter: %s
%s|-access_relations:
%s'''%(spaces,self.name,spaces,self.text,spaces,self.iter_space,spaces,self.scatter,spaces,ar_string)

	#---------- Access Relations ----------
	def get_access_relations(self): return self.access_relations.values()

	def add_access_relation(self,access_relation):
		#Checking
		if self.iter_space.arity()!=access_relation.iter_to_data.arity_in():
			raise iegen.util.DimensionalityError('The input arity of the access relation (%d) should be the arity of the iteration space (%d).'%(access_relation.iter_to_data.arity_in(),self.iter_space.arity()))

		self.access_relations[access_relation.name]=access_relation
	#--------------------------------------
#-------------------------------------

#---------- AccessRelation class ----------
class AccessRelation(object):
	__slots__=('name','data_array','iter_to_data','iter_space')

	def __init__(self,name,data_array,iter_to_data,iter_space=None):
		self.name=name
		self.data_array=data_array
		self.iter_to_data=iter_to_data
		self.iter_space=iter_space

		if self.data_array.bounds.arity()!=self.iter_to_data.arity_out():
			raise iegen.util.DimensionalityError('The output arity of the access relation (%d) should be the arity of the data space (%d).'%(self.iter_to_data.arity_out(),self.data_array.bounds.arity()))

	def __repr__(self):
		return 'AccessRelation(%s,%s,%s,%s)'%(self.name,self.data_array,self.iter_to_data,self.iter_space)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent
		return '''%sAccessRelation:
%s|-name: %s
%s|-data_array:
%s
%s|-iter_to_data: %s
%s|-iter_space: %s'''%(spaces,spaces,self.name,spaces,self.data_array._get_string(indent+13),spaces,self.iter_to_data,spaces,self.iter_space)
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
