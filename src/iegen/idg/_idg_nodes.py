#Inspector Dependence Graph Nodes
#Alan LaMielle: 1/13/2009

#---------- IDGNode ----------
class IDGNode(object):
	__slots__=('deps','uses','data')

	def __init__(self,data):
		self.deps=[]
		self.uses=[]
		self.data=data

	def add_dep(self,dep):
		self.deps.append(dep)
		dep.uses.append(self)

	def add_use(self,use):
		self.uses.append(use)
		use.deps.append(self)

	def apply_visitor(self,visitor):
		raise NotImplementedError('apply_visitor must be overridden in child classes')
#-----------------------------

#---------- IDGSymbolic ----------
class IDGSymbolic(IDGNode):
	def __init__(self,symbolic):
		IDGNode.__init__(self,symbolic)

	def apply_visitor(self,visitor):
		visitor.visitIDGSymbolic(self)
#---------------------------------

#---------- IDGDataArray ----------
class IDGDataArray(IDGNode):
	def __init__(self,data_array):
		IDGNode.__init__(self,data_array)

	def apply_visitor(self,visitor):
		visitor.visitIDGDataArray(self)
#----------------------------------

#---------- IDGERSpec ----------
class IDGERSpec(IDGNode):
	def __init__(self,er_spec):
		IDGNode.__init__(self,er_spec)

	def apply_visitor(self,visitor):
		visitor.visitIDGERSpec(self)
#---------------------------------

#---------- IDGIndexArray ----------
class IDGIndexArray(IDGERSpec):
	def __init__(self,index_array):
		IDGERSpec.__init__(self,index_array)

	def apply_visitor(self,visitor):
		visitor.visitIDGIndexArray(self)
#-----------------------------------

#---------- IDGCall ----------
class IDGCall(IDGNode):
	pass
#-----------------------------
