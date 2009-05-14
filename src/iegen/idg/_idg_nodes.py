#Inspector Dependence Graph Nodes
#Alan LaMielle: 1/13/2009

from iegen import IEGenObject

#-------------------- IDG Node Base Classes --------------------
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

#---------- IDGDataNode ----------
class IDGDataNode(IDGNode): pass
#---------------------------------

#---------- IDGTaskNode ----------
class IDGTaskNode(IDGNode): pass
#---------------------------------
#---------------------------------------------------------------

#-------------------- Data Nodes --------------------
#---------- IDGSymbolic ----------
class IDGSymbolic(IDGDataNode):
	_prefix='sym_'

	def apply_visitor(self,visitor):
		visitor.visitIDGSymbolic(self)
#---------------------------------

#---------- IDGDataArray ----------
class IDGDataArray(IDGDataNode):
	_prefix='data_array_'

	def apply_visitor(self,visitor):
		visitor.visitIDGDataArray(self)
#----------------------------------

#---------- IDGERSpec ----------
class IDGERSpec(IDGDataNode):
	_prefix='er_spec_'

	def apply_visitor(self,visitor):
		visitor.visitIDGERSpec(self)
#---------------------------------

#---------- IDGIndexArray ----------
class IDGIndexArray(IDGERSpec):
	_prefix='er_spec_'

	def apply_visitor(self,visitor):
		visitor.visitIDGIndexArray(self)
#-----------------------------------

#---------- IDGOutputERSpec ----------
class IDGOutputERSpec(IDGERSpec):
	_prefix='er_spec_'

	def apply_visitor(self,visitor):
		visitor.visitIDGOutputERSpec(self)
#-------------------------------------
#----------------------------------------------------

#-------------------- Task Nodes --------------------
#---------- IDGGenERSpec ----------
class IDGGenERSpec(IDGTaskNode):
	_prefix='gen_er_spec_'

	def apply_visitor(self,visitor):
		visitor.visitIDGGenERSpec(self)
#---------------------------------

#---------- IDGCall ----------
class IDGCall(IDGTaskNode):
	_prefix='call_'

	def apply_visitor(self,visitor):
		visitor.visitIDGCall(self)
#-----------------------------
#----------------------------------------------------
