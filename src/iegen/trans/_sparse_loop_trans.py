from cStringIO import StringIO
from iegen.trans import Transformation

#---------- SparseLoopTrans class ----------
class SparseLoopTrans(Transformation):
	__slots__=('statement_name',)

	def __init__(self,statement_name):
		Transformation.__init__(self,name)

		self.statement_name=statement_name

	def __repr__(self):
		return 'SparseLoopTrans(%s)'%(self.name,self.statement_name)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent

		inputs_string=StringIO()
		if len(self.inputs)>0:
			for input in self.inputs:
				print >>inputs_string,input._get_string(indent+5)
		inputs_string=inputs_string.getvalue()[:-1]
		if len(inputs_string)>0: inputs_string='\n'+inputs_string

		outputs_string=StringIO()
		if len(self.outputs)>0:
			for output in self.outputs:
				print >>outputs_string,output._get_string(indent+5)
		outputs_string=outputs_string.getvalue()[:-1]
		if len(outputs_string)>0: outputs_string='\n'+outputs_string

		return '''%sSparseLoopTrans:
%s|-name: %s
%s|-inputs: %s
%s|-outputs: %s
%s|-statement_name: %s'''%(spaces,spaces,self.name,
    spaces,inputs_string,
    spaces,outputs_string,
    spaces,self.statement_name,)

	#Calculate the inputs to the sparse loop optimization
	def calc_input(self,mapir):
		pass

	#Calculate the output from the sparse loop optimization
	def calc_output(self,mapir):
		pass

	#Update the MapIR based on this transformation
	def update_mapir(self,mapir):
		pass

	def update_idg(self,mapir):
		pass
#-------------------------------------------
