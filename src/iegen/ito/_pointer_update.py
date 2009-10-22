from iegen.ito import InterTransOpt
from iegen.ast.visitor import FindFuncNestVisitor

#---------- PointerUpdate class ----------
class PointerUpdate(InterTransOpt):
	__slots__=('nests',)

	def __init__(self,name,nests):
		InterTransOpt.__init__(self,name)
		self.nests = nests

	def __repr__(self):
		return 'PointerUpdate(%s,%s)'%(self.name,self.nests)

	def __str__(self):
		return self._get_string(0)

	def _get_string(self,indent):
		if indent>0: indent+=1
		spaces=' '*indent

		return '''%sPointerUpdate:
%s|-name: %s
%s|-nests: %s'''%(spaces,spaces,self.name,spaces,self.nests)


	def apply(self,mapir):
		self.print_detail("PointerUpdate.apply looking for nest patterns")

		#Look for each of the nest patterns in each of the ERSpecs.
		for nest in self.nests:
			nestrefs = []
			for er_spec in mapir.er_specs.values():
				self.print_detail("\ter_spec = %s"%er_spec)
				nestrefs.extend(
					FindFuncNestVisitor(nest).visit(er_spec.relation).nestrefs)
				self.print_detail("\tnestrefs = %s\n"%nestrefs)

			for stmt in mapir.statements.values():
				self.print_detail("\tstmt.scatter = %s"%(stmt.scatter))
				nestrefs.extend(
					FindFuncNestVisitor(nest).visit(stmt.scatter).nestrefs)
				self.print_detail("\tnestrefs = %s\n"%nestrefs)

				for ar in stmt.access_relations.values():
					self.print_detail("\tar = %s"%ar)
					nestrefs.extend(
						FindFuncNestVisitor(nest).visit(ar.iter_to_data).nestrefs)
					self.print_detail("\tnestrefs = %s\n"%nestrefs)
					
			#For this particular nest, if there are any nestdefs found
			#then create an ERSpec for nested function symbol.
			if len(nestrefs)>0:
				# concatenate function names to create new function name
				newfunc = ""
				for func in nest:
					newfunc = newfunc + func + "_"
				newfunc = newfunc[:-1]
				self.print_detail("\tnewfunc = %s"%newfunc)

				# use domain of innermost function symbol as domain
				#inner_domain = nestrefs[0].inner_node.?

				#Create ERSpec
				#ERSpec(
				#	name=newfunc,
				#	input_bounds=inner_domain,
				#	output_bounds=outer_range,
				#	relation=?
				#)


#-------------------------------------------
