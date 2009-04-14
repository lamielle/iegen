import iegen
from iegen.simplify import register_rule

#---------- Formula Simplification Rules ----------
#Simplification rule 1:
#Remove an equality constraint of the form:
#free_var=exp
#and replace all uses of 'free_var' in the remaining
#constraints with 'exp'
#
#Assumes 'formula' is a Set or Relation
#
#Returns True if any changes were made, False otherwise
def remove_free_var_equality(formula):
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
def remove_free_var_inequality(formula):
	from iegen.ast.visitor import RemoveFreeVarConstraintVisitor
	from iegen.ast import Inequality
	if iegen.debug: before=str(formula)
	changed=RemoveFreeVarConstraintVisitor(Inequality).visit(formula).changed
	if changed and iegen.debug: iegen.print_debug('Simplify: removed free variable inequality: %s -> %s'%(before,formula))
	return changed

#Uses the MergeExpTermsVisitor to combine common terms in NormExps
def merge_terms(obj):
	from iegen.ast.visitor import MergeExpTermsVisitor
	if iegen.debug: before=str(obj)
	merged_terms=MergeExpTermsVisitor().visit(obj).merged_terms
	if merged_terms and iegen.debug: iegen.print_debug('Simplify: merged terms: %s -> %s'%(before,obj))
	return merged_terms

#Uses the RemoveZeroCoeffVisitor to remove any terms in NormExps with a coefficient of 0
def remove_zero_coefficients(obj):
	from iegen.ast.visitor import RemoveZeroCoeffVisitor
	if iegen.debug: before=str(obj)
	removed_term=RemoveZeroCoeffVisitor().visit(obj).removed_term
	if removed_term and iegen.debug: iegen.print_debug('Simplify: removed zero coefficients: %s -> %s'%(before,obj))
	return removed_term

#Uses the RemoveEmptyConstraintsVisitor to remove any empty constraints from a conjunction
def remove_empty_constraints(obj):
	from iegen.ast.visitor import RemoveEmptyConstraintsVisitor
	if iegen.debug: before=str(obj)
	removed_constraint=RemoveEmptyConstraintsVisitor().visit(obj).removed_constraint
	if removed_constraint and iegen.debug: iegen.print_debug('Simplify: removed empty constraint: %s -> %s'%(before,obj))
	return removed_constraint

#Uses the RemoveDuplicateFormulasVisitor to remove any duplicated formulas in a Set or Relation
def remove_duplicate_formulas(obj):
	from iegen.ast.visitor import RemoveDuplicateFormulasVisitor
	if iegen.debug: before=str(obj)
	removed_formula=RemoveDuplicateFormulasVisitor().visit(obj).removed_formula
	if removed_formula and iegen.debug: iegen.print_debug('Simplify: removed duplicate forumla: %s -> %s'%(before,obj))
	return removed_formula

#Uses the RemoveSymbolicsVisitor to remove any duplicated or unused symbolic variables
def remove_symbolics(obj):
	from iegen.ast.visitor import RemoveSymbolicsVisitor
	if iegen.debug: before=str(obj)
	removed_symbolic=RemoveSymbolicsVisitor().visit(obj).removed_symbolic
	if removed_symbolic and iegen.debug: iegen.print_debug('Simplify: removed symbolic: %s -> %s'%(before,obj))
	return removed_symbolic

#Uses the RemoveDuplicateConstraintsVisitor to remove and duplicate constraints in formulas
def remove_duplicate_constraints(obj):
	from iegen.ast.visitor import RemoveDuplicateConstraintsVisitor
	if iegen.debug: before=str(obj)
	removed_constraint=RemoveDuplicateConstraintsVisitor().visit(obj).removed_constraint
	if removed_constraint and iegen.debug: iegen.print_debug('Simplify: removed duplicate constraint: %s -> %s'%(before,obj))
	return removed_constraint

#Uses the RemoveTautologiesVisitor to remove any tautologies
def remove_tautologies(obj):
	from iegen.ast.visitor import RemoveTautologiesVisitor
	if iegen.debug: before=str(obj)
	removed_tautology=RemoveTautologiesVisitor().visit(obj).removed_tautology
	if removed_tautology and iegen.debug: iegen.print_debug('Simplify: removed tautology: %s -> %s'%(before,obj))
	return removed_tautology

#Uses the RemoveContradictionsVisitor to remove any contradictions
def remove_contradictions(obj):
	from iegen.ast.visitor import RemoveContradictionsVisitor
	if iegen.debug: before=str(obj)
	removed_contradiction=RemoveContradictionsVisitor().visit(obj).removed_contradiction
	if removed_contradiction and iegen.debug: iegen.print_debug('Simplify: removed contradiction: %s -> %s'%(before,obj))
	return removed_contradiction

#---------- Inverse Simplification Rule ----------
#Runs the inverse simplification visitor on the given object
def inverse_simplify(obj):
	from iegen.ast.visitor import RemoveFreeVarFunctionVisitor
	from iegen import Set,Relation,PresSet,PresRelation
	from iegen.util import like_type

	if iegen.debug: before=str(obj)

	#Only apply this rule to Sets, Relations, PresSets, and PresRelations
	if like_type(obj,Set) or like_type(obj,Relation) or like_type(obj,PresSet) or like_type(obj,PresRelation):
		changed=RemoveFreeVarFunctionVisitor(iegen.simplify.inverse_pairs(),'_inv').visit(obj).changed
	else:
		changed=False
	if changed and iegen.debug: iegen.print_debug('Simplify: removed free variable function: %s -> %s'%(before,obj))

	return changed
#-------------------------------------------------
#--------------------------------------------------

#---------- Rule Registration ----------
register_rule(merge_terms,rule_group=0)
register_rule(remove_zero_coefficients,rule_group=0)
register_rule(remove_empty_constraints,rule_group=0)
register_rule(remove_symbolics,rule_group=0)
register_rule(remove_free_var_equality,rule_group=0)
register_rule(remove_duplicate_formulas,rule_group=0)
register_rule(remove_duplicate_constraints,rule_group=0)
register_rule(remove_tautologies,rule_group=0)
register_rule(remove_contradictions,rule_group=0)
register_rule(remove_free_var_equality,rule_group=0)
register_rule(remove_free_var_inequality,rule_group=1)
register_rule(inverse_simplify,rule_group=2)
#---------------------------------------
