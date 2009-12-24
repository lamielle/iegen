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

	#Test parsing sets
	def testParse(self):
		from iegen.parser import PresParser
		from iegen.util import parse_test,test_sets

		for set_string,set_ast in test_sets:
			parse_test(self,set_string,PresParser.parse_set)

#This test was disabled as AST equality testing no longer works
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

#---------- Relation Parser Tests ----------
#Test parsing of relations
class ParseRelationTestCase(TestCase):

	#Test parsing relations
	def testParse(self):
		from iegen.parser import PresParser
		from iegen.util import parse_test,test_relations

		for relation_string,relation_ast in test_relations:
			parse_test(self,relation_string,PresParser.parse_relation)

#This test was disabled as AST equality testing no longer works
#	#Test equality of parsed relations with correct AST
#	def testEquality(self):
#		from iegen.parser import PresParser
#		from iegen.util import ast_equality_test,test_relations
#		from iegen.ast import PresRelation,VarTuple,Conjunction,Equality,Inequality,NormExp,VarExp,FuncExp
#
#		for relation_string,relation_ast in test_relations:
#			exec('ast='+relation_ast)
#			ast_equality_test(self,relation_string,ast,PresParser.parse_relation)
#--------------------------------------
