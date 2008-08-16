from unittest import TestCase

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
		except Exception,e:
			self.fail("Importing classes from iegen.parser failed: "+str(e))

## Testing of the presburger set and relation parser.
#from pres_parser import PresParser
#
## set with no conditions
#PresParser.parse_set('{[i,j,k]}')
#
## set with simple conditions
#PresParser.parse_set('{[i,j,k]: 1 <= i && i <= 45 }')
#
## set with simple conditions
##PresParser.parse_set('{[i,j,k]: i!=54 }')
#
## set with more complex conditions
#PresParser.parse_set('{[i,j,k]: 1 <= i && 1<=j && 1<=k && i<= 45 && j<=45 && k<=45 }')
#
## Parsing relations
#
## A simple relation with only in and out tuple
#PresParser.parse_relation('{[i] -> [j]}')
#
## A simple relation with constraints
#PresParser.parse_relation('{[i] -> [j] : i = j }')
#
## A simple relation with constraints involving uninterp functions
#PresParser.parse_relation('{[i] -> [j] : i = delta(j) }')
#
## A simple relation with constraints involving nested uninterp functions
#PresParser.parse_relation('{[i] -> [j] : i = sigma(delta(j)) }')
#
## Checking that we can parse all examples from 
## iegen/docs/moldyn-data-iter-reord.txt
#print "========================= moldyn-data-iter-reord.txt ===="
#PresParser.parse_set('{ [ii,j] : j=1 && 0 <= ii && ii <= (n_inter-1)  } union { [ii,j] : j=2 && 0 <= ii && ii <= (n_inter-1)  }')
#PresParser.parse_set('{ [k] : 0 <= k && k <= (N-1) }')
#PresParser.parse_set('{ [k] : 0 <= k && k <= (n_inter-1) }')
#
#PresParser.parse_set('{ [k] : 0 <= k && k <= (n_inter-1) }')
#
#PresParser.parse_relation('{ [ii,j] -> [k] :j=2 && k=inter2(ii) }')
#PresParser.parse_relation('{ [ii,j] -> [ k ] : k=inter1(ii) && 1<=j && j<=2 } union { [ii,j] -> [ k ] : k=inter2(ii) && 1<=j && j<=2 }')
#PresParser.parse_relation('{ [ k ] -> [ r ] : r=sigma( k ) }')
#PresParser.parse_relation('{ [ ii, j ] -> [ ii ] }')
#PresParser.parse_relation('{ [ i ] -> [ k ] : k = delta( i ) }')
#PresParser.parse_relation('{ [a] -> [ k ] : k=inter1(a) } union { [a] -> [ k ] : k=inter2(a) }')
#PresParser.parse_relation('{ [k] -> [a] : a=ii && b=j && k=inter1(ii) && 1<=j && j<=2 }')
#PresParser.parse_relation('{ [k] -> [a] : k=inter1(a) && 1<=j && j<=2 }')
#PresParser.parse_relation('{ [k] -> [a] : k=inter1(a) }')
#PresParser.parse_relation('{ [a,b] -> [r] : r=sigma(inter1(delta_inv(a))) && 1 <=b && b<=2}')
#






#class formulas:
#
#	#Test formula strings with their associated strings for constructing them
#	test_sets=(
#		('{[]}',"PresSet.new(PresVarTupleSet.new(()),PresConstrAnd.new((),()))"),
#		('{[a]}',"PresSet.new(PresVarTupleSet.new((v1,)),PresConstrAnd.new((),()))"),
#		('{[a,b]}',"PresSet.new(PresVarTupleSet.new((v1,v2)),PresConstrAnd.new((),()))"),
#		('{[a,b,c]}',"PresSet.new(PresVarTupleSet.new((v1,v2,v3)),PresConstrAnd.new((),()))"),
#
#		('{[]:6=7 AND 6!=7}',"PresSet.new(PresVarTupleSet.new(()),c1)"),
#		('{[a]:6=7 AND 6!=7}',"PresSet.new(PresVarTupleSet.new((v1,)),c1)"),
#		('{[a,b]:6=7 AND 6!=7}',"PresSet.new(PresVarTupleSet.new((v1,v2)),c1)"),
#		('{[a,b,c]:6=7 AND 6!=7}',"PresSet.new(PresVarTupleSet.new((v1,v2,v3)),c1)"))
#
#	test_relations=(
#		('{[]->[]}',"PresRelation.new(PresVarTupleIn.new(()),PresVarTupleOut.new(()),PresConstrAnd.new((),()))"),
#		('{[a]->[]}',"PresRelation.new(PresVarTupleIn.new((v1,)),PresVarTupleOut.new(()),PresConstrAnd.new((),()))"),
#		('{[a,b]->[]}',"PresRelation.new(PresVarTupleIn.new((v1,v2)),PresVarTupleOut.new(()),PresConstrAnd.new((),()))"),
#		('{[a,b,c]->[]}',"PresRelation.new(PresVarTupleIn.new((v1,v2,v3)),PresVarTupleOut.new(()),PresConstrAnd.new((),()))"),
#		("{[]->[a']}","PresRelation.new(PresVarTupleIn.new(()),PresVarTupleOut.new((v4,)),PresConstrAnd.new((),()))"),
#		("{[]->[a',b']}","PresRelation.new(PresVarTupleIn.new(()),PresVarTupleOut.new((v4,v5)),PresConstrAnd.new((),()))"),
#		("{[]->[a',b',c']}","PresRelation.new(PresVarTupleIn.new(()),PresVarTupleOut.new((v4,v5,v6)),PresConstrAnd.new((),()))"),
#		("{[a]->[a']}","PresRelation.new(PresVarTupleIn.new((v1,)),PresVarTupleOut.new((v4,)),PresConstrAnd.new((),()))"),
#		("{[a,b]->[a',b']}","PresRelation.new(PresVarTupleIn.new((v1,v2)),PresVarTupleOut.new((v4,v5)),PresConstrAnd.new((),()))"),
#		("{[a,b,c]->[a',b',c']}","PresRelation.new(PresVarTupleIn.new((v1,v2,v3)),PresVarTupleOut.new((v4,v5,v6)),PresConstrAnd.new((),()))"),
#
#		('{[]->[]:6=7 AND 6!=7}',"PresRelation.new(PresVarTupleIn.new(()),PresVarTupleOut.new(()),c1)"),
#		('{[a]->[]:6=7 AND 6!=7}',"PresRelation.new(PresVarTupleIn.new((v1,)),PresVarTupleOut.new(()),c1)"),
#		('{[a,b]->[]:6=7 AND 6!=7}',"PresRelation.new(PresVarTupleIn.new((v1,v2)),PresVarTupleOut.new(()),c1)"),
#		('{[a,b,c]->[]:6=7 AND 6!=7}',"PresRelation.new(PresVarTupleIn.new((v1,v2,v3)),PresVarTupleOut.new(()),c1)"),
#		("{[]->[a']:6=7 AND 6!=7}","PresRelation.new(PresVarTupleIn.new(()),PresVarTupleOut.new((v4,)),c1)"),
#		("{[]->[a',b']:6=7 AND 6!=7}","PresRelation.new(PresVarTupleIn.new(()),PresVarTupleOut.new((v4,v5)),c1)"),
#		("{[]->[a',b',c']:6=7 AND 6!=7}","PresRelation.new(PresVarTupleIn.new(()),PresVarTupleOut.new((v4,v5,v6)),c1)"),
#		("{[a]->[a']:6=7 AND 6!=7}","PresRelation.new(PresVarTupleIn.new((v1,)),PresVarTupleOut.new((v4,)),c1)"),
#		("{[a,b]->[a',b']:6=7 AND 6!=7}","PresRelation.new(PresVarTupleIn.new((v1,v2)),PresVarTupleOut.new((v4,v5)),c1)"),
#		("{[a,b,c]->[a',b',c']:6=7 AND 6!=7}","PresRelation.new(PresVarTupleIn.new((v1,v2,v3)),PresVarTupleOut.new((v4,v5,v6)),c1)"))
#
#	#Tuple variable test formulas
#	tuple_var_sets=(
#		'{[]}','{[a]}','{[*]}',
#		'{[1:10]}','{[1:10:2]}','{[2*a]}')
#	var_list_sets=(
#		'{[a]}','{[a,b]}','{[a,b,c]}','{[a,b,c,d]}',
#		'{[a,*,1:10,1:10:2,2*a]}','{[i,1,j,2,k,4,*]}','{[i,1:4,j,1:8:2,k,2*a]}')
#	tuple_var_relations=(
#		'{[]->[]}',"{[]->[a']}",'{[a]->[]}',"{[a]->[a']}",
#		'{[*]->[]}','{[]->[*]}','{[*]->[*]}',
#		'{[]->[1:10]}','{[1:10]->[]}','{[1:10]->[1:10]}',
#		'{[]->[1:10:2]}','{[1:10:2]->[]}','{[1:10:2]->[1:10:2]}',
#		'{[]->[2*a]}','{[2*a]->[]}','{[2*a]->[2*a]}')
#	var_list_relations=(
#		'{[a]->[]}','{[a,b]->[c]}','{[a,b,c]->[a,b]}','{[a,b,c,d]->[a,b,c]}','{[a,b,c]->[a,b,c,d]}',
#		'{[]->[a,*,1:10,1:10:2,2*a]}','{[a,*,1:10,1:10:2,2*a]->[]}','{[a,*,1:10,1:10:2,2*a]->[a,*,1:10,1:10:2,2*a]}',
#		'{[]->[i,1,j,2,k,4,*]}','{[i,1,j,2,k,4,*]->[]}','{[i,1,j,2,k,4,*]->[i,1,j,2,k,4,*]}',
#		'{[]->[i,1:4,j,1:8:2,k,2*a]}','{[i,1:4,j,1:8:2,k,2*a]->[]}','{[i,1:4,j,1:8:2,k,2*a]->[i,1:4,j,1:8:2,k,2*a]}',
#		'{[a,b,c]->[a,1,b,2,c,3]}','{[a,1,b,2,c,3]->[a,b,c]}',
#		"{[a,*,10,1:10,1:10:2]->[a',*,10,1:10,1:10:2]}",'{[10:1]->[10:11:5]}',
#		'{[a,(2*a)]->[4-(a+3),b]}')
#
#	#Expression test formulas
#	simple_expression_sets=(
#		'{[1]}','{[a]}','{[-6]}','{[6+2]}','{[2+6]}','{[5*4]}',
#		'{[f(a)]}','{[f(a,b)]}','{[f(a,b,c)]}','{[(6)]}','{[5+((4+3)+(6-2)*8)]}')
#
#	#These sets and relations were taken mostly from the Omega documentation to be used for testing the parser
#	real_sets=(
#		'{[i,j]:1<=i<=10}',
#		'{[i,j]:1<=i,j<=10}',
#		'{[i,j,k]:1<=i,j,k<=10}',
#		'{[i,j,k,l]:1<=i,j,k,l<=10}',
#		'{[i,j]:1<=i<j<=n}',
#		'{[i]:1<=i<=9}',
#		'{[i]:2<=i<=10}',
#		'{[i]:5<=i<=25}',
#		'{[i]:EXISTS([alpha]:2*alpha=i AND 10<=i<=16)}',
#		'{[i]:1<=i<=11 AND EXISTS([a]:i=-2a)}',
#		'{[i]:EXISTS([alpha]:2*alpha=i AND 2<=i<=10)}',
#		'{[i,j]:1<=i+j,j<=10}',
#		'{[i]:2<=i<=n}',
#		'{[i,j]:2<=i<=n AND 1<=j<=i-1}',
#		'{[ir,jr]:1<=ir<=n AND i<=jr<=m}',
#		'{[iw,jw]:1<=iw<=n AND i<=jw<=m AND p(Set)>=0}',
#		'{[iw,jw]:1<=iw<=n AND i<=jw<=m AND p(Set)<0}',
#		'{[t]:1<=t<=n}',
#		'{[x]:0<=x<=100 AND EXISTS([y]:2*n<=y<=x AND x=2y+1)}',
#		'{[a,b,c]:1=1}')
#
#	real_relations=(
#		'{[i]->[i,j]:1<=i<j<=10}',
#		"{[i,j]->[j,j']:1<=i<j<j'<=n}",
#		"{[a,b]->[a',b']}",
#		"{[i,j]->[j,j']:1<=i<j<j'<=n}",
#		'{[i,j]->[i]:1<=i,j<=2}',
#		"{[i,j]->[i]:1<=i<=n AND 1<=j<=m}",
#		'{[p]->[2p,q]}',
#		"{[i,j]->[i]}",
#		"{[i,j]->[2i,q]}",
#		"{[i]->[i']:1<=i,i'<=10 AND i'=i+1}",
#		'{[i]->[i+1]:1<=i<=9}',
#		'{[i]->[i-1]:2<=i<=10}',
#		'{[i]->[i+2]:1<=i<=8}',
#		"{[i]->[i']:1<=i<i'<=10}",
#		"{[i]->[i']:i<=0}",
#		"{[i]->[i']:10<=i}",
#		"{[i]->[i']:1<=i<=9,i'-2}",
#		"{[i]->[i']:1,i'<=i<=9}",
#		'{[4]->[5]}',
#		"{[i]->[i']:5<=i<=25 AND 5<=i'<=25}",
#		"{[i]->[i']:5<=i,i'<=25}",
#		'{[9:16:2]->[17:19]}',
#		'{[i,j,k]->[t,x,z]:2*i+3*j<=5*k,p<=3*x-z=t}',
#		'{[i]->[0,i,0,0]}',
#		'{[i,j]->[1,j,0,i]}',
#		'{[i]->[1,i-1,1,0]}',
#		'{[i]->[j]:1<=i=j<=100 AND f(In)<=f(Out)}',
#		'{[i]->[j]:1<=i<=j<=100 AND f(In)=f(Out)}',
#		'{[i]->[j]:f(j)=f(i) AND 1<=i<j<=100}',
#		"{[i,j]->[i',j']:1<=i<=i'<=n AND NOT (F(i)=F(i')) AND 1<-j,j'<=m}",
#		'{[3a]->[b]}')
#
##Test parser functionality
#class PresParserTestCase(TestCase):
#
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
#class SetTestCase(TestCase):
#
#	def testSet(self):
#		from omega import Set
#
#		Set('{[a,b,a]}')
#		Set('{[a,b,*,c]}')
#		Set('{[a,b]:1=1}')
#		Set('{[a,b]:a=1}')
#		Set('{[a,b]:b=1}')
#		Set('{[a,b]:b=1 && b=a}')
#		Set('{[a]:a>=1}')
#		Set('{[a]:a>=n}')
#		Set('{[a]:a>=f(x)}')
#
#		Set('{[a]:a=0}')
#		Set('{[a]:a!=0}')
#		Set('{[a]:a>0}')
#		Set('{[a]:a>=0}')
#		Set('{[a]:a<0}')
#		Set('{[a]:a<=0}')
#
#		Set('{[a,b]:1<=a<=10<=15}')
#
##	def testOmega(self):
##		from omega import OmegaSet
##		set=OmegaSet(1)
##		set.test_omega()
#
#	def testMoldyn(self):
#		from omega import Set,Relation
#
#		#Iteration Space
#		II_0=Set('{ [ii,stmt] : 0 <= ii <= (n_inter-1) && stmt=1 }').union( Set('{ [ii,stmt] : 0 <= ii <= (n_inter-1) && stmt=2 }') )
#
#		#or better
#		#II_0a=Set('{ [ii,1] : 0 <= ii <= (n_inter-1)  }')
#		#II_0b=Set('{ [ii,2] : 0 <= ii <= (n_inter-1)  }')
#		#or even better
#		#II_0=Set('{ [ii,1:2] : 0 <= ii <= (n_inter-1)  }')
#
#		#Data Spaces
#		X_0=Set('{ [k] : 0 <= k <= (N-1) }')
#		FX_0=Set('{ [k] : 0 <= k <= (N-1) }')
#
#		#Index Arrays
#		INTER1_0=Set('{ [k] : 0 <= ii <= (n_inter-1) }')
#		INTER2_0=Set('{ [k] : 0 <= ii <= (n_inter-1) }')
#
#		#Index Array Value Constraints
#		Relation('{ [ii] -> [inter_func] : inter_func=inter1(i) && not (0 <= ii <= (n_inter-1)) || (0 <= inter1(i) <= (N-1)) }')
#		Relation('{ [ii] -> [inter_func] : inter_func=inter2(i) && not (0 <= ii <= (n_inter-1)) || (0 <= inter2(i) <= (N-1)) }')
#
#		#Data Mappings
#		M_II0_to_X0a=Relation('{ [ii,1] -> [inter_func] : inter_func=inter1(i) && 1 <= j <= T  && 1 <= i <= N }')
#		M_II0_to_X0b=Relation('{ [j,1,i,1] -> [ idx_func ] : idx_func=idx2(i) && 1<=j<= T  && 1<=i<= N }')
#
#class RelationTestCase(TestCase):
#
#	def testRelation(self):
#		from omega import Relation
#
#		Relation("{[a,b]->[a',b']: a=1}")
#		Relation("{[a,b]->[a',b']: b=1}")
#		Relation("{[a,b]->[a',b']: a'=1}")
#		Relation("{[a,b]->[a',b']: b'=1}")
#		Relation("{[a,b]->[a',b']: a=b}")
#		Relation("{[a,b]->[a',b']: a'=b'}")
#		Relation("{[a,b]->[a',b']: a=a' && b=b'}")
#		Relation("{[a,b]->[a',b']: a=b' && b=a'}")
#		Relation("{[a,b]->[a',b']: a=b && a=a' && a'=b'}")
#		Relation("{[a,b]->[a',b']: a=b && a=a' && a'=b' && a=1}")
#
#		Relation("{[a]->[b,c]: a=b && a=a' && a'=b' && a=1}")
#		Relation("{[a,b]->[c,*]: 1<=a<=b<=10}")
#		Relation("{[a,b]->[a',b']: a>=b && (a'>=b' || a=b)}")
#
#		Relation("{[ii] -> [inter_func]: ii>=f(x)}")

