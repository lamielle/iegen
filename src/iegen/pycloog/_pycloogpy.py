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
allocated=[]
def _string_allocator(size):
	allocated.append(create_string_buffer(size))
	return addressof(allocated[len(allocated)-1])

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
		if None is statements[s].scatter:
			new_statements[s].scatter=POINTER(_PYCLOOG_DOMAIN)()
		else:
			new_statements[s].scatter=pointer(_get_pycloog_domain(statements[s].scatter))

	return new_statements

#Translates the given iterator and parameter names to a ctypes PYCLOOG_NAMES structure
def _get_pycloog_names(iters,params):
	names=_PYCLOOG_NAMES()
	names.iters=_get_ctypes_str_arr(iters)
	names.num_iters=len(iters)
	names.params=_get_ctypes_str_arr(params)
	names.num_params=len(params)
	return names
#---------------------------------------

#---------- Public Interface ----------
#Class representing a single statement:
#Each statement has an associated iteration domain
#and scattering function
#Domains and scattering functions are Set objects
class Statement(object):
	__slots__=('domains','scatter','iters','params')

	def __init__(self,domain,scatter=None):
		from iegen.util import raise_objs_not_like_types
		from iegen import Set
		from iegen.ast.visitor import TransVisitor

		raise_objs_not_like_types(domain,Set)

		self.domains=TransVisitor().visit(domain).mats

		if None is scatter:
			self.scatter=None
		else:
			raise_objs_not_like_types(scatter,Set)
			self.scatter=TransVisitor().visit(scatter).mats[0]

		#Assumes that all variable and symbolic names are the same for
		#all sets in the union
		self.iters=[var.id for var in domain.sets[0].tuple_set.vars]
		self.params=[sym.name for sym in domain.sets[0].symbolics]

#The only public function of this module
#Uses CLooG to generate code based on the given
#Statement objects
def codegen(statements):
	#Convert the parmeters to ctypes
	names=byref(_get_pycloog_names(statements[0].iters,statements[0].params))
	statements=_get_pycloog_statements(statements)
	num_statements=len(statements)
	string_allocator=_string_allocator_type()(_string_allocator)

	#Get a function pointer to the pycloog_codegen function
	codegen_func=_get_codegen_func()

	#Call pycloog_codegen
	code=codegen_func(statements,num_statements,names,string_allocator)

	#Return the generated code with comments and empty lines
	lines=code.split('\n')
	lines=[line for line in lines if -1==line.find('/*') and -1==line.find('//') and line!='']
	return '\n'.join(lines)
#--------------------------------------
