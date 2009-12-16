from iegen.idg.visitor import TopoVisitor
from iegen.codegen import Statement

class OutputERVisitor(TopoVisitor):

	def __init__(self,mapir):
		TopoVisitor.__init__(self)
		self.mapir=mapir
		self.assigns=[]

	def get_assigns(self):
		return self.assigns

	def atIDGSymbolic(self,node): pass

	def atIDGDataArray(self,node): pass

	def atIDGERSpec(self,node): pass

	def atIDGIndexArray(self,node): pass

	#OutputERSpecs will be passed in as '**var'.
	#Here we assign the local ER variable *var
	def atIDGOutputERSpec(self,node):
		self.assigns.append(Statement('%s=*%s;'%(node.data.get_var_name(),node.data.get_param_name())))

	def atIDGGenERSpec(self,node): pass

	def atIDGGenOutputERSpec(self,node): pass

	def atIDGCall(self,node): pass
