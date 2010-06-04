#Standard library imports
from __future__ import with_statement
import os,os.path

#IEGen imports
import iegen
from iegen import IEGenObject
from iegen.ast import Node
from iegen.util import like_type,DimensionalityError,define_properties

#Store the directory where the iegen module is located
iegen.base_dir=os.path.dirname(os.path.abspath(iegen.__file__))

#---------- run_spec function ----------
#Function to run a given spec file
#The 'environment' for the spec file to run is setup before it is run
def run_spec(spec_file):
	#Import various packages and objects so they are available to spec files
	import iegen,iegen.trans,iegen.ito
	from iegen import Set,Relation,Symbolic

	#Get the current MapIR object
	spec=iegen.spec

	#Run the specified spec file
	with open(spec_file) as f:
		exec(f)
#---------------------------------------

#---------- include function ----------
#Includes the given spec file
#The path to this spec file should be relative to the dirname
# of the initial spec file given to IEGen
def include(spec_file):
	#Get the directory the original spec file is in
	dirname=os.path.dirname(os.path.abspath(iegen.settings.spec_file))

	#Calculate the name of the spec file to include
	spec_file=dirname+os.sep+spec_file

	#Run the spec file to include
	iegen.run_spec(spec_file)
#--------------------------------------

#---------- Symbolic class ----------
class Symbolic(Node):
	__slots__=('name','type','lower_bound','upper_bound')

	def __init__(self,name,type='int',lower_bound=None,upper_bound=None):
		self.name=name
		self.type=type
		self.lower_bound=lower_bound
		self.upper_bound=upper_bound

	def __repr__(self):
		#Use double quotes if this symbolic's name has a "'" in it
		if self.name.find("'")>=0 or self.type.find("'")>=0:
			return 'Symbolic("%s",type="%s",lower_bound=%s,upper_bound=%s)'%(self.name,self.type,self.lower_bound,self.upper_bound)
		else:
			return "Symbolic('%s',type='%s',lower_bound=%s,upper_bound=%s)"%(self.name,self.type,self.lower_bound,self.upper_bound)

	def __str__(self):
		return self.name

	def __cmp__(self,other):
		if like_type(other,Symbolic):
			return cmp(self.name,other.name)
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	def apply_visitor(self,visitor):
		visitor.visitSymbolic(self)

	def get_var_name(self):
		return self.name
#------------------------------------

#---------- DataArray class ----------
class DataArray(IEGenObject):
	__slots__=('name','type','elem_size','bounds','max_version')
	_set_fields=('bounds',)

	def __init__(self,name,type,elem_size,bounds):
		self.name=name
		self.type=type
		self.elem_size=elem_size
		self.bounds=bounds
		self.max_version=0

	def __repr__(self):
		return 'DataArray(%s,%s,%s,%s)'%(self.name,self.type,self.elem_size,self.bounds)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent
		return '''%sDataArray:
%s|-name: %s
%s|-bounds: %s'''%(spaces,spaces,self.name,spaces,self.bounds)
#-------------------------------------

#---------- VersionedDataArray ----------
class VersionedDataArray(IEGenObject):
	__slots__=('data_array','version')

	def __init__(self,data_array,version=None):
		self.data_array=data_array

		if version is not None:
			self.version=version
		else:
			self.version=self.data_array.max_version
			self.data_array.max_version+=1

	def _get_name(self): return self.data_array.name+'_'+str(self.version)
	name=property(_get_name)
#----------------------------------------

#---------- ERSpec class ----------
class ERSpec(IEGenObject):
	__slots__=('name','input_bounds','output_bounds','relation','_is_function','_is_permutation','is_inverse','inverse_of')

	def __init__(self,name,input_bounds,output_bounds,relation,is_function=False,is_permutation=False,is_inverse=False,inverse_of=None):
		self.name=name
		self.input_bounds=input_bounds
		self.output_bounds=output_bounds
		self.relation=relation
		self.is_function=is_function
		self.is_permutation=is_permutation
		self.is_inverse=is_inverse
		self.inverse_of=inverse_of

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
		return 'ERSpec(%s,%s,%s,%s,%s,%s,%s,%s)'%(self.name,repr(self.input_bounds),repr(self.output_bounds),repr(self.relation),self.is_function,self.is_permutation,self.is_inverse,self.inverse_of)

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
%s|-permutation: %s
%s|-is_inverse: %s
%s|-inverse_of: %s'''%(spaces,spaces,self.name,spaces,self.input_bounds,spaces,self.output_bounds,spaces,self.relation,spaces,self.is_function,spaces,self.is_permutation,spaces,self.is_inverse,spaces,self.inverse_of)

	#Returns all symbolics in each Set/Relation that this ERSpec contains
	def symbolics(self):
		return list(set(self.input_bounds.symbolic_names+self.output_bounds.symbolic_names+self.relation.symbolic_names))

	#Returns the names of all functions in the constraints of each Set/Relation that this ERSpec contains
	def functions(self):
		return list(set(self.input_bounds.function_names+self.output_bounds.function_names+self.relation.function_names))

	#EF_1D
	#- if in and out arity are both 1D.
	#- if ERSpec is a function.
	#- If only has one conjunction.
	def is_ef_1d(self):
		return (1,1)==self.relation.arity() and self.is_function and len(self.relation)==1

	#ER_U1D
	#- if in and out arity are both 1D.
	#- Each conjunction is a function.  (TODO: have a flag for this in Relation object)  More specifically, when doing code gen each conjunction should have an EF_1D associated with it.
	def is_union_1d(self):
		#return (1,1)==self.relation.arity() and self.is_function
		#TODO: add flag for individual relations being functions
		return (1,1)==self.relation.arity()

	#EF_2D
	#- if in and out arity are both less than or equal to 2.
	#- if ERSpec is a function.
	#- example: theta
	def is_ef_2d(self):
		return self.relation.arity_in()<=2 and self.relation.arity_out()<=2 and self.is_function

	#ER_1DCOO
	#- if in and out arity are both 1D.
	#- Do not have each conjunction as a function.
	#- Could be multiple conjunctions.q
	#TODO: Add support for this ER type

	#Returns the variable type string for this ERSpec
	def get_type(self):
		if self.is_ef_1d():
			return 'EF_1D *'
		elif self.is_union_1d():
			return 'ER_U1D *'
		elif self.is_ef_2d():
			return 'EF_2D *'
		else:
			raise ValueError('Unknown ERSpec type')

	#Returns the parameter type string for this ERSpec
	def get_param_type(self):
		if self.is_ef_1d():
			return 'EF_1D **'
		elif self.is_union_1d():
			return 'ER_U1D **'
		elif self.is_ef_2d():
			return 'EF_2D **'
		else:
			raise ValueError('Unknown ERSpec type')

	#Returns the name of the getter function
	def get_getter_str(self):
		if self.is_ef_1d():
			return 'EF_1D_get'
		elif self.is_union_1d():
			return 'ER_U1D_get'
		elif self.is_ef_2d():
			return 'EF_2D_get'
		else:
			raise ValueError('Unknown ERSpec type')

	#Returns the name of the ctor
	def get_ctor_str(self):
		if self.is_ef_1d():
			return 'EF_1D_ctor'
		elif self.is_union_1d():
			return 'ER_U1D_ctor'
		elif self.is_ef_2d():
			return 'EF_2D_ctor'
		else:
			raise ValueError('Unknown ERSpec type')

	#Returns the name of the genInverse routine
	def get_genInverse_str(self):
		if self.is_ef_1d():
			return 'EF_1D_genInverse'
		elif self.is_union_1d():
			return 'ER_U1D_genInverse'
		elif self.is_ef_2d():
			return 'EF_2D_genInverse'
		else:
			raise ValueError('Unknown ERSpec type')

	#Returns the name of the setter function
	def get_setter_str(self):
		if self.is_ef_1d():
			return 'EF_1D_set'
		elif self.is_union_1d():
			return 'ER_U1D_set'
		elif self.is_ef_2d():
			return 'EF_2D_set'
		else:
			raise ValueError('Unknown ERSpec type')

	#Returns the variable name for this ERSpec
	def get_var_name(self):
		if self.is_ef_1d():
			return self.name+'_EF_1D'
		elif self.is_union_1d():
			return self.name+'_ER_U1D'
		elif self.is_ef_2d():
			return self.name+'_EF_2D'
		else:
			raise ValueError('Unknown ERSpec type: %s %s'%(self.name,self.relation))

	#Returns the parameter name for this ERSpec
	def get_param_name(self):
		return self.name
#----------------------------------

#---------- IndexArray class ----------
class IndexArray(ERSpec):
	__slots__=('type',)
	_set_fields=('input_bounds','output_bounds')

	def __init__(self,name,type,input_bounds,output_bounds):
		from iegen import Relation
		ERSpec.__init__(self,name,input_bounds,output_bounds,Relation('{[]->[]}'),True,False)

		self.type=type

		#Checking
		if 1!=self.output_bounds.arity():
			raise DimensionalityError('The dimensionality of the output bounds of the index array (%d) should be 1.'%self.output_bounds.arity_out())

	def __repr__(self):
		return 'IndexArray(%s,%s,%s,%s)'%(self.name,repr(self.input_bounds),repr(self.output_bounds),repr(self.relation))

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

	#Returns the variable type string for this index array
	def get_type(self):
		return 'EF_1D *'

	#Returns the name of the getter function
	def get_getter_str(self):
		return 'EF_1D_get'

	#Returns the name of the setter function
	def get_setter_str(self):
		return 'EF_1D_set'

	#Returns the name of the ctor
	def get_ctor_str(self):
		return 'EF_1D_ctor'

	#Returns the variable name for this index array
	def get_var_name(self):
		return self.name+'_EF_1D'

	#Returns the parameter name for this index array
	def get_param_name(self):
		return self.name
#--------------------------------------

#---------- Statement class ----------
class Statement(IEGenObject):
	__slots__=('name','text','iter_space','scatter','access_relations')
	_set_fields=('iter_space',)
	_relation_fields=('scatter',)

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
		ar_string=StringIO()
		for access_relation in self.get_access_relations():
			print >>ar_string,access_relation._get_string(indent+5)
		ar_string=ar_string.getvalue()[:-1]
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
			raise DimensionalityError('The input arity of the access relation (%d) should be the arity of the iteration space (%d).'%(access_relation.iter_to_data.arity_in(),self.iter_space.arity()))

		self.access_relations[access_relation.name]=access_relation
	#--------------------------------------
#-------------------------------------

#---------- AccessRelation class ----------
class AccessRelation(IEGenObject):
	__slots__=('name','data_array','iter_to_data')
	_relation_fields=('iter_to_data',)
	_data_array_fields=('data_array',)

	def __init__(self,name,data_array,iter_to_data):
		self.name=name
		self.data_array=data_array
		self.iter_to_data=iter_to_data

		if self.data_array.bounds.arity()!=self.iter_to_data.arity_out():
			raise DimensionalityError('The output arity of the access relation (%d) should be the arity of the data space (%d).'%(self.iter_to_data.arity_out(),self.data_array.bounds.arity()))

	def __repr__(self):
		return 'AccessRelation(%s,%s,%s)'%(self.name,self.data_array,self.iter_to_data)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent
		return '''%sAccessRelation:
%s|-name: %s
%s|-data_array:
%s
%s|-iter_to_data: %s'''%(spaces,spaces,self.name,spaces,self.data_array._get_string(indent+13),spaces,self.iter_to_data)
#------------------------------------------

#---------- DataDependence class ----------
class DataDependence(IEGenObject):
	__slots__=('name','dep_rel')
	_relation_fields=('dep_rel',)

	def __init__(self,name,dep_rel):
		self.name=name
		self.dep_rel=dep_rel

	def __repr__(self):
		return 'DataDependence(%s,%s)'%(self.name,self.dep_rel)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent
		return '''%sDataDependence:
%s|-name: %s
%s|-dep_rel: %s'''%(spaces,spaces,self.name,spaces,self.dep_rel)

	#Returns all symbolics in this data dependence
	def symbolics(self):
		return list(set(self.dep_rel.symbolic_names))

	#Returns the names of all functions in this data dependence
	def functions(self):
		return list(set(self.dep_rel.function_names))

	def get_var_name(self):
		return self.name+'_ED'
#------------------------------------------

#---------- Function Call class ----------
class FunctionCallSpec(IEGenObject):
	__slots__=('name','function_name','arguments')

	def __init__(self,name,function_name,arguments):
		self.name=name
		self.function_name=function_name
		self.arguments=arguments
#-----------------------------------------
