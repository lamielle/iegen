from unittest import TestCase
from iegen.lib.nose.tools import raises

#---------- Import Tests ----------
#Test importing of iegen
class ImportTestCase(TestCase):

	#Test simple importing of iegen
	def testImport(self):
		try:
			import iegen
		except Exception,e:
			self.fail("'import iegen' failed: "+str(e))

	#Test simple importing of iegen classes
	def testNameImport(self):
		try:
			from iegen import IEGenObject,MapIR,Symbolic,DataArray,IndexArray,AccessRelation,Statement,FunctionCallSpec,DataDependence,Set,Relation

			#SparseFormula related imports
			from iegen import SparseFormula,SparseExpColumnType,TupleVarCol,SymbolicCol,FreeVarCol,ConstantCol,UFCall,SparseExp,SparseConstraint,SparseEquality,SparseInequality
		except Exception,e:
			self.fail("Importing classes from iegen failed: "+str(e))
#----------------------------------

#---------- Set Tests ----------
class SetTestCase(TestCase):

	#Tests that we can create a very simple set
	def testCreation(self):
		from iegen import Set

		Set('{[a]}')

	#Tests that we can get the tuple variable names
	def testTupleVarNames(self):
		from iegen import Set

		set=Set('{[a,b,c]}')

		self.failUnless('a'==set.tuple_vars[0],"First tuple var is not 'a'")
		self.failUnless('b'==set.tuple_vars[1],"Second tuple var is not 'b'")
		self.failUnless('c'==set.tuple_vars[2],"Third tuple var is not 'c'")
		self.failUnless('a'==set.tuple_set[0],"First tuple var is not 'a'")
		self.failUnless('b'==set.tuple_set[1],"Second tuple var is not 'b'")
		self.failUnless('c'==set.tuple_set[2],"Third tuple var is not 'c'")

	#Tests that we can get the symbolics
	def testSymbolics(self):
		from iegen import Set,Symbolic

		set=Set('{[a,b,c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(Symbolic('m')==set.symbolics[0],"First symbolic is not 'm'")
		self.failUnless(Symbolic('n')==set.symbolics[1],"Second symbolic is not 'n'")

	#Tests that we can get the symbolic names
	def testSymbolicNames(self):
		from iegen import Set,Symbolic

		set=Set('{[a,b,c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless('m'==set.symbolic_names[0],"First symbolic is not 'm'")
		self.failUnless('n'==set.symbolic_names[1],"Second symbolic is not 'n'")

	#Tests that we can get the symbolic names
	def testArity(self):
		from iegen import Set,Symbolic

		set=Set('{[a,b,c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(3==set.arity(),"Set's arity is not 3")

	#Test the __str__ method
	def testStr(self):
		from iegen import Set,Symbolic

		set_string='{[a,b]}'
		set=Set(set_string)
		res_string='{[a,b]}'

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

		set_string='{[a,b]: b=2n and a=10 and a>=m}'
		set=Set(set_string,[Symbolic('n'),Symbolic('m')])
		res_string='{[a,b]: b=2n and a=10 and a>=m | m,n}'

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

		set_string='{[a,b]: b=2n and a=10 and a+b>=c and a>=m}'
		set=Set(set_string,[Symbolic('n'),Symbolic('m')])
		res_string='{[a,b]: b=2n and a=10 and a+b>=c and a>=m | m,n}'

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

	def testStrEmptyInequality1(self):
		from iegen import Set

		set_string='{[a,b]: 0>=a+b}'

		set=Set(set_string)

		res_string=set_string

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

	def testStrEmptyInequality2(self):
		from iegen import Set

		set_string='{[a,b]: a+b>=0}'

		set=Set(set_string)

		res_string=set_string

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

	#Test the __repr__ method
	def testRepr(self):
		from iegen import Set,Symbolic

		set_string='{[a,b]: b=2n and a=10 and a>=m}'
		symbolics=[Symbolic('m'),Symbolic('n')]
		set=Set(set_string,symbolics)
		res_string='{[a,b]: b=2n and a=10 and a>=m | m,n}'
		res_string='Set("%s",%s)'%(res_string,repr(symbolics))

		self.failUnless(res_string==repr(set),'%s!=%s'%(repr(set),res_string))

		set_string='{[a,b]: b=2n and a=10 and a+b>=c and a>=m}'
		set=Set(set_string,symbolics)
		res_string='{[a,b]: b=2n and a=10 and a+b>=c and a>=m | m,n}'
		res_string='Set("%s",%s)'%(res_string,repr(symbolics))

		self.failUnless(res_string==repr(set),'%s!=%s'%(repr(set),res_string))

	def testDuplicateConstraint(self):
		from iegen import Set

		set_string='{[a]: a=10 and a=10}'
		set=Set(set_string)
		res_string=str(Set('{[a]: a=10}'))

		self.failUnless(res_string==str(set),'%s!=%s'%(str(set),res_string))

	def testSetEquality(self):
		from iegen import Set

		set1_string='{[a,b]: a=10 and b>=0 and a>=0}'
		set2_string='{[c,d]: c=10 and d>=0 and c>=0}'
		set3_string='{[a,d]: a=10 and d>=0 and a>=0}'

		set1=Set(set1_string)
		set2=Set(set2_string)
		set3=Set(set3_string)

		self.failUnless(set1==set2,'%s!=%s'%(set1,set2))
		self.failUnless(set1==set3,'%s!=%s'%(set1,set3))
		self.failUnless(set2==set3,'%s!=%s'%(set2,set3))

	def testCopy(self):
		from iegen import Set,Symbolic

		set=Set('{[a,b]: a=b and b=n}',symbolics=[Symbolic('n')])
		set_copy=set.copy()

		self.failIf(set_copy is set,'Copy returns same Set instance')
		self.failUnless(set_copy==set,'%s!=%s'%(set_copy,set))

		set=Set('{[a,b]: a=f(b) and b=n}',symbolics=[Symbolic('n')])
		set_copy=set.copy()

		self.failIf(set_copy is set,'Copy returns same Set instance')
		self.failUnless(set_copy==set,'%s!=%s'%(set_copy,set))

	def testSimpleFunction(self):
		from iegen import Set

		set_string='{[a,b]: b=f(a)}'

		set=Set(set_string)
		res_string=str(set)

		self.failUnless(res_string==set_string,'%s!=%s'%(res_string,set_string))

	def testNestedFunction(self):
		from iegen import Set

		set_string='{[a,b]: b=f(g(a))}'

		set=Set(set_string)
		res_string=str(set)

		self.failUnless(res_string==set_string,'%s!=%s'%(res_string,set_string))

	def testTwoArgumentFunction(self):
		from iegen import Set

		set_string='{[a,b,c]: c=f(a,b)}'

		set=Set(set_string)
		res_string=str(set)

		self.failUnless(res_string==set_string,'%s!=%s'%(res_string,set_string))

	def testConstantArgumentFunction(self):
		from iegen import Set

		set_string='{[a,b]: b=f(a,6)}'

		set=Set(set_string)
		res_string=str(set)

		self.failUnless(res_string==set_string,'%s!=%s'%(res_string,set_string))

	#Tests that a frozen set cannot be cleared
	@raises(ValueError)
	def testClearFrozen(self):
		from iegen import Set

		set1=Set('{[a]: a=10}')

		set1.clear()

	def testClear(self):
		from iegen import Set

		set1=Set('{[a,b,c]: a=b and c>10}',freeze=False)

		self.failUnless(1==len(set1.disjunction),'Set does not have exactly one conjunction')
		self.failUnless(2==len(list(set1.disjunction.conjunctions)[0]),'Set conjunction does not have exactly two constraints')

		set1.clear()

		self.failUnless(0==len(set1.disjunction),'Set does not have exactly zero conjunctions')

	@raises(ValueError)
	def testModifyFrozen1(self):
		from iegen import Set,SparseConjunction

		set1=Set('{[a,b,c]}')
		set1.add_conjunction(SparseConjunction())

	@raises(ValueError)
	def testModifyFrozen2(self):
		from iegen import Set,SparseDisjunction

		set1=Set('{[a,b,c]}')
		set1.add_disjunction(SparseDisjunction())

	def testManualConstruction(self):
		from iegen import Set

		set1=Set('{[a,b,c]}',freeze=False)

		#Add conjunction a=b and b>=c
		set1.clear()
		set1.add_conjunction(set1.get_conjunction([set1.get_equality({set1.get_column('a'):1,set1.get_column('b'):-1}),set1.get_inequality({set1.get_column('b'):1,set1.get_column('c'):-1})]))
		set1.freeze()

		set_res=Set('{[a,b,c]: a=b and b>=c}')

		self.failUnless(set1==set_res,'%s!=%s'%(set1,set_res))

	#Tests that the bounds method fails when given variable names that aren't part of the tuple
	@raises(ValueError)
	def testBoundsNonTupleVarFail(self):
		from iegen import Set
		set=Set('{[a,b]: 1<=a and a<=10 and 1<=b and b<=10}')
		set.bounds('c')

	#Tests that the bounds method fails with a non 1 and non -1 coefficient
	@raises(ValueError)
	def testBoundsNonOneCoeffFail1(self):
		from iegen import Set
		set=Set('{[a]: 3a>=10}')
		set.bounds('a')

	@raises(ValueError)
	def testBoundsNonOneCoeffFail2(self):
		from iegen import Set
		set=Set('{[a]: -3a>=10}')
		set.bounds('a')

	#Tests that the proper upper and lower bounds are calculated for a 1d set
	def testBounds1D(self):
		from iegen import Set

		set1=Set('{[a]: 1<=a and a<=10}')

		lbs=set([set1.get_expression({set1.get_constant_column():1})])
		ubs=set([set1.get_expression({set1.get_constant_column():10})])
		b_res=((lbs,ubs),)
		lb_res=(lbs,)
		ub_res=(ubs,)
		self.failUnless(set1.lower_bounds('a')==lb_res,"The lower bound of 'a' is not 1")
		self.failUnless(set1.upper_bounds('a')==ub_res,"The upper bound of 'a' is not 10")
		self.failUnless(set1.bounds('a')==b_res,"The bounds of 'a' are not (1,10)")

	#Tests that the proper upper and lower bounds are calculated for a 2d set
	def testBounds2D(self):
		from iegen import Set

		set1=Set('{[a,b]: 5<=a and a<=20 and -10<=b and b<=0}')

		lbs=set([set1.get_expression({set1.get_constant_column():5})])
		ubs=set([set1.get_expression({set1.get_constant_column():20})])
		b_res=((lbs,ubs),)
		lb_res=(lbs,)
		ub_res=(ubs,)
		self.failUnless(set1.lower_bounds('a')==lb_res,"The lower bound of 'a' is not 5 in set %s"%set1)
		self.failUnless(set1.upper_bounds('a')==ub_res,"The upper bound of 'a' is not 20")
		self.failUnless(set1.bounds('a')==b_res,"The bounds of 'a' are not (5,20)")

		lbs=set([set1.get_expression({set1.get_constant_column():-10})])
		ubs=set([set1.get_expression({set1.get_constant_column():0})])
		b_res=((lbs,ubs),)
		lb_res=(lbs,)
		ub_res=(ubs,)
		self.failUnless(set1.lower_bounds('b')==lb_res,"The lower bound of 'b' is not -10")
		self.failUnless(set1.upper_bounds('b')==ub_res,"The upper bound of 'b' is not 0")
		self.failUnless(set1.bounds('b')==b_res,"The bounds of 'b' are not (-10,0)")

	#Tests that the proper upper and lower bounds are calculated for a 2d set with symbolics
	def testBoundsSymbolic(self):
		from iegen import Set,Symbolic

		set1=Set('{[a,b]: 5<=a and a<=n and m<=b and b<=0}',[Symbolic('n'),Symbolic('m')])

		lbs=set([set1.get_expression({set1.get_constant_column():5})])
		ubs=set([set1.get_expression({set1.get_column('n'):1})])
		b_res=((lbs,ubs),)
		lb_res=(lbs,)
		ub_res=(ubs,)
		self.failUnless(set1.lower_bounds('a')==lb_res,"The lower bound of 'a' is not 5")
		self.failUnless(set1.upper_bounds('a')==ub_res,"The upper bound of 'a' is not n")
		self.failUnless(set1.bounds('a')==b_res,"The bounds of 'a' are not (5,n)")

		lbs=set([set1.get_expression({set1.get_column('m'):1})])
		ubs=set([set1.get_expression({set1.get_constant_column():0})])
		b_res=((lbs,ubs),)
		lb_res=(lbs,)
		ub_res=(ubs,)
		self.failUnless(set1.lower_bounds('b')==lb_res,"The lower bound of 'b' is not m")
		self.failUnless(set1.upper_bounds('b')==ub_res,"The upper bound of 'b' is not 0")
		self.failUnless(set1.bounds('b')==b_res,"The bounds of 'b' are not (m,0)")

	#Tests that the proper upper and lower bounds are calculated for a 2d set with symbolics
	def testBoundsSymbolicMuliTerm(self):
		from iegen import Set,Symbolic

		set1=Set('{[a,b]: 5<=a and a<=n+m+10 and m-6<=b and b<=0}',[Symbolic('n'),Symbolic('m')])

		lbs=set([set1.get_expression({set1.get_constant_column():5})])
		ubs=set([set1.get_expression({set1.get_column('n'):1,set1.get_column('m'):1,set1.get_constant_column():10})])
		b_res=((lbs,ubs),)
		lb_res=(lbs,)
		ub_res=(ubs,)
		self.failUnless(set1.lower_bounds('a')==lb_res,"The lower bound of 'a' is not 5")
		self.failUnless(set1.upper_bounds('a')==ub_res,"The upper bound of 'a' is not n+m+10")
		self.failUnless(set1.bounds('a')==b_res,"The bounds of 'a' are not (5,n+m+10)")

		lbs=set([set1.get_expression({set1.get_column('m'):1,set1.get_constant_column():-6})])
		ubs=set([set1.get_expression({set1.get_constant_column():0})])
		b_res=((lbs,ubs),)
		lb_res=(lbs,)
		ub_res=(ubs,)
		self.failUnless(set1.lower_bounds('b')==lb_res,"The lower bound of 'b' is not m-6")
		self.failUnless(set1.upper_bounds('b')==ub_res,"The upper bound of 'b' is not 0")
		self.failUnless(set1.bounds('b')==b_res,"The bounds of 'b' are not (m-6,0)")

	#Tests that the proper upper and lower bounds are calculated for a 2d set with mutiple conjunctions and multiple upper and lower bounds
	def testBoundsMultiConjunction(self):
		from iegen import Set

		set1=Set('{[a,b]: 5<=a and 10<=a and a<=b and a<=20}').union(Set('{[a,b]: -5<=a and -10<=a and a<=-b and a<=-20}'))

		lbs1=set([set1.get_expression({set1.get_constant_column():5}),set1.get_expression({set1.get_constant_column():10})])
		ubs1=set([set1.get_expression({set1.get_column('b'):1}),set1.get_expression({set1.get_constant_column():20})])
		lbs2=set([set1.get_expression({set1.get_constant_column():-5}),set1.get_expression({set1.get_constant_column():-10})])
		ubs2=set([set1.get_expression({set1.get_column('b'):-1}),set1.get_expression({set1.get_constant_column():-20})])
		b_res=((lbs1,ubs1),(lbs2,ubs2))
		lb_res=(lbs1,lbs2)
		ub_res=(ubs1,ubs2)
		self.failUnless(set1.lower_bounds('a')==lb_res,"The lower bound of 'a' is not ((5,10),(-5,-10))")
		self.failUnless(set1.upper_bounds('a')==ub_res,"The upper bound of 'a' is not ((b,20),(-b,-20))")
		self.failUnless(set1.bounds('a')==b_res,"The bounds of 'a' are not (((5,10),(b,20)),((-5,-10),(-b,-20)))")

	#Tests that Set implements __len__
	def testLen1(self):
		from iegen import Set

		self.failUnless(1==len(Set('{[a]: a=10}')))
	def testLen2(self):
		from iegen import Set

		self.failUnless(2==len(Set('{[a]: a=10}').union(Set('{[a]: a=5}'))))

	#----------------------------------------
	# Start simplification tests

	def testSimplifyEqualityFree(self):
		from iegen import Set

		set=Set('{[a,b]: a=c and c=b}')

		set_res=Set('{[a,b]: a=b}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyEqualityFunction(self):
		from iegen import Set

		set=Set('{[a,b]: b=c and c=f(a)}')

		set_res=Set('{[a,b]: b=f(a)}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyInequality(self):
		from iegen import Set

		set=Set('{[a,b]: a>=b and a<=b}')

		set_res=Set('{[a,b]: a=b}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyInequalitySub(self):
		from iegen import Set

		set=Set('{[a,b]: a>=c and c>=b}')

		set_res=Set('{[a,b]: a>=b}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyMixed1(self):
		from iegen import Set

		set=Set('{[a,b,c,d]: 2e+3a=5b and 7c>=11d+13e}')

		set_res=Set('{[a,b,c,d]: 14c>=22d+65b-39a}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyMixed2(self):
		from iegen import Set

		set=Set('{[a,b,c,d]: -2e+3a=5b and 7c>=11d+13e}')

		set_res=Set('{[a,b,c,d]: -14c<=-22d+65b-39a}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyRemoveTrue(self):
		from iegen import Set

		set=Set('{[a]: 10>=0}')

		set_res=Set('{[a]}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyReplaceInFunction1(self):
		from iegen import Set

		set=Set('{[a,b]: b=f(c) and c=g(a)}')

		set_res=Set('{[a,b]: b=f(g(a))}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyReplaceInFunction2(self):
		from iegen import Set

		set=Set('{[a,b]: 2b=3f(7c) and c=2g(5a)}')

		set_res=Set('{[a,b]: 2b=3f(14g(5a))}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyInverseFunction1(self):
		from iegen import Set
		import iegen.simplify

		iegen.simplify.register_inverse_pair('g')
		set=Set('{[a,b]: a=g(c) and b=f(c)}')
		iegen.simplify.unregister_inverse_pair('g')

		set_res=Set('{[a,b]: b=f(g_inv(a))}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyInverseFunction2(self):
		from iegen import Set
		import iegen.simplify

		iegen.simplify.register_inverse_pair('g')
		set=Set('{[a,b,c,d]: a+b=g(e)+c and b=f(e)}')
		iegen.simplify.unregister_inverse_pair('g')

		set_res=Set('{[a,b,c,d]: b=f(g_inv(a+b-c))}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	def testSimplifyInverseFunction3(self):
		from iegen import Set
		import iegen.simplify

		iegen.simplify.register_inverse_pair('g')
		set=Set('{[a,b,c,d]: 2a+3b=g(e)+7c and 11b=13f(17e)}')
		iegen.simplify.unregister_inverse_pair('g')

		set_res=Set('{[a,b,c,d]: 11b=13f(17g_inv(2a+3b-7c))}')

		self.failUnless(set==set_res,'%s!=%s'%(set,set_res))

	# End simplification tests
	#----------------------------------------

	#----------------------------------------
	# Start operation tests

	#Tests that hash doesn't work on an unfrozen set
	@raises(ValueError)
	def testHashUnfrozen(self):
		from iegen import Set

		hash(Set('{[a,b]}',freeze=False))

	#Tests that equality doesn't work on an unfrozen set
	@raises(ValueError)
	def testEqualityUnfrozen1(self):
		from iegen import Set

		Set('{[a,b]}',freeze=False)==Set('{[a,b]}')

	@raises(ValueError)
	def testEqualityUnfrozen2(self):
		from iegen import Set

		Set('{[a,b]}')==Set('{[a,b]}',freeze=False)

	#Tests that union does not allow sets of differing arity
	@raises(ValueError)
	def testUnionDiffArity(self):
		from iegen import Set

		set1=Set('{[]}')
		set2=Set('{[a]}')
		set1.union(set2)

	#Tests that union is not destructive
	def testUnionNonDestructive(self):
		from iegen import Set

		set1=Set('{[a]}')
		set2=Set('{[b]}')
		unioned=set1.union(set2)

		self.failIf(unioned is set1,'%s is %s'%(unioned,set1))
		self.failIf(unioned is set2,'%s is %s'%(unioned,set2))

	#Tests that the union operation doesn't work on an unfrozen set
	@raises(ValueError)
	def testUnionUnfrozen1(self):
		from iegen import Set

		set1=Set('{[a,b]}',freeze=False)
		set2=Set('{[c,d]}')

		set1.union(set2)

	@raises(ValueError)
	def testUnionUnfrozen2(self):
		from iegen import Set

		set1=Set('{[a,b]}')
		set2=Set('{[c,d]}',freeze=False)

		set1.union(set2)

	#Tests the union operation
	def testUnionEmpty(self):
		from iegen import Set

		set1=Set('{[a,b]}')
		set2=Set('{[c,d]}')

		set3=set1.union(set2)

		self.failUnless(1==len(set3.disjunction),'Unioned set should have exactly one conjunction')
		self.failUnless(set3==set1,'%s!=%s'%(set3,set1))
		self.failUnless(set2==set1,'%s!=%s'%(set2,set1))

	def testUnionConstraints(self):
		from iegen import Set

		set1=Set('{[a,b]: a=b}')
		set2=Set('{[c,d]: c=10 and d=10}')

		set_union=set1.union(set2)

		res_union=Set('{[a,b]}',freeze=False)
		res_union.clear()
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_column('b'):-1})]))
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_constant_column():-10}),res_union.get_equality({res_union.get_column('b'):1,res_union.get_constant_column():-10})]))
		res_union.freeze()

		self.failUnless(2==len(set_union.disjunction),'Unioned set should have exactly two conjunctions')
		self.failUnless(set_union==res_union,'%s!=%s'%(set_union,res_union))

		set1=Set('{[a,b]: a=b}')
		set2=Set('{[c,d]: c=d}')

		set_union=set1.union(set2)

		res_union=Set('{[a,b]}',freeze=False)
		res_union.clear()
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_column('b'):-1})]))
		res_union.freeze()

		self.failUnless(1==len(set_union.disjunction),'Unioned set should have exactly one conjunction')
		self.failUnless(set_union==res_union,'%s!=%s'%(set_union,res_union))

	def testUnionStr(self):
		from iegen import Set

		set1=Set('{[a,b]: a=b}')
		set2=Set('{[c,d]: c=10}')

		set_union=set1.union(set2)

		res_str='{[a,b]: a=10} union {[a,b]: a=b}'

		self.failUnless(res_str==str(set_union),'%s!=%s'%(str(set_union),res_str))

	#Tests that the apply operation doesn't work on unfrozen sets/relations
	@raises(ValueError)
	def testApplyUnfrozen1(self):
		from iegen import Set,Relation

		set=Set('{[a,b]: a=b}',freeze=False)
		relation=Relation('{[a]->[b]: b=10}')
		set.apply(relation)

	@raises(ValueError)
	def testApplyUnfrozen2(self):
		from iegen import Set,Relation

		set=Set('{[a,b]: a=b}')
		relation=Relation('{[a]->[b]: b=10}',freeze=False)
		set.apply(relation)

	#Tests that apply is not destructive
	def testApplyNonDestructive(self):
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[a]->[b]}')
		applied=set.apply(relation)

		self.failIf(applied is set,'%s is %s'%(applied,set))

	#Tests that apply fails when the arity of the set does not match the input arity of the relation
	@raises(ValueError)
	def testApplyArityFail1(self):
		from iegen import Set,Relation

		set=Set('{[a,b]}')
		relation=Relation('{[b]->[b]}')
		applied=set.apply(relation)

	@raises(ValueError)
	def testApplyArityFail2(self):
		from iegen import Set,Relation

		set=Set('{[a,b,c]}')
		relation=Relation('{[a,b]->[e,f]}')
		applied=set.apply(relation)

	#Tests the apply operation
	def testApply(self):
		from iegen import Set,Relation

		set=Set('{[a,b]:1<=a and a<=10}')
		relation=Relation('{[d,e]->[f,g,h]:d=f && 3e<=2h and h<=2e+1 and 11<=e and e<=13 and -10<=g and g<=0}')

		applied=set.apply(relation)

		applied_res=Set('{[f,g,h]: 1<=f and f<=10 && -10<=g and g<=0 and 33<=2h and -3<=h and h<=27}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests that variable name collisions are handled
	def testApplyRename(self):
		from iegen import Set,Relation

		set=Set('{[b,d]}')
		relation=Relation('{[a,b]->[c,d]}')

		applied=set.apply(relation)

		applied_res=Set('{[c,d]: b0=a and d0=b}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	#Tests the apply operation with equality constraints
	def testApplyEquality1(self):
		from iegen import Set,Relation

		set=Set('{[a]}')
		relation=Relation('{[d]->[e,f]:e=d and f=d}')

		applied=set.apply(relation)

		applied_res=Set('{[e,f]: e=f}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	def testApplyEquality2(self):
		from iegen import Set,Relation

		set=Set('{[a]: a=10}')
		relation=Relation('{[b]->[c,d]: b=c and d=10}')

		applied=set.apply(relation)

		applied_res=Set('{[c,d]: c=10 and d=10}')

		self.failUnless(applied==applied_res,'%s!=%s'%(applied,applied_res))

	# End operation tests
	#----------------------------------------
#-------------------------------------

#---------- Relation Tests ----------
class RelationTestCase(TestCase):

	#Tests that we can create a very simple relation
	def testCreation(self):
		from iegen import Relation

		Relation('{[a]->[b]}')

	#Tests that the names bijection is created correctly
	def testTupleVarNames(self):
		from iegen import Relation

		rel=Relation('{[a,b]->[c]}')

		self.failUnless(3==len(rel.tuple_vars),'The relation does not have 3 tuple vars')
		self.failUnless(2==len(rel.tuple_in),'The relation does not have 2 input tuple vars')
		self.failUnless(1==len(rel.tuple_out),'The relation does not have 1 output tuple var')

		self.failUnless('a'==rel.tuple_vars[0],"First tuple var is not 'a'")
		self.failUnless('b'==rel.tuple_vars[1],"Second tuple var is not 'b'")
		self.failUnless('c'==rel.tuple_vars[2],"Third tuple var is not 'c'")
		self.failUnless('a'==rel.tuple_in[0],"First in tuple var is not 'a'")
		self.failUnless('b'==rel.tuple_in[1],"Second in tuple var is not 'b'")
		self.failUnless('c'==rel.tuple_out[0],"First out tuple var is not 'c'")

	#Tests that we can get the symbolics
	def testSymbolics(self):
		from iegen import Relation,Symbolic

		rel=Relation('{[a,b]->[c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless(Symbolic('m')==rel.symbolics[0],"First symbolic is not 'm'")
		self.failUnless(Symbolic('n')==rel.symbolics[1],"Second symbolic is not 'n'")

	#Tests that we can get the symbolic names
	def testSymbolicNames(self):
		from iegen import Relation,Symbolic

		rel=Relation('{[a,b]->[c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless('m'==rel.symbolic_names[0],"First symbolic is not 'm'")
		self.failUnless('n'==rel.symbolic_names[1],"Second symbolic is not 'n'")

	#Tests that we can get the symbolic names
	def testArity(self):
		from iegen import Relation,Symbolic

		rel=Relation('{[a,b]->[c]: a=n and b=m}',[Symbolic('n'),Symbolic('m')])

		self.failUnless((2,1)==rel.arity(),"Relation's arity is not (2,1)")
		self.failUnless(2==rel.arity_in(),"Relation's input arity is not 2")
		self.failUnless(1==rel.arity_out(),"Relation's output arity is not 1")

	#Test the __str__ method
	def testStr(self):
		from iegen import Relation,Symbolic

		rel_string='{[a]->[b]}'
		rel=Relation(rel_string)
		res_string='{[a]->[b]}'

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

		rel_string='{[a]->[b]: b=2n and a=10 and a>=m}'
		rel=Relation(rel_string,[Symbolic('n'),Symbolic('m')])
		res_string='{[a]->[b]: b=2n and a=10 and a>=m | m,n}'

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

		rel_string='{[a]->[b]: b=2n and a=10 and a+b>=c and a>=m}'
		rel=Relation(rel_string,[Symbolic('n'),Symbolic('m')])
		res_string='{[a]->[b]: b=2n and a=10 and a+b>=c and a>=m | m,n}'

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

	def testStrEmptyInequality1(self):
		from iegen import Relation

		rel_string='{[a]->[b]: 0>=a+b}'

		rel=Relation(rel_string)

		res_string=rel_string

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

	def testStrEmptyInequality2(self):
		from iegen import Relation

		rel_string='{[a]->[b]: a+b>=0}'

		rel=Relation(rel_string)

		res_string=rel_string

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

	#Test the __repr__ method
	def testRepr(self):
		from iegen import Relation,Symbolic

		rel_string='{[a]->[b]: b=2n and a=10 and a>=m}'
		symbolics=[Symbolic('m'),Symbolic('n')]
		rel=Relation(rel_string,symbolics)
		res_string='{[a]->[b]: b=2n and a=10 and a>=m | m,n}'
		res_string='Relation("%s",%s)'%(res_string,repr(symbolics))

		self.failUnless(res_string==repr(rel),'%s!=%s'%(repr(rel),res_string))

		rel_string='{[a]->[b]: b=2n and a=10 and a+b>=c and a>=m}'
		rel=Relation(rel_string,symbolics)
		res_string='{[a]->[b]: b=2n and a=10 and a+b>=c and a>=m | m,n}'
		res_string='Relation("%s",%s)'%(res_string,repr(symbolics))

		self.failUnless(res_string==repr(rel),'%s!=%s'%(repr(rel),res_string))

	def testDuplicateConstraint(self):
		from iegen import Relation

		rel_string='{[a]->[b]: a=10 and a=10}'
		rel=Relation(rel_string)
		res_string=str(Relation('{[a]->[b]: a=10}'))

		self.failUnless(res_string==str(rel),'%s!=%s'%(str(rel),res_string))

	def testRelationEquality(self):
		from iegen import Relation

		rel1_string='{[a]->[b]: a=10 and b>=0 and a>=0}'
		rel2_string='{[c]->[d]: c=10 and d>=0 and c>=0}'
		rel3_string='{[a]->[d]: a=10 and d>=0 and a>=0}'

		rel1=Relation(rel1_string)
		rel2=Relation(rel2_string)
		rel3=Relation(rel3_string)

		self.failUnless(rel1==rel2,'%s!=%s'%(rel1,rel2))
		self.failUnless(rel1==rel3,'%s!=%s'%(rel1,rel3))
		self.failUnless(rel2==rel3,'%s!=%s'%(rel2,rel3))

	def testCopy(self):
		from iegen import Relation,Symbolic

		rel=Relation('{[a]->[b]: a=b and b=n}',symbolics=[Symbolic('n')])
		rel_copy=rel.copy()

		self.failIf(rel_copy is rel,'Copy returns same Relation instance')
		self.failUnless(rel_copy==rel,'%s!=%s'%(rel_copy,rel))

		rel=Relation('{[a]->[b]: a=f(b) and b=n}',symbolics=[Symbolic('n')])
		rel_copy=rel.copy()

		self.failIf(rel_copy is rel,'Copy returns same Relation instance')
		self.failUnless(rel_copy==rel,'%s!=%s'%(rel_copy,rel))

	def testSimpleFunction(self):
		from iegen import Relation

		rel_string='{[a]->[b]: b=f(a)}'

		rel=Relation(rel_string)
		res_string=str(rel)

		self.failUnless(res_string==rel_string,'%s!=%s'%(res_string,rel_string))

	def testNestedFunction(self):
		from iegen import Relation

		rel_string='{[a]->[b]: b=f(g(a))}'

		rel=Relation(rel_string)
		res_string=str(rel)

		self.failUnless(res_string==rel_string,'%s!=%s'%(res_string,rel_string))

	def testTwoArgumentFunction(self):
		from iegen import Relation

		rel_string='{[a,b]->[c]: c=f(a,b)}'

		rel=Relation(rel_string)
		res_string=str(rel)

		self.failUnless(res_string==rel_string,'%s!=%s'%(res_string,rel_string))

	def testConstantArgumentFunction(self):
		from iegen import Relation

		rel_string='{[a]->[b]: b=f(a,6)}'

		rel=Relation(rel_string)
		res_string=str(rel)

		self.failUnless(res_string==rel_string,'%s!=%s'%(res_string,rel_string))

	#Tests that a frozen relation cannot be cleared
	@raises(ValueError)
	def testClearFrozen(self):
		from iegen import Relation

		rel=Relation('{[a]->[b]: a=10}')

		rel.clear()

	def testClear(self):
		from iegen import Relation

		rel=Relation('{[a]->[b,c]: a=b and c>10}',freeze=False)

		self.failUnless(1==len(rel.disjunction),'Relation does not have exactly one conjunction')
		self.failUnless(2==len(list(rel.disjunction.conjunctions)[0]),'Relation conjunction does not have exactly two constraints')

		rel.clear()

		self.failUnless(0==len(rel.disjunction),'Relation does not have exactly zero conjunctions')

	@raises(ValueError)
	def testModifyFrozen1(self):
		from iegen import Relation,SparseConjunction

		rel=Relation('{[a]->[b,c]}')
		rel.add_conjunction(SparseConjunction())

	@raises(ValueError)
	def testModifyFrozen2(self):
		from iegen import Relation,SparseDisjunction

		rel=Relation('{[a]->[b,c]}')
		rel.add_disjunction(SparseDisjunction())

	def testManualConstruction(self):
		from iegen import Relation

		rel=Relation('{[a]->[b,c]}',freeze=False)

		#Add conjunction a=b and b>=c
		rel.clear()
		rel.add_conjunction(rel.get_conjunction([rel.get_equality({rel.get_column('a'):1,rel.get_column('b'):-1}),rel.get_inequality({rel.get_column('b'):1,rel.get_column('c'):-1})]))
		rel.freeze()

		rel_res=Relation('{[a]->[b,c]: a=b and b>=c}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	#Tests that Relation implements __len__
	def testLen1(self):
		from iegen import Relation

		self.failUnless(1==len(Relation('{[a]->[b]: a=10}')))
	def testLen2(self):
		from iegen import Relation

		self.failUnless(2==len(Relation('{[a]->[b]: a=10}').union(Relation('{[a]->[b]: a=5}'))))

	#----------------------------------------
	# Start simplification tests

	def testSimplifyEqualityFree(self):
		from iegen import Relation

		rel=Relation('{[a]->[b]: a=c and c=b}')

		rel_res=Relation('{[a]->[b]: a=b}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyEqualityFunction(self):
		from iegen import Relation

		rel=Relation('{[a]->[b]: b=c and c=f(a)}')

		rel_res=Relation('{[a]->[b]: b=f(a)}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyInequality(self):
		from iegen import Relation

		rel=Relation('{[a]->[b]: a>=b and a<=b}')

		rel_res=Relation('{[a]->[b]: a=b}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyInequalitySub(self):
		from iegen import Relation

		rel=Relation('{[a]->[b]: a>=c and c>=b}')

		rel_res=Relation('{[a]->[b]: a>=b}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyMixed1(self):
		from iegen import Relation

		rel=Relation('{[a,b]->[c,d]: 2e+3a=5b and 7c>=11d+13e}')

		rel_res=Relation('{[a,b]->[c,d]: 14c>=22d+65b-39a}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyMixed2(self):
		from iegen import Relation

		rel=Relation('{[a,b]->[c,d]: -2e+3a=5b and 7c>=11d+13e}')

		rel_res=Relation('{[a,b]->[c,d]: -14c<=-22d+65b-39a}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyRemoveTrue(self):
		from iegen import Relation

		rel=Relation('{[a]->[b]: 10>=0}')

		rel_res=Relation('{[a]->[b]}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyReplaceInFunction1(self):
		from iegen import Relation

		rel=Relation('{[a]->[b]: b=f(c) and c=g(a)}')

		rel_res=Relation('{[a]->[b]: b=f(g(a))}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyReplaceInFunction2(self):
		from iegen import Relation

		rel=Relation('{[a]->[b]: b=3f(7c) and c=2g(5a)}')

		rel_res=Relation('{[a]->[b]: b=3f(14g(5a))}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyInverseFunction1(self):
		from iegen import Relation
		import iegen.simplify

		iegen.simplify.register_inverse_pair('g')
		rel=Relation('{[a]->[b]: a=g(c) and b=f(c)}')
		iegen.simplify.unregister_inverse_pair('g')

		rel_res=Relation('{[a]->[b]: b=f(g_inv(a))}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyInverseFunction2(self):
		from iegen import Relation
		import iegen.simplify

		iegen.simplify.register_inverse_pair('g')
		rel=Relation('{[a,b]->[c,d]: a+b=g(e)+c and b=f(e)}')
		iegen.simplify.unregister_inverse_pair('g')

		rel_res=Relation('{[a,b]->[c,d]: b=f(g_inv(a+b-c))}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	def testSimplifyInverseFunction3(self):
		from iegen import Relation
		import iegen.simplify

		iegen.simplify.register_inverse_pair('g')
		rel=Relation('{[a,b]->[c,d]: 2a+3b=g(e)+7c and 11b=13f(17e)}')
		iegen.simplify.unregister_inverse_pair('g')

		rel_res=Relation('{[a,b]->[c,d]: 11b=13f(17g_inv(2a+3b-7c))}')

		self.failUnless(rel==rel_res,'%s!=%s'%(rel,rel_res))

	# End simplification tests
	#----------------------------------------


	#----------------------------------------
	# Start operation tests

	#Tests that hash doesn't work on an unfrozen relation
	@raises(ValueError)
	def testHashUnfrozen(self):
		from iegen import Relation

		hash(Relation('{[a]->[b]}',freeze=False))

	#Tests that equality doesn't work on an unfrozen relation
	@raises(ValueError)
	def testEqualityUnfrozen1(self):
		from iegen import Relation

		Relation('{[a]->[b]}',freeze=False)==Relation('{[a]->[b]}')

	@raises(ValueError)
	def testEqualityUnfrozen2(self):
		from iegen import Relation

		Relation('{[a]->[b]}')==Relation('{[a]->[b]}',freeze=False)

	#Tests that union does not allow relations of differing arity
	@raises(ValueError)
	def testUnionDiffArity(self):
		from iegen import Relation

		relation1=Relation('{[]->[]}')
		relation2=Relation('{[a]->[a]}')
		relation1.union(relation2)

	#Tests that union is not destructive
	def testUnionNonDestructive(self):
		from iegen import Relation

		relation1=Relation('{[a]->[a]}')
		relation2=Relation('{[b]->[b]}')
		unioned=relation1.union(relation2)

		self.failIf(unioned is relation1,'%s is %s'%(unioned,relation1))
		self.failIf(unioned is relation2,'%s is %s'%(unioned,relation2))

	#Tests that the union operation doesn't work on an unfrozen relation
	@raises(ValueError)
	def testUnionUnfrozen1(self):
		from iegen import Relation

		rel1=Relation('{[a]->[b]}',freeze=False)
		rel2=Relation('{[c]->[d]}')

		rel1.union(rel2)

	@raises(ValueError)
	def testUnionUnfrozen2(self):
		from iegen import Relation

		rel1=Relation('{[a]->[b]}')
		rel2=Relation('{[c]->[d]}',freeze=False)

		rel1.union(rel2)

	#Tests the union operation
	def testUnionEmpty(self):
		from iegen import Relation

		rel1=Relation('{[a]->[b]}')
		rel2=Relation('{[c]->[d]}')

		rel3=rel1.union(rel2)

		self.failUnless(1==len(rel3.disjunction),'Unioned relation should have exactly one conjunction')
		self.failUnless(rel3==rel1,'%s!=%s'%(rel3,rel1))
		self.failUnless(rel2==rel1,'%s!=%s'%(rel2,rel1))

	def testUnionConstraints(self):
		from iegen import Relation

		rel1=Relation('{[a]->[b]: a=b}')
		rel2=Relation('{[c]->[d]: c=10 and d=10}')

		rel_union=rel1.union(rel2)

		res_union=Relation('{[a]->[b]}',freeze=False)
		res_union.clear()
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_column('b'):-1})]))
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_constant_column():-10}),res_union.get_equality({res_union.get_column('b'):1,res_union.get_constant_column():-10})]))
		res_union.freeze()

		self.failUnless(2==len(rel_union.disjunction),'Unioned relation should have exactly two conjunctions')
		self.failUnless(rel_union==res_union,'%s!=%s'%(rel_union,res_union))

		rel1=Relation('{[a]->[b]: a=b}')
		rel2=Relation('{[c]->[d]: c=d}')

		rel_union=rel1.union(rel2)

		res_union=Relation('{[a]->[b]}',freeze=False)
		res_union.clear()
		res_union.add_conjunction(res_union.get_conjunction([res_union.get_equality({res_union.get_column('a'):1,res_union.get_column('b'):-1})]))
		res_union.freeze()

		self.failUnless(1==len(rel_union.disjunction),'Unioned relation should have exactly one conjunction')
		self.failUnless(rel_union==res_union,'%s!=%s'%(rel_union,res_union))

	def testUnionStr(self):
		from iegen import Relation

		rel1=Relation('{[a]->[b]: a=b}')
		rel2=Relation('{[c]->[d]: c=10}')

		rel_union=rel1.union(rel2)

		res_str='{[a]->[b]: a=10} union {[a]->[b]: a=b}'

		self.failUnless(res_str==str(rel_union),'%s!=%s'%(str(rel_union),res_str))

	#Tests that the inverse operation doesn't work on an unfrozen relation
	@raises(ValueError)
	def testInverseUnfrozen(self):
		from iegen import Relation

		Relation('{[a]->[b]: a=b}',freeze=False).inverse()

	#Tests the inverse operation
	def testInverseEmpty(self):
		from iegen import Relation

		inverse=Relation('{[a,b]->[c,d]}').inverse()
		res_inverse=Relation('{[c,d]->[a,b]}')

		self.failUnless(inverse==res_inverse,'%s!=%s'%(inverse,res_inverse))
		self.failUnless(str(inverse)==str(res_inverse),'%s!=%s'%(str(inverse),str(res_inverse)))

	#Tests the inverse operation with constraints
	def testInverseConstraints(self):
		from iegen import Relation

		inverse=Relation('{[a,b]->[c,d]:a>=n && b<5 and c+d=15}').inverse()
		res_inverse=Relation('{[c,d]->[a,b]:b<5 and a>=n && c+d=15}')

		self.failUnless(inverse==res_inverse,'%s!=%s'%(inverse,res_inverse))
		self.failUnless(str(inverse)==str(res_inverse),'%s!=%s'%(str(inverse),str(res_inverse)))

	def testInverseArity(self):
		from iegen import Relation

		rel=Relation('{[a,b]->[c,d,e,f,g]}')
		inverse=rel.inverse()

		self.failUnless((2,5)==rel.arity(),'Arity of %s is not (2,5)'%(rel))
		self.failUnless((5,2)==inverse.arity(),'Arity of %s is not (5,2)'%(inverse))

	#Tests that the compose operation doesn't work on unfrozen relations
	@raises(ValueError)
	def testComposeUnfrozen1(self):
		from iegen import Relation

		rel1=Relation('{[a]->[b]: a=b}',freeze=False)
		rel2=Relation('{[a]->[b]: b=10}')
		rel1.compose(rel2)

	@raises(ValueError)
	def testComposeUnfrozen2(self):
		from iegen import Relation

		rel1=Relation('{[a]->[b]: a=b}')
		rel2=Relation('{[a]->[b]: b=10}',freeze=False)
		rel1.compose(rel2)

	#Tests that compose is not destructive
	def testComposeNonDestructive(self):
		from iegen import Relation

		rel1=Relation('{[a]->[a]}')
		rel2=Relation('{[b]->[b]}')
		composed=rel1.compose(rel2)

		self.failIf(composed is rel1,'%s is %s'%(composed,rel1))
		self.failIf(composed is rel2,'%s is %s'%(composed,rel2))

	#Tests that compose fails when the output arity of the second relation does not match the input arity of the first relation
	@raises(ValueError)
	def testComposeArityFail1(self):
		from iegen import Relation

		rel1=Relation('{[a,b]->[c]}')
		rel2=Relation('{[b]->[b]}')
		composed=rel1.compose(rel2)

	@raises(ValueError)
	def testComposeArityFail2(self):
		from iegen import Relation

		rel1=Relation('{[]->[c]}')
		rel2=Relation('{[a,b,c,d]->[e]}')
		composed=rel1.compose(rel2)

	#Tests the compose operation
	def testCompose(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c]:1<=a and a<=10 and 1<=b and b<=10}')
		relation2=Relation('{[d]->[e,f]:-10<=d and d<=0}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[d]->[c]: -10<=d and d<=0}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests that variable name collisions are handled
	def testComposeRename(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c,d]}')
		relation2=Relation('{[b,c]->[d,e]}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[b,c]->[c0,d]: d0=a and e=b0}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	#Tests the compose operation with equality constraints
	def testComposeEquality1(self):
		from iegen import Relation

		relation1=Relation('{[a,b]->[c]:c=a}')
		relation2=Relation('{[d]->[e,f]:e=d and f=d}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[d]->[c]: d=c}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	def testComposeEquality2(self):
		from iegen import Relation

		relation1=Relation('{[a]->[b,c]: a=10}')
		relation2=Relation('{[d,e]->[f]: f=10}')

		composed=relation2.compose(relation1)

		composed_res=Relation('{[a]->[f]: a=10 and f=10}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	def testComposeEquality3(self):
		from iegen import Relation

		relation1=Relation('{[a]->[b,c]: a=10}')
		relation2=Relation('{[d,e]->[f]: f=10}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[d,e]->[b,c]}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	def testComposeEquality4(self):
		from iegen import Relation

		relation1=Relation('{[a]->[b,c]: a=10}')
		relation2=Relation('{[c,d]->[e]: e=10}')

		composed=relation2.compose(relation1)

		composed_res=Relation('{[a]->[e]: a=10 and e=10}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	def testComposeEquality5(self):
		from iegen import Relation

		relation1=Relation('{[a]->[b,c]: a=10}')
		relation2=Relation('{[c,d]->[e]: e=10}')

		composed=relation1.compose(relation2)

		composed_res=Relation('{[c,d]->[b,c0]}')

		self.failUnless(composed==composed_res,'%s!=%s'%(composed,composed_res))

	# End operation tests
	#----------------------------------------
#------------------------------------------
