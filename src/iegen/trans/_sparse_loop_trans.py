from cStringIO import StringIO
from iegen.trans import Transformation
from iegen import ERSpec,Set,Relation,Constant
from iegen.codegen import calc_equality_value,calc_erg_call
from iegen.idg import IDGCall,IDGOutputERSpec

#---------- SparseLoopTrans class ----------
class SparseLoopTrans(Transformation):
	__slots__=('statement_name','tiling_name','erg_func_name')

	def __init__(self,name,statement_name,tiling_name,erg_func_name):
		Transformation.__init__(self,name)

		self.statement_name=statement_name
		self.tiling_name=tiling_name
		self.erg_func_name=erg_func_name

	def __repr__(self):
		return 'SparseLoopTrans(%s,%s,%s)'%(self.name,self.statement_name,self.tiling_name,self.erg_func_name)

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

		return '''%sSparseLoopTrans:
%s|-name: %s
%s|-inputs: %s
%s|-outputs: %s
%s|-statement_name: %s
%s|-tiling_name: %s
%s|-erg_func_name: %s'''%(spaces,spaces,self.name,
    spaces,inputs_string,
    spaces,outputs_string,
    spaces,self.statement_name,
    spaces,self.tiling_name,
    spaces,self.erg_func_name)

	#Calculate the inputs to the sparse loop optimization
	def calc_input(self,mapir):
		#This transformation requires the ER for the given sparse tiling
		self.inputs.append(mapir.er_specs[self.tiling_name])

		#and the constant for the specific loop nest
		statement=mapir.statements[self.statement_name]
		loop_pos=calc_equality_value(statement.scatter.tuple_vars[-3],list(statement.scatter)[0],mapir)
		#TODO: The loop constants don't match exactly, they are off by one.
		loop_pos=str(int(loop_pos)+1)
		self.inputs.append(Constant(loop_pos))

	#Calculate the output from the sparse loop optimization
	def calc_output(self,mapir):
		#Create the name of the sparse schedule
		sparse_sched_name='%s_sched'%(self.statement_name)

		#Get the ERSpec for the specified tiling function
		tiling_er_spec=mapir.er_specs[self.tiling_name]

		statement=mapir.statements[self.statement_name]
		sparse_loop_iter=statement.iter_space.tuple_vars[-2]

		#Extract the sparse loop bounds from the statement's iteration space
		output_bounds=statement.iter_space.bounds(sparse_loop_iter)
		lower_bounds=' and '.join(list('%s<=%s'%(str(bound),sparse_loop_iter) for bound in list(output_bounds[0])[0]))
		upper_bounds=' and '.join(list('%s<=%s'%(sparse_loop_iter,str(bound)) for bound in list(output_bounds[0])[1]))
		output_bounds=Set('{[%s]: %s and %s}'%(sparse_loop_iter,lower_bounds,upper_bounds),symbolics=statement.iter_space.symbolics)

		#Get the constant for the position of the sparse loop within the tile loop
		loop_pos=calc_equality_value(statement.scatter.tuple_vars[-3],list(statement.scatter)[0],mapir)
		#TODO: The loop constants don't match exactly, they are off by one.
		loop_pos=str(int(loop_pos)+1)

		relation=Relation('{[tile]->[iter]: tile=theta(%s,iter)}'%(loop_pos))

		#Create a new ERSpec that represents the specified statement's sparse schedule
		self.outputs.append(ERSpec(
		    name=sparse_sched_name,
		    input_bounds=tiling_er_spec.output_bounds.copy(),
		    output_bounds=output_bounds,
		    relation=relation,
		    is_function=False,
		    is_permutation=False,
		    is_gen_output=True))

		#Add the ERSpec to the MapIR
		mapir.add_er_spec(self.outputs[0])

		self.print_progress("Calculated output ERSpec '%s' for transformation '%s'..."%(self.outputs[0].name,self.name))
		self.print_detail(self.outputs[0])

	#Update the MapIR based on this transformation
	def update_mapir(self,mapir):
		#Create the name of the sparse schedule
		sparse_sched_name='%s_sched'%(self.statement_name)

		#Update the statement's sparse_sched field with the name of the ERSpec that represents this statement's sparse schedule
		statement=mapir.statements[self.statement_name]
		statement.sparse_sched=sparse_sched_name

	def update_idg(self,mapir):
		#Add a call node for the ERG that will create the sparse schedule ER
		erg_call_node=mapir.idg.get_node(IDGCall,calc_erg_call(self.name,self.erg_func_name,self.inputs,self.outputs))

		#Add an output ER node for the result of the call to the ERG
		er_node=mapir.idg.get_node(IDGOutputERSpec,self.outputs[0])

		#Add a dependence of the ER on the ERG call
		er_node.add_dep(erg_call_node)
#-------------------------------------------
