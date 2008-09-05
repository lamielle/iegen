# Definitions of the Set and Relation classes that represent Presburger Sets and Relations.

from iegen.parser import PresParser

#---------- Formula class ----------
#Parent class for Sets and Relations
class Formula(object):

	#Uses the sort visitor to sort all lists in this formula and the ASTs it contains
	def _sort(self):
		from iegen.ast.visitor import SortVisitor
		SortVisitor().visit(self)

	#Check method that makes sure its argument 'looks like' a Set
	#Returns True if it does, False otherwise
	def _like_set(self,exp):
		if not hasattr(exp,'sets'):
			return False
		else:
			return True

	#Check method that makes sure its argument 'looks like' a Relation
	#Returns True if it does, False otherwise
	def _like_relation(self,exp):
		if not hasattr(exp,'relations'):
			return False
		else:
			return True

	#Check method that makes sure its argument 'looks like' a PresSet
	#Returns True if it does, False otherwise
	def _like_pres_set(self,exp):
		if not hasattr(exp,'tuple_set') or not hasattr(exp,'conjunct'):
			return False
		else:
			return True

	#Check method that makes sure its argument 'looks like' a PresRelation
	#Returns True if it does, False otherwise
	def _like_pres_relation(self,exp):
		if not hasattr(exp,'tuple_in') or not hasattr(exp,'tuple_out') or not hasattr(exp,'conjunct'):
			return False
		else:
			return True

	#Creates a dictionary for renaming variables in a relation
	def _get_rename_dict(self,relation,prefix):
		rename={}

		#Make sure we are given a PresRelation
		if not self._like_pres_relation(relation):
			raise ValueError("The given relation, '%s', must have the 'tuple_in', 'tuple_out', and 'conjunct' attributes."%relation)

		for var in relation.tuple_in.vars:
			rename[var.id]=prefix+'_in_'+var.id
		for var in relation.tuple_out.vars:
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
	def __init__(self,set_string=None,sets=None):
		if None!=set_string and None==sets:
			self.sets=[PresParser.parse_set(set_string)]
		elif None!=sets and None==set_string:
			if len(sets)>0:
				self.sets=sets
			else:
				raise ValueError('Must specify at least one set in the sets collection')
		else:
			raise ValueError('Set.__init__ takes either a set string or a collection of sets.')

		self._set_check()
		self._arity_check()
		self._sort()

	def __repr__(self):
		return "Set(sets=%s)"%(self.sets)

	#Comparison operator
	def __cmp__(self,other):
		#Compare Sets by their set collection
		if hasattr(other,'sets') and hasattr(other,'sets'):
			return cmp(self.sets,other.sets)
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	#Makes sure all sets 'look like' PresSets
	def _set_check(self):
		if len(self.sets)>0:
			for set in self.sets:
				if not hasattr(set,'tuple_set') or not hasattr(set,'conjunct'):
					raise ValueError("Object of type '%s' does not have the required attributes 'tuple_set' and 'conjunct'."%(type(set)))

	def _arity_check(self):
		if len(self.sets)>0:
			set_arity=self.sets[0].arity()
			for set in self.sets[1:]:
				if set.arity()!=set_arity:
					raise ValueError('All sets in a Set must have the same arity.')

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
		if not hasattr(set,'sets'):
			raise ValueError("Cannot add object of type '%s' to Set."%type(set))
		self.sets.extend(set.sets)

	#Takes the union of this Set and the given Set
	def union(self,other):
		from copy import deepcopy

		if hasattr(other,'sets'):
			if self.arity()==other.arity():
				self=deepcopy(self)
				other=deepcopy(other)
				self._add_set(other)
				self._sort()
				return self
			else:
				raise ValueError('Cannot union sets with differing arity (%d and %d).'%(self.arity(),other.arity()))
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))

	#Application of a relation to a set: self(other)
	#Application of unions of relations to unions of sets is defined as:
	#Let S=A union B
	#Let R=C union D
	#
	#Then R(S)=C(A) union C(B) union D(A) union D(B)
	def apply(self,other):
		from copy import deepcopy

		#Make sure we are given a Relation
		if not self._like_relation(other):
			raise ValueError('Apply failure: Can only apply objects that look like a Relation object to a Set')

		#Make sure the arities are valid
		if other.arity_in()!=self.arity():
			raise ValueError('Apply failure: Output arity of second relation (%d) does not match input arity of first relation (%d)'%(other.arity_out(),self.arity_in()))

		#Collection of new composed relations
		new_relations=[]

		for rel1 in self.relations:
			for rel2 in other.relations:
				new_relations.append(self._compose(rel1,rel2))

		return Relation(relations=new_relations)


#	#Given a collection of scattering functions for each statement
#	#Returns the code that iterates over the tuples in this set
#	#This code is generated by CLooG
#	#
##	def get_code():

#-------------------------------


#---------- Relation class ----------
class Relation(Formula):
	__slots__=('relations',)

	#Constructor for Relation:
	#Takes EITHER a relation string, ex {[a]->[a']: a>10}, in relation_string
	#OR a collection of PresRelation instances in relations
	#but NOT both
	def __init__(self,relation_string=None,relations=None):
		if None!=relation_string and None==relations:
			self.relations=[PresParser.parse_relation(relation_string)]
		elif None!=relations and None==relation_string:
			if len(relations)>0:
				self.relations=relations
			else:
				raise ValueError('Must specify at least one relation in the relations collection')
		else:
			raise ValueError('Relation.__init__ takes either a relation string or a collection of relations.')

		self._relation_check()
		self._arity_check()
		self._sort()

	def __repr__(self):
		return "Relation(relations=%s)"%(self.relations)

	#Comparison operator
	def __cmp__(self,other):
		#Compare Relations by their relation collection
		if hasattr(other,'relations') and hasattr(other,'relations'):
			return cmp(self.relations,other.relations)
		else:
			raise ValueError("Comparison between a '%s' and a '%s' is undefined."%(type(self),type(other)))

	#Makes sure all relations 'look like' PresRelations
	def _relation_check(self):
		if len(self.relations)>0:
			for relation in self.relations:
				if not hasattr(relation,'tuple_in') or not hasattr(relation,'tuple_out') or not hasattr(relation,'conjunct'):
					raise ValueError("Object of type '%s' does not have the required attributes 'tuple_in', 'tuple_out', and 'conjunct'."%(type(relation)))

	#Checks that all relations in this Relation have the same input and output arity
	def _arity_check(self):
		self._arity_in_check()
		self._arity_out_check()

	#Checks that all relations in this Relation have the same input arity
	def _arity_in_check(self):
		if len(self.relations)>0:
			relation_arity=self.relations[0].arity_in()
			for relation in self.relations[1:]:
				if relation.arity_in()!=relation_arity:
					raise ValueError('All relations in a Relation must have the same input arity.')

	#Checks that all relations in this Relation have the same output arity
	def _arity_out_check(self):
		if len(self.relations)>0:
			relation_arity=self.relations[0].arity_out()
			for relation in self.relations[1:]:
				if relation.arity_out()!=relation_arity:
					raise ValueError('All relations in a Relation must have the same output arity.')

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
		if not hasattr(relation,'relations'):
			raise ValueError("Cannot add object of type '%s' to Relation."%type(relation))
		self.relations.extend(relation.relations)

	#Takes the union of this Relation and the given Relation
	def union(self,other):
		from copy import deepcopy

		if hasattr(other,'relations'):
			if self.arity_in()==other.arity_in() and self.arity_out()==other.arity_out():
				self=deepcopy(self)
				other=deepcopy(other)
				self._add_relation(other)
				self._sort()
				return self
			else:
				raise ValueError('Cannot union relations with differing arity ((%d->%d) and (%d->%d)).'%(self.arity_in(),self.arity_out(),other.arity_in(),other.arity_out()))
		else:
			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))


	#Takes the inverse of all of the PresRelations in this Relation
	def inverse(self):
		from copy import deepcopy

		self=deepcopy(self)
		for relation in self.relations:
			#Swap input and output tuples
			relation.tuple_in,relation.tuple_out=relation.tuple_out,relation.tuple_in

		self._sort()
		return self

	#Relation composition: self(other)
	#Composition of unions of relations is defined as:
	#Let R1=A union B
	#Let R2=C union D
	#
	#Then R1(R2)=A(C) union A(D) union B(C) union B(D)
	def compose(self,other):
		from copy import deepcopy

		#Make sure we are given a Relation
		if not self._like_relation(other):
			raise ValueError("Compose failure: The given relation, '%s', must have the 'tuple_in', 'tuple_out', and 'conjunct' attributes."%(other))

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
		if not self._like_pres_relation(r1) or not self._like_pres_relation(r2):
			raise ValueError("Compose failure: The given relations, '%s' and '%s', must have the 'tuple_in', 'tuple_out', and 'conjunct' attributes."%(r1,r2))

		#Make sure the arities are valid
		if r2.arity_out()!=r1.arity_in():
			raise ValueError('Compose failure: Output arity of second relation (%d) does not match input arity of first relation (%d)'%(r2.arity_out(),r1.arity_in()))

		#Copy the relations so this operation is using fresh copies of the objects
		r1=deepcopy(r1)
		r2=deepcopy(r2)

		#Create dictionaries for renaming the tuple variables
		r1_rename=self._get_rename_dict(r1,'r1')
		r1_unrename=self._get_unrename_dict(r1,'r1')
		r2_rename=self._get_rename_dict(r2,'r2')
		r2_unrename=self._get_unrename_dict(r2,'r2')

		#Rename the tuple varibles in r1 and r2
		RenameVisitor(r1_rename).visit(r1)
		RenameVisitor(r2_rename).visit(r2)

		#Create a new relation
		new_rel=PresRelation(deepcopy(r2.tuple_in),deepcopy(r1.tuple_out),Conjunction([]))

		#Add equality constraints for the 'inner' tuple variables of the composition to the new relation
		#We know there are the same number of variables since we checked above
		for i in xrange(r2.arity_out()):
			#Get the variables from the relations
			var1=deepcopy(r1.tuple_in.vars[i])
			var2=deepcopy(r2.tuple_out.vars[i])

			#Set the coefficient on the first variable to -1 since:
			#var2=var1 -> var2-var1=0
			var1.coeff=-1

			#Create a constraint where these variables are equal
			constraint=Equality(NormExp([var1,var2],0))

			#Add the new constraint to the new relation
			new_rel.conjunct.constraint_list.append(constraint)

		#Add the constraints of both relations to the new relation
		for constraint in r1.conjunct.constraint_list:
			new_rel.conjunct.constraint_list.append(deepcopy(constraint))
		for constraint in r2.conjunct.constraint_list:
			new_rel.conjunct.constraint_list.append(deepcopy(constraint))

		#Sort the constraints
		new_rel.conjunct.constraint_list.sort()

		#Rename the variables back to what the were before
		RenameVisitor(r1_unrename).visit(new_rel)
		RenameVisitor(r2_unrename).visit(new_rel)

		return new_rel
#------------------------------------
