import os

#Runs all of the IEGen tests
def run_tests(subdir=''):
	import iegen.lib.nose
	iegen.lib.nose.run(argv=['','-v','-s','-w%s'%iegen.base_dir+os.sep+subdir])

#Runs all of the IEGen tests with coverage turned on
def run_coverage():
	import sys
	import iegen.lib.coverage
	iegen.lib.coverage.start()
	run_tests()
	iegen.lib.coverage.stop()
	mods=[module for module in sys.modules.values() if str(module).find('iegen.')>=0 and str(module).find('iegen.lib.')<0]
	iegen.lib.coverage.report(mods)

#Runs the given spec file under the profiler
def run_profile(spec_file_name):
	import pstats,commands

	prof_file_name=spec_file_name+'.prof'
	commands.getoutput("python -m cProfile -o %s '%s'"%(prof_file_name,spec_file_name))
	p=pstats.Stats(prof_file_name)
	p.sort_stats('cumulative').print_stats(10)

#Iterator wrapper:
#Rather than yielding just the item, yields a tuple where
#the first element is the item and the second is a boolean.
#The boolean is True if the item is the last in the sequence
#and is False for all other items
#Code from: http://code.activestate.com/recipes/392015/
def iter_islast(iterable):
	""" iter_islast(iterable) -> generates (item, islast) pairs

Generates pairs where the first element is an item from the iterable
source and the second element is a boolean flag indicating if it is the
last item in the sequence.
"""

	it = iter(iterable)
	prev = it.next()
	for item in it:
		yield prev, False
		prev = item
	yield prev, True

#Determines the sign of the given number
#Returns -1 if the number is <0
#Returns 1 if the number is >=0
def sign(num):
	if num<0:
		return -1
	else:
		return 1

#Inverts key/value pairs of the given dictionary
def invert_dict(d):
	return dict(((v,k) for k,v in d.iteritems()))

#Defines a property called m_name
#This property is assigned to the given class
#The getter and setter access a member of the class called _'name'
def define_properties(add_to_class,names):
	for name in names:
		#Define the getter and setter methods themselves
		exec '''
def _get(self): return self._%s
def _set(self,value): self._%s=value'''%(name,name)

		#Create a property from these methods and assign it to the class
		exec '''add_to_class.m_%s=property(_get,_set)'''%(name,)

#Given a term (VarExp or FuncExp), returns the equivalent term
#With a coefficient of 1
#Returns a new object that is a copy of the given term
def get_basic_term(term):
	from copy import deepcopy
	term=deepcopy(term)
	term.coeff=1
	return term

#Search for the given term in the given collection of terms
#Searching is done by variable name and function name/arguments
#Coefficients are not used
#
#Returns the position of the term if found, None otherwise
def find_term(term,terms):
	term=get_basic_term(term)
	terms=[get_basic_term(t) for t in terms]

	#Try to find the index of the term
	try:
		res=terms.index(term)
	except:
		res=None
	return res

#Checks that the given object has all attributes of the __slots__ property of the given class
#Returns True if so, False otherwise
def like_type(obj,type):
	for attr in type.__slots__:
		if not hasattr(obj,attr):
			return False
	return True

#Determines if the given object is iterable
#If so, returns True, otherwise returns False
def is_iterable(obj):
	try:
		iter(obj)
		iterable=True
	except:
		iterable=False
	return iterable

#Raises a ValueError if the any of the given objects are not like any of the given types
#If either of objs of types are not iterable, they will be added as the lone element to a new list
#If a message is given, it will be used as the exception string rather than the default
def raise_objs_not_like_types(objs,types,message=''):
	if not is_iterable(objs):
		objs=[objs]

	if not is_iterable(types):
		types=[types]

	attrs=[[type.__slots__] for type in types]

	for obj in objs:
		found=False
		for type in types:
			if like_type(obj,type):
				found=True
				break
		if not found:
			raise ValueError("The given object, '%s', must have one of the following sets of attributes: %s"%(obj,attrs))

class DimensionalityError(Exception):
	pass

#Given a Set or Relation, renames all tuple variables in the
#PresSets/PresRelations in the union to have the same names
#The first PresSet/PresRelation in the union is what the other
#tuple variables are renamed to
def normalize_names(obj):
	from iegen.ast.visitor import RenameVisitor
	from iegen import Formula

	#Do the normalization only if we are given a Set or Relation
	if like_type(obj,Formula):
		formula=obj
		for i in xrange(len(formula.formulas)):
			form=formula.formulas[i]
			if 0==i:
				base_form=form
			else:
				#Rename vars to something 'unique'
				RenameVisitor(formula._get_prefix_rename_dict(form,'f%d'%i)).visit(form)
				#Rename to target names
				RenameVisitor(formula._get_formula_rename_dict(form,base_form)).visit(form)

#Runs normalization code that only needs to be run once rather than multiple
# times over the life of the object
def one_time_normalize(obj):
	from iegen.ast.visitor import UniqueTupleVarsVisitor

	#Run UniqueTupleVarsVisitor
	UniqueTupleVarsVisitor().visit(obj)

#---------- Decorators ----------
from iegen.lib.decorator import decorator

#Runs the SortVisitor on the given object
def sort_visit(obj):
	from iegen.ast.visitor import SortVisitor
	SortVisitor().visit(obj)

#Runs the CheckVisitor on the given object
def check_visit(obj):
	from iegen.ast.visitor import CheckVisitor
	CheckVisitor().visit(obj)

#Calls the simplification routine on the given object
def run_simplify(obj):
	from iegen.simplify import simplify
	simplify(obj)

#Decorator that normalizes the first implicit 'self' argument of the decorated function
#Normalization is renaming -> sorting -> simplification -> sorting
@decorator
def normalize_self(func,*args,**kw):
	result=func(*args,**kw)
	normalize_names(args[0])
	sort_visit(args[0])
	run_simplify(args[0])
	sort_visit(args[0])
	return result

#Decorator that normalizes the result of the decorated function
#Normalization is renaming -> sorting -> simplification -> sorting
@decorator
def normalize_result(func,*args,**kw):
	result=func(*args,**kw)
	normalize_names(result)
	sort_visit(result)
	run_simplify(result)
	sort_visit(result)
	return result

#Decorator that uses the CheckVisitor to check the first implicit 'self' argument of the decorated function
@decorator
def check(func,*args,**kw):
	result=func(*args,**kw)
	check_visit(args[0])
	return result
#--------------------------------
