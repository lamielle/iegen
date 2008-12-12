#---------- Transformation base class ----------
class Transformation(object):
	__slots__=('name','inputs','input_deps','outputs','output_deps','simplifications','itos','symbolic_inputs')

	def __init__(self,name):
		from iegen.trans import TransDeps

		self.name=name
		self.inputs=[]
		self.input_deps=TransDeps()
		self.outputs=[]
		self.output_deps=TransDeps()
		self.simplifications=[]
		self.itos=[]
		self.symbolic_inputs=[]

	def calc_input(self,mapir):
		raise NotImplementedException('Subclasses of Transformation must implement calc_input')
	def calc_output(self,mapir):
		raise NotImplementedException('Subclasses of Transformation must implement calc_output')
	def calc_apply(self,mapir):
		raise NotImplementedException('Subclasses of Transformation must implement calc_apply')
	def calc_data_remaps(self,mapir):
		raise NotImplementedException('Subclasses of Transformation must implement calc_data_remaps')
	def calc_input_deps(self,mapir):
		raise NotImplementedException('Subclasses of Transformation must implement calc_input_deps')
	def calc_output_deps(self,mapir):
		raise NotImplementedException('Subclasses of Transformation must implement calc_output_deps')
#-------------------------------------
