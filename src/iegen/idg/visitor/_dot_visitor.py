from __future__ import with_statement
from iegen.idg.visitor import TopoVisitor
from cStringIO import StringIO

class DotVisitor(TopoVisitor):

	def __init__(self):
		TopoVisitor.__init__(self)
		self.dot_body=StringIO()

	def write_dot(self,file_name):
		with open(file_name,'w') as dot_file:
			print >>dot_file,'digraph IDG'
			print >>dot_file,'{'
			for line in self.dot_body.getvalue().strip().split('\n'):
				if len(line)>0:
					print >>dot_file,'  '+line
				else:
					print >>dot_file
			print >>dot_file,'}'

	def writeln(self,s=''): print >>self.dot_body,s
	def write(self,s): print >>self.dot_body,s,

	def write_node_def(self,name,text=None,shape=None):
		if not text and not shape:
			self.writeln('%s;'%(name))
		else:
			if not shape:
				self.writeln('%s [ label="%s" ];'%(name,text))
			else:
				self.writeln('%s [ label="%s" shape=%s];'%(name,text,shape))

	def write_node_uses(self,node):
		for use in node.uses:
			self.writeln('%s -> %s;'%(node.key,use))
		self.writeln()

	def atIDGSymbolic(self,node):
		self.write_node_def(node.key,'IDGSymbolic\\n%s'%(node.data.name),'rectangle')
		self.write_node_uses(node)

	def atIDGDataArray(self,node):
		self.write_node_def(node.key,'IDGDataArray\\n%s: %d'%(node.data.data_array.name,node.data.version),'rectangle')
		self.write_node_uses(node)

	def atIDGERSpec(self,node):
		self.write_node_def(node.key,'IDGERSpec\\n%s'%(node.data.name),'rectangle')
		self.write_node_uses(node)

	def atIDGIndexArray(self,node):
		self.write_node_def(node.key,'IDGIndexArray\\n%s'%(node.data.name),'rectangle')
		self.write_node_uses(node)

	def atIDGOutputERSpec(self,node):
		self.write_node_def(node.key,'IDGOutputERSpec\\n%s'%(node.data.name),'rectangle')
		self.write_node_uses(node)

	def atIDGDataDep(self,node):
		self.write_node_def(node.key,'IDGDataDep\\n%s'%(node.data.name),'rectangle')
		self.write_node_uses(node)

	def atIDGGenERSpec(self,node):
		self.write_node_def(node.key,'IDGGenERSpec\\n%s'%(node.data.name))
		self.write_node_uses(node)

	def atIDGGenOutputERSpec(self,node):
		self.write_node_def(node.key,'IDGGenOutputERSpec\\n%s'%(node.data.name))
		self.write_node_uses(node)

	def atIDGGenDataDep(self,node):
		self.write_node_def(node.key,'IDGGenDataDep\\n%s'%(node.data.name))
		self.write_node_uses(node)

	def atIDGCall(self,node):
		self.write_node_def(node.key,'IDGCall\\n%s'%(node.data.function_name))
		self.write_node_uses(node)
