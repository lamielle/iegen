# _visitor.py
#
# Visitor class for traversing an IDG

# Alan LaMielle 1/7/2009

from iegen import IEGenObject

#---------- Topological Visitor ----------
class TopoVisitor(IEGenObject):

	def __init__(self):
		pass

	#---------- Default At Method ----------
	#Do nothing by default
	def defaultAt(self,node): pass
	#---------------------------------------

	#---------- At Methods ----------
	def atIDGSymbolic(self,node): self.defaultAt(node)
	def atIDGDataArray(self,node): self.defaultAt(node)
	def atIDGERSpec(self,node): self.defaultAt(node)
	def atIDGIndexArray(self,node): self.defaultAt(node)
	def atIDGOutputERSpec(self,node): self.defaultAt(node)
	def atIDGGenERSpec(self,node): self.defaultAt(node)
	def atIDGGenOutputERSpec(self,node): self.defaultAt(node)
	def atIDGCall(self,node): self.defaultAt(node)
	#--------------------------------

	#---------- Visit methods ----------
	def visit(self,idg):
		#Create mappings from node keys to number of dependences
		num_deps=dict(((node_key,len(node.deps)) for node_key,node in idg.nodes.iteritems()))

		#Loop until we have visited all nodes
		while(len(num_deps)>0):
			#Gather the keys of all nodes with no dependences
			no_deps=[dep_key for dep_key in num_deps if 0==num_deps[dep_key]]

			#If no nodes have no dependences then a cycle exists
			if 0==len(no_deps):
				raise ValueError('A cycle exists in the IDG!')

			#Visit all nodes with no dependences
			#Remove the node from the 'graph'
			# and update dependence counts accordingly
			for dep_key in no_deps:
				#Visit the node
				idg.nodes[dep_key].apply_visitor(self)

				#Reduce the dependence counts
				for use_key in idg.nodes[dep_key].uses:
					num_deps[use_key]-=1

				#Remove the node from dependence counts
				del num_deps[dep_key]

		return self

	#These may seem redundant in combination with the 'At Methods'
	# but they may be useful if we need to do something before calling
	# the 'at' method
	#Just another level of indirection for posterity
	def visitIDGSymbolic(self,node): self.atIDGSymbolic(node)
	def visitIDGDataArray(self,node): self.atIDGDataArray(node)
	def visitIDGERSpec(self,node): self.atIDGERSpec(node)
	def visitIDGIndexArray(self,node): self.atIDGIndexArray(node)
	def visitIDGOutputERSpec(self,node): self.atIDGOutputERSpec(node)
	def visitIDGGenERSpec(self,node): self.atIDGGenERSpec(node)
	def visitIDGGenOutputERSpec(self,node): self.atIDGGenOutputERSpec(node)
	def visitIDGCall(self,node): self.atIDGCall(node)
	#-----------------------------------
#-----------------------------------------
