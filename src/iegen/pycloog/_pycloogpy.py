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
	         ('num_params',c_int),
	         ('context_domains',POINTER(_PYCLOOG_DOMAIN)),
	         ('num_context_domains',c_int)]

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
		num_domains=len(statements[s].domain)
		new_domains=(_PYCLOOG_DOMAIN*num_domains)()
		for d in xrange(num_domains):
			new_domains[d]=_get_pycloog_domain(statements[s].domain[d])
		new_statements[s].domains=new_domains
		new_statements[s].num_domains=num_domains

		#Set the scattering function related fields
		if None is statements[s].scatter:
			new_statements[s].scatter=POINTER(_PYCLOOG_DOMAIN)()
		else:
			new_statements[s].scatter=pointer(_get_pycloog_domain(statements[s].scatter))

	return new_statements

#Translates the given iterator and parameter names to a ctypes PYCLOOG_NAMES structure
def _get_pycloog_names(iters,params,param_names):
	names=_PYCLOOG_NAMES()
	names.iters=_get_ctypes_str_arr(iters)
	names.num_iters=len(iters)
	names.params=_get_ctypes_str_arr(param_names)
	names.num_params=len(params)

	#Create the context based on the upper and lower bounds of the params
	num_cols=names.num_params+2
	context=[]
	for col,param in enumerate(params):
		if param.lower_bound is not None:
			constraint=[0]*num_cols

			#param>=lb
			constraint[0]=1
			constraint[col+1]=1
			constraint[-1]=-param.lower_bound

			context.append(constraint)

		if param.upper_bound is not None:
			constraint=[0]*num_cols

			#param<=ub
			constraint[0]=1
			constraint[col+1]=-1
			constraint[-1]=param.upper_bound

			context.append(constraint)

	#If we have at least one constraint, convert the context to a pycloog_domain
	if len(context)>0:
		contexts=(_PYCLOOG_DOMAIN*1)()
		contexts[0]=_get_pycloog_domain(context)
		names.context_domains=contexts

		#Only one conjunction in the context (a single polyhedron)
		names.num_context_domains=1
	else:
		names.context_domains=POINTER(_PYCLOOG_DOMAIN)()
		names.num_context_domains=0

	return names
#---------------------------------------

#---------- Public Interface ----------
#Class representing a single statement:
#Each statement has an associated iteration domain
#and optional scattering function
#Domains are Set objects and scattering functions are Relation objects
class Statement(object):
	__slots__=('domain','scatter')

	def __init__(self,domain,scatter=None):
		from iegen.util import raise_objs_not_like_types
		from iegen import Set,Relation

#		raise_objs_not_like_types(domain,Set)
		self.domain=domain

#		if scatter is not None: raise_objs_not_like_types(scatter,Relation)
		self.scatter=scatter

#The only public function of this module
#Uses CLooG to generate code based on the given
#Statement objects
def codegen(statements):
	#Process the statements
	iters=statements[0].domain.tuple_vars

	#This previously checked that all iterators had the same names.
	#It isn't strictly necessary, and thus has been commented out for now
	#for statement in statements[1:]:
	#	if statement.domain.tuple_vars!=iters:
	#		raise ValueError("Statements's domains do not have the same iterator names: %s!=%s"%(statement.domain.tuple_vars,iters))

	#Collect the params from all domain/scatter fields in all statements
	params=[symbolic for statement in statements for symbolic in statement.domain.symbolics]
	params+=[symbolic for statement in statements if statement.scatter is not None for symbolic in statement.scatter.symbolics]

	#Reduce the collected parameters to a unique set
	params=list(set(params))

	#Get a list of just the parameter names
	param_names=[param.name for param in params]

	#Convert the domain/scatter fields into the CLooG matrix format
	for statement in statements:
		statement.domain=statement.domain.get_constraint_mat(params)
		if statement.scatter is not None:
			statement.scatter=statement.scatter.get_scatter_mat(params)

		#Make sure there is a single conjunction for the scattering function
		if statement.scatter is not None:
			if len(statement.scatter)>1:
				raise ValueError('Scattering functions with unions are not supported')
			statement.scatter=statement.scatter[0]

	#Convert the parmeters to ctypes
	names=byref(_get_pycloog_names(iters,params,param_names))
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
