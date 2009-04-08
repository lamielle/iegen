#Standard library imports
from __future__ import with_statement
import os.path

#IEGen imports
import iegen
from iegen import IEGenObject
from iegen.ast import Node
from iegen.util import like_type,DimensionalityError,define_properties

#Store the directory where the iegen module is located
iegen.base_dir=os.path.dirname(os.path.abspath(iegen.__file__))

#---------- Are we debugging? ----------
#Setup a property, iegen.debug, that determines if we are debugging
def _debug(): return iegen.IEGenObject.settings.debug
debug=property(_debug())
#---------------------------------------

#---------- Printing methods -----
def print_gen(type,output=None):
	for dest in IEGenObject.settings.outputs[type]:
		if dest is None:
			if output is None: print
			else: print output
		else:
			#Code is a special case as we don't want to append
			if 'code'==type:
				mode='w'
				print_progress("Writing generated code to file '%s'..."%(dest))
			else:
				mode='a'

			with file(dest,mode) as f:
				if output is None: print >>f
				else: print >>f,output

#Dynamically define printing methods based on output types
for type,short,default,quiet,verbose,help in IEGenObject.output_types:
	exec("def print_%s(output=None): print_gen('%s',output)"%(type,type))
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
		if like_type(other,Symbolic):
			return cmp(self.name,other.name)
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	def apply_visitor(self,visitor):
		visitor.visitSymbolic(self)
#------------------------------------

#---------- DataArray class ----------
class DataArray(IEGenObject):
	__slots__=('name','bounds')
	_set_fields=('bounds',)

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
class ERSpec(IEGenObject):
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
%s|-permutation: %s'''%(spaces,spaces,self.name,spaces,self.input_bounds,spaces,self.output_bounds,spaces,self.relation,spaces,self.is_function,spaces,self.is_permutation)

	#Returns all symbolics in each Set/Relation that this ERSpec contains
	def symbolics(self):
		return list(set(self.input_bounds.symbolics()+self.output_bounds.symbolics()+self.relation.symbolics()))

	#Returns the names of all functions in the constraints of each Set/Relation that this ERSpec contains
	def functions(self):
		return list(set(self.input_bounds.functions()+self.output_bounds.functions()+self.relation.functions()))
#----------------------------------

#---------- IndexArray class ----------
class IndexArray(ERSpec):
	_set_fields=('input_bounds','output_bounds')

	def __init__(self,name,input_bounds,output_bounds):
		from iegen import Relation
		ERSpec.__init__(self,name,input_bounds,output_bounds,Relation('{[]->[]}'),True,False)

		#Checking
		if 1!=self.output_bounds.arity():
			raise DimensionalityError('The dimensionality of the output bounds of the index array (%d) should be 1.'%self.output_bounds.arity_out())

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

#---------- ERGSpec class ----------
class ERGSpec(IEGenObject):
	__slots__=('name','erg_func_name','inputs','outputs')

	def __init__(self,name,erg_func_name,inputs,outputs):
		self.name=name
		self.erg_func_name=erg_func_name
		self.inputs=inputs
		self.outputs=outputs

	def __repr__(self):
		return 'ERGSpec(%s,%s,%s,%s)'%(self.name,self.erg_func_name,self.inputs,self.outputs)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		from cStringIO import StringIO

		if indent>0: indent+=1
		spaces=' '*indent

		#Calculate the string for the inputs
		inputs_string=StringIO()
		for input in self.inputs:
			print >>inputs_string,input._get_string(indent+8)
		inputs_string=inputs_string.getvalue()[:-1]

		#Calculate the string for the ouputs
		outputs_string=StringIO()
		for output in self.outputs:
			print >>outputs_string,output._get_string(indent+8)
		outputs_string=outputs_string.getvalue()[:-1]

		return '''%sERGSpec:
%s|-name: %s
%s|-erg_func_name: %s:
%s|-inputs:
%s
%s|-outputs:
%s'''%(spaces,spaces,self.name,spaces,self.erg_func_name,spaces,inputs_string,spaces,outputs_string)
#-----------------------------------

#---------- DataDependence class ----------
class DataDependence(IEGenObject):
	__slots__=('_iterspace','_dataspace','_data_dependence')

	def __init__(self,iterspace,dataspace,data_dependence):
		self.m_iterspace=iterspace
		self.m_dataspace=dataspace
		self.m_data_dependence=data_dependence

		#Checking
		#Can we check that given the iteration space, data spaces, and access functions, the given data dependence is valid?  Is it overly conservative?  optimistic?

define_properties(DataDependence,('iterspace','dataspace','data_dependence'))
#------------------------------------------

#---------- Inverse Simplification Rule ----------
#Runs the inverse simplification visitor on the given object
def inverse_simplify(mapir,obj):
	from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
	from iegen import Set,Relation,PresSet,PresRelation

	if iegen.debug: before=str(obj)

	#Gather the permutable functions from the MapIR
	permutations=[]
	for er_spec_name,er_spec in mapir.er_specs.items():
		if er_spec.is_permutation: permutations.append(er_spec_name)

	#Only apply this rule to Sets, Relations, PresSets, and PresRelations
	if like_type(obj,Set) or like_type(obj,Relation) or like_type(obj,PresSet) or like_type(obj,PresRelation):
		changed=RemoveFreeVarFunctionVisitor(permutations,'_inv').visit(obj).changed
	else:
		changed=False
	if changed and iegen.debug: iegen.print_debug('Simplify: removed free variable function: %s -> %s'%(before,obj))

	return changed
#-------------------------------------------------
