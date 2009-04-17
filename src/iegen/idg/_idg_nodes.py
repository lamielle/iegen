#Inspector Dependence Graph Nodes
#Alan LaMielle: 1/13/2009

from iegen import IEGenObject

#---------- IDGNode ----------
class IDGNode(IEGenObject):
	__slots__=('deps','uses','key','data')

	def __init__(self,key,data):
		self.deps={}
		self.uses={}
		self.key=key
		self.data=data

	def add_dep(self,dep):
		self.deps[dep.key]=dep
		dep.uses[self.key]=self

	def add_use(self,use):
		self.uses[use.key]=use
		use.deps[self.key]=self

	def apply_visitor(self,visitor):
		raise NotImplementedError('apply_visitor must be overridden in child classes')
#-----------------------------

#---------- IDGSymbolic ----------
class IDGSymbolic(IDGNode):
	def __init__(self,key,symbolic):
		IDGNode.__init__(self,key,symbolic)

	def apply_visitor(self,visitor):
		visitor.visitIDGSymbolic(self)
#---------------------------------

#---------- IDGDataArray ----------
class IDGDataArray(IDGNode):
	def __init__(self,key,data_array):
		IDGNode.__init__(self,key,data_array)

	def apply_visitor(self,visitor):
		visitor.visitIDGDataArray(self)
#----------------------------------

#---------- IDGERSpec ----------
class IDGERSpec(IDGNode):
	def __init__(self,key,er_spec):
		IDGNode.__init__(self,key,er_spec)

	def apply_visitor(self,visitor):
		visitor.visitIDGERSpec(self)
#---------------------------------

#---------- IDGIndexArray ----------
class IDGIndexArray(IDGERSpec):
	def __init__(self,key,index_array):
		IDGERSpec.__init__(self,key,index_array)

	def apply_visitor(self,visitor):
		visitor.visitIDGIndexArray(self)
#-----------------------------------

#---------- IDGOutputERSpec ----------
class IDGOutputERSpec(IDGERSpec):
	def __init__(self,key,er_spec):
		IDGNode.__init__(self,key,er_spec)

	def apply_visitor(self,visitor):
		visitor.visitIDGOutputERSpec(self)
#-------------------------------------

#---------- IDGERGCall ----------
class IDGERGCall(IDGNode):
	def __init__(self,key,erg_spec):
		IDGNode.__init__(self,key,erg_spec)

	def apply_visitor(self,visitor):
		visitor.visitIDGERGCall(self)
#-----------------------------

#---------- IDGReorderCall ----------
class IDGReorderCall(IDGNode):
	def __init__(self,key,call_spec):
		IDGNode.__init__(self,key,call_spec)

	def apply_visitor(self,visitor):
		visitor.visitIDGReorderCall(self)
#-----------------------------
