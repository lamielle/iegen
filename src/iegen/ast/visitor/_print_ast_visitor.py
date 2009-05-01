from iegen.ast.visitor import DFVisitor

class PrintASTVisitor(DFVisitor):
	def __init__(self):
		self.tabsize = 0
		self.tab = ''
		
	def incrementTab(self):
		self.tabsize = self.tabsize + 2
		self.resetTabString()
		
	def decrementTab(self):
		self.tabsize = self.tabsize - 2
		self.resetTabString()
	    
	def resetTabString(self):
		self.tab = ''
		for i in range(0,self.tabsize):
			self.tab = self.tab + ' '
		
	def printTab(self):
		print 

	def defaultIn(self,node):
		print self.tab, repr(node), " __str__ = ", node
		self.incrementTab()

	def defaultOut(self,node):	
		self.decrementTab()		

