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

	def atIDGOutputERSpec(self,node): pass
