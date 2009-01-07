#Inspector Dependence Graph classes
#Alan LaMielle: 1/7/2009

#---------- Inspector Dependence Graph ----------
class IDG(object):
	__slots__=('nodes')

	_symbolic_prefix='sym_'
	_data_array_prefix='data_array_'

	def __init__(self):
		self.nodes={}

	def get_symbolic_id(symbolic):
		return _symbolic_prefix+symbolic.name

	def get_symbolic_node(symbolic):
		#Get the internal id of the given symbolic
		key=self.get_symbolic_id(symbolic)

		#Create a new node if it doesn't already exist
		#Return the existing node if it exists
		if key not in self.nodes.keys():
			node=IDGSymbolic(symbolic)
			self.nodes[key]=node

		#Return the requested node
		return self.nodes[key]

	def get_data_array_id(data_array):
		return _data_array_prefix+data_array.name

	def get_data_array_node(data_array):
		#Get the internal id of the given data array
		key=self.get_data_array_id(data_array)

		#Create a new node if it doesn't already exist
		#Return the existing node if it exists
		if key not in self.nodes.keys():
			node=IDGSymbolic(data_array)
			self.nodes[key]=node

		#Return the requested node
		return self.nodes[key]
#------------------------------------------------

#---------- IDGNode ----------
class IDGNode(object):
	__slots__=('deps','uses','data')

	def __init__(self,data):
		self.deps=[]
		self.uses=[]
		self.data=data

	def add_dep(dep):
		self.deps.append(dep)
		dep.uses.add(self)

	def add_use(use):
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

#---------- IDGRelation ----------
class IDGRelation(IDGNode):
	def __init__(self,relation):
		IDGNode.__init__(self,relation)

	def apply_visitor(self,visitor):
		visitor.visitIDGRelation(self)
#---------------------------------

#---------- IDGCall ----------
class IDGCall(IDGNode):
	pass
#-----------------------------
