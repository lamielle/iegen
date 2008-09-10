from iegen.ast.visitor import DFVisitor

class RenameVisitor(DFVisitor):
	def __init__(self,rename_dict):
		self.rename_dict=rename_dict

	def inVarExp(self,node):
		if node.id in self.rename_dict:
			node.id=self.rename_dict[node.id]
