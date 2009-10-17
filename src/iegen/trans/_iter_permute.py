from cStringIO import StringIO
from iegen.trans import Transformation
from iegen import Relation,ERSpec
from iegen.idg import IDGCall,IDGOutputERSpec,IDGERSpec,IDGGenERSpec
from iegen.codegen import calc_erg_call

#---------- IterPermuteTrans class ----------
class IterPermuteTrans(Transformation):
	__slots__=('reordering_name','iter_sub_space_relation','target_data_arrays','erg_func_name','iter_space_trans','_data_reordering')

	_relation_fields=('iter_sub_space_relation',)
	_data_arrays_fields=('target_data_arrays',)

	def __init__(self,name,reordering_name,iter_sub_space_relation,target_data_arrays,erg_func_name,iter_space_trans):
		Transformation.__init__(self,name)
		self.reordering_name=reordering_name
		self.iter_sub_space_relation=iter_sub_space_relation
		self.target_data_arrays=target_data_arrays
		self.erg_func_name=erg_func_name
		self.iter_space_trans=iter_space_trans

		#Calculate the data reordering relation
		self._data_reordering=Relation('{[%s_in]->[%s_out]: %s_out=%s(%s_in)}'%(5*(self.reordering_name,)))

		#Make sure the target data arrays all have the same bounds
		#We do this by unioning all bounds and simply checking that there is a single conjunction in the disjunction
		target_bounds=[data_array.bounds for data_array in self.target_data_arrays]
		unioned_bounds=reduce(lambda da1,da2: da1.union(da2),target_bounds)
		if len(unioned_bounds.sets)!=1:
			raise ValueError('All target data arrays must have the same bounds')

	def __repr__(self):
		return 'IterPermuteTrans(%s,%s,%s,%s,%s)'%(self.reordering_name,self.iter_sub_space_relation,self.target_data_arrays,self.erg_func_name,self.iter_space_trans)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent

		inputs_string=StringIO()
		if len(self.inputs)>0:
			for input in self.inputs:
				print >>inputs_string,input._get_string(indent+5)
		inputs_string=inputs_string.getvalue()[:-1]
		if len(inputs_string)>0: inputs_string='\n'+inputs_string

		outputs_string=StringIO()
		if len(self.outputs)>0:
			for output in self.outputs:
				print >>outputs_string,output._get_string(indent+5)
		outputs_string=outputs_string.getvalue()[:-1]
		if len(outputs_string)>0: outputs_string='\n'+outputs_string

		target_data_arrays_string=StringIO()
		if len(self.target_data_arrays)>0:
			for data_array in self.target_data_arrays:
				print >>target_data_arrays_string,data_array._get_string(indent+13)
		target_data_arrays_string=target_data_arrays_string.getvalue()[:-1]
		if len(target_data_arrays_string)>0: target_data_arrays_string='\n'+target_data_arrays_string

		return '''%sIterPermuteTrans:
%s|-name: %s
%s|-reordering_name: %s
%s|-iter_sub_space_relation: %s
%s|-inputs: %s
%s|-outputs: %s
%s|-target_data_arrays:
%s
%s|-erg_func_name: %s
%s|-iter_space_trans: %s
%s|-_data_reordering: %s'''%(spaces,spaces,self.name,
    spaces,self.reordering_name,
    spaces,self.iter_sub_space_relation,
    spaces,inputs_string,
    spaces,outputs_string,
    spaces,target_data_arrays_string,
    spaces,self.erg_func_name,
    spaces,self.iter_space_trans,
    spaces,self._data_reordering)

	#Calculate a specification for the explicit relation that is input to
	# the data reordering algorithm.
	#This input is a relation from the iteration sub space to the
	# the target data space.
	#It is a relation of how the the loop to be permuted accesses the
	# target data arrays.
	def calc_input(self,mapir):
		#Iteration Sub Space Relation
		issr=self.iter_sub_space_relation

		#Calculate the full iteration space to data space relation #Collect all iter_to_data relations in all access relations
		self.print_detail("Filtering access relations...")
		access_relations=[ar.iter_to_data for stmt in mapir.get_statements() for ar in stmt.get_access_relations() if set()!=set([ar.data_array]).intersection(set(self.target_data_arrays))]

		#Union all the relations that were collected into a single relation
		self.print_detail("Unioning access relations...")
		iter_to_data=reduce(lambda form1,form2: form1.union(form2),access_relations)

		#Compose the unioned access relation with the iteration subspace
		# relation to remove conjunctions we are not interested in
		self.print_detail("Calculating final iteration to data relation...")
		iter_to_data=self.iter_sub_space_relation.compose(iter_to_data.inverse()).inverse()

		#Create the ERSpec for the relation that is input to the reordering
		self.inputs.append(ERSpec(
		    name='%s_input'%(self.name),
		    input_bounds=mapir.full_iter_space.apply(self.iter_sub_space_relation),
		    output_bounds=self.target_data_arrays[0].bounds.copy(),
		    relation=iter_to_data))

		#Add the ERSpec to the MapIR
		mapir.add_er_spec(self.inputs[0])

		self.print_progress("Calculated input ERSpec '%s' for transformation '%s'..."%(self.inputs[0].name,self.name))

		self.print_detail(self.inputs[0])

	#Create an ERSpec for the output of the reordering function
	def calc_output(self,mapir):

		#Need to create a static description of the output of the reordering
		self.outputs.append(ERSpec(
		    name=self.reordering_name,
		    input_bounds=mapir.full_iter_space.apply(self.iter_sub_space_relation),
		    output_bounds=mapir.full_iter_space.apply(self.iter_sub_space_relation),
		    relation=self._data_reordering.copy(),
		    is_permutation=True))

		#Add the ERSpec to the MapIR
		mapir.add_er_spec(self.outputs[0])

		self.print_progress("Calculated output ERSpec '%s' for transformation '%s'..."%(self.outputs[0].name,self.name))

		self.print_detail(self.outputs[0])

	#Modify access relations and data deps
	def update_mapir(self,mapir):
		#Update the access relations of all statements
		self.print_progress('Updating access relations...')
		for statement in mapir.get_statements():
			for access_relation in statement.get_access_relations():
				self.print_detail("Updating access relation '%s'..."%(access_relation.name))
				access_relation.iter_to_data=access_relation.iter_to_data.compose(self.iter_space_trans.inverse())

	#Add output ER and ERG call node to IDG
	def update_idg(self,mapir):
		#Add the ERG call node to the IDG
		erg_call_node=mapir.idg.get_node(IDGCall,calc_erg_call(self.name,self.erg_func_name,self.inputs,self.outputs))

		#Add the input ERSpecs to the IDG
		for input_er_spec in self.inputs:
			#Get a node for the ERSpec
			input_er_spec_node=mapir.idg.get_node(IDGERSpec,input_er_spec)

			#Get a gen node for the ERSpec
			gen_input_er_spec_node=mapir.idg.get_node(IDGGenERSpec,input_er_spec)

			#Add dependence of the GenERSpec node to ERSpec node
			input_er_spec_node.add_dep(gen_input_er_spec_node)

			#Add dependence of the call to the input
			erg_call_node.add_dep(input_er_spec_node)

		#Add the output ERSpecs to the IDG
		for output_er_spec in self.outputs:
			#Get a node for the ERSpec
			output_er_spec_node=mapir.idg.get_node(IDGOutputERSpec,output_er_spec)

			#Add dependence of the output on the call
			output_er_spec_node.add_dep(erg_call_node)
#-------------------------------------------
