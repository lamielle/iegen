from iegen.util import raise_objs_not_like_types,like_type

#Given a MapIR object, calculates the combined iteration space of all statements
def full_iter_space(statements):
	#Get the iteration space of the first statement
	statement=statements[0]
	full_iter=statement.iter_space.apply(statement.scatter)

	#Now union this with the rest of the statement's iteration spaces
	for statement in statements[1:]:
		full_iter=full_iter.union(statement.iter_space.apply(statement.scatter))

	return full_iter

#---------- Formula Simplification ----------
#Replaces all occurrences of the given variable name with the given expression in the given expression
#Returns True if any replacements were made, False otherwise
def _replace_in_exp(var_name,exp_to_replace,exp_to_modify):
	from iegen.ast import VarExp,FuncExp

	res=False

	#Look at each term in the expression
	for i in xrange(len(exp_to_modify.terms)):
		term=exp_to_modify.terms[i]

		#See if it is a VarExp and it matches the given variable name
		if like_type(term,VarExp):
			if var_name==term.id:
				pass

#Replaces all occurrences of the given variable name with the given expression in the given formula
#Returns True if any replacements were made, False otherwise
def _replace_var_with_exp(var_name,exp,formula):
	from iegen import Set,Relation

	if like_type(formula,Set):
		formulas=formula.sets
	else:
		formulas=formula.relations


	for formula in formulas:
		for constraint in formula.constraint_list:
			constraint.exp

#Simplification rule 1:
#Remove an equality constraint of the form:
#free_var=exp
#and replace all uses of 'free_var' in the remaining
#constraints with 'exp'
#
#Assumes 'formula' is a Set or Relation
#
#Returns True if any changes were made, False otherwise
def _simplify_free_var_equality(formula):
	from iegen.ast.visitor import FindFreeVarEqualityVisitor
	from iegen.ast import NormExp

	#Search for an equality with a free variable
	var_equality_tuple=FindFreeVarEqualityVisitor().visit(formula).var_equality_tuple

	#See if one was found
	if None is not var_equality_tuple:
		free_var,equality=var_equality_tuple

		#Remove the variable from the expression
		exp=equality.exp
		exp=exp-NormExp([free_var],0)

		#Do the replacement of the variable with the new expression
		res=_replace_var_with_exp(free_var.id,exp,formula)
	else:
		res=False

	return res

#TEMPORARY: Rewrite as a visitor!
def _remove_zero_coefficients(obj):
	from iegen.ast import NormExp
	if like_type(obj,NormExp):
		res=False
		removed=True
		while removed:
			removed=False
			for term in obj.terms:
				if 0==term.coeff:
					obj.terms.remove(term)
					removed=True
					res=True
					break
		return res

#Uses the MergeExpTermsVisitor to combine common terms in NormExps
def _merge_terms(obj):
	from iegen.ast.visitor import MergeExpTermsVisitor
	return MergeExpTermsVisitor().visit(obj).merged_terms

#Given an object of the following types:
#Set,Relation,PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp
#Applies various simplification rules to reduce the complexity of the object
def simplify(obj):
	from iegen import Set,Relation
	from iegen.ast import PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp

	raise_objs_not_like_types(obj,[Set,Relation,PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp])

	#Iteratively apply simplification rules until no rules apply
	changed=True
	while changed:
		changed=False

		#Remove terms in expressions with a coefficient of 0
		changed=_remove_zero_coefficients(obj) or changed

		#Merge common terms in NormExps
		changed=_merge_terms(obj) or changed

		#changed=_simplify_free_var_equality(obj) or changed
#--------------------------------------------
