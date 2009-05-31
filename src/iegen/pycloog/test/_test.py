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

	def testPYCLooGNoScattering(self):
		from iegen.pycloog import Statement,codegen
		from iegen import Set,Symbolic

		code='''if (n >= 1) {
  for (i=1;i<=n;i++) {
    for (j=1;j<=n;j++) {
      S0(i,j);
      S1(i,j);
    }
  }
}'''

		old_code='''if (n >= 1) {
  for (i=1;i<=n;i++) {
    for (j=1;j<=n;j++) {
      S0 ;
      S1 ;
    }
  }
}'''

		old_old_code='''for (i=1;i<=n;i++) {
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

	def testPYCLooGSimple(self):
		from iegen.pycloog import Statement,codegen
		from iegen import Set,Relation,Symbolic

		code='''for (i=0;i<=n;i++) {
  for (j=0;j<=m;j++) {
    S1(i,j);
  }
}
for (i=0;i<=n;i++) {
  for (j=0;j<=m;j++) {
    S0(i,j);
  }
}'''

		old_code='''if ((m >= 1) && (n >= 1)) {
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

		old_old_code='''if (m >= 1) {
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

		dom1=Set('{[i,j]:0<=i and i<=n and 0<=j and j<=m}',[Symbolic('n'),Symbolic('m')])
		scat1=Relation('{[i,j]->[p0,i,p1,j,p2]: p0=1 and p1=0 and p2=0}')

		dom2=Set('{[i,j]:0<=i and i<=n and 0<=j and j<=m}',[Symbolic('n'),Symbolic('m')])
		scat2=Relation('{[i,j]->[p0,i,p1,j,p2]: p0=0 and p1=0 and p2=0}')

		stmt1=Statement(dom1,scat1)
		stmt2=Statement(dom2,scat2)
		stmts=(stmt1,stmt2)

		res=codegen(stmts)
		self.failUnless(code==res,'PYCLooG generated:\n\n%s\n\nbut test expected:\n\n%s'%(res,code))

	def testPYCLooGScatter(self):
		from iegen.pycloog import Statement,codegen
		from iegen import Set,Relation,Symbolic

		code='''for (s=0;s<=T;s++) {
  for (i=0;i<=N;i++) {
    S0(s,i);
  }
  for (i=0;i<=n_inter;i++) {
    S1(s,i);
    S2(s,i);
  }
}'''

		dom0=Set('{[s,i]: 0<=s && s<=T && 0<=i && i<=N}',[Symbolic('T'),Symbolic('N')])
		scat0=Relation('{[s,i]->[c0,s,c1,i,c2]: c0=0 && c1=0 && c2=0}')

		dom1=Set('{[s,i]: 0<=s && s<=T && 0<=i && i<=n_inter}',[Symbolic('T'),Symbolic('n_inter')])
		scat1=Relation('{[s,i]->[c0,s,c1,i,c2]: c0=0 && c1=1 && c2=0}')

		dom2=Set('{[s,i]: 0<=s && s<=T && 0<=i && i<=n_inter}',[Symbolic('T'),Symbolic('n_inter')])
		scat2=Relation('{[s,i]->[c0,s,c1,i,c2]: c0=0 && c1=1 && c2=1}')

		stmt0=Statement(dom0,scat0)
		stmt1=Statement(dom1,scat1)
		stmt2=Statement(dom2,scat2)
		stmts=(stmt0,stmt1,stmt2)

		res=codegen(stmts)
		self.failUnless(code==res,'PYCLooG generated:\n\n%s\n\nbut test expected:\n\n%s'%(res,code))
#----------------------------------
