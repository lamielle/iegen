#---------- Transformation base class ----------
from iegen import IEGenObject

class Transformation(IEGenObject):
	__slots__=('name','inputs','outputs','simplifications','symbolic_inputs')

	def __init__(self,name):
		self.name=name
		self.inputs=[]
		self.outputs=[]
		self.simplifications=[]
		self.symbolic_inputs=[]

	def calc_input(self,mapir):
		raise NotImplementedException('Subclasses of Transformation must implement calc_input')
	def calc_output(self,mapir):
		raise NotImplementedException('Subclasses of Transformation must implement calc_output')
	def update_mapir(self,mapir):
		raise NotImplementedException('Subclasses of Transformation must implement update_mapir')
	def update_idg(self,mapir):
		raise NotImplementedException('Subclasses of Transformation must implement update_idg')
#-------------------------------------
