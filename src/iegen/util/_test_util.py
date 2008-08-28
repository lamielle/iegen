#---------- Testing related utility items ----------

#---------- Character tuple generation methods ----------
def tuple_gen(num,from_string):
	num=min(num,len(from_string))
	chars=from_string[:num]
	return (tuple(chars[:num]) for num in xrange(len(chars)+1))

#Returns a generator that returns tuples in the following sequence:
# () ('a',) ('a','b') ('a','b','c') ...
# Up to a tuple of length min(num,len(lowercase))
def lower_gen(num):
	from string import lowercase
	return tuple_gen(num,lowercase)

#Returns a generator that returns tuples in the following sequence:
# () ('A',) ('A','B') ('A','B','C') ...
# Up to a tuple of length min(num,len(uppercase))
def upper_gen(num):
	from string import uppercase
	return tuple_gen(num,uppercase)
#--------------------------------------------------

#Attempts to parse the given formula using the given parsing method
#If a SyntaxError is thrown, calls 'fail' on the given test case with an error string
def parse_test(test_case,formula,parse):
	try:
		result=parse(formula)
	except SyntaxError,e:
		test_case.fail("Syntax error while parsing string '%s': %s"%(formula,e))
	return result

#Attempts to parse the given formula using the given parsing method
#If a SyntaxError is thrown, calls 'fail' on the given test case with an error string
#After parsing, checks if the given AST is equal to the parsed AST
def ast_equality_test(test_case,formula,ast,parse):
	parsed=parse_test(test_case,formula,parse)
	test_case.failUnless(repr(ast)==repr(parsed),"repr(%s): %s!=%s"%(formula,ast,parsed))
	test_case.failUnless(ast==parsed,"eq(%s):%s!=%s"%(formula,ast,parsed))

#Collection of set strings and a string that will create an equivalent ast when executed
test_sets=(
	('{[]}','PresSet(VarTuple([]),Conjunction([]))'),
	("{[a]}","PresSet(VarTuple([VarExp(1,'a')]),Conjunction([]))"),
	("{[a,b]}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([]))"),
	("{[a,b,c]}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b'), VarExp(1,'c')]),Conjunction([]))"),
	("{[]:6=7}","PresSet(VarTuple([]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a]:6=7}","PresSet(VarTuple([VarExp(1,'a')]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a,b]:6=7}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a,b,c]:6=7}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b'), VarExp(1,'c')]),Conjunction([Equality(NormExp([],1))]))"),
	("{[]:6=7}","PresSet(VarTuple([]),Conjunction([Equality(NormExp([],1))]))"),
	("{[]:6=7}","PresSet(VarTuple([]),Conjunction([Equality(NormExp([],1))]))"),
	("{[]:6=7}","PresSet(VarTuple([]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a]:6=7}","PresSet(VarTuple([VarExp(1,'a')]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a,b]:6=7}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a,b,c]:6=7}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b'), VarExp(1,'c')]),Conjunction([Equality(NormExp([],1))]))"),

	("{[a,b]: a=1}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([VarExp(-1,'a')],1))]))"),
	("{[a,b]: b=1}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([VarExp(-1,'b')],1))]))"),
	("{[a,b]: a'=1}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([VarExp(-1,\"a'\")],1))]))"),
	("{[a,b]: b'=1}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([VarExp(-1,\"b'\")],1))]))"),
	("{[a,b]: a=b}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([VarExp(-1,'b'), VarExp(1,'a')],0))]))"),
	("{[a,b]: a'=b'}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([VarExp(-1,\"b'\"), VarExp(1,\"a'\")],0))]))"),
	("{[a,b]: a=a' && b=b'}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([VarExp(-1,\"a'\"), VarExp(1,'a')],0)), Equality(NormExp([VarExp(-1,\"b'\"), VarExp(1,'b')],0))]))"),
	("{[a,b]: a=b' && b=a'}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([VarExp(-1,'b'), VarExp(1,\"a'\")],0)), Equality(NormExp([VarExp(-1,\"b'\"), VarExp(1,'a')],0))]))"),
	("{[a,b]: a=b && a=a' and a'=b'}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([VarExp(-1,\"a'\"), VarExp(1,'a')],0)), Equality(NormExp([VarExp(-1,'b'), VarExp(1,'a')],0)), Equality(NormExp([VarExp(-1,\"b'\"), VarExp(1,\"a'\")],0))]))"),
	("{[a,b]: a=b && a=a' and a'=b' && a=1}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Equality(NormExp([VarExp(-1,\"a'\"), VarExp(1,'a')],0)), Equality(NormExp([VarExp(-1,'b'), VarExp(1,'a')],0)), Equality(NormExp([VarExp(-1,\"b'\"), VarExp(1,\"a'\")],0)), Equality(NormExp([VarExp(-1,'a')],1))]))"),
	("{[a,b]: 1<=a and a<=b && b<=10}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Inequality(NormExp([VarExp(1,'a')],-1)), Inequality(NormExp([VarExp(-1,'a'), VarExp(1,'b')],0)), Inequality(NormExp([VarExp(-1,'b')],10))]))"),
	("{[a,b]: a>=b && c>=d AND a=b}","PresSet(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),Conjunction([Inequality(NormExp([VarExp(-1,'b'), VarExp(1,'a')],0)), Inequality(NormExp([VarExp(-1,'d'), VarExp(1,'c')],0)), Equality(NormExp([VarExp(-1,'b'), VarExp(1,'a')],0))]))"),
	("{[ii]: ii>=f(x)}","PresSet(VarTuple([VarExp(1,'ii')]),Conjunction([Inequality(NormExp([VarExp(1,'ii'), FuncExp(-1,'f',[NormExp([VarExp(1,'x')],0)])],0))]))"),
	("{[a]:f(a,a)>=0}","PresSet(VarTuple([VarExp(1,'a')]),Conjunction([Inequality(NormExp([FuncExp(1,'f',[NormExp([VarExp(1,'a')],0), NormExp([VarExp(1,'a')],0)])],0))]))"),
	("{[a]:f(g(a,a))>=0}","PresSet(VarTuple([VarExp(1,'a')]),Conjunction([Inequality(NormExp([FuncExp(1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'a')],0), NormExp([VarExp(1,'a')],0)])],0)])],0))]))"),
	("{[a]:3f(5*g(2a,-5*a)-5)>=0}","PresSet(VarTuple([VarExp(1,'a')]),Conjunction([Inequality(NormExp([FuncExp(3,'f',[NormExp([FuncExp(5,'g',[NormExp([VarExp(-5,'a')],0), NormExp([VarExp(2,'a')],0)])],-5)])],0))]))"))

#PresParser.parse_set('{[i,j,k]}')
#
#PresParser.parse_set('{[i,j,k]: 1 <= i && i <= 45 }')
##PresParser.parse_set('{[i,j,k]: i!=54 }')
#PresParser.parse_set('{[i,j,k]: 1 <= i && 1<=j && 1<=k && i<= 45 && j<=45 && k<=45 }')

#PresParser.parse_set('{ [ii,j] : j=1 && 0 <= ii && ii <= (n_inter-1)  } union { [ii,j] : j=2 && 0 <= ii && ii <= (n_inter-1)  }')
#PresParser.parse_set('{ [k] : 0 <= k && k <= (N-1) }')
#PresParser.parse_set('{ [k] : 0 <= k && k <= (n_inter-1) }')
#
#PresParser.parse_set('{ [k] : 0 <= k && k <= (n_inter-1) }')
#		'{[1]}','{[a]}','{[-6]}','{[6+2]}','{[2+6]}','{[5*4]}',
#		'{[f(a)]}','{[f(a,b)]}','{[f(a,b,c)]}','{[(6)]}','{[5+((4+3)+(6-2)*8)]}')
#
#	#These sets and relations were taken mostly from the Omega documentation to be used for testing the parser
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

#Collection of relation strings and a string that will create an equivalent ast when executed
test_relations=(
	("{[]->[]}","PresRelation(VarTuple([]),VarTuple([]),Conjunction([]))"),
	("{[a]->[]}","PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([]),Conjunction([]))"),
	("{[a,b]->[]}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([]),Conjunction([]))"),
	("{[a,b,c]->[]}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b'), VarExp(1,'c')]),VarTuple([]),Conjunction([]))"),
	("{[]->[a']}","PresRelation(VarTuple([]),VarTuple([VarExp(1,\"a'\")]),Conjunction([]))"),
	("{[]->[a',b']}","PresRelation(VarTuple([]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([]))"),
	("{[]->[a',b',c']}","PresRelation(VarTuple([]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\"), VarExp(1,\"c'\")]),Conjunction([]))"),
	("{[a]->[a']}","PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,\"a'\")]),Conjunction([]))"),
	("{[a,b]->[a',b']}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([]))"),
	("{[a,b,c]->[a',b',c']}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b'), VarExp(1,'c')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\"), VarExp(1,\"c'\")]),Conjunction([]))"),
	("{[]->[]:6=7}","PresRelation(VarTuple([]),VarTuple([]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a]->[]:6=7}","PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a,b]->[]:6=7}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a,b,c]->[]:6=7}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b'), VarExp(1,'c')]),VarTuple([]),Conjunction([Equality(NormExp([],1))]))"),
	("{[]->[a']:6=7}","PresRelation(VarTuple([]),VarTuple([VarExp(1,\"a'\")]),Conjunction([Equality(NormExp([],1))]))"),
	("{[]->[a',b']:6=7}","PresRelation(VarTuple([]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([],1))]))"),
	("{[]->[a',b',c']:6=7}","PresRelation(VarTuple([]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\"), VarExp(1,\"c'\")]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a]->[a']:6=7}","PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,\"a'\")]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a,b]->[a',b']:6=7}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([],1))]))"),
	("{[a,b,c]->[a',b',c']:6=7}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b'), VarExp(1,'c')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\"), VarExp(1,\"c'\")]),Conjunction([Equality(NormExp([],1))]))"),

	("{[a,b]->[a',b']: a=1}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([VarExp(-1,'a')],1))]))"),
	("{[a,b]->[a',b']: b=1}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([VarExp(-1,'b')],1))]))"),
	("{[a,b]->[a',b']: a'=1}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([VarExp(-1,\"a'\")],1))]))"),
	("{[a,b]->[a',b']: b'=1}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([VarExp(-1,\"b'\")],1))]))"),
	("{[a,b]->[a',b']: a=b}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([VarExp(-1,'b'), VarExp(1,'a')],0))]))"),
	("{[a,b]->[a',b']: a'=b'}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([VarExp(-1,\"b'\"), VarExp(1,\"a'\")],0))]))"),
	("{[a,b]->[a',b']: a=a' && b=b'}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([VarExp(-1,\"a'\"), VarExp(1,'a')],0)), Equality(NormExp([VarExp(-1,\"b'\"), VarExp(1,'b')],0))]))"),
	("{[a,b]->[a',b']: a=b' && b=a'}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([VarExp(-1,'b'), VarExp(1,\"a'\")],0)), Equality(NormExp([VarExp(-1,\"b'\"), VarExp(1,'a')],0))]))"),
	("{[a,b]->[a',b']: a=b && a=a' and a'=b'}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([VarExp(-1,\"a'\"), VarExp(1,'a')],0)), Equality(NormExp([VarExp(-1,'b'), VarExp(1,'a')],0)), Equality(NormExp([VarExp(-1,\"b'\"), VarExp(1,\"a'\")],0))]))"),
	("{[a,b]->[a',b']: a=b && a=a' and a'=b' && a=1}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,\"a'\"), VarExp(1,\"b'\")]),Conjunction([Equality(NormExp([VarExp(-1,\"a'\"), VarExp(1,'a')],0)), Equality(NormExp([VarExp(-1,'b'), VarExp(1,'a')],0)), Equality(NormExp([VarExp(-1,\"b'\"), VarExp(1,\"a'\")],0)), Equality(NormExp([VarExp(-1,'a')],1))]))"),
	("{[a,b]->[c,d]: 1<=a and a<=b && b<=10}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,'c'), VarExp(1,'d')]),Conjunction([Inequality(NormExp([VarExp(1,'a')],-1)), Inequality(NormExp([VarExp(-1,'a'), VarExp(1,'b')],0)), Inequality(NormExp([VarExp(-1,'b')],10))]))"),
	("{[a,b]->[c,d]: a>=b && c>=d AND a=b}","PresRelation(VarTuple([VarExp(1,'a'), VarExp(1,'b')]),VarTuple([VarExp(1,'c'), VarExp(1,'d')]),Conjunction([Inequality(NormExp([VarExp(-1,'b'), VarExp(1,'a')],0)), Inequality(NormExp([VarExp(-1,'d'), VarExp(1,'c')],0)), Equality(NormExp([VarExp(-1,'b'), VarExp(1,'a')],0))]))"),
	("{[ii] -> [inter_func]: ii>=f(x)}","PresRelation(VarTuple([VarExp(1,'ii')]),VarTuple([VarExp(1,'inter_func')]),Conjunction([Inequality(NormExp([VarExp(1,'ii'), FuncExp(-1,'f',[NormExp([VarExp(1,'x')],0)])],0))]))"),
	("{[a]->[b]:f(a,a)>=0}","PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,'b')]),Conjunction([Inequality(NormExp([FuncExp(1,'f',[NormExp([VarExp(1,'a')],0), NormExp([VarExp(1,'a')],0)])],0))]))"),
	("{[a]->[b]:f(g(a,a))>=0}","PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,'b')]),Conjunction([Inequality(NormExp([FuncExp(1,'f',[NormExp([FuncExp(1,'g',[NormExp([VarExp(1,'a')],0), NormExp([VarExp(1,'a')],0)])],0)])],0))]))"),
	("{[a]->[b]:3f(5*g(2a,-5*a)-5)>=0}","PresRelation(VarTuple([VarExp(1,'a')]),VarTuple([VarExp(1,'b')]),Conjunction([Inequality(NormExp([FuncExp(3,'f',[NormExp([FuncExp(5,'g',[NormExp([VarExp(-5,'a')],0), NormExp([VarExp(2,'a')],0)])],-5)])],0))]))"))

#PresParser.parse_relation('{[i] -> [j]}')
#PresParser.parse_relation('{[i] -> [j] : i = j }')
#PresParser.parse_relation('{[i] -> [j] : i = delta(j) }')
#PresParser.parse_relation('{[i] -> [j] : i = sigma(delta(j)) }')

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
#---------------------------------------------------
