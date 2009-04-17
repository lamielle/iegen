from iegen.idg.visitor import TopoVisitor
from iegen.codegen import gen_er_spec,gen_index_array,gen_output_er_spec,gen_erg_spec,gen_reorder_call

class CodegenVisitor(TopoVisitor):

	def __init__(self):
		TopoVisitor.__init__(self)
		self.stmts=[]

	def atIDGSymbolic(self,node): pass

	def atIDGDataArray(self,node): pass

	def atIDGERSpec(self,node): self.stmts.extend(gen_er_spec(node.data))

	def atIDGIndexArray(self,node): self.stmts.extend(gen_index_array(node.data))

	def atIDGOutputERSpec(self,node): pass

	def atIDGERGCall(self,node):
		output_er_specs=[out_node.data for out_node in node.uses.values()]
		self.stmts.extend(gen_erg_spec(node.data,output_er_specs))

	def atIDGReorderCall(self,node):
		#TODO: This assumes the order of the dependences is reordering
		# then data_array which may not always be the case
		reordering=node.deps.values()[0].data
		data_array=node.deps.values()[1].data
		self.stmts.extend(gen_reorder_call(data_array,reordering))
