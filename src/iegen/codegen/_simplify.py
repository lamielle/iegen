from iegen.util import raise_objs_not_like_types,like_type

#---------- Formula Simplification ----------
#Simplification rule 1:
#Remove an equality constraint of the form:
#free_var=exp
#and replace all uses of 'free_var' in the remaining
#constraints with 'exp'
#
#Assumes 'formula' is a Set or Relation
#
#Returns True if any changes were made, False otherwise
def _remove_free_var_equality(formula):
	from iegen.ast.visitor import RemoveFreeVarEqualityVisitor
	return RemoveFreeVarEqualityVisitor().visit(formula).changed

#Uses the MergeExpTermsVisitor to combine common terms in NormExps
def _merge_terms(obj):
	from iegen.ast.visitor import MergeExpTermsVisitor
	return MergeExpTermsVisitor().visit(obj).merged_terms

#Uses the RemoveZeroCoeffVisitor to remove any terms in NormExps with a coefficient of 0
def _remove_zero_coefficients(obj):
	from iegen.ast.visitor import RemoveZeroCoeffVisitor
	return RemoveZeroCoeffVisitor().visit(obj).removed_term

#Uses the RemoveEmptyConstraintsVisitor to remove any empty constraints from a conjunction
def _remove_empty_constraints(obj):
	from iegen.ast.visitor import RemoveEmptyConstraintsVisitor
	return RemoveEmptyConstraintsVisitor().visit(obj).removed_constraint

#Given an object of the following types:
#Set,Relation,PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp
#Applies various simplification rules to reduce the complexity of the object
def simplify(obj):
	from iegen import Set,Relation
	from iegen.ast import PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp
	from iegen.ast.visitor import SortVisitor

	raise_objs_not_like_types(obj,[Set,Relation,PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp])

	#Iteratively apply simplification rules until no rules apply
	changed=True
	while changed:
		changed=False

		#Merge common terms in NormExps
		changed=_merge_terms(obj) or changed

		#Remove terms in expressions with a coefficient of 0
		changed=_remove_zero_coefficients(obj) or changed

		#Remove empty constraints
		changed=_remove_empty_constraints(obj) or changed

		changed=_remove_free_var_equality(obj) or changed

	SortVisitor().visit(obj)
#--------------------------------------------