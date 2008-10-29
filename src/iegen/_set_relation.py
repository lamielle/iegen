# Definitions of the Set and Relation classes that represent Presburger Sets and Relations.

from cStringIO import StringIO
from iegen.ast import Node
from iegen.parser import PresParser
from iegen.lib.decorator import decorator
from iegen.util import normalize_self,normalize_result,check,like_type,raise_objs_not_like_types

#---------- Formula class ----------
#Parent class for Sets and Relations
class Formula(Node):

	def __str__(self,formulas):
		s=StringIO()
		for formula in formulas:
			s.write('%s%s'%(str(formula),' union '))
		return s.getvalue()[:-7]

	#Private utility method that combines the given formulas
	#
	#form{1,2} are either PresSets or PresRelations
	#form{1,2}_tuple are strings that name the attribute of that formulas tuple
	#Equality constraints will be added between these tuples
	#These tuples MUST have the same arity
	#new_form is the new formula object that will be manipulated
	def _combine_pres_formulas(self,form1,form1_tuple,form2,form2_tuple,new_form):
		from copy import deepcopy
		from iegen.ast import Equality,NormExp
		from iegen.ast.visitor import RenameVisitor

		#Copy the formulas so this operation is using fresh copies of the objects
		form1=deepcopy(form1)
		form2=deepcopy(form2)

		#Create dictionaries for renaming the tuple variables
		form1_rename=self._get_rename_dict(form1,'form1')
		form1_unrename=self._get_unrename_dict(form1,'form1')
		form2_rename=self._get_rename_dict(form2,'form2')
		form2_unrename=self._get_unrename_dict(form2,'form2')

		#Rename the tuple varibles in form1 and form2
		RenameVisitor(form1_rename).visit(form1)
		RenameVisitor(form2_rename).visit(form2)

		#Get the formula variable tuples
		form1_tuple=getattr(form1,form1_tuple)
		form2_tuple=getattr(form2,form2_tuple)

		#Add equality constraints for form1_tuple = form2_tuple
		for i in xrange(len(form1_tuple.vars)):
			#Get the variables from the formulas
			var1=deepcopy(form1_tuple.vars[i])
			var2=deepcopy(form2_tuple.vars[i])

			#Set the coefficients on the variables:
			#var1=var2 -> var1-var2=0
			var1.coeff=1
			var2.coeff=-1

			#Create a constraint where these variables are equal
			constraint=Equality(NormExp([var1,var2],0))

			#Add the new constraint to the new relation
			new_form.conjunct.constraint_list.append(constraint)

		#Add the constraints of both relations to the new relation
		for constraint in form1.conjunct.constraint_list+form2.conjunct.constraint_list:
			new_form.conjunct.constraint_list.append(deepcopy(constraint))

		#Rename the variables back to what the were before
		RenameVisitor(form1_unrename).visit(new_form)
		RenameVisitor(form2_unrename).visit(new_form)

		return new_form

	#Creates a dictionary for renaming variables in a relation
	def _get_rename_dict(self,formula,prefix):
		from iegen.ast import PresSet,PresRelation

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

	#Returns a dictionary that is the inverse of that returned by _get_rename_dict
	def _get_unrename_dict(self,relation,prefix):
		from iegen.util import invert_dict
		return invert_dict(self._get_rename_dict(relation,prefix))
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
		from copy import deepcopy

		if like_type(other,Set):
			if self.arity()==other.arity():
				self=deepcopy(self)
				other=deepcopy(other)
				self._add_set(other)
			else:
				raise ValueError('Cannot union sets with differing arity (%d and %d).'%(self.arity(),other.arity()))
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))

		return self

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
		from copy import deepcopy

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

		return Set(sets=new_sets)

	#Private utility method to perform the apply operation between a PresSet and a PresRelation
	#Returns the PresSet resulting from the apply operation rel(set)
	def _apply(self,set,rel):
		from copy import deepcopy
		from iegen.ast import PresSet,PresRelation,Conjunction
		from iegen.ast.visitor import RenameVisitor

		#Make sure we are given a PresSet and a PresRelation
		raise_objs_not_like_types(set,PresSet)
		raise_objs_not_like_types(rel,PresRelation)

		#Make sure the arities are valid
		if rel.arity_in()!=set.arity():
			raise ValueError('Apply failure: Input arity of relation (%d) does not match arity of set (%d)'%(rel.arity_out(),set.arity()))

		return self._combine_pres_formulas(set,'tuple_set',rel,'tuple_in',PresSet(deepcopy(rel.tuple_out),Conjunction([]),deepcopy(set.symbolics)+deepcopy(rel.symbolics)))

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
		from copy import deepcopy
		from iegen.ast.visitor import CollectBoundsVisitor

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
				mod_set.sets[0].tuple_set.vars.remove(var)

		#Collect the bounds on the variable in question
		lower_bounds,upper_bounds=CollectBoundsVisitor(var_name).visit(mod_set).bounds
		lower_bounds=[exp for coeff,exp,ineq in lower_bounds]
		upper_bounds=[exp for coeff,exp,ineq in upper_bounds]
		return (lower_bounds,upper_bounds)

	#Projects the variable with the given name out of the constraints of this Set
	#Destructive call: 'self' is modified rather than creating a new set
	@normalize_self
	def _project_out(self,var_name):
		from iegen.ast import Inequality,NormExp
		from iegen.ast.visitor import CollectBoundsVisitor

		lower_bounds,upper_bounds=CollectBoundsVisitor(var_name).visit(self).bounds
		#Fourier-Motzkin Main Loop
		#Look at all pairs of upper and lower bounds
		first_lb=True
		for lb_coeff,lb_exp,lb_ineq in lower_bounds:
			#Remove the lower bound from the constraints
			self.sets[0].conjunct.constraint_list.remove(lb_ineq)
			for ub_coeff,ub_exp,ub_ineq in upper_bounds:
				#Remove the upper bound from the constraints (first time only)
				if first_lb: self.sets[0].conjunct.constraint_list.remove(ub_ineq)

				#Add a new constraint with the variable being projected out removed
				new_ineq=Inequality(NormExp([],ub_coeff)*lb_exp-(NormExp([],lb_coeff)*ub_exp))
				self.sets[0].conjunct.constraint_list.append(new_ineq)
			first_lb=False
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
		from copy import deepcopy

		if like_type(other,Relation):
			if self.arity_in()==other.arity_in() and self.arity_out()==other.arity_out():
				self=deepcopy(self)
				other=deepcopy(other)
				self._add_relation(other)
			else:
				raise ValueError('Cannot union relations with differing arity ((%d->%d) and (%d->%d)).'%(self.arity_in(),self.arity_out(),other.arity_in(),other.arity_out()))
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))

		return self

	#Takes the inverse of all of the PresRelations in this Relation
	@normalize_result
	def inverse(self):
		from copy import deepcopy

		self=deepcopy(self)
		for relation in self.relations:
			#Swap input and output tuples
			relation.tuple_in,relation.tuple_out=relation.tuple_out,relation.tuple_in

		return self

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
		from copy import deepcopy

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

		return Relation(relations=new_relations)

	#Private utility method to perform the compose operation between two PresRelation objects
	#Returns the PresRelation resulting from the composition operation r1(r2)
	def _compose(self,r1,r2):
		from copy import deepcopy
		from iegen.ast import PresRelation,Conjunction,Equality,NormExp
		from iegen.ast.visitor import RenameVisitor

		#Make sure we are given PresRelations
		raise_objs_not_like_types([r1,r2],PresRelation)

		#Make sure the arities are valid
		if r2.arity_out()!=r1.arity_in():
			raise ValueError('Compose failure: Output arity of second relation (%d) does not match input arity of first relation (%d)'%(r2.arity_out(),r1.arity_in()))

		return self._combine_pres_formulas(r1,'tuple_in',r2,'tuple_out',PresRelation(deepcopy(r2.tuple_in),deepcopy(r1.tuple_out),Conjunction([]),deepcopy(r1.symbolics)+deepcopy(r2.symbolics)))
#------------------------------------
