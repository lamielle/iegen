from iegen.idg.visitor import TopoVisitor
from iegen.codegen import gen_er_spec,gen_index_array,gen_output_er_spec,gen_call

class CodegenVisitor(TopoVisitor):

	def __init__(self):
		TopoVisitor.__init__(self)
		self.stmts=[]

	def atIDGSymbolic(self,node): pass

	def atIDGDataArray(self,node): pass

	def atIDGERSpec(self,node): self.stmts.extend(gen_er_spec(node.data))

	def atIDGIndexArray(self,node): self.stmts.extend(gen_index_array(node.data))

	def atIDGOutputERSpec(self,node): pass

	def atIDGGenERSpec(self,node): pass

	def atIDGCall(self,node):
		#First generate any ERs that are output from this call
		#TODO: Use a better method of checking that a node is an ER node
		output_er_specs=(out_node.data for out_node in node.uses.values() if 'er_spec_'==node._prefix)
		for output_er_spec in output_er_specs:
			gen_output_er_spec(output_er_spec)

		#Generate the call
		gen_call(node.data)
