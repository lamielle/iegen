#!/usr/bin/env python

from pres_parser import PresParser
from ast import Equality,Inequality,IdExp,IntExp
from pycloog import Statement,Names,codegen

def trans_to_mat(set,params):
	vars=set._setTuple._idList
	num_params=len(params)
	num_vars=len(vars)
	num_cols=1+num_vars+num_params+1

	mat=[]

	for conjunction in set._conjunct._constraintList:
		#Create a new row with the correct number of columns
		row=[0]*num_cols

		#Set whether this constraint is an equality or inequality
		if isinstance(conjunction,Equality):
			row[0]=0
		elif isinstance(conjunction,Inequality):
			row[0]=1
		else:
			raise ValueError("Conjunction '%s' is neither an equality nor an inequality."%conjunction)

		#Only support integer and ID expressions right now

		#LHS of conjunction
		if isinstance(conjunction._lhs,IdExp):
			id=conjunction._lhs._id
			if id in vars:
				row[vars.index(id)+1]=1
			elif id in params:
				row[params.index(id)+num_vars+1]=1
			else:
				raise ValueError('Existential variable in set.')
		elif isinstance(conjunction._lhs,IntExp):
			row[-1]=conjunction._lhs._val
		else:
			raise ValueError('Only IntExpr and IdExpr nodes are currently supported.')

		#RHS of conjunction
		if isinstance(conjunction._rhs,IdExp):
			id=conjunction._rhs._id
			if id in vars:
				row[vars.index(id)+1]=-1
			elif id in params:
				row[params.index(id)+1]=-1
			else:
				raise ValueError('Existential variable in set.')
		elif isinstance(conjunction._rhs,IntExp):
			row[-1]=-1*conjunction._rhs._val
		else:
			raise ValueError('Only IntExpr and IdExpr nodes are currently supported.')

		mat.append(row)

	return mat

set=PresParser.parse_set('{[a,b]:a=1 && 1<=b}')
params=['n']
mat=trans_to_mat(set,params)

set_string='{[i,j]:i>=1 && i<=n && j>=1 && j<=n}'
print 'Set:',set_string
set=PresParser.parse_set(set_string)
params=['n']
mat=trans_to_mat(set,params)

scat=[[0,1,0,0,0,0]]
stmt=Statement(mat,scat)
names=Names(['i','j'],['n'])
codegen([stmt],names)
