# Definitions of the Set and Relation classes that represent Presburger Sets and Relations.

from iegen.parser import PresParser

class Set(object):
	__slots__=('set',)

	def __init__(self,set_string):
		self.set=PresParser.parse_set(set_string)

class Relation(object):
	__slots__=('relation',)

	def __init__(self,relation_string):
		self.relation=PresParser.parse_relation(relation_string)
