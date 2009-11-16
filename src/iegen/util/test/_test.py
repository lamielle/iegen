from unittest import TestCase
from iegen.lib.nose.tools import raises

#---------- Import Tests ----------
#Test importing of iegen.util
class ImportTestCase(TestCase):

	#Test simple importing of iegen.util
	def testImport(self):
		try:
			import iegen.util
		except Exception,e:
			self.fail("'import iegen.util' failed: "+str(e))

	#Test simple importing of iegen.util classes
	def testNameImport(self):
		try:
			#_util.py
			from iegen.util import run_tests,iter_islast,sign,invert_dict,equality_sets,define_properties,get_basic_term,find_term,like_type,is_iterable,raise_objs_not_like_types,DimensionalityError,biject,normalize_self,normalize_result,check,one_time_normalize
			#_test_util.py
			from iegen.util import tuple_gen,lower_gen,upper_gen,parse_test,ast_equality_test,var_exp_strings,func_exp_strings,norm_exp_strings,test_sets,test_set_strings,test_relations,test_relation_strings
		except Exception,e:
			self.fail("Importing classes from iegen.util failed: "+str(e))
#----------------------------------

#---------- iter_islast Tests ----------
class iter_islastTestCase(TestCase):

	#Tests that iter_islast works for a sequence of 10 numbers
	def testSeqNums(self):
		from iegen.util import iter_islast
		count=0
		for i,is_last in iter_islast(range(10)):
			self.failUnless(count==i,'%d!=%d'%(i,count))
			if i<9:
				self.failIf(is_last,'is_last is True but we are not at the last item')
			else:
				self.failUnless(is_last,'is_last is False but we are at the last item')
			count+=1

	#Tests that iter_islast works for a single item sequence
	def testSeq1Num(self):
		from iegen.util import iter_islast
		for i,is_last in iter_islast(range(1)):
			self.failUnless(0==i,'0!=%d'%(i))
			self.failUnless(is_last,'is_last is False but we are at the last item')

	#Tests that iter_islast works for a two item sequence
	def testSeq2Num(self):
		from iegen.util import iter_islast
		count=0
		for i,is_last in iter_islast(range(2)):
			self.failUnless(count==i,'%d!=%d'%(i,count))
			if i<1:
				self.failIf(is_last,'is_last is True but we are not at the last item')
			else:
				self.failUnless(is_last,'is_last is False but we are at the last item')
			count+=1

	#Tests that iter_islast works for an empty sequence
	def testSeq0Num(self):
		from iegen.util import iter_islast
		for i,is_last in iter_islast(range(0)):
			self.fail('This loop should have no iterations')

	#Tests that iter_islast works for a single item sequence
	def testStringSeq(self):
		from iegen.util import iter_islast
		text='Upper Class Twit of The Year 2'
		pos=0
		for ch,is_last in iter_islast(text):
			self.failUnless(text[pos]==ch,'%s!=%s'%(text[pos],ch))
			if pos<len(text)-1:
				self.failIf(is_last,'is_last is True but we are not at the last item')
			else:
				self.failUnless(is_last,'is_last is False but we are at the last item')
			pos+=1
#---------------------------------------

#---------- Sign Tests ----------
class SignTestCase(TestCase):

	#Tests that sign(1)==1
	def testSign1(self):
		from iegen.util import sign
		self.failUnless(1==sign(1),'sign(1)!=1')

	#Tests that sign(-1)==-1
	def testSignNeg1(self):
		from iegen.util import sign
		self.failUnless(-1==sign(-1),'sign(-1)!=-1')

	#Tests that sign(0)==1
	def testSign0(self):
		from iegen.util import sign
		self.failUnless(1==sign(1),'sign(0)!=1')

	#Tests that sign(6)==1
	def testSign6(self):
		from iegen.util import sign
		self.failUnless(1==sign(6),'sign(6)!=1')

	#Tests that sign(-6)==-1
	def testSignNeg6(self):
		from iegen.util import sign
		self.failUnless(-1==sign(-6),'sign(-6)!=-1')
#--------------------------------

#---------- Invert Dict Tests ----------
class InvertDictTestCase(TestCase):

	#Tests simple one element dictionary inversions
	def testInvertOneItem(self):
		from iegen.util import invert_dict
		self.failUnless({1:3}==invert_dict({3:1}),'invert_dict({3:1})!={1:3}: %s'%(invert_dict({3:1})))
		self.failUnless({'a':3}==invert_dict({3:'a'}),"invert_dict({3:'a'})!={'a':3}: %s"%(invert_dict({3:'a'})))
		self.failUnless({'b':'a'}==invert_dict({'a':'b'}),"invert_dict({'a':'b'})!={'b':'a'}: %s"%(invert_dict({'a':'b'})))

	#Tests multiple element dictionary inversions
	def testInvertMultipleItems(self):
		from iegen.util import invert_dict
		dict=invert_dict({'a':3,6:'d','c':10.3})
		dict_res={3:'a','d':6,10.3:'c'}
		self.failUnless(dict_res==dict,'%s!=%s'%(dict_res,dict))
#---------------------------------------

#---------- Equality Sets Tests ----------
class EqualitySestsTestCase(TestCase):

	#Tests a simple case where there are no equality sets
	def testNoSets(self):
		from iegen.util import equality_sets
		eq_sets=equality_sets({'a':[1],'b':[2],'c':[3],'d':[4]})
		res={}
		self.failUnless(res==eq_sets,'%s!=%s'%(res,eq_sets))

	#Tests a simple case with one equality set
	def testSingleSet(self):
		from iegen.util import equality_sets
		eq_sets=equality_sets({'a':[1],'b':[1]})
		res={1:set(['a','b'])}
		self.failUnless(res==eq_sets,'%s!=%s'%(res,eq_sets))

	#Tests a simple case with two equality sets
	def testTwoSets(self):
		from iegen.util import equality_sets
		eq_sets=equality_sets({'a':[1],'b':[2],'c':[1],'d':[2]})
		res={1:set(['a','c']),2:set(['b','d'])}
		self.failUnless(res==eq_sets,'%s!=%s'%(res,eq_sets))

	#Tests a more complicated case
	def testMoreComplex(self):
		from iegen.util import equality_sets
		eq_sets=equality_sets({'a':[1,2],'b':[1],'c':[2],'d':[3],'e':[3,4],'f':[2],'g':[6]})
		res={1:set(['a','b']),2:set(['a','c','f']),3:set(['d','e'])}
		self.failUnless(res==eq_sets,'%s!=%s'%(res,eq_sets))

	#Test with multiple duplicate equality values
	def testDuplicateValues(self):
		from iegen.util import equality_sets
		eq_sets=equality_sets({'a':[1,2,2,1],'b':[1,1],'c':[2],'d':[3],'e':[3,4,3,4],'f':[2]})
		res={1:set(['a','b']),2:set(['a','c','f']),3:set(['d','e'])}
		self.failUnless(res==eq_sets,'%s!=%s'%(res,eq_sets))
#-----------------------------------------

#---------- biject Tests ----------
class EqualitySestsTestCase(TestCase):

	def testEmptyConstruction(self):
		from iegen.util import biject
		biject()

	def testSetItem(self):
		from iegen.util import biject
		b=biject()
		b['a']=1

	def testGetItem(self):
		from iegen.util import biject
		b=biject()
		b['a']=1

		self.failUnless(1==b['a'],"b['a']!=%s"%(b['a']))
		self.failUnless('a'==b[1],"b[1]!=%s"%(b[1]))

	def testOverrideItem(self):
		from iegen.util import biject
		b=biject()
		b['a']=1
		b['a']=2

		self.failUnless(2==b['a'],"b['a']!=%s"%(b['a']))
		self.failUnless('a'==b[2],"b[2]!=%s"%(b[2]))

		b[2]='b'

		self.failUnless(2==b['b'],"b['b']!=%s"%(b['b']))
		self.failUnless('b'==b[2],"b[2]!=%s"%(b[2]))

	def testOverrideBackwards(self):
		from iegen.util import biject
		b=biject()
		b['a']=1
		b[2]='a'

		self.failUnless(2==b['a'],"b['a']!=%s"%(b['a']))
		self.failUnless('a'==b[2],"b[2]!=%s"%(b[2]))

	def testLength1(self):
		from iegen.util import biject
		b=biject()
		self.failUnless(0==len(b),'Length of biject is not 0')

		b['a']=1
		self.failUnless(1==len(b),'Length of biject is not 1')

		b['b']=2
		self.failUnless(2==len(b),'Length of biject is not 2')

		b['c']=3
		self.failUnless(3==len(b),'Length of biject is not 3')

	@raises(KeyError)
	def testFailCollision(self):
		from iegen.util import biject
		b=biject()
		b['a']=1
		b[2]='b'
		b['a']=2

	@raises(KeyError)
	def testFailNotContains(self):
		from iegen.util import biject
		b=biject()
		b['a']

	def testLength2(self):
		from iegen.util import biject

		b0=biject()

		b1=biject()
		b1['asdf']=20

		b2=biject()
		b2['a']=47
		b2['b']=10

		self.failUnless(0==len(b0),'len(%s)!=0'%(b0))
		self.failUnless(1==len(b1),'len(%s)!=1'%(b1))
		self.failUnless(2==len(b2),'len(%s)!=2'%(b2))

	def testClear(self):
		from iegen.util import biject

		b0=biject()
		b0.clear()

		b1=biject()
		b1['asdf']=20
		b1.clear()

		b2=biject()
		b2['a']=47
		b2['b']=10
		b2.clear()

		self.failUnless(0==len(b0),'len(%s)!=0'%(b0))
		self.failUnless(0==len(b1),'len(%s)!=0'%(b1))
		self.failUnless(0==len(b2),'len(%s)!=0'%(b2))
#-------------------------------------
