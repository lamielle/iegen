from cStringIO import StringIO
from iegen.trans import Transformation
from iegen import ERSpec,Set,Relation,VersionedDataArray,DataDependence
from iegen.idg import IDGDataArray,IDGERSpec,IDGOutputERSpec,IDGGenERSpec,IDGCall,IDGSymbolic,IDGDataDep,IDGGenDataDep
from iegen.codegen import calc_erg_call,calc_reorder_call,calc_data_dep_deps,calc_equality_value

#---------- CacheBlockTrans class ----------
class CacheBlockTrans(Transformation):
	__slots__=('grouping_name','num_cb_name','col_name','iter_sub_space_relation','erg_func_name','iter_space_trans')

	def __init__(self,name,grouping_name,num_cb_name,col_name,iter_sub_space_relation,erg_func_name,iter_space_trans):
		Transformation.__init__(self,name)

		self.grouping_name=grouping_name
		self.num_cb_name=num_cb_name
		self.col_name=col_name
		self.iter_sub_space_relation=iter_sub_space_relation
		self.erg_func_name=erg_func_name
		self.iter_space_trans=iter_space_trans

		#TODO: Do we need to do any validation of the transformation arguments?

	def __repr__(self):
		return 'CacheBlockTrans(%s,%s,%s,%s,%s)'%(self.name,self.grouping_name,self.iter_sub_space_relation,self.erg_func_name,self.iter_space_trans)

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

		return '''%sCacheBlockTrans:
%s|-name: %s
%s|-inputs: %s
%s|-outputs: %s
%s|-grouping_name: %s
%s|-iter_sub_space_relation: %s
%s|-erg_func_name: %s
%s|-iter_space_trans: %s'''%(spaces,spaces,self.name,
    spaces,inputs_string,
    spaces,outputs_string,
    spaces,self.grouping_name,
    spaces,self.iter_sub_space_relation,
    spaces,self.erg_func_name,
    spaces,self.iter_space_trans)

	#Calculate the inputs to the sparse tiling routine
	def calc_input(self,mapir):
		#Create a new Symbolic for the number of tiles
		#TODO: The type is constant here, it would be better if this were defined somewhere else
		mapir.add_symbolic(name=self.num_cb_name,type='int %s',lower_bound=1)

		self.inputs.append(mapir.er_specs[self.col_name])
		self.inputs.append(mapir.symbolics[self.num_cb_name])

	#Calculate the output from the sparse tiling routine
	def calc_output(self,mapir):
		#input bounds calculated based on full iteration space and the specified iter_sub_space_relation
		input_bounds=self.inputs[0].input_bounds

		#output is a tile number, therefore the bounds are from 0 to the number of tiles
		output_bounds=Set('{[block]: 0<=block and block<%s}'%(self.num_cb_name,),symbolics=[mapir.symbolics[self.num_cb_name]])

		#the relation takes the input loop position and iterator and yields a tile number
		input_tuple_vars=[]
		for i in xrange(input_bounds.arity()):
			input_tuple_vars.append('%s_in%d'%(self.grouping_name,i))
		input_tuple=','.join(input_tuple_vars)
		relation=Relation('{[%s]->[b]: b=%s(%s)}'%(input_tuple,self.grouping_name,input_tuple))
		relation=relation.restrict_domain(input_bounds)
		relation=relation.restrict_range(output_bounds)

		#Create a static description of the tiling function (theta) that is the output of the tiling routine
		self.outputs.append(ERSpec(
		    name=self.grouping_name,
		    input_bounds=input_bounds,
		    output_bounds=output_bounds,
		    relation=relation,
		    is_function=True,
		    is_permutation=False))

		#Add the ERSpec to the MapIR
		mapir.add_er_spec(self.outputs[0])

		self.print_progress("Calculated output ERSpec '%s' for transformation '%s'..."%(self.outputs[0].name,self.name))
		self.print_detail(self.outputs[0])

	#Update the MapIR based on this transformation
	def update_mapir(self,mapir):
		#Update the iteration spcaes, scattering functions, and access relations of all statements based on the specified transformation
		self.print_progress('Updating iteration spaces, scattering functions, and access relations...')
		for statement in mapir.get_statements():
			self.print_detail("Updating statement '%s'..."%(statement.name))
			statement.iter_space=statement.iter_space.apply(self.iter_space_trans)
			statement.scatter=self.iter_space_trans.compose(statement.scatter)

			for access_relation in statement.get_access_relations():
				self.print_detail("Updating access relation '%s'..."%(access_relation.name))
				access_relation.iter_to_data=access_relation.iter_to_data.compose(self.iter_space_trans.inverse())

		#Update the data dependences
		self.print_progress('Updating data dependences for CacheBlockTrans...')
		for data_dependence in mapir.get_data_dependences():
			self.print_detail("Updating data dependence '%s'..."%(data_dependence.name))
			data_dependence.dep_rel=self.iter_space_trans.compose(data_dependence.dep_rel.compose(self.iter_space_trans.inverse()))

	def update_idg(self,mapir):
		#Add the ERG call node to the IDG
		#This is the node that represents the call to the cache blocking routine
		erg_call_node=mapir.idg.get_node(IDGCall,calc_erg_call(self.name,self.erg_func_name,self.inputs,self.outputs))

		#Add the input col ER node to the IDG
		col_er_spec_node=mapir.idg.get_node(IDGERSpec,self.inputs[0])

		#Add a dependence of the call to the input col ER
		erg_call_node.add_dep(col_er_spec_node)

		#Add the number of cache blocks symbolic node to the IDG
		num_tile_node=mapir.idg.get_node(IDGSymbolic,mapir.symbolics[self.num_cb_name])

		#Add a dependence of the ERG call on the symbolic
		erg_call_node.add_dep(num_tile_node)

		#Add the output node to the IDG
		output_node=mapir.idg.get_node(IDGOutputERSpec,self.outputs[0])

		#Add a dependence of the output on the ERG call node
		output_node.add_dep(erg_call_node)
#-------------------------------------------
