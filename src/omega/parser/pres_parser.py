from omega.parser.ast import *

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
		'and':'AND','AND':'AND',
		'or':'OR','OR':'OR',
		'not':'NOT','NOT':'NOT',
		'exists':'EXISTS','EXISTS':'EXISTS',
		'forall':'FORALL','FORALL':'FORALL'}

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

	def t_AMP(self,t):
		r'\&'
		t.type='AND'
		return t

	def t_DOUBLE_PIPE(self,t):
		r'\|\|'
		t.type='OR'
		return t

	def t_PIPE(self,t):
		r'\|'
		t.type='OR'
		return t

	#Lexer error routine
	def t_error(self,t):
		print "Illegal character '%s'" % t.value[0]
		t.lexer.skip(1)

	#---------- Parser methods/members ----------
	precedence=(
		('left','PLUS','DASH'),
		('left','STAR'),
		('left','UMINUS'),
		('left','OR'),
		('left','AND'),
		('right','NOT'),
	)

	#Parser error routine
	def p_error(self,t):
		from ply import yacc
		raise SyntaxError("Syntax error at '%s' [%d,%d]" %(t.value,t.lineno,t.lexpos))

	def p_set(self,t):
		'''set : LBRACE variable_tuple_set optional_constraints RBRACE'''
		t[0]=PresSet.new(t[2],t[3])

#		print t
#		print t.slice
#		print len(t)
#		print [i for i in t]
#		t[0]=
#		Relation * r = new Relation($1->size);
#		resetGlobals();
#		F_And *f = r->add_and();
#		int i;
#		for(i=1;i<=$1->size;i++) {
#			$1->vars[i]->vid = r->set_var(i);
#			if (!$1->vars[i]->anonymous)
#				r->name_set_var(i,$1->vars[i]->stripped_name);
#			};
#					 foreach(e,Exp*,$1->eq_constraints, install_eq(f,e,0));
#		foreach(e,Exp*,$1->geq_constraints, install_geq(f,e,0));
#		foreach(c,strideConstraint*,$1->stride_constraints, install_stride(f,c));
#		if ($2) $2->install(f);
#		delete $1;
#		delete $2;
#		$$ = r; }

	def p_relation(self,t):
		'''relation : LBRACE variable_tuple_in ARROW variable_tuple_out optional_constraints RBRACE'''
		t[0]=PresRelation.new(t[2],t[4],t[5])

#		Relation * r = new Relation($1->size,$4->size);
#		resetGlobals();
#		F_And *f = r->add_and();
#		int i;
#		for(i=1;i<=$1->size;i++) {
#			$1->vars[i]->vid = r->input_var(i);
#			if (!$1->vars[i]->anonymous)
#				r->name_input_var(i,$1->vars[i]->stripped_name);
#			};
#		for(i=1;i<=$4->size;i++) {
#			$4->vars[i]->vid = r->output_var(i);
#			if (!$4->vars[i]->anonymous)
#				r->name_output_var(i,$4->vars[i]->stripped_name);
#			};
#		foreach(e,Exp*,$1->eq_constraints, install_eq(f,e,0));
#					 foreach(e,Exp*,$1->geq_constraints, install_geq(f,e,0));
#		foreach(c,strideConstraint*,$1->stride_constraints, install_stride(f,c));
#		foreach(e,Exp*,$4->eq_constraints, install_eq(f,e,0));
#		foreach(e,Exp*,$4->geq_constraints, install_geq(f,e,0));
#		foreach(c,strideConstraint*,$4->stride_constraints, install_stride(f,c));
#		if ($6) $6->install(f);
#		delete $1;
#		delete $4;
#		delete $6;
#		$$ = r; }

#Is this necessary? (it was a third production in OC in addition to set/relation)
#| constraints {
#	Relation * r = new Relation(0,0);
#	F_And *f = r->add_and();
#	$1->install(f);
#	delete $1;
#	$$ = r;
#	}
#;

	#epsilon (empty production)
	def p_epsilon(self,t):
		'''epsilon :'''
		t[0]=None

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
		t[0]=PresVarTupleSet.new(t[1])
	def p_variable_tuple_in(self,t):
		'''variable_tuple_in : variable_tuple'''
		t[0]=PresVarTupleIn.new(t[1])
	def p_variable_tuple_out(self,t):
		'''variable_tuple_out : variable_tuple'''
		t[0]=PresVarTupleOut.new(t[1])

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
		'''tuple_variable : tuple_variable_id
		                  | tuple_variable_unnamed
		                  | tuple_variable_expr
		                  | tuple_variable_range
		                  | tuple_variable_stride'''
		t[0]=t[1]
	def p_tuple_variable_id(self,t):
		'''tuple_variable_id : ID'''
		t[0]=PresVarID.new(t[1])
	def p_tuple_variable_unnamed(self,t):
		'''tuple_variable_unnamed : STAR'''
		t[0]=PresVarUnnamed.new()
	def p_tuple_variable_expr(self,t):
		'''tuple_variable_expr : expression'''
		t[0]=PresVarExpr.new(t[1])
	def p_tuple_variable_range(self,t):
		'''tuple_variable_range : expression COLON expression'''
		t[0]=PresVarRange.new(t[1],t[3])
	def p_tuple_variable_stride(self,t):
		'''tuple_variable_stride : expression COLON expression COLON expression_int'''
		t[0]=PresVarStride.new(t[1],t[3],t[5])
	#--------------------------------------------------

	#---------- Constraint Productions ----------
	def p_optional_constraints(self,t):
		'''optional_constraints : COLON constraints
		                        | epsilon'''
		if 3==len(t):
			t[0]=t[2]
		else:
			#Empty constraints
			t[0]=PresConstrAnd.new((),())
	def p_constraints(self,t):
		'''constraints : constraint_and
		               | constraint_or
		               | constraint_not
		               | constraint_paren
		               | constraint_exists
		               | constraint_forall
		               | statement_chain'''
		if not issubclass(t[1].__class__,PresConstr):
			if issubclass(t[1].__class__,str): print "is a string: %s"%t[1]
			t[1]=PresConstrAnd.new((),(t[1],))
		t[0]=t[1]

	#And/Or/Not/Paren productions
	def p_constraint_and(self,t):
		'''constraint_and : constraints AND constraints'''
		t[0]=PresConstrAnd.new((t[1],t[3]),())
	def p_constraint_or(self,t):
		'''constraint_or : constraints OR constraints'''
		t[0]=PresConstrOr.new((t[1],t[3]),())
	def p_constraint_not(self,t):
		'''constraint_not : NOT constraints'''
		t[0]=PresConstrNot.new(t[2])
	def p_constraint_paren(self,t):
		'''constraint_paren : LPAREN constraints RPAREN'''
		t[0]=PresConstrParen.new(t[2])

	#Existential quantifier
	def p_constraint_exists(self,t):
		'''constraint_exists : constraint_exists_start constraint_quant_var_decl_optional_brackets COLON constraints constraint_quant_end'''
		t[0]=PresConstrExists.new(t[2],t[4])
	def p_constraint_exists_start(self,t):
		'''constraint_exists_start : LPAREN EXISTS
		                           | EXISTS LPAREN'''

	#Universal quantifier
	def p_constraint_forall(self,t):
		'''constraint_forall : constraint_forall_start constraint_quant_var_decl_optional_brackets COLON constraints constraint_quant_end'''
		t[0]=PresConstrForall.new(t[2],t[4])
	def p_constraint_forall_start(self,t):
		'''constraint_forall_start : LPAREN FORALL
		                           | FORALL LPAREN'''

	#Common quantifier productions
	def p_constraint_quant_var_decl_optional_brackets(self,t):
		'''constraint_quant_var_decl_optional_brackets : LBRACKET constraint_quant_var_decl RBRACKET
		                              | constraint_quant_var_decl'''
		if 4==len(t):
			t[0]=t[2]
		else:
			t[0]=t[1]
	def p_constraint_quant_var_decl(self,t):
		'''constraint_quant_var_decl : var_id_list'''
		t[0]=t[1]
	def p_constraint_quant_end(self,t):
		'''constraint_quant_end : RPAREN'''

	#Statement productions
	def p_statement_chain(self,t):
		'''statement_chain : expr_list statement_relational_operator expr_list
		                   | expr_list statement_relational_operator statement_chain'''
		if hasattr(t[1],'append'):
			t[1]=PresExprList.new(t[1])
		if hasattr(t[3],'append'):
			t[3]=PresExprList.new(t[3])
		if '='==t[2]:
			t[0]=PresStmtEQ.new(t[1],t[3])
		elif '!='==t[2]:
			t[0]=PresStmtNEQ.new(t[1],t[3])
		elif '>'==t[2]:
			t[0]=PresStmtGT.new(t[1],t[3])
		elif '>='==t[2]:
			t[0]=PresStmtGTE.new(t[1],t[3])
		elif '<'==t[2]:
			t[0]=PresStmtLT.new(t[1],t[3])
		elif '<='==t[2]:
			t[0]=PresStmtLTE.new(t[1],t[3])
		else:
			assert False
	def p_statement_relational_operator(self,t):
		'''statement_relational_operator : EQ
		                                 | NEQ
		                                 | GT
		                                 | GTE
		                                 | LT
		                                 | LTE'''
		t[0]=t[1]
	def p_expr_list(self,t):
		'''expr_list : expr_list COMMA expression
		             | expression'''
		if 4==len(t):
			if hasattr(t[1],'append'):
				t[1].append(t[3])
			else:
				t[1]=[t[1],t[3]]
			t[0]=t[1]
		else:
			t[0]=t[1]
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
		t[0]=PresExprInt.new(int(t[1]))
	def p_expression_unop(self,t):
		'''expression_unop : DASH expression %prec UMINUS'''
		t[0]=PresExprNeg.new(t[2])
	def p_expression_binop(self,t):
		'''expression_binop : expression PLUS expression
								  | expression DASH expression
								  | expression STAR expression'''
		if '+'==str(t[2]):
			t[0]=PresExprAdd.new(t[1],t[3])
		elif '-'==str(t[2]):
			t[0]=PresExprSub.new(t[1],t[3])
		elif '*'==str(t[2]):
			t[0]=PresExprMult.new(t[1],t[3])
		else:
			assert False
	def p_expression_int_mult(self,t):
		'''expression_int_mult : INT expression_simple'''
		t[0]=PresExprMult.new(PresExprInt.new(int(t[1])),t[2],True)
	def p_expression_simple(self,t):
		'''expression_simple : expression_id
		                     | expression_func
		                     | expression_paren'''
		t[0]=t[1]
	def p_expression_id(self,t):
		'''expression_id : ID'''
		t[0]=PresExprID.new(t[1])
	def p_expression_func(self,t):
		'''expression_func : tuple_variable_id LPAREN var_id_list RPAREN'''
		t[0]=PresExprFunc.new(t[1],t[3])
	def p_expression_paren(self,t):
		'''expression_paren : LPAREN expression RPAREN'''
		t[0]=PresExprParen.new(t[2])
	#--------------------------------------------------
#-------------------------------------------------------------------------
