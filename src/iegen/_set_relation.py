# Definitions of the Set and Relation classes that represent Presburger Sets and Relations.

from iegen.parser import PresParser

#---------- Set class ----------
#Presburger Set that is a disjunction of a collection of PresSet instances
class Set(object):
	__slots__=('sets',)

	#Constructor for Set:
	#Takes EITHER a set string, ex {[a]: a>10}, in set_string
	#OR a collection of PresSet instances in sets
	#but NOT both
	def __init__(self,set_string=None,sets=None):
		if None!=set_string and None==sets:
			self.sets=[PresParser.parse_set(set_string)]
		elif None!=sets and None==set_string:
			self.sets=sets
		else:
			raise ValueError('Set.__init__ takes either a set string or a collection of sets.')

		self._set_check()
		self._arity_check()

	def __repr__(self):
		return "Set(sets=%s)"%(self.sets)

	#Makes sure all sets 'look like' PresSets
	def _set_check(self):
		if len(self.sets)>0:
			for set in self.sets:
				if not hasattr(set,'set_tuple') or not hasattr(set,'conjunct'):
					raise ValueError("Object of type '%s' does not have the required attributes 'set_tuple' and 'conjunct'."%(type(set)))

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







#	#Given a collection of scattering functions for each statement
#	#Returns the code that iterates over the tuples in this set
#	#This code is generated by CLooG
#	#
##	def get_code():
#
#	#Union implementation from PresSet
#	def union(self,other):
#		if isinstance(other,PresSet):
#			return PresSetUnion([self,other])
#		elif isinstance(other,PresSetUnion):
#			return other.union(self)
#		else:
#			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))
#
#	#Methods from PresSetUnion
#	def _add_set(self,set):
#		if not isinstance(set,PresSet):
#			raise ValueError("Cannot add object of type '%s' to PresSetUnion."%type(set))
#		self.sets.append(set)
#
#	def _add_union(self,union):
#		if not isinstance(set,PresSetUnion):
#			raise ValueError("Cannot add sets from object of type '%s' to PresSetUnion."%type(set))
#		self.sets.extend(union.sets)
#
#	def union(self,other):
#		if isinstance(other,PresSet):
#			self._add_set(other)
#			return self
#		elif isinstance(other,PresSetUnion):
#			self._add_union(other)
#			return self
#		else:
#			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))
#-------------------------------


#---------- Relation class ----------
class Relation(object):
	__slots__=('relations',)

	#Constructor for Relation:
	#Takes EITHER a relation string, ex {[a]->[a']: a>10}, in relation_string
	#OR a collection of PresRelation instances in relations
	#but NOT both
	def __init__(self,relation_string=None,relations=None):
		if None!=relation_string and None==relations:
			self.relations=[PresParser.parse_relation(relation_string)]
		elif None!=relations and None==relation_string:
			self.relations=relations
		else:
			raise ValueError('Relation.__init__ takes either a relation string or a collection of relations.')

		self._relation_check()
		self._arity_check()

	def __repr__(self):
		return "Relation(relations=%s)"%(self.relations)

	#Makes sure all relations 'look like' PresRelations
	def _relation_check(self):
		if len(self.relations)>0:
			for relation in self.relations:
				if not hasattr(relation,'in_tuple') or not hasattr(relation,'out_tuple') or not hasattr(relation,'conjunct'):
					raise ValueError("Object of type '%s' does not have the required attributes 'in_tuple', 'out_tuple', and 'conjunct'."%(type(relation)))

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
	#Assumption: All PresRelation instances in sets have the same input arity
	#This should be checked with _arity_check upon creation
	def arity_in(self):
		if len(self.relations)>0:
			return self.relations[0].arity_in()
		else:
			raise ValueError('Cannot determine input arity of a Relation that contains no relations.')

	#Returns the output arity of this relation
	#Assumption: All PresRelation instances in sets have the same output arity
	#This should be checked with _arity_check upon creation
	def arity_out(self):
		if len(self.relations)>0:
			return self.relations[0].arity_out()
		else:
			raise ValueError('Cannot determine output arity of a Relation that contains no relations.')

#	#Methods from PresRelation
#	def union(self,other):
#		if isinstance(other,PresRelation):
#			result=PresRelationUnion([self])
#			result.union(other)
#			return result
#		elif isinstance(other,PresRelationUnion):
#			return other.union(self)
#		else:
#			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))
#
#	def inverse(self):
#		outTemp=self.out_tuple
#		self.out_tuple=self.in_tuple
#		self.in_tuple=outTemp
#		return self
#
#	def _add_relation(self,relation):
#		if not isinstance(relation,PresRelation):
#			raise ValueError("Cannot add object of type '%s' to PresRelationUnion."%type(relation))
#		self.relations.append(relation)
#
#	def _add_union(self,union):
#		if not isinstance(relation,PresRelationUnion):
#			raise ValueError("Cannot add relations from object of type '%s' to PresRelationUnion."%type(relation))
#		self.relations.extend(union.relations)
#
#	#Relation composition: self(other)
#	def compose(self,other):
#		#Composing two relations?
#		if isinstance(other,PresRelation):
#			#Make sure the arities are valid
#			if other.arity_out()!=self.arity_in():
#				raise ValueError('Output arity of first relation (%d) does not match input arity of second relation (%d)'%(other.arity_out(),self.arity_in()))
#
#			#Add equalities of tuple variables
#			#We know there are the same number of variables since we checked above
#			for i in xrange(self.arity_in()):
#				constraint=Equality(MinusExp(VarExp(other.in_tuple[i]),VarExp(self.out_tuple[i])))
#				self.conjunct.constraint_list.append(constraint)
#
#			#Add the other's constraints to this relation
#			self.conjunct.extend(other.conjunct.constraint_list)
#
#			return self
#		#Composing a relation with union of relations?
#		elif isinstance(other,PresRelationUnion):
#			new_union=PresRelationUnion([])
#			for relation in other.relations:
#				new_union._add_relation(self.compose(relation))
#			return new_union
#		else:
#			raise ValueError("Unsupported argument of type '%s' for operation compose."%type(other))
#
#	#Methods from PresRelationUnion
#	def union(self,other):
#		#Unioning a single relation?
#		if isinstance(other,PresRelation):
#			if 0==len(self.relations):
#				self._add_relation(other)
#			else:
#				#Assuming that all relations already within the union
#				#have matching arities
#				if self.relations[0].arity_in()==other.arity_in() and \
#				   self.relations[0].arity_out()==other.arity_out():
#					self._add_relation(other)
#				else:
#					raise ValueError('Cannot union relations with differing in or out arity')
#			return self
#		#Unioning another union?
#		elif isinstance(other,PresRelationUnion):
#			if 0==len(self.relations) or 0==len(other.relations):
#				self._add_union(other)
#			else:
#				#Assuming that all relations already within the unions
#				#have matching arities
#				if self.relations[0].arity_in()==other.relations[0].arity_in() and \
#				   self.relations[0].arity_out()==other.relations[0].arity_out():
#					self._add_union(other)
#				else:
#					raise ValueError('Cannot union relations with differing in or out arity')
#			return self
#		else:
#			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))
#
#	def inverse(self):
#		for relation in self.relations:
#			relation.inverse()
#		return self
#
#	def compose(self,other):
#		#Composing with a single relation?
#		if isinstance(other,PresRelation):
#			new_union=PresRelationUnion([])
#			for relation in self.relations:
#				new_union._add_relation(relation.compose(other))
#			return new_union
#		#Composing two unions?
#		elif isinstance(other,PresRelationUnion):
#			new_union=PresRelationUnion([])
#			for self_relation in self.relations:
#				for other_relation in other.relations:
#					new_union._add_relation(self_relation.compose(other_relation))
#			return new_union
#		else:
#			raise ValueError("Unsupported argument of type '%s' for operation union."%type(other))
#------------------------------------
