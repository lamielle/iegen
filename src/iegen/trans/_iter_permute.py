from iegen.trans import Transformation

#---------- IterPermuteTrans class ----------
class IterPermuteTrans(Transformation):
	__slots__=('iter_reordering','iter_space','access_relation','iter_sub_space_relation','iag_func_name','iag_type')

	def __init__(self,iter_reordering,iter_space,access_relation,iter_sub_space_relation,iag_func_name,iag_type):
		self.iter_reordering=iter_reordering
		self.iter_space=iter_space
		self.access_relation=access_relation
		self.iter_sub_space_relation=iter_sub_space_relation
		self.iag_func_name=iag_func_name
		self.iag_type=iag_type
#-------------------------------------------
