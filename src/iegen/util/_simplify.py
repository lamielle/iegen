import iegen
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
	from iegen.ast.visitor import RemoveFreeVarConstraintVisitor
	from iegen.ast import Equality
	if iegen.debug: before=str(formula)
	changed=RemoveFreeVarConstraintVisitor(Equality).visit(formula).changed
	if changed and iegen.debug: iegen.print_debug('Simplify: removed free variable equality: %s -> %s'%(before,formula))
	return changed

#Simplification rule 2:
#Remove an inequality constraint of the form:
#{free_var}++{symbolic constants}*+c>=0
#(ie one or more free variables, zero or more symbolic constants
# and some constant)
#
#This inequality is only constraining the free variable(s), and thus can be removed
#Assumes 'formula' is a Set or Relation
#
#Returns True if any changes were made, False otherwise
def _remove_free_var_inequality(formula):
	from iegen.ast.visitor import RemoveFreeVarConstraintVisitor
	from iegen.ast import Inequality
	if iegen.debug: before=str(formula)
	changed=RemoveFreeVarConstraintVisitor(Inequality).visit(formula).changed
	if changed and iegen.debug: iegen.print_debug('Simplify: removed free variable inequality: %s -> %s'%(before,formula))
	return changed

#Uses the MergeExpTermsVisitor to combine common terms in NormExps
def _merge_terms(obj):
	from iegen.ast.visitor import MergeExpTermsVisitor
	if iegen.debug: before=str(obj)
	merged_terms=MergeExpTermsVisitor().visit(obj).merged_terms
	if merged_terms and iegen.debug: iegen.print_debug('Simplify: merged terms: %s -> %s'%(before,obj))
	return merged_terms

#Uses the RemoveZeroCoeffVisitor to remove any terms in NormExps with a coefficient of 0
def _remove_zero_coefficients(obj):
	from iegen.ast.visitor import RemoveZeroCoeffVisitor
	if iegen.debug: before=str(obj)
	removed_term=RemoveZeroCoeffVisitor().visit(obj).removed_term
	if removed_term and iegen.debug: iegen.print_debug('Simplify: removed zero coefficients: %s -> %s'%(before,obj))
	return removed_term

#Uses the RemoveEmptyConstraintsVisitor to remove any empty constraints from a conjunction
def _remove_empty_constraints(obj):
	from iegen.ast.visitor import RemoveEmptyConstraintsVisitor
	if iegen.debug: before=str(obj)
	removed_constraint=RemoveEmptyConstraintsVisitor().visit(obj).removed_constraint
	if removed_constraint and iegen.debug: iegen.print_debug('Simplify: removed empty constraint: %s -> %s'%(before,obj))
	return removed_constraint

#Uses the RemoveDuplicateFormulasVisitor to remove any duplicated formulas in a Set or Relation
def _remove_duplicate_formulas(obj):
	from iegen.ast.visitor import RemoveDuplicateFormulasVisitor
	if iegen.debug: before=str(obj)
	removed_formula=RemoveDuplicateFormulasVisitor().visit(obj).removed_formula
	if removed_formula and iegen.debug: iegen.print_debug('Simplify: removed duplicate forumla: %s -> %s'%(before,obj))
	return removed_formula

#Uses the RemoveSymbolicsVisitor to remove any duplicated or unused symbolic variables
def _remove_symbolics(obj):
	from iegen.ast.visitor import RemoveSymbolicsVisitor
	if iegen.debug: before=str(obj)
	removed_symbolic=RemoveSymbolicsVisitor().visit(obj).removed_symbolic
	if removed_symbolic and iegen.debug: iegen.print_debug('Simplify: removed symbolic: %s -> %s'%(before,obj))
	return removed_symbolic

#Uses the RemoveDuplicateConstraintsVisitor to remove and duplicate constraints in formulas
def _remove_duplicate_constraints(obj):
	from iegen.ast.visitor import RemoveDuplicateConstraintsVisitor
	if iegen.debug: before=str(obj)
	removed_constraint=RemoveDuplicateConstraintsVisitor().visit(obj).removed_constraint
	if removed_constraint and iegen.debug: iegen.print_debug('Simplify: removed duplicate constraint: %s -> %s'%(before,obj))
	return removed_constraint

#Uses the RemoveTautologiesVisitor to remove any tautologies
def _remove_tautologies(obj):
	from iegen.ast.visitor import RemoveTautologiesVisitor
	if iegen.debug: before=str(obj)
	removed_tautology=RemoveTautologiesVisitor().visit(obj).removed_tautology
	if removed_tautology and iegen.debug: iegen.print_debug('Simplify: removed tautology: %s -> %s'%(before,obj))
	return removed_tautology

#Uses the RemoveContradictionsVisitor to remove any contradictions
def _remove_contradictions(obj):
	from iegen.ast.visitor import RemoveContradictionsVisitor
	if iegen.debug: before=str(obj)
	removed_contradiction=RemoveContradictionsVisitor().visit(obj).removed_contradiction
	if removed_contradiction and iegen.debug: iegen.print_debug('Simplify: removed contradiction: %s -> %s'%(before,obj))
	return removed_contradiction

#Given an object of the following types:
#Set,Relation,PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp
#Applies various simplification rules to reduce the complexity of the object
def simplify(obj):
	from iegen import Set,Relation
	from iegen.ast import PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp
	from iegen.ast.visitor import SortVisitor

	raise_objs_not_like_types(obj,[Set,Relation,PresSet,PresRelation,VarTuple,Conjunction,Equality,Inequality,VarExp,FuncExp,NormExp])

	#Iteratively apply simplification rules until no rules apply

	#Note: Rather than running _remove_free_var_inequality separately from
	#the other simplification routines and convoluting this loop structure,
	#if would be better to use Fourier-Motzkin to project out free variables
	#and keep this loop clean
	#Leaving it this way for now...
	changed_outer=True
	while changed_outer:
		changed_outer=False

		changed=True
		while changed:
			changed=False

			#Merge common terms in NormExps
			changed=_merge_terms(obj) or changed

			#Remove terms in expressions with a coefficient of 0
			changed=_remove_zero_coefficients(obj) or changed

			#Remove empty constraints
			changed=_remove_empty_constraints(obj) or changed

			#Remove redundant and unused symbolic variables
			changed=_remove_symbolics(obj) or changed

			#Remove equalities that contain a free variable
			changed=_remove_free_var_equality(obj) or changed

			#Remove duplicate equivalent formulas
			changed=_remove_duplicate_formulas(obj) or changed

			#Remove duplicate constraints in formulas
			changed=_remove_duplicate_constraints(obj) or changed

			#Remove tautologies
			changed=_remove_tautologies(obj) or changed

			#Remove contradictions
			changed=_remove_contradictions(obj) or changed

			#Apply a sort just to make sure things are ordered properly
			SortVisitor().visit(obj)

			changed_outer=changed or changed_outer

		#The simplification routines called in this loop must be run
		#following all of those that were run above
		changed=True
		while changed:
			changed=False

			#Remove inequalities that contain a free variable
			changed=_remove_free_var_inequality(obj) or changed

			#Apply a sort just to make sure things are ordered properly
			SortVisitor().visit(obj)

			changed_outer=changed or changed_outer
#--------------------------------------------
