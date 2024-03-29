#
# _parser.py

# A python parser for presburger sets and relations.
# Copied and trimmed from omega_bindings/src/omega/parser/pres_parser.py,
# which was written by Alan LaMielle.
#
# Assumptions and set and relation language restrictions
#   - All constraints must be written as binary operations.
#     For example, 1<=i<=10 must be written as 1<=i && i<=10.
#   - The constraints will all be part of a conjunction (AND).  For disjunction
#     union separate Set/Relation objects (iegen.Set/Relation)
#   - This grammar does NOT include Exists, Forall, or not keywords.
#
# MMS 7/21/08
# AML 8/13/2008: Modified to use rewritten expressions and their operators
# AML 8/25/2008: Removed union support from parser

import iegen.util
from iegen import IEGenObject
from iegen.util import is_iterable
from iegen.ast import PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp

#---------- Presburger Formula Parser Class ----------
class PresParser(object):

	#---------- Public Interface ----------
	#Parse the given set string and return the associated AST
	def parse_set(set,symbolics=None):
		#Remove relation-only tokens and rules
		relation_rule=PresParser.p_relation
		del PresParser.p_relation
		arrow_token=PresParser.t_ARROW
		del PresParser.t_ARROW

		try:
			#Define what tokens the lexer should use
			PresParser.tokens=PresParser.set_tokens

			#Return the parsed AST
			set=PresParser.get_set_parser(set).parse(set)
			set.symbolics=[] if symbolics is None else symbolics

			#Run one time normalization
			iegen.util.one_time_normalize(set)

			return set
		finally:
			#Replace the relation-only tokens and rules
			PresParser.p_relation=relation_rule
			PresParser.t_ARROW=arrow_token
	parse_set=staticmethod(parse_set)

	#Parse the given relation string and return the associated AST
	def parse_relation(relation,symbolics=None):
		#Remove set-only tokens and rules
		p_set=PresParser.p_set
		del PresParser.p_set

		try:
			#Define what tokens the lexer should use
			PresParser.tokens=PresParser.relation_tokens

			#Return the parsed AST
			relation=PresParser.get_relation_parser(relation).parse(relation)
			relation.symbolics=[] if symbolics is None else symbolics

			#Run one time normalization
			iegen.util.one_time_normalize(relation)

			return relation
		finally:
			#Replace the set-only tokens and rules
			PresParser.p_set=p_set
	parse_relation=staticmethod(parse_relation)
	#--------------------------------------

	#---------- Private Interface ----------
	def __init__(self,parser_type,formula):
		self._parser_type=parser_type
		self._formula=formula

	#Strings used to differentiate between sets and relations
	_set='set'
	_relation='relation'

	#Static factory method to obtain a new set parser
	def get_set_parser(set):
		return PresParser._get_parser(PresParser._set,set)
	get_set_parser=staticmethod(get_set_parser)

	#Static factory method to obtain a new relation parser
	def get_relation_parser(relation):
		return PresParser._get_parser(PresParser._relation,relation)
	get_relation_parser=staticmethod(get_relation_parser)

	#Static factory method to obtain a new parser of the given type
	def _get_parser(parser_type,formula):
		from ply import lex,yacc
		lex.lex(module=PresParser(parser_type,formula))
		return yacc.yacc(start=parser_type,module=PresParser(parser_type,formula),tabmodule='iegen.parsetab_%s'%parser_type,debug=0)
	_get_parser=staticmethod(_get_parser)

	#---------- Lexer methods/members ----------
	#Token definitions
	keywords={
		'and':'AND','AND':'AND'
    }
	set_tokens=('LBRACE','RBRACE','LBRACKET','RBRACKET','LPAREN','RPAREN','COMMA','COLON','STAR','PLUS','DASH','EQ','NEQ','GT','GTE','LT','LTE','ID','INT')+tuple(set(keywords.values()))

	relation_tokens=set_tokens+('ARROW',)

	t_LBRACE=r'\{'
	t_RBRACE=r'\}'
	t_LBRACKET=r'\['
	t_RBRACKET=r'\]'
	t_LPAREN=r'\('
	t_RPAREN=r'\)'
	t_COMMA=r'\,'
	t_COLON=r'\:'
	t_STAR=r'\*'
	t_PLUS=r'\+'
	t_DASH=r'\-'
	t_EQ=r'\='
	t_NEQ=r'\!\='
	t_GT=r'\>'
	t_GTE=r'\>\='
	t_LT=r'\<'
	t_LTE=r'\<\='
	t_ARROW=r'\-\>'
	t_INT=r'[0-9]+'
	t_ignore=' \n\t'

	def t_ID(self,t):
		r'[A-Za-z][A-Za-z0-9_\']*'
		t.type=self.keywords.get(t.value,'ID')
		return t

	def t_DOUBLE_AMP(self,t):
		r'\&\&'
		t.type='AND'
		return t

	#Lexer error routine
	def t_error(self,t):
		iegen.print_error("Illegal character '%s'" % t.value[0])
		t.lexer.skip(1)
	#-------------------------------------------

	#---------- Parser methods/members ----------
	precedence=(
		('left','PLUS','DASH'),
		('left','STAR'),
		('left','UMINUS'),
		('left','AND'),
	)

	#Parser error routine
	def p_error(self,t):
		from ply import yacc
		if None is t:
			raise SyntaxError("Syntax when parsing '%s'" %(self._formula,))
		else:
			raise SyntaxError("Syntax error at '%s' (%d:%d) when parsing '%s'" %(t.value,t.lineno,t.lexpos,self._formula))

	def p_set(self,t):
		'''set : LBRACE variable_tuple optional_constraints RBRACE'''
		t[0] = PresSet(t[2],t[3])

	def p_relation(self,t):
		'''relation : LBRACE variable_tuple ARROW variable_tuple optional_constraints RBRACE'''
		t[0] = PresRelation(t[2],t[4],t[5])

	#epsilon (empty production)
	def p_epsilon(self,t):
		'''epsilon :'''
		t[0]=["epsilon"]
	#--------------------------------------------

	#---------- Variable Tuple Productions ----------
	def p_variable_tuple(self,t):
		'''variable_tuple : LBRACKET tuple_variable_list RBRACKET
		                  | LBRACKET RBRACKET'''
		if 4==len(t):
			t[0]=VarTuple(t[2])
		else:
			t[0]=VarTuple([])

	def p_tuple_variable_list(self,t):
		'''tuple_variable_list : tuple_variable
		                       | tuple_variable_list COMMA tuple_variable'''
		#Starting a new list
		if 2==len(t):
			t[0]=[t[1]]
		#Adding to an existing list
		else:
			t[1].append(t[3])
			t[0]=t[1]

	def p_tuple_variable(self,t):
		'''tuple_variable : variable_id'''
		t[0]=VarExp(1,t[1])

	def p_variable_id(self,t):
		'''variable_id : ID'''
		t[0] = t[1]
	#--------------------------------------------------

	#---------- Constraint Productions ----------
	def p_optional_constraints(self,t):
		'''optional_constraints : COLON constraint_list
		                        | epsilon'''
		if 3==len(t):
			t[0]=Conjunction(t[2])
		else:
			#Empty constraints
			t[0]=Conjunction([])

	def p_constraint_list(self,t):
		'''constraint_list : constraint
		                   | constraint_list AND constraint'''
		#Starting a new list
		if 2==len(t):
			t[0]=[t[1]]
		#Adding to an existing list
		else:
			if is_iterable(t[3]):
				t[1].extend(t[3])
			else:
				t[1].append(t[3])
			t[0]=t[1]

	def p_constraint(self,t):
		'''constraint :  constraint_eq
		               | constraint_neq
		               | constraint_gt
		               | constraint_gte
		               | constraint_lt
		               | constraint_lte'''
		t[0]=t[1]

	def p_constraint_eq(self,t):
		'''constraint_eq : expression EQ expression'''
		# (t[1] = t[3]) = (t[1]-t[3]=0)
		t[0]=Equality(t[1]-t[3])

	def p_constraint_neq(self,t):
		'''constraint_neq : expression NEQ expression'''
		# (t[1]!=t[3]) = (t[3]>t[1] && t[1]>t[3])
		#              = (t[3]>=t[1]+1 && t[1]>=t[3]+1)
		raise Exception('This should be || and not &&!  Need to fix!')
		t[0]=[Inequality(t[3]-(t[1]+NormExp([],1))),
		      Inequality(t[1]-(t[3]+1))]

	def p_constraint_gt(self,t):
		'''constraint_gt : expression GT expression'''
		# (t[1] > t[3]) = (t[1] >= t[3]+1) = (t[1]-(t[3]+1) >= 0)
		t[0]=Inequality(t[1]-(t[3]+NormExp([],1)))

	def p_constraint_gte(self,t):
		'''constraint_gte : expression GTE expression'''
		# (t[1] >= t[3]) = (t[1]-t[3] >= 0)
		t[0]=Inequality(t[1]-t[3])

	def p_constraint_lt(self,t):
		'''constraint_lt : expression LT expression'''
		# (t[1] < t[3]) = (t[3] > t[1]) = (t[3] >= t[1]+1) = (t[3]-(t[1]+1) >= 0)
		t[0]=Inequality(t[3]-(t[1]+NormExp([],1)))

	def p_constraint_lte(self,t):
		'''constraint_lte : expression LTE expression'''
		# (t[1] <= t[3]) = (t[3] >= t[1]) = (t[3]-t[1] >= 0)
		t[0]=Inequality(t[3]-t[1])
	#--------------------------------------------------

	#---------- Expression Productions ----------
	def p_expression(self,t):
		'''expression : expression_int
		              | expression_unop
		              | expression_binop
		              | expression_int_mult
		              | expression_simple'''
		t[0]=t[1]

	def p_expression_int(self,t):
		'''expression_int : INT'''
		t[0]=NormExp([],int(t[1]))

	def p_expression_unop(self,t):
		'''expression_unop : DASH expression %prec UMINUS'''
		t[0]=NormExp([],-1)*t[2]

	def p_expression_binop(self,t):
		'''expression_binop : expression PLUS expression
								  | expression DASH expression
								  | expression STAR expression'''
		if '+'==str(t[2]):
			t[0]=t[1]+t[3]
		elif '-'==str(t[2]):
			t[0]=t[1]-t[3]
		elif '*'==str(t[2]):
				t[0]=t[1]*t[3]
		else:
			raise ValueError("Unsupported binary operator '%s'."%t[2])

	def p_expression_int_mult(self,t):
		'''expression_int_mult : INT expression_simple'''
		t[0]=NormExp([],int(t[1]))*t[2]

	def p_expression_simple(self,t):
		'''expression_simple : expression_id
		                     | expression_func
		                     | expression_paren'''
		t[0]=t[1]

	def p_expression_id(self,t):
		'''expression_id : ID'''
		t[0]=NormExp([VarExp(1,t[1])],0)

	def p_expression_func(self,t):
		'''expression_func : variable_id LPAREN expr_list RPAREN'''
		t[0]=NormExp([FuncExp(1,t[1],t[3])],0)

	def p_expression_paren(self,t):
		'''expression_paren : LPAREN expression RPAREN'''
		t[0]=t[2]

	def p_expr_list(self,t):
		'''expr_list : expr_list COMMA expression
		             | expression'''
		if 4==len(t):
			t[1].append(t[3])
			t[0]=t[1]
		else:
			t[0]=[t[1]]
	#--------------------------------------------------
	#---------------------------------------
#-------------------------------------------------------------------------
