from copy import deepcopy
from cStringIO import StringIO
from iegen.rtrt import RTRT
from iegen import ERSpec

#---------- DataPermuteRTRT class ----------
class DataPermuteRTRT(RTRT):
	__slots__=('data_reordering','data_arrays','iter_sub_space_relation','target_data_array','iag_func_name')

	def __init__(self,name,data_reordering,data_arrays,iter_sub_space_relation,target_data_array,iag_func_name):
		RTRT.__init__(self,name)
		self.data_reordering=data_reordering
		self.data_arrays=data_arrays
		self.iter_sub_space_relation=iter_sub_space_relation
		self.target_data_array=target_data_array
		self.iag_func_name=iag_func_name

	def __repr__(self):
		return 'DataPermuteRTRT(%s,%s,%s,%s,%s)'%(self.data_reordering,self.data_arrays,self.iter_sub_space_relation,self.target_data_array,self.iag_func_name)

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

		itos_string=StringIO()
		if len(self.itos)>0:
			print >>itos_string
			for ito in self.itos:
				print >>itos_string,ito._get_string(indent+5)
		itos_string=itos_string.getvalue()[:-1]

		return '''%sDataPermuteRTRT:
%s|-inputs: %s
%s|-outputs: %s
%s|-simplifications: %s
%s|-itos: %s
%s|-symbolic_inputs: %s
%s|-data_reordering: %s
%s|-data_arrays: %s
%s|-iter_sub_space_relation: %s
%s|-target_data_array: %s
%s|-iag_func_name: %s'''%(spaces,spaces,inputs_string,spaces,outputs_string,spaces,simplifications_string,spaces,itos_string,spaces,self.symbolic_inputs,spaces,self.data_reordering,spaces,self.data_arrays,spaces,self.iter_sub_space_relation,spaces,self.target_data_array,spaces,self.iag_func_name)

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
			if not iter_to_data:
				iter_to_data=issr.compose(stmt.scatter.compose(stmt.get_access_relations()[0].iter_to_data.inverse())).inverse()
			else:
				iter_to_data=iter_to_data.union(issr.compose(stmt.scatter.compose(stmt.get_access_relations()[0].iter_to_data.inverse())).inverse())

			for ar in stmt.get_access_relations()[1:]:
				iter_to_data=iter_to_data.union(issr.compose(stmt.scatter.compose(ar.iter_to_data.inverse())).inverse())

		#Create the ERSpec for the relation that is input to the reordering
		self.inputs.append(ERSpec(
		    name='%s_input'%(self.name),
		    input_bounds=mapir.full_iter_space.apply(self.iter_sub_space_relation),
		    output_bounds=deepcopy(self.target_data_array.bounds),
		    relation=iter_to_data))

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
		#-relation: data reordering relation that was specified
		#-it is a permutation
		self.outputs.append(ERSpec(
		    name='%s_output'%(self.name),
		    input_bounds=deepcopy(self.target_data_array.bounds),
		    output_bounds=deepcopy(self.target_data_array.bounds),
		    relation=deepcopy(self.data_reordering),
		    is_permutation=True))

	#Update the mapir based on this transformation
	def calc_apply(self,mapir):
		#Data spaces are not changed
		#Scattering functions are not changed

		#Update the access relations of all statements
		for statement in mapir.get_statements():
			for access_relation in statement.get_access_relations():
				access_relation.iter_to_data=self.data_reordering.compose(access_relation.iter_to_data)

	def calc_data_remaps(self):
		pass
#-------------------------------------------
