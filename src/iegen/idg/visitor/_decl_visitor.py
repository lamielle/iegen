from iegen.idg.visitor import TopoVisitor
from iegen.codegen import VarDecl

class DeclVisitor(TopoVisitor):

	def __init__(self):
		TopoVisitor.__init__(self)
		self.decls=[]

	def atIDGSymbolic(self,node): pass

	def atIDGDataArray(self,node): pass

	def atIDGERSpec(self,node):
		self.decls.append(VarDecl('ExplicitRelation *',[node.data.name+'_ER']))

	def atIDGIndexArray(self,node):
		self.decls.append(VarDecl('ExplicitRelation *',[node.data.name+'_ER']))

	#OutputERSpecs will be passed in with type 'ExplicitRelation **var'.
	#For convenience, we declare another variable 'ExplicitRelation *var_ER'
	def atIDGOutputERSpec(self,node):
		self.decls.append(VarDecl('ExplicitRelation *',[node.data.name+'_ER'],['*'+node.data.name]))

	def atIDGCall(self,node): pass
