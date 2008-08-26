from iegen.ast.visitor import DFVisitor

class RenameVisitor(DFVisitor):
	def __init__(self,rename_dict):
		self.rename_dict=rename_dict

	#Do nothing by default
	def defaultIn(self,node):
		pass
	def defaultOut(self,node):
		pass

	def inVarTuple(self,node):
		for i in xrange(len(node.id_list)):
			if node.id_list[i] in self.rename_dict:
				node.id_list[i]=self.rename_dict[node.id_list[i]]

	def inVarExp(self,node):
		if node.id in self.rename_dict:
			node.id=self.rename_dict[node.id]
