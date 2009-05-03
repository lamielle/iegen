# Script written to play around with existing visitors and make
# a visitor that just output everything as it is visited and a
# visitor that pretty prints relations.

#!/usr/bin/env python

import iegen
from iegen import Set,Relation,Symbolic

import iegen.simplify

# Enabling debug output
#from iegen import IEGenObject
# None corresponds to stdout
#IEGenObject.settings.outputs['debug'].append(None)

# Some example visitors
from iegen.ast.visitor import FindConstraintVisitor, PrintASTVisitor
from iegen.ast import Equality


everything = Relation('{[c0,i,j] -> [c0,i,k] : c0=0 && i>=1 && i<=10 && k=f(j) }')
everythingCompose = everything.compose(everything)

# Calling a visitor that just prints "I'm here" messages at every AST node
#PrintASTVisitor().visit(everythingCompose)

from iegen.ast.visitor import PrettyPrintVisitor
print '====================='
PrettyPrintVisitor().visit(everythingCompose)
print everythingCompose

T_I1_to_I2 = Relation("{[c0,s1,c1,i,c2] -> [c3,s2,c4,j,c5] : s1=s2 && c0=0 && c1=0 && c2=0 && c3=0 && c4=0 && c5=0 && i=j}").union( Relation("{[c6,s3,c7,ii,x] -> [c8,s4,c9,j,y] : s3=s4 && j = delta(ii) && c6=0 && c8=0 && c7=1 && c9=1 && x=y }"))
print '====================='
PrettyPrintVisitor().visit(T_I1_to_I2)
print T_I1_to_I2
