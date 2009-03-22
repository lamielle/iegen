from __future__ import with_statement

#Standard library imports
from cStringIO import StringIO

#IEGen imports
import iegen.codegen
from iegen import Symbolic,DataArray,IndexArray,Statement,AccessRelation,Set,Relation
from iegen.idg import IDG

#---------- MapIR class ----------
class MapIR(object):
	__slots__=('symbolics','data_arrays','er_specs','index_arrays','statements','transformations','erg_specs','full_iter_space','idg')

	def __init__(self):
		self.symbolics={}
		self.data_arrays={}
		self.index_arrays={}
		self.er_specs={}
		self.statements={}
		self.transformations=[]
		self.erg_specs={}
		self.idg=IDG()

	#---------- Symbolics ----------
	#Returns the symbolics that are present in the MapIR
	def get_symbolics(self): return self.symbolics.values()

	#Adds a symbolic constructed from the given arguments to the MapIR
	def add_symbolic(self,**kwargs):
		print "Adding symbolic '%s'"%kwargs['name']
		self._convert_create_add(Symbolic,[self.symbolics],**kwargs)
	#-------------------------------

	#---------- Data Arrays ----------
	#Returns the data arrays that are present in the MapIR
	def get_data_arrays(self): return self.data_arrays.values()

	#Adds a data array constructed from the given arguments to the MapIR
	def add_data_array(self,**kwargs):
		print "Adding data array '%s'"%kwargs['name']
		self._convert_create_add(DataArray,[self.data_arrays],**kwargs)
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

	#Adds a index array constructed from the given arguments to the MapIR
	def add_index_array(self,**kwargs):
		print "Adding index array '%s'"%kwargs['name']
		self._convert_create_add(IndexArray,[self.index_arrays,self.er_specs],**kwargs)
	#----------------------------------

	#---------- Statements ----------
	#Returns the statements that are present in the MapIR
	def get_statements(self): return self.statements.values()

	#Adds a statement constructed from the given arguments to the MapIR
	def add_statement(self,**kwargs):
		print "Adding statement '%s'"%kwargs['name']
		self._convert_create_add(Statement,[self.statements],**kwargs)
	#--------------------------------

	#---------- Access Relations ----------
	def get_access_relations(self,statement_name): return self.statements[statement_name].get_access_relations()

	#Adds an access relation to the named statement constructed from the given arguments to the MapIR
	def add_access_relation(self,statement_name,**kwargs):
		print "Adding access relation '%s'"%kwargs['name']

		#Create the access relation
		access_relation=self._convert_create_add(AccessRelation,**kwargs)

		#Add the access relation to the specified statement
		self.statements[statement_name].add_access_relation(access_relation)
	#--------------------------------------

	#---------- Transformations ----------
	#Adds a transformation of the given and constructed from the given arguments to the MapIR
	#Transformations are not stored as a dictionary as
	#the ordering is meaningful (they will be applied in the order the are added)
	def add_transformation(self,type,**kwargs):
		print "Adding transformation '%s'"%kwargs['name']

		#Create the transformation
		transformation=self._convert_create_add(type,**kwargs)

		#Add the transformation to the list of transformations
		self.transformations.append(transformation)
	#-------------------------------------

	#---------- ERGSpecs ----------
	#Returns the ERGSpecs that are present in the MapIR
	def get_erg_specs(self): return self.erg_specs.values()

	#Adds the given ERGSpec to the collection of ERGSpecs
	def add_erg_spec(self,erg_spec):
		print "Adding ERGSpec '%s'"%(erg_spec.name)
		self.erg_specs[erg_spec.name]=erg_spec
	#------------------------------

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
	#---------------------------------------

	#---------- Utility methods ----------
	#Creates an object and adds it to each of the given dictionaries
	#This method does three things:
	#-Creates Sets/Relations for certain fields in kwargs
	#-Creates an object using the given class and arguments
	#-Adds the object to the given dictionaries, if any are given
	#In case it is needed, the created object is returned
	def _convert_create_add(self,CreateClass,add_dicts=None,**kwargs):
		#Convert all set/relation strings to Sets/Relations
		self._generic_convert(CreateClass,kwargs)

		#Create the object using the modified kwargs and the given class
		obj=self._generic_create(CreateClass,**kwargs)

		#Add the created object to the add_dicts
		if add_dicts: self._generic_add(obj,add_dicts)

		return obj

	#Convert all elements in kwargs named in CreateClass._{set,relation}_fields to a Set or Relation
	def _generic_convert(self,CreateClass,kwargs):
		#Convert all set_fields into Sets
		try:
			self._create_sets(CreateClass._set_fields,kwargs)
		except AttributeError,e: pass

		#Convert all relation_fields into Relations
		try:
			self._create_relations(CreateClass._relation_fields,kwargs)
		except AttributeError,e: pass

		#Convert all data_array_fields into DataArrays
		try:
			self._convert_data_arrays(CreateClass._data_array_fields,kwargs)
		except AttributeError,e: pass

		#Convert all data_arrays_fields into collections of DataArrays
		try:
			self._convert_data_arrays_collection(CreateClass._data_arrays_fields,kwargs)
		except AttributeError,e: pass

	#Add the given object to the given dicts based on the objects 'name' field
	def _generic_add(self,obj,add_dicts):
		for add_dict in add_dicts:
			add_dict[obj.name]=obj

	#Return the result of creating an object using the given class and constructor arguments
	def _generic_create(self,CreateClass,**kwargs):
		return CreateClass(**kwargs)

	#Converts dict entries named in set_fields into Set objects
	def _create_sets(self,set_fields,dict):
		#Convert any fields named in set_fields from set strings to Set objects
		for field_name in set_fields:
			dict[field_name]=self._create_set(dict[field_name])

	#Creates a Set from the given set string and passing in the current symbolics
	def _create_set(self,set_string):
		return Set(set_string,self.get_symbolics())

	#Converts dict entries named in relation_fields into Relation objects
	def _create_relations(self,relation_fields,dict):
		#Convert any fields named in relation_fields from relation strings to Relation objects
		for field_name in relation_fields:
			dict[field_name]=self._create_relation(dict[field_name])

	#Creates a Relation from the given relation string and passing in the current symbolics
	def _create_relation(self,rel_string):
		return Relation(rel_string,self.get_symbolics())

	#Converts dict entries named in data_array_fields into existing DataArray objects in the MapIR
	#If a data array with the name found in the dict is not in the MapIR, a NameError is raised
	def _convert_data_arrays(self,data_array_fields,dict):
		#Convert any fields named in data_array_fields from strings to data arrays from the MapIR
		for field_name in data_array_fields:
			try:
				dict[field_name]=self.data_arrays[dict[field_name]]
			except KeyError,e:
				raise NameError("Data array '%s' does not exist in the MapIR"%(dict[field_name]))

	#Converts dict entries named in data_arrays_fields into collections of existing DataArray objects in the MapIR
	#If a data array with the name found in the dict is not in the MapIR, a NameError is raised
	def _convert_data_arrays_collection(self,data_arrays_fields,dict):
		#Convert any fields named in data_arrays_fields from collections of strings to collections of data arrays from the MapIR
		for field_name in data_arrays_fields:
			#Convert each string in the collection to an existing DataArray
			for pos in xrange(len(dict[field_name])):
				try:
					dict[field_name][pos]=self.data_arrays[dict[field_name][pos]]
				except KeyError,e:
					raise NameError("Data array '%s' does not exist in the MapIR"%(dict[field_name][pos]))
	#-------------------------------------
#---------------------------------
