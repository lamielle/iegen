from unittest import TestCase

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
			from iegen import MapIR,IterationSpace,DataSpace,IndexArray,AccessRelation,Statement,DataDependence,RTRT,DataPermuteRTRT,IterPermuteRTRT,Set,Relation
		except Exception,e:
			self.fail("Importing classes from iegen failed: "+str(e))
#----------------------------------

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
