#Inspector Dependence Graph
#Alan LaMielle: 1/7/2009

from iegen import IEGenObject
from iegen.idg import IDGSymbolic,IDGDataArray,IDGERSpec,IDGIndexArray,IDGOutputERSpec,IDGERGCall,IDGCall

#---------- Inspector Dependence Graph ----------
class IDG(IEGenObject):
	__slots__=('nodes')

	_prefixes={
	           IDGSymbolic:'sym_',
	           IDGDataArray:'data_array_',
	           IDGERSpec:'er_spec_',
	           IDGIndexArray:'er_spec_',
	           IDGOutputERSpec:'er_spec_',
	           IDGERGCall:'erg_spec_',
	           IDGCall:'gen_call_',
	          }

	def __init__(self):
		self.nodes={}

	def _get_id(self,node_data,prefix_key):
		return self._prefixes[prefix_key]+node_data.name

	def _get_node(self,node_data,node_class):
		#Get the internal id for the given node data
		key=self._get_id(node_data,node_class)

		#Create a new node if it doesn't already exist
		#Return the existing node if it exists
		if key not in self.nodes:
			node=node_class(key,node_data)
			self.nodes[key]=node

		#Return the requested node
		return self.nodes[key]

	def get_symbolic_node(self,symbolic):
		return self._get_node(symbolic,IDGSymbolic)

	def get_data_array_node(self,data_array):
		return self._get_node(data_array,IDGDataArray)

	def get_er_spec_node(self,er_spec):
		return self._get_node(er_spec,IDGERSpec)

	def get_index_array_node(self,index_array):
		return self._get_node(index_array,IDGIndexArray)

	def get_output_er_spec_node(self,er_spec):
		return self._get_node(er_spec,IDGOutputERSpec)

	def get_erg_call_node(self,erg_spec):
		return self._get_node(erg_spec,IDGERGCall)

	def get_call_node(self,erg_spec):
		return self._get_node(erg_spec,IDGCall)
#------------------------------------------------
