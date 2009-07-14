# compose_bug_136.py
#

import iegen
from iegen import Set
from iegen import Relation
from iegen import Symbolic

import iegen.simplify
iegen.simplify.register_inverse_pair('delta','delta_inv')

from iegen.ast.visitor import PrettyPrintVisitor

D_ST = Relation("{ [c0,i] -> [x,j] : i+-1*sigma(inter1(delta_inv(j)))=0 && c0=0 }")
D_ST = D_ST.union(Relation("{ [c0,i] -> [x,j] : i+-1*sigma(inter2(delta_inv(j)))=0 && c0 = 0  }"))

D_ST.compose( D_ST )

