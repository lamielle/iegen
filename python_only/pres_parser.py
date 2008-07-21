#
# Attempting a python only manipulation of presburger sets and relations.
# Copied and trimmed from omega_bindings/src/omega/parser/pres_parser.py.
# MMS 7/21/08
# 

#---------- Presburger Formula Parser Class ----------
class PresParser(object):
	def __init__(self,parser_type):
		self._parser_type=parser_type

	#Strings used to differentiate between sets and relations
	_set='set'
	_relation='relation'

	#Static factory method to obtain a new set parser
	def get_set_parser():
		return PresParser._get_parser(PresParser._set)
	get_set_parser=staticmethod(get_set_parser)

	#Parse the given set string and return the associated AST
	def parse_set(set,debug=False):
		from ply import lex
		if debug:
			PresParser.get_set_parser()
			print dir(lex)
			print set
			lex.input(set)
			while 1:
				tok = lex.token()
				if not tok: break      # No more input
				print tok
		return PresParser.get_set_parser().parse(set)
	parse_set=staticmethod(parse_set)

	#Static factory method to obtain a new relation parser
	def get_relation_parser():
		return PresParser._get_parser(PresParser._relation)
	get_relation_parser=staticmethod(get_relation_parser)

	#Parse the given relation string and return the associated AST
	def parse_relation(relation,debug=False):
		return PresParser.get_relation_parser().parse(relation)
	parse_relation=staticmethod(parse_relation)

	#Static factory method to obtain a new parser of the given type
	def _get_parser(parser_type):
		from ply import lex,yacc
		lex.lex(module=PresParser(parser_type))
		return yacc.yacc(start=parser_type,module=PresParser(parser_type),tabmodule="parsetab_%s"%parser_type)
	_get_parser=staticmethod(_get_parser)

	#---------- Lexer methods/members ----------
	#Token definitions
	keywords={
		}

	tokens=('LBRACE','RBRACE','LBRACKET','RBRACKET','LPAREN','RPAREN','COMMA','COLON','STAR','PLUS','DASH','EQ','NEQ','GT','GTE','LT','LTE','ARROW','ID','INT')+tuple(set(keywords.values()))

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

#	def t_AMP(self,t):
#		r'\&'
#		t.type='AND'
#		return t

#	def t_DOUBLE_PIPE(self,t):
#		r'\|\|'
#		t.type='OR'
#		return t

#	def t_PIPE(self,t):
#		r'\|'
#		t.type='OR'
#		return t

	#Lexer error routine
	def t_error(self,t):
		print "Illegal character '%s'" % t.value[0]
		t.lexer.skip(1)

	#---------- Parser methods/members ----------
#	precedence=(
#		('left','PLUS','DASH'),
#		('left','STAR'),
#		('left','UMINUS'),
#		('left','OR'),
#		('left','AND'),
#		('right','NOT'),
#	)

	#Parser error routine
	def p_error(self,t):
		from ply import yacc
		raise SyntaxError("Syntax error at '%s' [%d,%d]" %(t.value,t.lineno,t.lexpos))

	def p_set(self,t):
		'''set : LBRACE variable_tuple_set RBRACE'''
		t[0] = t[2]
		print "in p_set, t = ", t
        

	def p_relation(self,t):
		'''relation : LBRACE variable_tuple_in ARROW variable_tuple_out RBRACE'''
		print "in p_relation, t = ", t

	#epsilon (empty production)
#	def p_epsilon(self,t):
#		'''epsilon :'''
#		t[0]=None

	def p_var_id_list(self,t):
		'''var_id_list : var_id_list COMMA tuple_variable_id
		           | tuple_variable_id'''
		if 4==len(t):
			t[1].append(t[3])
			t[0]=t[1]
		else:
			t[0]=[t[1]]

	#---------- Variable Tuple Productions ----------
	def p_variable_tuple_set(self,t):
		'''variable_tuple_set : variable_tuple'''
		print "in p_variable_tuple_set, t = ", t

	def p_variable_tuple_in(self,t):
		'''variable_tuple_in : variable_tuple'''
		print "in p_variable_tuple_in, t = ", t
		
	def p_variable_tuple_out(self,t):
		'''variable_tuple_out : variable_tuple'''
		print "in p_variable_tuple_out, t = ", t

	def p_variable_tuple(self,t):
		'''variable_tuple : LBRACKET tuple_variable_list RBRACKET
		                  | LBRACKET RBRACKET'''
		if 4==len(t):
			t[0]=t[2]
		else:
			t[0]=[]
			
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
		'''tuple_variable : tuple_variable_id'''
		t[0]=t[1]
		
	def p_tuple_variable_id(self,t):
		'''tuple_variable_id : ID'''
		print "in p_tuple_variable_id, t = ", t
		t[0] = t[1]

	#--------------------------------------------------


#-------------------------------------------------------------------------
