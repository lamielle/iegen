#---------- RTRT base class ----------
class RTRT(object):
	__slots__=('name','inputs','outputs','simplifications','itos','symbolic_inputs')

	def __init__(self,name):
		self.name=name
		self.inputs=[]
		self.outputs=[]
		self.simplifications=[]
		self.itos=[]
		self.symbolic_inputs=[]

	def calc_input(self,mapir):
		raise NotImplementedException('Subclasses of RTRT must implement calc_input')
	def calc_output(self,mapir):
		raise NotImplementedException('Subclasses of RTRT must implement calc_output')
	def calc_apply(self,mapir):
		raise NotImplementedException('Subclasses of RTRT must implement calc_apply')
	def calc_data_remaps(self,mapir):
		raise NotImplementedException('Subclasses of RTRT must implement calc_data_remaps')
#-------------------------------------
