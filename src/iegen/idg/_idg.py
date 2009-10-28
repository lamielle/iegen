#Inspector Dependence Graph
#Alan LaMielle: 1/7/2009

from iegen import IEGenObject

#---------- Inspector Dependence Graph ----------
class IDG(IEGenObject):
	__slots__=('nodes')

	def __init__(self):
		self.nodes={}

	def _get_id(self,node_class,node_data):
		return node_class._prefix+node_data.name

	def get_node(self,node_class,node_data):
		#Get the internal id for the given node data
		key=self._get_id(node_class,node_data)

		#Create a new node if it doesn't already exist
		#Return the existing node if it exists
		if key not in self.nodes:
			node=node_class(key,node_data)
			self.nodes[key]=node

		#Return the requested node
		return self.nodes[key]
#------------------------------------------------
