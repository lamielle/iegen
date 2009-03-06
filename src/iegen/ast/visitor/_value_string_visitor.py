import os
from iegen.ast.visitor import DFVisitor

#Produces a string for a NormExp that is the value of that expression
#If functions are present, uses the runtime library functions to
#look up the value of the input to the function
#
#The resulting string is placed in the 'value' field
class ValueStringVisitor(DFVisitor):
	def __init__(self,raw_array=False):
		from cStringIO import StringIO
		self._value=StringIO()

		#True if raw array accesses should be used, otherwise ER accesses will be used
		self.raw_array=raw_array

	def _get_value(self): return self._value.getvalue()
	value=property(_get_value)

	def defaultIn(self,node):
		raise ValueError("Nodes of type '%s' are not supported."%(type(node)))

	def inVarExp(self,node):
		self._value.write(str(node))
	def outVarExp(self,node):
		pass

	def inFuncExp(self,node):
		if self.raw_array:
			self._value.write('%s['%(node.name))
		else:
			self._value.write('ER_out_given_in(%s_ER,'%(node.name))
	def outFuncExp(self,node):
		if self.raw_array:
			self._value.write(']')
		else:
			self._value.write(')')

	def inNormExp(self,node):
		self.multi_terms=False
	def betweenNormExp(self,node):
		self.multi_terms=True
		self._value.write('+')
	def outNormExp(self,node):
		if len(node.terms)>0 and 0!=node.const: self._value.write('+')
		if 0!=node.const: self._value.write(str(node.const))
		self.multi_terms=False
