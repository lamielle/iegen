from cStringIO import StringIO
from iegen.trans import Transformation

#---------- IterAlignTrans class ----------
class IterAlignTrans(Transformation):
	__slots__=('iter_space_trans',)
#	_relation_fields=('iter_space_trans',)

	def __init__(self,name,iter_space_trans):
		Transformation.__init__(self,name)
		self.iter_space_trans=iter_space_trans

	def __repr__(self):
		return 'IterAlignTrans(%s)'%(self.iter_space_trans)

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

		return '''%sIterAlignTrans:
%s|-name: %s
%s|-inputs: %s
%s|-outputs: %s
%s|-iter_space_trans: %s'''%(spaces,spaces,self.name,
    spaces,inputs_string,
    spaces,outputs_string,
    spaces,self.iter_space_trans)

	#Nothing to do as no inputs and outputs exist for this transformation
	def calc_input(self,mapir): pass
	def calc_output(self,mapir): pass

	#Update access relations based on the specified transformation
	def update_mapir(self,mapir):
		#Update the access relations of all statements
		self.print_progress('Updating access relations for IterAlignTrans...')
		for statement in mapir.get_statements():
			for access_relation in statement.get_access_relations():
				self.print_detail("Updating access relation '%s'..."%(access_relation.name))
				access_relation.iter_to_data=access_relation.iter_to_data.compose(self.iter_space_trans.inverse())

	#This transformation only needs to modify the MapIR, because if
	#any inverse ERs were needed then they should be determined
	#somewhere else.
	def update_idg(self,mapir): pass
#-------------------------------------------
