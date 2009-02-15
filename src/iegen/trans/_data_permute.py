from copy import deepcopy
from cStringIO import StringIO
from iegen.trans import Transformation
from iegen import ERSpec,Relation

#---------- DataPermuteTrans class ----------
class DataPermuteTrans(Transformation):
	__slots__=('reordering_name','_data_reordering','data_arrays','iter_sub_space_relation','target_data_array','erg_func_name')

	def __init__(self,name,reordering_name,data_arrays,iter_sub_space_relation,target_data_array,erg_func_name):
		Transformation.__init__(self,name)
		self.reordering_name=reordering_name
		self.data_arrays=data_arrays
		self.iter_sub_space_relation=iter_sub_space_relation
		self.target_data_array=target_data_array
		self.erg_func_name=erg_func_name

		#Calculate the data reordering relation
		self._data_reordering=Relation('{[%s_in]->[%s_out]: %s_out=%s(%s_in)}'%(5*(self.reordering_name,)))

	def __repr__(self):
		return 'DataPermuteTrans(%s,%s,%s,%s,%s)'%(self.data_reordering,self.data_arrays,self.iter_sub_space_relation,self.target_data_array,self.erg_func_name)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent

		inputs_string=StringIO()
		if len(self.inputs)>0:
			print >>inputs_string
			for input in self.inputs:
				print >>inputs_string,input._get_string(indent+5)
		inputs_string=inputs_string.getvalue()[:-1]

		outputs_string=StringIO()
		if len(self.outputs)>0:
			print >>outputs_string
			for output in self.outputs:
				print >>outputs_string,output._get_string(indent+5)
		outputs_string=outputs_string.getvalue()[:-1]

		simplifications_string=StringIO()
		if len(self.simplifications)>0:
			print >>simplifications_string
			for simplification in self.simplifications:
				print >>simplifications_string,simplification._get_string(indent+5)
		simplifications_string=simplifications_string.getvalue()[:-1]

		return '''%sDataPermuteTrans:
%s|-name: %s
%s|-inputs: %s
%s|-outputs: %s
%s|-simplifications: %s
%s|-symbolic_inputs: %s
%s|-reordering_name: %s
%s|-_data_reordering: %s
%s|-data_arrays: %s
%s|-iter_sub_space_relation: %s
%s|-target_data_array: %s
%s|-erg_func_name: %s'''%(spaces,spaces,self.name,spaces,inputs_string,spaces,outputs_string,spaces,simplifications_string,spaces,self.symbolic_inputs,spaces,self.reordering_name,spaces,self._data_reordering,spaces,self.data_arrays,spaces,self.iter_sub_space_relation,spaces,self.target_data_array,spaces,self.erg_func_name)

	#Calculate a specification for the explicit relation that is input to
	# the data reordering algorithm.
	#This input is a relation from the iteration sub space to the
	# the target data space.
	def calc_input(self,mapir):
		#Iteration Sub Space Relation
		issr=self.iter_sub_space_relation

		#Calculate the iteration space to data space relation
		iter_to_data=None
		for stmt in mapir.get_statements():
			for ar in stmt.get_access_relations():
				if not iter_to_data:
					iter_to_data=issr.compose(stmt.scatter.compose(ar.iter_to_data.inverse())).inverse()
				else:
					iter_to_data=iter_to_data.union(issr.compose(stmt.scatter.compose(ar.iter_to_data.inverse())).inverse())

		#Create the ERSpec for the relation that is input to the reordering
		self.inputs.append(ERSpec(
		    name='%s_input'%(self.name),
		    input_bounds=mapir.full_iter_space.apply(self.iter_sub_space_relation),
		    output_bounds=deepcopy(self.target_data_array.bounds),
		    relation=iter_to_data))

		#Add the ERSpec to the MapIR
		mapir.add_er_spec(self.inputs[0])

	#Calculate a specification for the explicit relation that is the
	# output of this data reordering.
	#This relation is a permutation of the original data space, permuted
	# based on the heuristics of the reordering algorithm.
	def calc_output(self,mapir):

		#Need to create a static description of the output of the reordering
		#What does this look like:
		#It will be an ERSpec:
		#-name: %s_output
		#-input_bounds: deepcopy(self.target_data_array)
		#-output_bounds: deepcopy(self.target_data_array)
		#-relation: data reordering relation that was calculated
		#-it is a permutation
		self.outputs.append(ERSpec(
		    name=self.reordering_name,
		    input_bounds=deepcopy(self.target_data_array.bounds),
		    output_bounds=deepcopy(self.target_data_array.bounds),
		    relation=deepcopy(self._data_reordering),
		    is_permutation=True))

		#Add the ERSpec to the MapIR
		mapir.add_er_spec(self.outputs[0])

	#Update the MapIR based on this transformation
	def update_mapir(self,mapir):
		from iegen import ERGSpec
		#Data spaces are not changed
		#Scattering functions are not changed

		#Update the access relations of all statements
		for statement in mapir.get_statements():
			for access_relation in statement.get_access_relations():
				access_relation.iter_to_data=self._data_reordering.compose(access_relation.iter_to_data)

		#Add the ERGSpec for this transformation to the MapIR
		mapir.add_erg_spec(ERGSpec(self._get_erg_spec_name(),self.erg_func_name,self.inputs,self.outputs))

	#Update the idg based on this transformation
	def update_idg(self,mapir):
		#Add the ERG call node to the IDG
		call_node=mapir.idg.get_call_node(mapir.erg_specs[self._get_erg_spec_name()])

		#Add the input ERSpecs to the IDG
		for input_er_spec in self.inputs:
			#Get a node for the ERSpec
			input_er_spec_node=mapir.idg.get_er_spec_node(input_er_spec)

			#Add dependence of the call to the input
			call_node.add_dep(input_er_spec_node)

			#Add any dependences that this ERSpec has
			self.add_er_spec_deps(input_er_spec,mapir)

		#Add the output ERSpecs to the IDG
		for output_er_spec in self.outputs:
			#Get a node for the ERSpec
			output_er_spec_node=mapir.idg.get_output_er_spec_node(output_er_spec)

			#Add dependence of the output on the call
			output_er_spec_node.add_dep(call_node)

			#Add any dependences that this ERSpec has
			self.add_er_spec_deps(output_er_spec,mapir)

	#Adds any dependences the given ERSpec has to the IDG
	def add_er_spec_deps(self,er_spec,mapir):
		#Get the IDG node for the given ERSpec
		er_spec_node=mapir.idg.get_er_spec_node(er_spec)

		#Gather symbolic dependences
		for symbolic in er_spec.symbolics():
			symbolic_node=mapir.idg.get_symbolic_node(mapir.symbolics[symbolic])
			er_spec_node.add_dep(symbolic_node)

		#Gather other ERSpec dependences
		for function in er_spec.functions():
			#Die if the function is referenced but no associated ERSpec exists in the MapIR
			if function not in mapir.er_specs:
				raise ValueError("Function '%s' referenced but no associated ERSpec exists"%function)

			#Ignore self references
			if function!=er_spec.name:
				#Get the IDG node for the ERSpec that represents this function
				#Check if the function is an index array
				if function in mapir.index_arrays:
					dep_node=mapir.idg.get_index_array_node(mapir.index_arrays[function])
				else:
					dep_node=mapir.idg.get_er_spec_node(mapir.er_specs[function])

				#Setup the dependence relationship
				er_spec_node.add_dep(dep_node)

				#Recursively add dependences for the dependence node
				self.add_er_spec_deps(dep_node.data,mapir)

	def _get_erg_spec_name(self):
		return self.name+'_'+self.erg_func_name
#-------------------------------------------
