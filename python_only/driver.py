# driver.py
# 
# Driver to test the python only parsing and representation of Presburger sets 
# and relations with uninterpreted function symbols.

# Initial testing of the ast
from ast import *

root = PresSet(VarTuple(['a','b']),Conjunction([Inequality(IdExp('a'),IntExp('5'))]))

# Testing of the presburger set and relation parser.
import pres_parser

parser = pres_parser.PresParser('set')

# set with no conditions
parser.parse_set('{[i,j,k]}')

# set with simple conditions
parser.parse_set('{[i,j,k]: 1 <= i <= 45 }')

# set with more complex conditions
parser.parse_set('{[i,j,k]: 1 <= i,j,k <= 45 }')

# Parsing relations
rparser = pres_parser.PresParser('relation')

# A simple relation with only in and out tuple
rparser.parse_relation('{[i] -> [j]}')

# A simple relation with constraints
rparser.parse_relation('{[i] -> [j] : i = j }')

# A simple relation with constraints involving uninterp functions
rparser.parse_relation('{[i] -> [j] : i = delta(j) }')

# A simple relation with constraints involving nested uninterp functions
rparser.parse_relation('{[i] -> [j] : i = sigma(delta(j)) }')

# Checking that we can parse all examples from 
# iegen/docs/moldyn-data-iter-reord.txt
parser.parse_set('{ [ii,j] : j=1 && 0 <= ii <= (n_inter-1)  } union { [ii,j] : j=2 && 0 <= ii <= (n_inter-1)  }')
parser.parse_set('{ [k] : 0 <= k <= (N-1) }')
parser.parse_set('{ [k] : 0 <= k <= (n_inter-1) }')

parser.parse_set('{ [k] : 0 <= k <= (n_inter-1) }')

rparser.parse_relation('{ [ii,j] -> [k] :j=2 && k=inter2(ii) }')
rparser.parse_relation('{ [ii,j] -> [ k ] : k=inter1(ii) && 1<=j<=2 } union { [ii,j] -> [ k ] : k=inter2(ii) && 1<=j<=2 }')
rparser.parse_relation('{ [ k ] -> [ r ] : r=sigma( k ) }')
rparser.parse_relation('{ [ ii, j ] -> [ ii ] }')
rparser.parse_relation('{ [ i ] -> [ k ] : k = delta( i ) }')
rparser.parse_relation('{ [a] -> [ k ] : k=inter1(a) } union { [a] -> [ k ] : k=inter2(a) }')
rparser.parse_relation('{ [k] -> [a] : a=ii && b=j && k=inter1(ii) && 1<=j<=2 }')
rparser.parse_relation('{ [k] -> [a] : k=inter1(a) && 1<=j<=2 }')
rparser.parse_relation('{ [k] -> [a] : k=inter1(a) }')
rparser.parse_relation('{ [a,b] -> [r] : r=sigma(inter1(delta_inv(a))) && 1 <=b<=2}')


