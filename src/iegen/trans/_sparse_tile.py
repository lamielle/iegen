from cStringIO import StringIO
from iegen.trans import Transformation
from iegen import ERSpec,Set,Relation,VersionedDataArray,DataDependence
from iegen.idg import IDGDataArray,IDGERSpec,IDGOutputERSpec,IDGGenERSpec,IDGCall,IDGSymbolic
from iegen.codegen import calc_erg_call,calc_reorder_call

#---------- SparseTileTrans class ----------
class SparseTileTrans(Transformation):
	__slots__=('grouping_name','num_tile_name','iter_sub_space_relation','iter_seed_space_relation','to_deps','from_deps','erg_func_name','iter_space_trans')
	_relation_fields=('iter_sub_space_relation','iter_seed_space_relation',)

	def __init__(self,name,grouping_name,num_tile_name,iter_sub_space_relation,iter_seed_space_relation,to_deps,from_deps,erg_func_name,iter_space_trans):
		Transformation.__init__(self,name)

		self.grouping_name=grouping_name
		self.num_tile_name=num_tile_name
		self.iter_sub_space_relation=iter_sub_space_relation
		self.iter_seed_space_relation=iter_seed_space_relation
		self.to_deps=to_deps
		self.from_deps=from_deps
		self.erg_func_name=erg_func_name
		self.iter_space_trans=iter_space_trans

		#TODO: Do we need to do any validation of the transformation arguments?

	def __repr__(self):
		return 'SparseTileTrans(%s,%s,%s,%s,%s,%s,%s,%s)'%(self.name,self.grouping_name,self.iter_sub_space_relation,self.iter_seed_space_relation,self.to_deps,self.from_deps,self.erg_func_name,self.iter_space_trans)

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

		return '''%sSparseTileTrans:
%s|-name: %s
%s|-inputs: %s
%s|-outputs: %s
%s|-grouping_name: %s
%s|-iter_sub_space_relation: %s
%s|-iter_seed_space_relation: %s
%s|-to_deps: %s
%s|-from_deps: %s
%s|-erg_func_name: %s
%s|-iter_space_trans: %s'''%(spaces,spaces,self.name,
    spaces,inputs_string,
    spaces,outputs_string,
    spaces,self.grouping_name,
    spaces,self.iter_sub_space_relation,
    spaces,self.iter_seed_space_relation,
    spaces,self.to_deps,
    spaces,self.from_deps,
    spaces,self.erg_func_name,
    spaces,self.iter_space_trans)

	#Calculate the inputs to the sparse tiling routine
	def calc_input(self,mapir):
		#The tiling routine takes the dependences into and out of the iteration seed space
		#These dependences are given by the user currently, so we do not need to calculate them
		#Create a DataDependence instance for the dependences
		self.to_deps=DataDependence('to_deps',self.to_deps)

		#Create a new Symbolic for the number of tiles
		#TODO: The type is constant here, it would be better if this were defined somewhere else
		mapir.add_symbolic(name=self.num_tile_name,type='int %s',lower_bound=0)

	#Calculate the output from the sparse tiling routine
	def calc_output(self,mapir):
		#Create a static description of the tiling function (theta) that is the output of the tiling routine
		self.outputs.append(ERSpec(
		    name=self.grouping_name,
		    #TODO: Need to define input bounds
		    input_bounds=Set('{[c,i]}'),
		    output_bounds=Set('{[tile]: 0<=tile and tile<=%s}'%(self.num_tile_name,)),
		    relation=Relation('{[%s_in]->[%s_out]: %s_out=%s(%s_in)}'%(5*(self.grouping_name,))),
		    is_function=True,
		    is_permutation=False))

		#Add the ERSpec to the MapIR
		mapir.add_er_spec(self.outputs[0])

		self.print_progress("Calculated output ERSpec '%s' for transformation '%s'..."%(self.outputs[0].name,self.name))
		self.print_detail(self.outputs[0])

	#Update the MapIR based on this transformation
	def update_mapir(self,mapir):
		#Update the scattering functions and access relations of all statements
		self.print_progress('Updating scattering functions and access relations...')
		for statement in mapir.get_statements():
			statement.scatter=self.iter_space_trans.compose(statement.scatter)

			for access_relation in statement.get_access_relations():
				self.print_detail("Updating access relation '%s'..."%(access_relation.name))
				access_relation.iter_to_data=access_relation.iter_to_data.compose(self.iter_space_trans.inverse())

		#Update the data dependences
		self.print_progress('Updating data dependences for SparseTileTrans...')
		for data_dependence in mapir.get_data_dependences():
			self.print_detail("Updating data dependence '%s'..."%(data_dependence.name))
			data_dependence.dep_rel=self.iter_space_trans.compose(data_dependence.dep_rel.compose(self.iter_space_trans.inverse()))

	def update_idg(self,mapir):
		#Add the ERG call node to the IDG
		#This is the node that represents the call to the sparse tiling routine
		erg_call_node=mapir.idg.get_node(IDGCall,calc_erg_call(self.name,self.erg_func_name,self.inputs,self.outputs))

		#Add the symbolic node to the IDG
		num_tile_node=mapir.idg.get_node(IDGSymbolic,mapir.symbolics[self.num_tile_name])

		#Add a dependence of the ERG call on the symbolic
		erg_call_node.add_dep(num_tile_node)

		#Add the output node to the IDG
		output_node=mapir.idg.get_node(IDGERSpec,self.outputs[0])

		#Add a dependence of the output on the ERG call node
		output_node.add_dep(erg_call_node)
#-------------------------------------------
