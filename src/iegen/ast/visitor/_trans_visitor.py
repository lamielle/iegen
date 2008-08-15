#!/usr/bin/env python

from iegen.ast.visitor import DFVisitor
#from pres_parser import PresParser
#from pycloog import Statement,Names,codegen

class TransVisitor(DFVisitor):
	def __init__(self,params):
		self.params=params
		self.num_params=len(params)

	def defaultIn(self,node):
		pass
	def defaultOut(self,node):
		pass

	def inPresRelation(self,node):
		raise ValueError('This visitor only works on PresSets and PresSetUnions.')
	def inPresRelationUnion(self,node):
		raise ValueError('This visitor only works on PresSets and PresSetUnions.')

	def inPresSet(self,node):
		self.mat=[]

	def inVarTuple(self,node):
		self.vars=node._idList
		self.num_vars=len(self.vars)
		self.num_cols=1+self.num_vars+self.num_params+1

	def inInequality(self,node):
		self.row=[0]*self.num_cols
		self.row[0]=1

		self.minus=0

	def outInequality(self,node):
		self.mat.append(self.row)
		assert 0==self.minus

	def inEquality(self,node):
		self.row=[0]*self.num_cols
		self.row[0]=0

		self.minus=0

	def outEquality(self,node):
		self.mat.append(self.row)
		assert 0==self.minus

	def inIntExp(self,node):
#		print 'In IntExp node:',node._val,self.minus%2
		self.row[-1]= node._val if 0==self.minus%2 else -1*node._val

	def inIdExp(self,node):
		pass
#		print 'InIdExp node:',node._id,self.minus%2

		if node._id in self.vars:
			self.row[self.vars.index(node._id)+1]=1 if 0==self.minus%2 else -1
		elif node._id in self.params:
			self.row[self.params.index(node._id)+self.num_vars+1]=1 if 0==self.minus%2 else -1
		else:
			raise ValueError('Existential variable in set.')

	def inMinusExp(self,node):
		self.minus+=1
	def outMinusExp(self,node):
		self.minus-=1

	def inPlusExp(self,node):
		pass
#		print 'In PlusExp'
	def outPlusExp(self,node):
		pass
#		print 'Out PlusExp'

#params=['n']
#v=TransVisitor(params)

#v.visit(PresParser.parse_set('{[i,j]:1<=i && i<=n && 1<=j && j<=n}'))

#print v.mat
#scat=[[0,1,0,0,0,0]]
#stmt=Statement(v.mat,scat)
#names=Names(['i','j'],['n'])
#codegen([stmt],names)
