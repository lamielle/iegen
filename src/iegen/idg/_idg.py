#Inspector Dependence Graph

#---------- IDGNode ----------
class IDGNode(object):
	__slots__=('deps','uses')

	def __init__(self):
		pass
#-----------------------------

#---------- IDGSymbolic ----------
class IDGSymbolic(IDGNode):
	pass
#---------------------------------

#---------- IDGDataSpace ----------
class IDGDataSpace(IDGNode):
	pass
#----------------------------------

#---------- IDGRelation ----------
class IDGRelation(IDGNode):
	pass
#---------------------------------

#---------- IDGCall ----------
class IDGCall(IDGNode):
	pass
#-----------------------------
