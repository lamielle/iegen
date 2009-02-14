from iegen.idg.visitor import TopoVisitor
from iegen.codegen import gen_er_spec,gen_index_array,gen_output_er_spec,gen_erg_spec

class CodegenVisitor(TopoVisitor):

	def __init__(self):
		TopoVisitor.__init__(self)
		self.stmts=[]

	def atIDGSymbolic(self,node): pass

	def atIDGDataArray(self,node): pass

	def atIDGERSpec(self,node): self.stmts.extend(gen_er_spec(node.data))

	def atIDGIndexArray(self,node): self.stmts.extend(gen_index_array(node.data))

	def atIDGOutputERSpec(self,node): pass

	def atIDGCall(self,node):
		output_er_specs=[out_node.data for out_node in node.uses.values()]
		self.stmts.extend(gen_erg_spec(node.data,output_er_specs))
