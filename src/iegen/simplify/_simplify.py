import iegen
from iegen.util import raise_objs_not_like_types,like_type

#---------- Formula Simplification ----------
#---------- Rule Registration ----------
#Dictionary containing rule groups
#This is a dictionary that maps integers to lists of tuples
#Each tuple in the list contains:
#0) Function to call for rule
#1) If this is a method call, the instance for self
_registered_rules={}

#Register the given function as a simplification rule
#rule_func: The function to run for the rule
#instance: If this is a method, the instance to use for self
#rule_group: What group (int) to put this rule into
#            0 and 1 are reserved, 3+ are for users
def register_rule(rule_func,instance=None,rule_group=3):
	iegen.print_debug("Registering rule '%s' in rule group '%s'..."%(rule_func,rule_group))
	if rule_group not in _registered_rules:
		_registered_rules[rule_group]=[]
	_registered_rules[rule_group].append((rule_func,instance))
#---------------------------------------

#---------- Inverse Pair Registration ----------
#Dictionary of mappings from function names to inverse function names
#If f->f_inv, then the corresponding f_inv->f should exist here as well
_inverse_pairs={}

#Accessor function for obtaining the inverse pairs dictionary
def inverse_pairs():
	return _inverse_pairs

#Standard suffix for an inverse function
_inverse_suffix='_inv'

#Accesor function for obtaining the inverse suffix string
def inverse_suffix():
	return _inverse_suffix

#Registers the given function and its inverse as a pair
#If inverse_function_name is not given, the name is function_name+inverse_suffix
def register_inverse_pair(function_name,inverse_function_name=None):
	#Build the inverse_function_name if it was not given
	if inverse_function_name is None:
		inverse_function_name=function_name+inverse_suffix()

	iegen.print_detail('Registering inverse function pair (%s,%s)...'%(function_name,inverse_function_name))

	#Register the names in the dictionary of function name pairs
	_inverse_pairs[function_name]=inverse_function_name
	_inverse_pairs[inverse_function_name]=function_name
#-----------------------------------------------

#Given an object of the following types:
#Set,Relation,PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp
#Applies the registered simplification rules to reduce the complexity of the object
def simplify(obj):
	from iegen import Set,Relation
	from iegen.ast import PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp
	from iegen.ast.visitor import SortVisitor

	raise_objs_not_like_types(obj,[Set,Relation,PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp])

	#Iteratively apply simplification rules until no rules apply
	changed_outer=True
	while changed_outer:
		changed_outer=False

		#Iteratively apply simplification rules for each rule group
		for rule_group in _registered_rules:
			changed=True
			while changed:
				changed=False

				#Apply each simplification rule in the current rule group
				for rule,instance in _registered_rules[rule_group]:
					#Is this a function call?
					if instance is None:
						changed=rule(obj) or changed
					#This is a method call
					else:
						changed=rule(instance,obj) or changed

				changed_outer=changed or changed_outer

	#Apply a sort just to make sure things are ordered properly
	SortVisitor().visit(obj)
#--------------------------------------------
