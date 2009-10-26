from iegen.ito import InterTransOpt
from iegen.ast.visitor import FindFuncNestVisitor
from iegen import ERSpec,Relation
from iegen.idg import IDGERSpec, IDGGenERSpec, IDGOutputERSpec

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
			#Look for a single nest pattern.
			(nestrefs, affected_er_specs) = self.find_nestrefs(nest,mapir)
			self.print_detail("\tnestrefs = %s\n"%nestrefs)
					
			#For this particular nest, if there are any nestdefs found
			#then create an ERSpec for nested function symbol.
			if len(nestrefs)>0:
				newfunc_ERSpec = self.create_ERSpec(nest,nestrefs[0],mapir)
				self.print_detail("\tnewfunc_ERSpec = %s"%newfunc_ERSpec)

				#For each of the nest references,
				#modify the outer function expression so that it now
				#calls the new function with the args from the innermost
				#function call.
				for nestref in nestrefs:
					nestref.outer_node.name = newfunc_ERSpec.name
					nestref.outer_node.args = nestref.inner_node.args

			#Modify the IDG by removing old dependences coming
			#from individual functions, putting in a new dependences
			#between the new function ERSpec and where it will be
			#now used, and putting dependences between the individual
			#functions and the new function ERSpec.
			self.update_IDG_for_newfunc(mapir,newfunc_ERSpec,affected_er_specs,nest)
					
	#Look for a nest patterns in each of the ERSpecs in mapir.
	#Input: list of function name strings that specify nest, ["f","g"]
	#Output: tuple with a list of FuncNest references for function nests 
    # that fit pattern and the list of ERSpecs in IDG where those patterns 
    # were found.
	def find_nestrefs(self,nest,mapir):
		nestrefs = []
		affected_er_specs = []

		#All of the ERSpecs in IDG and MapIR.
		for er_spec in mapir.er_specs.values():
			self.print_detail("\ter_spec = %s"%er_spec)
			found_nestrefs = \
				FindFuncNestVisitor(nest).visit(er_spec.relation).nestrefs
			if len(found_nestrefs)>0:
				nestrefs.extend(found_nestrefs)
				affected_er_specs.append(er_spec)
			self.print_detail("\tnestrefs = %s\n"%nestrefs)

		#The scattering functions and access relations.
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

		return (nestrefs,affected_er_specs)

	#Returns the ERSpec for the collapsed function.
	#Input: nest specification ["f","g"], example FuncNest/nestref, and mapir
	#Output: ERSpec for f_g
	def create_ERSpec(self,nest,nestref,mapir):
		# concatenate function names to create new function name
		newfunc = ""
		for func in nest:
			newfunc = newfunc + func + "_"
		newfunc = newfunc[:-1]
		self.print_detail("\tnewfunc = %s"%newfunc)

		# use domain of innermost function symbol as domain
		inner_ERSpec = mapir.er_specs[nestref.inner_node.name]
		inner_domain = inner_ERSpec.input_bounds.copy()
		# use range of outermost function symbol as range
		outer_ERSpec = mapir.er_specs[nestref.outer_node.name]
		outer_range = outer_ERSpec.output_bounds.copy()
	
		#Create ERSpec
		#Explicit relation is a function because it is
		#the composition of two uninterpreted functions.
		#FIXME: currently assuming that domain and range
		#are both 1D.  At some point we may want to remove
		#this restriction.
		#FIXME: Alan, how do I "assert" that the above is
		#true?  Also need to assert that inner function
		#calls have coefficients  of 1.
		return ERSpec(
			name=newfunc,
			input_bounds=inner_domain,
			output_bounds=outer_range,
			is_function=True,
			relation=Relation('{[i] -> [j] : j=%s(%s(i))}'%tuple(nest))
		)

	#Input: 
	#   mapir: The MapIR data structure.
	#   newfunc_ERSpec: ERSpec for new function
	#   affected_er_specs: ERSpecs that had nest, which will be replaced with
	#       new function.
	#   nest: list of function name strings that specify nest, ["f","g"]
	#
	#SideEffect:
	#   Modifies the IDG by removing old dependences coming
	#   from individual functions, putting in a new dependences
	#   between the new function ERSpec and where it will be
	#   now used, and putting dependences between the individual
	#   functions and the new function ERSpec.
	def update_IDG_for_newfunc(self,mapir,newfunc_ERSpec,affected_er_specs,nest):

		#Create node for new function ERSpec
		newfunc_node = mapir.idg.get_node(IDGOutputERSpec,newfunc_ERSpec)

		#Get a gen node for the ERSpec
		gen_newfunc_node=mapir.idg.get_node(IDGGenERSpec,newfunc_ERSpec)

		#Add dependence between the two.
		newfunc_node.add_dep(gen_newfunc_node)

		#For each of the ERSpecs that used to depend on the old
		#functions and now will depend on new function...
		for er_spec in affected_er_specs:
			er_node = mapir.idg.get_node(IDGERSpec,er_spec)

			#Remove dependence on old functions.
			for func_name in nest:
				func_node = mapir.idg.get_node(IDGERSpec, 
					mapir.er_specs[func_name])
				er_node.remove_dep(func_node)

			#Add dependence on new function.
			er_node.add_dep(newfunc_node)

		#Have new function node depend on old functions.
		for func_name in nest:
			func_node = mapir.idg.get_node(IDGERSpec, 
				mapir.er_specs[func_name])
			gen_newfunc_node.add_dep(func_node)

#-------------------------------------------
