from iegen.trans import Transformation

#---------- IterPermuteTrans class ----------
class IterPermuteTrans(Transformation):
	__slots__=('iter_reordering','iter_space','access_relation','iter_sub_space_relation','erg_func_name','erg_type')

	def __init__(self,iter_reordering,iter_space,access_relation,iter_sub_space_relation,erg_func_name,erg_type):
		self.iter_reordering=iter_reordering
		self.iter_space=iter_space
		self.access_relation=access_relation
		self.iter_sub_space_relation=iter_sub_space_relation
		self.erg_func_name=erg_func_name
		self.erg_type=erg_type
#-------------------------------------------
