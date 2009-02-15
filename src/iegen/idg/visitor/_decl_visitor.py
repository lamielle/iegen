from iegen.idg.visitor import TopoVisitor
from iegen.codegen import VarDecl,gen_tuple_vars_decl

class DeclVisitor(TopoVisitor):

	def __init__(self):
		TopoVisitor.__init__(self)
		self.decls={}

	def atIDGSymbolic(self,node): pass

	def atIDGDataArray(self,node): pass

	def atIDGERSpec(self,node):
		self.decls[node.data.name]=VarDecl('ExplicitRelation *',[node.data.name+'_ER'])
		for var_decl in gen_tuple_vars_decl(node.data.input_bounds):
			for var_name in var_decl.var_names:
				self.decls[var_name]=VarDecl('int',var_name)

	def atIDGIndexArray(self,node):
		self.decls[node.data.name]=VarDecl('ExplicitRelation *',[node.data.name+'_ER'])

	#OutputERSpecs will be passed in with type 'ExplicitRelation **var'.
	#For convenience, we declare another variable 'ExplicitRelation *var_ER'
	def atIDGOutputERSpec(self,node):
		self.decls[node.data.name]=VarDecl('ExplicitRelation *',[node.data.name+'_ER'],['*'+node.data.name])

	def atIDGCall(self,node): pass
