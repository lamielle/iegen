from iegen.idg.visitor import TopoVisitor
from iegen.codegen import VarDecl,gen_tuple_vars_decl

class DeclVisitor(TopoVisitor):

	def __init__(self,mapir):
		TopoVisitor.__init__(self)
		self.mapir=mapir
		self.decls={}
		self.int_vars=set()

	def get_decls(self):
		self.collect_iter_space_vars()
		decls=self.decls.values()
		if len(self.int_vars)>0: decls.append(VarDecl('int',list(self.int_vars)))
		return decls

	def add_int_vars(self,vars):
		self.int_vars=self.int_vars.union(vars)

	def collect_iter_space_vars(self):
		from iegen.ast.visitor import CollectVarsVisitor
		for statement in self.mapir.get_statements():
			self.add_int_vars(statement.iter_space.variables())

	def atIDGSymbolic(self,node): pass

	def atIDGDataArray(self,node): pass

	def atIDGERSpec(self,node):
		self.decls[node.data.name]=VarDecl('ExplicitRelation *',[node.data.name+'_ER'])
		for var_decl in gen_tuple_vars_decl(node.data.input_bounds):
			self.add_int_vars(var_decl.var_names)

	def atIDGIndexArray(self,node):
		self.decls[node.data.name]=VarDecl('ExplicitRelation *',[node.data.name+'_ER'])

	#OutputERSpecs will be passed in with type 'ExplicitRelation **var'.
	#For convenience, we declare another variable 'ExplicitRelation *var_ER'
	def atIDGOutputERSpec(self,node):
		self.decls[node.data.name]=VarDecl('ExplicitRelation *',[node.data.name+'_ER'],['*'+node.data.name])

	def atIDGERGCall(self,node): pass

	def atIDGCall(self,node): pass
