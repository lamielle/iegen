from iegen.ast.visitor import DFVisitor


# This visitor takes list of function names as input and
# returns a list of FuncNest objects.  A FuncNest object
# contains references to the outermost FuncExp and innermost
# FuncExp for AST subtrees that match the given nest pattern.
#
class FuncNest:
	__slots__=('outer_node','inner_node')
	
	def __init__(self,outer,inner):
		self.outer_node = outer
		self.inner_node = inner

	def __repr__(self):
		return 'FuncNest(%s,%s)'%(self.outer_node.__repr__,
			self.inner_node.__repr__)

	def __str__(self):
		return self.__repr__


class FindFuncNestVisitor(DFVisitor):
	__slots__=('nest_spec','nestrefs')

	#At construction pass in list of strings that specify nest.
	#For example, ['f','g'] will cause the visitor to look for
	#the nest f(g(*))
	def __init__(self,nest):
		self.nest_spec = nest
		self.nestrefs = []
		self._curr_index = 0
		
	def inFuncExp(self,node):
		#Determine if this function matches the next function
		#name in our pattern.
		if node.name==self.nest_spec[self._curr_index]:
			#If this is the first function in the pattern
			#then record this node as a possible candidate.
			if self._curr_index==0:
				self._candidate = node

			#If pattern is done then put candidate in nestrefs
			#and reset.
			if self._curr_index==(len(self.nest_spec)-1):
				self.nestrefs.append(FuncNest(self._candidate,node))
				self._curr_index=0

			else:
				self._curr_index = self._curr_index+1


