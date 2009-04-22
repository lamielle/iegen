from iegen.trans import Transformation

#---------- IterAlignTrans class ----------
class IterAlignTrans(Transformation):
	__slots__=('reordering_name','iter_sub_space_relation')

	def __init__(self,reordering_name,iter_sub_space_relation):
		self.reordering_name=reordering_name
		self.iter_sub_space_relation=iter_sub_space_relation
#-------------------------------------------
