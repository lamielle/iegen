from ctypes import *

#---------- Private Interface ----------
#Defines a ctypes structure matching the pycloog_domain
#structure found in pycloog.h
class _PYCLOOG_DOMAIN(Structure):
	_fields_=[('domain',POINTER(POINTER(c_int))),
	          ('num_rows',c_int),
	          ('num_cols',c_int)]

#Defines a ctypes structure matching the pycloog_statement
#structure found in pycloog.h
class _PYCLOOG_STATEMENT(Structure):
	_fields_=[('domains',POINTER(_PYCLOOG_DOMAIN)),
	          ('num_domains',c_int),
	          ('scatter',POINTER(_PYCLOOG_DOMAIN))]

#Defines a ctypes structure matching the pycloog_names
#structure found in pycloog.h
class _PYCLOOG_NAMES(Structure):
	_fields_=[('iters',POINTER(c_char_p)),
	         ('num_iters',c_int),
	         ('params',POINTER(c_char_p)),
	         ('num_params',c_int)]

#Returns a ctypes type for an array of integer pointers
#The size of the array is equal to num_rows
def _mat_type(num_rows):
	return POINTER(c_int)*num_rows

#Returns a ctypes type for an array of integers
#The size of the array is equal to num_cols
def _row_type(num_cols):
	return c_int*num_cols

#Returns a ctypes type for an array of char*s
#The size of the array is equal to the num_strings
def _str_arr_type(num_strings):
	return c_char_p*num_strings

#Gets an array of char* based on the given collection of strings
def _get_ctypes_str_arr(strs):
	num_strs=len(strs)
	cstrs=_str_arr_type(num_strs)()
	for i in xrange(num_strs):
		cstrs[i]=strs[i]
	return cstrs

#Allocator callback function for allocation of strings from C
def _string_allocator(size):
	return addressof(c_char_p(' '*size))

#Returns the type of the string_allocator
def _string_allocator_type():
	return CFUNCTYPE(c_char_p,c_int)

#Loads the '_pycloog.so' shared object and returns a function pointer
#to the pycloog_codegen function in that library
def _get_codegen_func():
	from os import sep
	from os.path import dirname
	pycloog=CDLL(dirname(__file__)+sep+'_pycloog.so')
	pycloog.pycloog_codegen.argtypes=[POINTER(_PYCLOOG_STATEMENT),c_int,POINTER(_PYCLOOG_NAMES),_string_allocator_type()]
	pycloog.pycloog_codegen.restype=c_char_p
	return pycloog.pycloog_codegen

#Converts the given two dimensional array (mat)
#to a ctypes two diminsional integer array
#contained in a _PYCLOOG_DOMAIN structure
#NOTE: This function assumes all rows have
#the same length (mat is not a jagged array)
def _get_pycloog_domain(mat):
	domain=_PYCLOOG_DOMAIN()

	#Set the dimensions of the domain
	domain.num_rows=len(mat)
	domain.num_cols=len(mat[0])

	#Create a ctypes two-dimensional array
	cmat=_mat_type(domain.num_rows)()

	#Copy the data from the given two-dimensional array to the ctypes two-dimensional array
	for row in xrange(domain.num_rows):
		cmat[row]=_row_type(domain.num_cols)()
		for col in xrange(domain.num_cols):
			cmat[row][col]=c_int(mat[row][col])

	#Set the new domain
	domain.domain=cmat

	return domain

#Translates the given collection of Statement classes
#to a ctypes array of PYCLOOG_STATEMENT structures
def _get_pycloog_statements(statements):
	num_statements=len(statements)
	new_statements=(_PYCLOOG_STATEMENT*num_statements)()
	for s in xrange(num_statements):
		#XXX: This may not be necessary, once finished check
		new_statements[s]=_PYCLOOG_STATEMENT()

		#Set the domain related fields
		num_domains=len(statements[s].domains)
		new_domains=(_PYCLOOG_DOMAIN*num_domains)()
		for d in xrange(num_domains):
			new_domains[d]=_get_pycloog_domain(statements[s].domains[d])
		new_statements[s].domains=new_domains
		new_statements[s].num_domains=num_domains

		#Set the scattering function related fields
		if None==statements[s].scatter:
			new_statements[s].scatter=POINTER(_PYCLOOG_DOMAIN)()
		else:
			new_statements[s].scatter=pointer(_get_pycloog_domain(statements[s].scatter))

	return new_statements

#Translates the given Names object to a ctypes PYCLOOG_NAMES structure
def _get_pycloog_names(names):
	new_names=_PYCLOOG_NAMES()
	new_names.iters=_get_ctypes_str_arr(names.iters)
	new_names.num_iters=len(names.iters)
	new_names.params=_get_ctypes_str_arr(names.params)
	new_names.num_params=len(names.params)
	return new_names
#---------------------------------------

#---------- Public Interface ----------
#Class representing a single statement:
#Each statement has an associated collection of iteration domains
#and a scattering function
class Statement(object):
	__slots__=('domains','scatter')

	def __init__(self,domains,scatter):
		self.domains=domains
		self.scatter=scatter

#Class containing a collection of iterator names
#and parameter names
class Names(object):
	__slots__=('iters','params')

	def __init__(self,iters,params):
		self.iters=iters
		self.params=params

#The only public function of this module
#It takes a collection of Statment objects
#and a Names object and uses CLooG to generate
#code based on these objects
def codegen(statements,names):
	#Convert the parmeters to ctypes
	statements=_get_pycloog_statements(statements)
	num_statements=len(statements)
	names=byref(_get_pycloog_names(names))
	string_allocator=_string_allocator_type()(_string_allocator)

	#Get a function pointer to the pycloog_codegen function
	codegen_func=_get_codegen_func()

	#Call pycloog_codegen
	code=codegen_func(statements,num_statements,names,string_allocator)

	#Return the generated code and trim off the trailing newline
	return code[:-1]
#--------------------------------------
