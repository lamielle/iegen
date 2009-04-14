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
			from iegen.util import run_tests,iter_islast,sign,invert_dict,define_properties,get_basic_term,find_term,like_type,is_iterable,raise_objs_not_like_types,DimensionalityError,normalize_self,normalize_result,check,one_time_normalize
			#_test_util.py
			from iegen.util import tuple_gen,lower_gen,upper_gen,parse_test,ast_equality_test,test_sets,test_set_strings,test_relations,test_relation_strings
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
