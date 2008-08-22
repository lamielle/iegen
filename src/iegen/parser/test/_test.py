from unittest import TestCase

#---------- Import Tests ----------
#Test importing of iegen.parser
class ImportTestCase(TestCase):

	#Test simple importing of iegen.parser
	def testImport(self):
		try:
			import iegen.parser
		except Exception,e:
			self.fail("'import iegen.parser' failed: "+str(e))

	#Test simple importing of iegen.parser classes
	def testNameImport(self):
		try:
			from iegen.parser import PresParser
		except ImportError,e:
			self.fail('Importing classes from iegen.parser failed: '+str(e))
#----------------------------------

#---------- Set Parser Tests ----------
#Test parsing of sets
class ParseSetTestCase(TestCase):
	pass
#	#Test parsing sets
#	def testParse(self):
#		from iegen.parser import PresParser
#		from iegen.util import parse_test,test_sets
#
#		for set_string,set_ast in test_sets:
#			parse_test(self,set_string,PresParser.parse_set)
#
#	#Test equality of parsed sets with correct AST
#	def testEquality(self):
#		from iegen.parser import PresParser
#		from iegen.util import ast_equality_test,test_sets
#		from iegen.ast import PresSet,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp
#
#		for set_string,set_ast in test_sets:
#			exec('ast='+set_ast)
#			ast_equality_test(self,set_string,ast,PresParser.parse_set)
#--------------------------------------

#	def formula_test(self,formulas,parse):
#		for formula in formulas:
#			try:
#				result=str(parse(formula))
#			except SyntaxError,e:
#				self.fail("Syntax error while parsing string '%s': %s"%(formula,str(e)))
#
#			self.failUnless(formula==result,"Result string '%s' does not match parsed string '%s'"%(result,formula))
#
#	def testSetVarTuples(self):
#		from omega.parser import PresParser
#		self.formula_test(formulas.tuple_var_sets,PresParser.parse_set)
#		self.formula_test(formulas.var_list_sets,PresParser.parse_set)
#
#	def testRelationVarTuples(self):
#		from omega.parser import PresParser
#		self.formula_test(formulas.tuple_var_relations,PresParser.parse_relation)
#		self.formula_test(formulas.var_list_relations,PresParser.parse_relation)
#
#	def testExpressionParser(self):
#		from omega.parser import PresParser
#
#		self.formula_test(formulas.simple_expression_sets,PresParser.parse_set)
#
#	def testRealSetsRelations(self):
#		from omega.parser import PresParser
#
#		self.formula_test(formulas.real_sets,PresParser.parse_set)
#		self.formula_test(formulas.real_relations,PresParser.parse_relation)
#
#class PresVisitorTestCase(TestCase):
#
#	def formula_test(self,formulas,formula_with_ast,parse):
#		from omega.parser.ast.visitor import PresReprVisitor
#
#		from omega.parser.ast import PresSet,PresRelation
#		from omega.parser.ast import PresVarTupleSet,PresVarTupleIn,PresVarTupleOut
#		from omega.parser.ast import PresVarID,PresVarUnnamed,PresVarRange,PresVarStride,PresVarExpr
#		from omega.parser.ast import PresConstrAnd,PresConstrOr,PresConstrNot,PresConstrForall,PresConstrExists,PresConstrParen
#		from omega.parser.ast import PresStmtEQ,PresStmtNEQ,PresStmtGT,PresStmtGTE,PresStmtLT,PresStmtLTE
#		from omega.parser.ast import PresExprInt,PresExprID,PresExprNeg,PresExprAdd,PresExprSub,PresExprMult,PresExprList,PresExprFunc,PresExprParen
#
#		for formula in formulas:
#			if formula_with_ast:
#				formula=formula[0]
#			try:
#				ast=parse(formula)
#			except SyntaxError,e:
#				self.fail("Syntax error while parsing string '%s': %s"%(formula,str(e)))
#
#			v=PresReprVisitor()
#			v.visit(ast)
#
#			try:
#				eval_ast=eval(str(v))
#			except SyntaxError,e:
#				self.fail("Syntax error while evaluating repr of ast for string '%s': %s"%(formula,str(e)))
##			except ArgumentError,e:
##				self.fail("Argument error while evaluating repr of ast for string '%s': %s"%(formula,str(e)))
#
#			self.failUnless(str(ast)==formula,"AST string '%s' does not match parsed string '%s'"%(str(ast),formula))
#			self.failUnless(str(eval_ast)==formula,"Evaluated AST string '%s' does not match parsed string '%s'"%(str(eval_ast),formula))
#
#	def testDFV(self):
#		from omega.parser import PresParser
#
#		self.formula_test(formulas.simple_expression_sets,False,PresParser.parse_set)
#		self.formula_test(formulas.tuple_var_sets,False,PresParser.parse_set)
#		self.formula_test(formulas.var_list_sets,False,PresParser.parse_set)
#		self.formula_test(formulas.tuple_var_relations,False,PresParser.parse_relation)
#		self.formula_test(formulas.var_list_relations,False,PresParser.parse_relation)
#
#		self.formula_test(formulas.test_sets,True,PresParser.parse_set)
#		self.formula_test(formulas.test_relations,True,PresParser.parse_relation)
#		self.formula_test(formulas.real_sets,False,PresParser.parse_set)
#		self.formula_test(formulas.real_relations,False,PresParser.parse_relation)
#

