from iegen.ito import InterTransOpt
from iegen.ast.visitor import FindFuncNestVisitor
from iegen import ERSpec,Relation
from iegen.idg import IDGERSpec, IDGGenOutputERSpec, IDGOutputERSpec

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
		self.print_progress("PointerUpdate.apply looking for nest patterns")

		#Look for each of the nest patterns in each of the ERSpecs.
		for nest in self.nests:
			#Search the MapIR for any instances of the current nesting
			#Collapse any instances that are found
			affected_er_specs,found_nest=self.collapse_nest(nest,mapir)

			#If we found a nesting anywhere above...
			if found_nest:
				#Create an ERSpec for the collapsed functions
				newfunc_ERSpec = self.create_ERSpec(nest,mapir)

				self.print_detail("\tnewfunc_ERSpec = %s"%newfunc_ERSpec)

			#Modify the IDG by removing old dependences coming
			#from individual functions, putting in a new dependences
			#between the new function ERSpec and where it will be
			#now used, and putting dependences between the individual
			#functions and the new function ERSpec.
			self.update_IDG_for_newfunc(mapir,newfunc_ERSpec,affected_er_specs,nest)

	#Searches for the given function nest in the given MapIR
	#
	#Returns (affected_er_specs,found_nest):
	#affected_er_specs: ERSpecs that contain the given nest
	#found_nest: True if the given nest was found anywhere
	def collapse_nest(self,nest,mapir):
		affected_er_specs=[]
		found_nest=False

		#Search for the given nest in the MapIR and replace any occurrences
		# of the given nest
		#Also create ERSpecs for the replaced nestings and update the IDG

		#Search for nests in the ERSpecs
		for er_spec in mapir.get_er_specs():
			self.print_detail("\ter_spec = %s"%er_spec)
			if er_spec.relation.contains_nest(nest):
				affected_er_specs.append(er_spec)
				er_spec.relation=er_spec.relation.copy(collapse=[nest])
				found_nest=True

		#Search for nests in the scattering functions and access relations.
		for statement in mapir.get_statements():
			self.print_detail("\tstatement.scatter = %s"%(statement.scatter))

			if statement.scatter.contains_nest(nest):
				#Replace the scattering function with a collapsed relation
				statement.scatter=statement.scatter.copy(collapse=[nest])
				found_nest=True

			#Search for nests in the current statement's access relations
			for access_relation in statement.get_access_relations():
				self.print_detail("\taccess_relation = %s"%access_relation)

				if access_relation.iter_to_data.contains_nest(nest):
					access_relation.iter_to_data=access_relation.iter_to_data.copy(collapse=[nest])
					found_nest=True

		return (affected_er_specs,found_nest)

	#Returns the ERSpec for the collapsed function.
	#Input: nest specification ["f","g"] and mapir
	#Output: ERSpec for f_g
	def create_ERSpec(self,nest,mapir):
		# concatenate function names to create new function name
		newfunc='_'.join(nest)
		self.print_detail("\tnewfunc = %s"%newfunc)

		# use domain of innermost function symbol as domain
		inner_ERSpec = mapir.er_specs[nest[-1]]
		inner_domain = inner_ERSpec.input_bounds.copy()
		# use range of outermost function symbol as range
		outer_ERSpec = mapir.er_specs[nest[0]]
		outer_range = outer_ERSpec.output_bounds.copy()

		#FIXME: currently assuming that domain and range
		#are both 1D.  At some point we may want to remove
		#this restriction.
		if 1!=inner_domain.arity():
			raise ValueError('Domain arity is not 1')
		if 1!=outer_range.arity():
			raise ValueError('Range arity is not 1')

		#Create ERSpec
		#Explicit relation is a function because it is
		#the composition of two uninterpreted functions.
		new_ERSpec=ERSpec(
		     name=newfunc,
		     input_bounds=inner_domain,
		     output_bounds=outer_range,
		     is_function=True,
		     relation=Relation('{[i] -> [j] : j=%s(i%s}'%('('.join(nest),')'*len(nest)))
		     )
		mapir.add_er_spec(new_ERSpec)

		return new_ERSpec

	#Input:
	#   mapir: The MapIR data structure.
	#   newfunc_ERSpec: ERSpec for new function
	#   affected_er_specs: ERSpecs that had nest, which will be replaced with
	#       new function.
	#   nest: list of function name strings that specify nest, ["f","g"] #
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
		gen_newfunc_node=mapir.idg.get_node(IDGGenOutputERSpec,newfunc_ERSpec)

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
