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

	#OutputERSpecs will be passed in with type 'ExplicitRelation **var'.
	#Here we assign the var_ER variable *var
	def atIDGOutputERSpec(self,node):
		self.assigns.append(Statement('%s_ER=*%s;'%(node.data.name,node.data.name)))

	def atIDGGenERSpec(self,node): pass

	def atIDGCall(self,node): pass
