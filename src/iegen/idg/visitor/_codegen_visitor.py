from iegen.idg.visitor import TopoVisitor
from iegen.idg import IDGOutputERSpec
from iegen.codegen import gen_er_spec,gen_index_array,gen_output_er_spec,gen_data_dep,gen_call,Comment,Statement

class CodegenVisitor(TopoVisitor):

	def __init__(self,mapir):
		TopoVisitor.__init__(self)
		self.mapir=mapir
		self.stmts=[]

	def atIDGSymbolic(self,node): pass

	def atIDGDataArray(self,node): pass

	def atIDGERSpec(self,node): pass

	def atIDGIndexArray(self,node): self.stmts.extend(gen_index_array(node.data))

	def atIDGOutputERSpec(self,node): pass

	def atIDGDataDep(self,node): pass

	def atIDGGenERSpec(self,node): self.stmts.extend(gen_er_spec(node.data,self.mapir))

	def atIDGGenOutputERSpec(self,node): self.stmts.extend(gen_output_er_spec(node.data,False,self.mapir))

	def atIDGGenDataDep(self,node): self.stmts.extend(gen_data_dep(node.data,self.mapir))

	def atIDGCall(self,node):

		#First generate any ERs that are output from this call
		#TODO: Use a better method of checking that a node is an ER node
		output_er_specs=[out_node.data for out_node in node.uses.values() if 'er_spec_'==out_node._prefix]
		for output_er_spec in output_er_specs:
			self.stmts.extend(gen_output_er_spec(output_er_spec,True,self.mapir))

		#Generate the call
		self.stmts.extend(gen_call(node.data))
