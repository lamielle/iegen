from iegen.idg.visitor import TopoVisitor
from iegen.codegen import Parameter

class ParamVisitor(TopoVisitor):

	def __init__(self):
		TopoVisitor.__init__(self)
		self.symbolics=[]
		self.data_arrays=[]
		self.index_arrays=[]
		self.output_er_specs=[]

	def get_params(self):
		#Sort the parameters
		self.symbolics.sort()
		self.data_arrays.sort()
		self.index_arrays.sort()
		self.output_er_specs.sort()

		#Init final list of parameters
		params=[]

		#Add each symbolic parameter
		for symbolic in self.symbolics:
			params.append(Parameter('int',symbolic))
			params.append

		#Add each data array parameter
		for data_array in self.data_arrays:
			params.append(Parameter('double *',data_array))

		#Add each index array parameter
		for index_array in self.index_arrays:
			params.append(Parameter('int *',index_array))

		#Add each output ERSpec parameter
		for output_er_spec in self.output_er_specs:
			params.append(Parameter('ExplicitRelation **',output_er_spec))

		return params

	def atIDGSymbolic(self,node): self.symbolics.append(node.data.name)

	def atIDGDataArray(self,node):
		if 0==node.data.version:
			self.data_arrays.append(node.data.data_array.name)

	def atIDGERSpec(self,node): pass

	def atIDGIndexArray(self,node): self.index_arrays.append(node.data.name)

	def atIDGOutputERSpec(self,node): self.output_er_specs.append(node.data.name)

	def atIDGGenERSpec(self,node): pass

	def atIDGCall(self,node): pass
