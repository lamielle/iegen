# Definitions of the Set and Relation classes that represent Presburger Sets and Relations.

from cStringIO import StringIO
from copy import deepcopy
from iegen import Symbolic
from iegen.ast import Node,PresSet,PresRelation,Conjunction,Equality,Inequality,NormExp,VarExp
from iegen.ast.visitor import RenameVisitor,CollectVarsVisitor,FindFunctionsVisitor,CollectSymbolicsVisitor,CollectBoundsVisitor
from iegen.parser import PresParser
from iegen.lib.decorator import decorator
from iegen.util import normalize_self,normalize_result,check,like_type,raise_objs_not_like_types

#---------- Formula class ----------
#Parent class for Sets and Relations
class Formula(Node):
	__slots__=('formulas',)

	def __str__(self,formulas):
		s=StringIO()
		for formula in formulas:
			s.write('%s%s'%(str(formula),' union '))
		return s.getvalue()[:-7]

	#Returns True if this Formula is a true statement (any terms in its union are tautologies)
	#Returns False otherwise
	#Determines the 'truthiness' of the formula (thanks Colbert!)
	def is_tautology(self):
		res=False
		for formula in self.formulas:
			res=res or formula.is_tautology()
		return res

	#Returns True if this Formula is a false statement (all terms in its union are contradictions)
	#Returns False otherwise
	#Determines the 'truthiness' of the formula (thanks Colbert!)
	def is_contradiction(self):
		res=True
		for formula in self.formulas:
			res=res and formula.is_contradiction()
		return res

	#Returns a sorted list of all tuple variables present in this formula
	def variables(self):
		return CollectVarsVisitor().visit(self).vars

	#Returns a list of all functions that are present in this formula's constraints
	def functions(self):
		return FindFunctionsVisitor().visit(self).functions

	#Returns a list of the names of all symbolics that are present in this formula's constraints
	def symbolics(self):
		return CollectSymbolicsVisitor().visit(self).symbolics

	#Copies the constraints from the two given formulas (from{1,2})
	# and appends them to the given formula (form)
	def _copy_constraints(self,form,from1,from2):
		for constraint in from1.conjunct.constraints+from2.conjunct.constraints:
			form.conjunct.constraints.append(deepcopy(constraint))

	#Appends equality constraints for each pair of variables in vars1 and vars2
	#This implies that var1 and var2 must have the same length
	def _create_equality_constraints(self,form,vars1,vars2):
		#Create an equality constraint for each pair of variables
		for i in xrange(len(vars1)):
			#Get the variables from the formulas
			var1=deepcopy(vars1[i])
			var2=deepcopy(vars2[i])

			#Set the coefficients on the variables: var1=var2 -> var1-var2=0
			var1.coeff=1
			var2.coeff=-1

			#Create a constraint where these variables are equal
			constraint=Equality(NormExp([var1,var2],0))

			#Add the new constraint to the formula
			form.conjunct.constraints.append(constraint)

	#Creates a dictionary of var.id -> var.id+suffix
	# for each given variable.
	#Runs RenameVisitor using this dictionary on the given formula
	def _rename_vars(self,form,vars,suffix):
		rename={}
		for var in vars:
			rename[var.id]=var.id+suffix
		RenameVisitor(rename).visit(form)

	#Creates a dictionary of var.id+suffix -> var.id
	# for each given variable.
	#Runs RenameVisitor using this dictionary on the given formula
	def _unrename_vars(self,form,vars,suffix):
		rename={}
		for var in vars:
			rename[var.id+suffix]=var.id
		RenameVisitor(rename).visit(form)

	#Creates a dictionary for renaming variables in a formula
	#The new names are prefixed with the given prefix
	def _get_prefix_rename_dict(self,formula,prefix):
		rename={}

		#Make sure we are given a PresSet or a PresRelation
		raise_objs_not_like_types(formula,[PresSet,PresRelation])

		if like_type(formula,PresSet):
			for var in formula.tuple_set.vars:
				rename[var.id]=prefix+'_'+var.id
		else:
			for var in formula.tuple_in.vars:
				rename[var.id]=prefix+'_in_'+var.id
			for var in formula.tuple_out.vars:
				rename[var.id]=prefix+'_out_'+var.id

		return rename

	#Returns a dictionary that is the inverse of that returned by _get_prefix_rename_dict
	def _get_prefix_unrename_dict(self,formula,prefix,filter=''):
		from iegen.util import invert_dict

		#Build a new dictionary containing only those (k,v) pairs whose key contains the given filter string
		dict=invert_dict(self._get_prefix_rename_dict(formula,prefix))
		new_dict={}
		for k in dict:
			try:
				k.index(filter)
				new_dict[k]=dict[k]
			except: pass
		return new_dict

	#Creates a dictionary for renaming variables in a formula
	#The formula's names are renamed to the corresponding variables
	#in other_formula
	def _get_formula_rename_dict(self,formula,other_formula):
		rename={}

		#Make sure we are given a PresSet or a PresRelation
		raise_objs_not_like_types(formula,[PresSet,PresRelation])

		#Make sure the two sets have the same arity
		if formula.arity()!=other_formula.arity():
			raise ValueError('The given formulas differ in arity')

		if like_type(formula,PresSet):
			from_vars=formula.tuple_set.vars
			to_vars=other_formula.tuple_set.vars
			for i in xrange(len(from_vars)):
				rename[from_vars[i].id]=to_vars[i].id
		else:
			from_vars=formula.tuple_in.vars
			to_vars=other_formula.tuple_in.vars
			for i in xrange(len(from_vars)):
				rename[from_vars[i].id]=to_vars[i].id
			from_vars=formula.tuple_out.vars
			to_vars=other_formula.tuple_out.vars
			for i in xrange(len(from_vars)):
				rename[from_vars[i].id]=to_vars[i].id

		return rename
#-----------------------------------


#---------- Set class ----------
#Presburger Set that is a disjunction of a collection of PresSet instances
class Set(Formula):
	__slots__=('sets',)

	#Constructor for Set:
	#Takes EITHER a set string, ex {[a]: a>10}, in set_string
	#OR a collection of PresSet instances in sets
	#but NOT both
	#Also, an optional parameter, 'symbolics', is a collection
	#of instances of the iegen.Symbolic class.
	@normalize_self
	@check
	def __init__(self,set_string=None,symbolics=None,sets=None):
		symbolics=[] if symbolics is None else symbolics
		if None is not set_string and None is sets:
			#Ensure we are given Symbolic objects
			raise_objs_not_like_types(symbolics,Symbolic,'Set construction failure: symbolics must be a collect of objects that look like a Symbolic')

			self.sets=[PresParser.parse_set(set_string,symbolics)]
		elif None is not sets and None is set_string:
			if len(symbolics)>0:
				raise ValueError('Cannot specify symbolics when specifying a collection of sets.')
			if len(sets)>0:
				self.sets=sets
			else:
				raise ValueError('Must specify at least one set in the sets collection.')
		else:
			raise ValueError('Set.__init__ takes either a set string or a collection of sets.')

	def __repr__(self):
		return "Set(sets=%s)"%(self.sets)

	def __str__(self):
		return Formula.__str__(self,self.sets)

	#Sets property wrapper for the formulas collection
	def get_sets(self): return self.formulas
	def set_sets(self,sets): self.formulas=sets
	sets=property(get_sets,set_sets)

	#Comparison operator
	def __cmp__(self,other):
		#Compare Sets by their set collection
		if like_type(other,Set):
			return cmp(self.sets,other.sets)
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	#Returns the arity (size of the tuples) of this set
	#Assumption: All PresSet instances in sets have the same arity
	#This should be checked with _arity_check upon creation
	def arity(self):
		if len(self.sets)>0:
			return self.sets[0].arity()
		else:
			raise ValueError('Cannot determine arity of a Set that contains no sets.')

	def apply_visitor(self,visitor):
		visitor.visitSet(self)

	#Adds all of the PresSets in the given Set to this Set
	def _add_set(self,set):
		if not like_type(set,Set):
			raise ValueError("Cannot add object of type '%s' to Set."%type(set))
		self.sets.extend(set.sets)

	#Takes the union of this Set and the given Set
	@normalize_result
	def union(self,other):
		if like_type(other,Set):
			if self.arity()==other.arity():
				selfcopy=deepcopy(self)
				other=deepcopy(other)
				selfcopy._add_set(other)
			else:
				raise ValueError("Cannot union sets with differing arity: '%s' (arity %d) and '%s' (arity %d)"%(self,self.arity(),other,other.arity()))
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))

		self.print_debug('Set Union: %s.union(%s)=%s'%(self,other,selfcopy))

		return selfcopy

	#Application of a relation to a set: other(self)
	#Application of unions of relations to unions of sets is defined as:
	#Let S=S1 union S2 union ... union SN
	#Let R=R1 union R2 union ... union RM
	#
	#Then R(S)=R1(S1) union R1(S2) union ... union R1(SN) union
	#          R2(S1) union R2(S2) union ... union R2(SN) union
	#          ...
	#          RM(S1) union RM(S2) union ... union RM(SN)
	@normalize_result
	def apply(self,other):
		#Make sure we are given a Relation
		raise_objs_not_like_types(other,Relation,'Apply failure: Can only apply objects that look like a Relation object to a Set')

		#Make sure the arities are valid
		if other.arity_in()!=self.arity():
			raise ValueError('Apply failure: Input arity of relation (%d) does not match arity of set (%d)'%(other.arity_out(),self.arity()))

		#Collection of new applied sets
		new_sets=[]

		for set in self.sets:
			for rel in other.relations:
				new_sets.append(self._apply(set,rel))

		new_set=Set(sets=new_sets)

		self.print_debug('Apply: %s.apply(%s)=%s'%(self,other,new_set))

		return new_set

	#Private utility method to perform the apply operation between a PresSet and a PresRelation
	#Returns the PresSet resulting from the apply operation rel(set)
	def _apply(self,set,rel):
		#Make sure we are given a PresSet and a PresRelation
		raise_objs_not_like_types(set,PresSet)
		raise_objs_not_like_types(rel,PresRelation)

		#Make sure the arities are valid
		if rel.arity_in()!=set.arity():
			raise ValueError('Apply failure: Input arity of relation (%d) does not match arity of set (%d)'%(rel.arity_out(),set.arity()))

		#Copy the given set and relation
		set_copy=deepcopy(set)
		rel_copy=deepcopy(rel)

		#Rename tuple variables by appending '1' and '2'
		self._rename_vars(set_copy,set_copy.tuple_set.vars,'1')
		self._rename_vars(rel_copy,rel_copy.tuple_in.vars+rel_copy.tuple_out.vars,'2')

		#Create the new set that will end up being the final result
		new_tuple_set=deepcopy(rel_copy.tuple_out)
		new_symbolics=deepcopy(set_copy.symbolics)+deepcopy(rel_copy.symbolics)
		new_set=PresSet(new_tuple_set,Conjunction([]),new_symbolics)

		#Copy over the constraints from the set and relation
		self._copy_constraints(new_set,set_copy,rel_copy)

		#Add equality constraints for set_tuple = rel_tuple_in
		self._create_equality_constraints(new_set,set_copy.tuple_set.vars,rel_copy.tuple_in.vars)

		#Rename the resulting tuple back to the original names
		self._unrename_vars(new_set,rel.tuple_in.vars+rel.tuple_out.vars,'2')

		return new_set

	#Returns the lower bound of the given tuple variable
	def lower_bound(self,var_name):
		return self.bounds(var_name)[0]
	#Returns the upper bound of the given tuple variable
	def upper_bound(self,var_name):
		return self.bounds(var_name)[1]

	#Returns a 2-tuple of bounds on the given variable name:
	#-The first element is a collection of lower bound expressions
	#-The second element is a collection of upper bound expressions
	def bounds(self,var_name):
		#Make sure the given variable is a tuple variable
		if not self.sets[0].is_tuple_var(var_name):
			raise ValueError("'%s' is not a tuple variable"%(var_name))

		#Make a copy of myself
		mod_set=deepcopy(self)

		#Project out all other variables
		#XXX: Assumes bounds are only coming from the first set of the union
		for var in mod_set.sets[0].tuple_set.vars:
			if var_name!=var.id:
				mod_set._project_out(var.id)

		#Collect the bounds on the variable in question
		lower_bounds,upper_bounds=CollectBoundsVisitor(var_name).visit(mod_set).bounds
		lower_bounds=[exp for coeff,exp,ineq in lower_bounds]
		upper_bounds=[exp for coeff,exp,ineq in upper_bounds]
		return (lower_bounds,upper_bounds)

	#Projects the variable with the given name out of the constraints of this Set
	#Destructive call: 'self' is modified rather than creating a new set
	@normalize_self
	def _project_out(self,var_name):
		lower_bounds,upper_bounds=CollectBoundsVisitor(var_name).visit(self).bounds

		#Fourier-Motzkin Main Loop
		#Look at all pairs of upper and lower bounds
		first_lb=True
		for lb_coeff,lb_exp,lb_ineq in lower_bounds:
			#Remove the lower bound from the constraints
			self.sets[0].conjunct.constraints.remove(lb_ineq)
			for ub_coeff,ub_exp,ub_ineq in upper_bounds:
				#Remove the upper bound from the constraints (first time only)
				if first_lb: self.sets[0].conjunct.constraints.remove(ub_ineq)

				#Create a new constraint with the variable being projected out removed
				new_ineq=Inequality(NormExp([],ub_coeff)*lb_exp-(NormExp([],lb_coeff)*ub_exp))

				#Add the new constraint if it is not a tautology or contradiction
				if not new_ineq.is_tautology() and not new_ineq.is_contradiction():
					self.sets[0].conjunct.constraints.append(new_ineq)
			first_lb=False

		#Remove the variable from the tuple variables
		self.sets[0].tuple_set.vars.remove(VarExp(1,var_name))
#-------------------------------

#---------- Relation class ----------
class Relation(Formula):
	__slots__=('relations',)

	#Constructor for Relation:
	#Takes EITHER a relation string, ex {[a]->[a']: a>10}, in relation_string
	#OR a collection of PresRelation instances in relations
	#but NOT both
	#Also, an optional parameter, 'symbolics', is a collection
	#of instances of the iegen.Symbolic class.
	@normalize_self
	@check
	def __init__(self,relation_string=None,symbolics=None,relations=None):
		symbolics=[] if symbolics is None else symbolics
		if None is not relation_string and None is relations:
			#Ensure we are given Symbolic objects
			raise_objs_not_like_types(symbolics,Symbolic,'Set construction failure: symbolics must be a collect of objects that look like a Symbolic')

			self.relations=[PresParser.parse_relation(relation_string,symbolics)]
		elif None is not relations and None is relation_string:
			if len(symbolics)>0:
				raise ValueError('Cannot specify symbolics when specifying a collection of relations.')
			if len(relations)>0:
				self.relations=relations
			else:
				raise ValueError('Must specify at least one relation in the relations collection')
		else:
			raise ValueError('Relation.__init__ takes either a relation string or a collection of relations.')

	def __repr__(self):
		return "Relation(relations=%s)"%(self.relations)

	def __str__(self):
		return Formula.__str__(self,self.relations)

	#Relations property wrapper for the formulas collection
	def get_relations(self): return self.formulas
	def set_relations(self,relations): self.formulas=relations
	relations=property(get_relations,set_relations)

	#Comparison operator
	def __cmp__(self,other):
		#Compare Relations by their relation collection
		if like_type(other,Relation):
			return cmp(self.relations,other.relations)
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	#Returns a tuple of the input and output arities of this relation
	#Assumption: All PresRelation instances in relations have the same input and output arities
	#This should be checked with _arity_check upon creation
	def arity(self):
		return (self.arity_in(),self.arity_out())

	#Returns the input arity of this relation
	#Assumption: All PresRelation instances in relations have the same input arity
	#This should be checked with _arity_check upon creation
	def arity_in(self):
		if len(self.relations)>0:
			return self.relations[0].arity_in()
		else:
			raise ValueError('Cannot determine input arity of a Relation that contains no relations.')

	#Returns the output arity of this relation
	#Assumption: All PresRelation instances in relations have the same output arity
	#This should be checked with _arity_check upon creation
	def arity_out(self):
		if len(self.relations)>0:
			return self.relations[0].arity_out()
		else:
			raise ValueError('Cannot determine output arity of a Relation that contains no relations.')

	def apply_visitor(self,visitor):
		visitor.visitRelation(self)

	#Adds all of the PresRelations in the given Relation to this Relation
	def _add_relation(self,relation):
		if not like_type(relation,Relation):
			raise ValueError("Cannot add object of type '%s' to Relation."%type(relation))
		self.relations.extend(relation.relations)

	#Takes the union of this Relation and the given Relation
	@normalize_result
	def union(self,other):
		if like_type(other,Relation):
			if self.arity_in()==other.arity_in() and self.arity_out()==other.arity_out():
				selfcopy=deepcopy(self)
				other=deepcopy(other)
				selfcopy._add_relation(other)
			else:
				raise ValueError('Cannot union relations with differing arity ((%d->%d) and (%d->%d)).'%(self.arity_in(),self.arity_out(),other.arity_in(),other.arity_out()))
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))

		self.print_debug('Relation Union: %s.union(%s)=%s'%(self,other,selfcopy))

		return selfcopy

	#Takes the inverse of all of the PresRelations in this Relation
	@normalize_result
	def inverse(self):
		selfcopy=deepcopy(self)
		for relation in selfcopy.relations:
			#Swap input and output tuples
			relation.tuple_in,relation.tuple_out=relation.tuple_out,relation.tuple_in

		self.print_debug('Relation Inverse: %s.inverse()=%s'%(self,selfcopy))

		return selfcopy

	#Relation composition: self(other)
	#Composition of unions of relations is defined as:
	#Let R1=R11 union R12 union ... union R1N
	#Let R2=R21 union R22 union ... union R2M
	#
	#Then R1(R2)=R11(R21) union R11(R22) union ... union R11(R2M) union
	#            R12(R21) union R12(R22) union ... union R12(R2M) union
	#            ...
	#            R1N(R21) union R1N(R22) union ... union R1N(R2M)
	@normalize_result
	def compose(self,other):
		#Make sure we are given a Relation
		raise_objs_not_like_types(other,Relation)

		#Make sure the arities are valid
		if other.arity_out()!=self.arity_in():
			raise ValueError('Compose failure: Output arity of second relation (%d) does not match input arity of first relation (%d)'%(other.arity_out(),self.arity_in()))

		#Collection of new composed relations
		new_relations=[]

		for rel1 in self.relations:
			for rel2 in other.relations:
				new_relations.append(self._compose(rel1,rel2))

		new_relation=Relation(relations=new_relations)

		self.print_debug('Compose: %s.compose(%s)=%s'%(self,other,new_relation))

		return new_relation

	#Private utility method to perform the compose operation between two PresRelation objects
	#Returns the PresRelation resulting from the composition operation r1(r2)
	def _compose(self,r1,r2):
		#Make sure we are given PresRelations
		raise_objs_not_like_types([r1,r2],PresRelation)

		#Make sure the arities are valid
		if r2.arity_out()!=r1.arity_in():
			raise ValueError('Compose failure: Output arity of second relation (%d) does not match input arity of first relation (%d)'%(r2.arity_out(),r1.arity_in()))

		#Copy the given relationsn
		r1_copy=deepcopy(r1)
		r2_copy=deepcopy(r2)

		#Rename tuple variables by appending '1' and '2'
		self._rename_vars(r1_copy,r1_copy.tuple_in.vars+r1_copy.tuple_out.vars,'1')
		self._rename_vars(r2_copy,r2_copy.tuple_in.vars+r2_copy.tuple_out.vars,'2')

		#Create the new relation that will end up being the final result
		new_tuple_in=deepcopy(r2_copy.tuple_in)
		new_tuple_out=deepcopy(r1_copy.tuple_out)
		new_symbolics=deepcopy(r1_copy.symbolics)+deepcopy(r2_copy.symbolics)
		new_rel=PresRelation(new_tuple_in,new_tuple_out,Conjunction([]),new_symbolics)

		#Copy over the constraints from the relations
		self._copy_constraints(new_rel,r1_copy,r2_copy)

		#Add equality constraints for r2_out = r1_in
		self._create_equality_constraints(new_rel,r2_copy.tuple_out.vars,r1_copy.tuple_in.vars)

		#Rename the resulting tuple back to the original names if necessary
		r2_in_ids=[var.id for var in r2.tuple_in.vars]
		r1_out_ids=[var.id for var in r1.tuple_out.vars]
		if 0==len(set(r2_in_ids).intersection(set(r1_out_ids))):
			self._unrename_vars(new_rel,r1.tuple_out.vars,'1')
			self._unrename_vars(new_rel,r2.tuple_in.vars,'2')

		return new_rel
#------------------------------------
