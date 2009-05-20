# compose_bug.py
#
# Turned out this was another un-renaming bug.  Issue #124 is now fixed.

import iegen
from iegen import Set
from iegen import Relation
from iegen import Symbolic

import iegen.simplify
iegen.simplify.register_inverse_pair('delta','delta_inv')

from iegen.ast.visitor import PrettyPrintVisitor



D_1_2 = Relation("{[c0,s,c1,i,c2] -> [c0,s,c3,ii,c2] : i = inter1(ii) && c1=0 && c2=0 && c0=0 && c3=1}")
D_1_2 = D_1_2.union(Relation("{[c0,s,c1,i,c2] -> [c0,s,c3,ii,c2] : i = inter2(ii) && c1=0 && c2=0 && c0=0 && c3=1}"))
print
print "D_1_2 = ", D_1_2
PrettyPrintVisitor().visit(D_1_2)
D_1_3 = D_1_2


print
T_I0_to_I1 = Relation('{[c0, s, c0, i, c0] -> [c0, s, c0, j, c0] : c0=0 && j=sigma(i)}')
T_I0_to_I1 = T_I0_to_I1.union( Relation('{[c0, s, c1, ii, x] -> [c0, s, c1, ii, x] : c0=0 && c1=1}') )
print "\tT_I0_to_I1 = "
PrettyPrintVisitor().visit(T_I0_to_I1)
print
T_I1_to_I2 = Relation("{[c0,s,c0,i,c0] -> [c0,s,c0,i,c0] : c0=0 }")
T_I1_to_I2 = T_I1_to_I2.union( Relation("{[c0,s,c1,ii,x] -> [c7,s,c8,j,x] : j = delta(ii) && c0=0  && c1=1 }"))
print "T_I1_to_I2 = "
PrettyPrintVisitor().visit(T_I1_to_I2)


print
D_1_2 = T_I0_to_I1.compose( D_1_2.compose( T_I0_to_I1.inverse() ) )
print "\t\tD_1_2 = T_I0_to_I1 compose ( D_1_2 compose (inverse T_I0_to_I1) ) ) = ", D_1_2
PrettyPrintVisitor().visit(D_1_2)
print
D_1_2 = T_I1_to_I2.compose( D_1_2.compose( T_I1_to_I2.inverse() ) )
print "\t\tD_1_2 = T_I1_to_I2 compose ( D_1_2 compose (inverse T_I1_to_I2) ) ) =", D_1_2
PrettyPrintVisitor().visit(D_1_2)

print
print "\t\tD_1_3 = T_I0_to_I1 compose ( D_1_3 compose (inverse T_I0_to_I1) ) ) ="
D_1_3 = T_I0_to_I1.compose( D_1_3.compose( T_I0_to_I1.inverse() ) )
PrettyPrintVisitor().visit(D_1_3)
print
print "\t\tD_1_3 = T_I1_to_I2 compose ( D_1_3 compose (inverse T_I1_to_I2) ) ) ="
D_1_3 = T_I1_to_I2.compose( D_1_3.compose( T_I1_to_I2.inverse() ) )
PrettyPrintVisitor().visit(D_1_3)



print
iter_sub_space_relation = Relation("{[c0,s,x,i,y]->[x,i]}")
print "\t\titer_sub_space_relation (issr) = ", iter_sub_space_relation
PrettyPrintVisitor().visit(iter_sub_space_relation)

print
temp = iter_sub_space_relation.compose(D_1_2)
print "\t\t\tissr compose D_1_2 =", temp
PrettyPrintVisitor().visit(temp)

D_ST = iter_sub_space_relation.compose(iter_sub_space_relation.compose(D).inverse()).inverse()
PrettyPrintVisitor().visit(D_ST)
