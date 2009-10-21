#---------- Inter-Transformation Optimization base class ----------
from iegen import IEGenObject

class InterTransOpt(IEGenObject):
	__slots__=('name')

	def __init__(self,name):
		self.name=name

	def apply(self,mapir):
		raise NotImplementedException('Subclasses of InterTransOpt must implement apply')
#-------------------------------------
