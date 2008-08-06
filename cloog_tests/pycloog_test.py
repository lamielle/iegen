#!/usr/bin/env python

from ctypes import *

def mat_type(num_rows,num_cols):
	return POINTER(c_int)*num_rows
def row_type(num_cols):
	return c_int*num_cols

def str_arr_type(num_strings):
	return c_char_p*num_strings

def get_code_gen_func(num_rows,num_cols,num_iters,num_params):
	pycloog=CDLL('./pycloog.so')
	pycloog.code_gen.argtypes=[mat_type(num_rows,num_cols),c_int,c_int,str_arr_type(num_iters),c_int,str_arr_type(num_params),c_int]
	return pycloog.code_gen

#Assumes all rows have the same length
#(no jagged arrays)
def get_ctypes_mat(mat):
	num_rows=len(mat)
	num_cols=len(mat[0])
	cmat=mat_type(num_rows,num_cols)()

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
num_cols=6
num_iters=2
num_params=2

dom=[[1, 1, 0,0, 0,-6],
     [1,-1, 0,1, 0,-1],
     [1, 0, 1,0, 0, 9],
     [1, 0,-1,0,-1,-1]]
dom=get_ctypes_mat(dom)

iters=get_ctypes_str_arr(["i","j"])
params=get_ctypes_str_arr(["k","l"])

code_gen=get_code_gen_func(num_rows,num_cols,num_iters,num_params)

code_gen(dom,num_rows,num_cols,iters,num_iters,params,num_params)
