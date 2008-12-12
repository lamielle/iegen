#---------- Transformation Dependences class ----------
#All fields in this class are collections of names, not the objects themselv es
class TransDeps(object):
	__slots__=('data_arrays','explicit_relations','symbolics')

	def __init__(self):
		self.data_arrays=set()
		self.explicit_relations=set()
		self.symbolics=set()

	def add_data_array(self,data_array):
		self.data_arrays=list(set(self.data_arrays).union(set(data_array)))

	def add_explicit_relation(self,explicit_relation):
		self.explicit_relations=list(set(self.explicit_relations).union(set(explicit_relation)))

	def add_symbolic(self,symbolic):
		self.symbolics=list(set(self.symbolics).union(set(symbolic)))
#--------------------------------------------
