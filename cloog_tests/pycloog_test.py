#!/usr/bin/env python

from ctypes import *

def mat_type(num_rows,num_cols):
	return c_int64*num_cols*num_rows


num_rows=5
num_cols=10
#size=10
#i_array=c_int*size

#PI=POINTER(c_int)

pycloog=CDLL('./pycloog.so')
pycloog.print_mat.argtypes=[POINTER(mat_type(num_rows,num_cols)),c_int,c_int]

mat=mat_type(num_rows,num_cols)()
for row in xrange(num_rows):
	for col in xrange(num_cols):
		mat[row][col]=row*col
print mat
for row in xrange(num_rows):
	print mat[row]
	for col in xrange(num_cols):
		print mat[row][col]

pycloog.print_mat(byref(mat),num_rows,num_cols)

##val=c_int(10)
##p_val=pointer(val)
##print p_val.contents
##print p_val[0]

##val=PI(c_int(10))
