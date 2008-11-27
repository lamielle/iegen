from unittest import TestCase

#---------- Import Tests ----------
#Test importing of iegen.pycloog
class ImportTestCase(TestCase):

	#Test simple importing of iegen.pycloog
	def testImport(self):
		try:
			import iegen.pycloog
		except Exception,e:
			self.fail("'import iegen.pycloog' failed: "+str(e))

	#Test simple importing of iegen.pycloog classes
	def testNameImport(self):
		try:
			from iegen.pycloog import Statement,codegen
		except Exception,e:
			self.fail("Importing classes from iegen.pycloog failed: "+str(e))
#----------------------------------

#---------- PYCLooG Tests ----------
class PYCLooGTestCase(TestCase):

	def testPYCLooGSimple(self):
		from iegen.pycloog import Statement,codegen
		from iegen import Set,Symbolic

		code='''if ((m >= 1) && (n >= 1)) {
  for (i=1;i<=n;i++) {
    for (j=1;j<=m;j++) {
      S1 ;
    }
  }
  for (i=1;i<=n;i++) {
    for (j=1;j<=m;j++) {
      S0 ;
    }
  }
}'''

		old_code='''if (m >= 1) {
  for (i=1;i<=n;i++) {
    for (j=1;j<=m;j++) {
      S2 ;
    }
  }
}
if (m >= 1) {
  for (i=1;i<=n;i++) {
    for (j=1;j<=m;j++) {
      S1 ;
    }
  }
}'''

		dom1=Set('{[i,j]:1<=i and i<=n and 1<=j and j<=m and m>=1}',[Symbolic('n'),Symbolic('m')])
		scat1=Set('{[p1,p2,i,j,n,m]: p1=1 and p2=1}')

		dom2=Set('{[i,j]:1<=i and i<=n and 1<=j and j<=m and m>=1}',[Symbolic('n'),Symbolic('m')])
		scat2=Set('{[p1,p2,i,j,n,m]: p1=0 and p2=0}')

		stmt1=Statement(dom1,scat1)
		stmt2=Statement(dom2,scat2)
		stmts=(stmt1,stmt2)

		res=codegen(stmts)
		self.failUnless(code==res,'PYCLooG generated:\n\n%s\n\nbut test expected:\n\n%s'%(res,code))

	def testPYCLooGNoScattering(self):
		from iegen.pycloog import Statement,codegen
		from iegen import Set,Symbolic

		code='''if (n >= 1) {
  for (i=1;i<=n;i++) {
    for (j=1;j<=n;j++) {
      S0 ;
      S1 ;
    }
  }
}'''

		old_code='''for (i=1;i<=n;i++) {
  for (j=1;j<=n;j++) {
    S1 ;
    S2 ;
  }
}'''

		dom1=Set('{[i,j]:1<=i and i<=n and 1<=j and j<=n}',[Symbolic('n')])
		dom2=Set('{[i,j]:1<=i and i<=n and 1<=j and j<=n}',[Symbolic('n')])

		stmt1=Statement(dom1)
		stmt2=Statement(dom2)
		stmts=(stmt1,stmt2)

		res=codegen(stmts)
		self.failUnless(code==res,'PYCLooG generated:\n\n%s\n\nbut test expected:\n\n%s'%(res,code))
#----------------------------------
