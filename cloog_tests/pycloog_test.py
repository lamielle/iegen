#!/usr/bin/env python

from ctypes import *

class PYCLOOG_STATEMENT(Structure):
	_fields_=[('domain',POINTER(POINTER(c_int))),
	          ('domain_num_rows',c_int),
	          ('domain_num_cols',c_int),
	          ('scatter',POINTER(POINTER(c_int))),
	          ('scatter_num_rows',c_int),
	          ('scatter_num_cols',c_int)]

class PYCLOOG_NAMES(Structure):
	_fields_=[('iters',POINTER(c_char_p)),
	         ('num_iters',c_int),
	         ('params',POINTER(c_char_p)),
	         ('num_params',c_int)]

def mat_type(num_rows):
	return POINTER(c_int)*num_rows
def row_type(num_cols):
	return c_int*num_cols

def str_arr_type(num_strings):
	return c_char_p*num_strings

def code_gen():
	pycloog=CDLL('./pycloog.so')
	pycloog.pycloog_codegen.argtypes=[POINTER(PYCLOOG_STATEMENT),c_int,POINTER(PYCLOOG_NAMES)]
	return pycloog.pycloog_codegen

#Assumes all rows have the same length
#(no jagged arrays)
def get_ctypes_mat(mat):
	num_rows=len(mat)
	num_cols=len(mat[0])
	cmat=mat_type(num_rows)()

	for row in xrange(num_rows):
		cmat[row]=row_type(num_cols)()
		for col in xrange(num_cols):
			cmat[row][col]=c_int(mat[row][col])
	return cmat

def get_ctypes_str_arr(strs):
	num_strs=len(strs)
	cstrs=str_arr_type(num_strs)()
	for i in xrange(num_strs):
		cstrs[i]=strs[i]
	return cstrs

num_rows=4
num_cols=5
num_iters=2
num_params=1

dom1=[[1, 1, 0,0, -1],
     [1,-1, 0,1, 0],
     [1, 0, 1,0, -1],
     [1, 0,-1,1,0]]
dom1=get_ctypes_mat(dom1)
scat1=[[0,1,0,0,0,1]]
scat1=get_ctypes_mat(scat1)

dom2=[[1, 1, 0,0, -1],
     [1,-1, 0,1, 0],
     [1, 0, 1,0, -1],
     [1, 0,-1,1,0]]
dom2=get_ctypes_mat(dom2)
scat2=[[0,1,0,0,0,2]]
scat2=get_ctypes_mat(scat2)

stmts=(PYCLOOG_STATEMENT*2)()
stmts[0]=PYCLOOG_STATEMENT()
stmts[0].domain=dom1
stmts[0].domain_num_rows=num_rows
stmts[0].domain_num_cols=num_cols
stmts[0].scatter=scat1
stmts[0].scatter_num_rows=1
stmts[0].scatter_num_cols=6
stmts[1]=PYCLOOG_STATEMENT()
stmts[1].domain=dom2
stmts[1].domain_num_rows=num_rows
stmts[1].domain_num_cols=num_cols
stmts[1].scatter=scat2
stmts[1].scatter_num_rows=1
stmts[1].scatter_num_cols=6

names=PYCLOOG_NAMES()
names.iters=get_ctypes_str_arr(['i','j'])
names.num_iters=2
names.params=get_ctypes_str_arr(['n'])
names.num_params=1

code_gen()(stmts,2,byref(names))
