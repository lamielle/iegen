#Runs all of the IEGen tests
def run_tests():
	import iegen.lib.nose
	iegen.lib.nose.run(argv=['','-v','-s','-w%s'%iegen.dir])

#Runs all of the IEGen tests with coverage turned on
def run_coverage():
	import sys
	import iegen.lib.coverage
	iegen.lib.coverage.start()
	run_tests()
	iegen.lib.coverage.stop()
	mods=[module for module in sys.modules.values() if str(module).find('iegen.')>=0 and str(module).find('iegen.lib.')<0]
	iegen.lib.coverage.report(mods)

#Given a MapIR object, calculates the combined iteration space of all statements
def full_iter_space(statements):
	#Get the iteration space of the first statement
	statement=statements[0]
	full_iter=statement.iter_space.apply(statement.scatter)

	#Now union this with the rest of the statement's iteration spaces
	for statement in statements[1:]:
		full_iter=full_iter.union(statement.iter_space.apply(statement.scatter))

	return full_iter

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

#Decorator that uses the SortVisitor to sort the first implicit 'self' argument of the decorated function
@decorator
def sort_self(func,*args,**kw):
	result=func(*args,**kw)
	sort_visit(args[0])
	return result

#Decorator that uses the SortVisitor to sort the result of the decorated function
@decorator
def sort_result(func,*args,**kw):
	result=func(*args,**kw)
	sort_visit(result)
	return result

#Decorator that uses the CheckVisitor to check the first implicit 'self' argument of the decorated function
@decorator
def check(func,*args,**kw):
	result=func(*args,**kw)
	check_visit(args[0])
	return result
#--------------------------------
