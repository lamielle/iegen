from iegen.idg.visitor import TopoVisitor
from iegen.codegen import Parameter

class ParamVisitor(TopoVisitor):

	def __init__(self):
		TopoVisitor.__init__(self)
		self.params=[]

	def atIDGSymbolic(self,node):
		self.params.append(Parameter('int',node.data.name))

	def atIDGDataArray(self,node):
		self.params.append(Parameter('double *',node.data.name))

	def atIDGERSpec(self,node): pass

	def atIDGIndexArray(self,node):
		self.params.append(Parameter('int *',node.data.name))

	def atIDGOutputERSpec(self,node):
		self.params.append(Parameter('ExplicitRelation **',node.data.name))

	def atIDGGenERSpec(self,node): pass

	def atIDGCall(self,node): pass
