class Formula(object):
	__slots__=('_formula','_ast','_visitor')

	def __init__(self,formula,ast,visitor):
		if Formula==type(self):
			raise Exception('Cannot instantiate instance of Formula.  Instantiate a subclass instead.')
		self.m_formula=formula
		self.m_ast=ast
		self.m_visitor=visitor
		self.m_visitor.visit(self.m_ast)

	#Formula string getters/setters
	def _get_formula(self): return self._formula
	def _set_formula(self,value): self._formula=value
	m_formula=property(_get_formula,_set_formula)

	#AST getters/setters
	def _get_ast(self): return self._ast
	def _set_ast(self,value): self._ast=value
	m_ast=property(_get_ast,_set_ast)

	#Visitor getters/setters
	def _get_visitor(self): return self._visitor
	def _set_visitor(self,value): self._visitor=value
	m_visitor=property(_get_visitor,_set_visitor)

	def union(self,other_formula):
		self.m_visitor.union(other_formula.m_visitor)
		return self

class Set(Formula):
	__slots__=()

	def __init__(self,set):
		from omega.parser import PresParser
		from omega.parser.ast.visitor import PresTransSetVisitor

		Formula.__init__(self,set,PresParser.parse_set(set),PresTransSetVisitor())

	def __str__(self):
		print "In Set.__str__"
		return '(Set: formula: %s ast: %s set: %s)'%(self.m_formula,self.m_ast,self.m_visitor)

	def __repr__(self):
		return 'Set("%s")'%self.m_formula

class Relation(Formula):
	__slots__=()

	def __init__(self,relation):
		from omega.parser import PresParser
		from omega.parser.ast.visitor import PresTransRelationVisitor

		Formula.__init__(self,relation,PresParser.parse_relation(relation),PresTransRelationVisitor())

	def __str__(self):
		return '(Relation: formula: %s ast: %s relation: %s)'%(self.m_formula,self.m_ast,self.m_visitor)

	def __repr__(self):
		return 'Relation("%s")'%self.m_formula
