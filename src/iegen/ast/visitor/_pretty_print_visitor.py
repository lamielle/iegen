from iegen.ast.visitor import DFVisitor
from iegen.ast import VarExp
from cStringIO import StringIO


# This visitor will print the relation being visited to stdout.
# All vars set to constants will show up as constants in the
# tuples, the equalities involving vars set to constants will
# be removed, all vars will have the shortest possible names
# that still maintain uniqueness, any equalities between vars
# will be removed, and vars that are equal will all be mapped
# to the same name.
#
# Limitations
#	-Doesn't work for sets yet.
#	-Should only have horizontal bar if have symbolics.
#	-The same inequality may show up multiple times due to 
#	equal vars being mapped to same string.
#

class PrettyPrintVisitor(DFVisitor):
	__slots__=('helper','var2string')

	def __init__(self):
		self.var2string = {}
		self.pretty = StringIO()
		

	def visitRelation(self,node):
		first_time = True
		for relation in node.relations:
			# for all conjuncts but first, we need union connective
			if not first_time:
				self.pretty.write('\nunion ')
			else:
				first_time = False
	
			relation.apply_visitor(self)
		print self.pretty.getvalue()

	def visitPresRelation(self,node):
		# have the helper visit the whole relation
		# it will create a mapping of vars to new strings
		self.helper = PrettyPrintHelper()
		self.helper.visit(node)
		self.var2string = self.helper.getVarMap()
		self.no_print_set = self.helper.getNoPrintSet()
		
		self.pretty.write('{ ')
		node.tuple_in.apply_visitor(self)
		self.pretty.write(' -> ')
		node.tuple_out.apply_visitor(self)
		self.pretty.write(' : ')
		node.conjunct.apply_visitor(self)
		self.pretty.write(' | ')
		for symbolic in node.symbolics:
			self.pretty.write(symbolic)
		self.outPresRelation(node)
		self.pretty.write(' }')

	def visitVarTuple(self,node):
		self.pretty.write('[')
		first_time = True
		for var in node.vars:
			if not first_time:
				self.pretty.write(',')
			else:
				first_time = False
			var.apply_visitor(self)
		self.pretty.write(']')

	def visitConjunction(self,node):
		first_time = True
		for constraint in node.constraints:
			if constraint not in self.no_print_set:
				if not first_time:
					self.pretty.write(' and ')
				else:
					first_time = False
				constraint.apply_visitor(self)

	def visitInequality(self,node):
		node.exp.apply_visitor(self)
		self.pretty.write('>=0')

	def visitEquality(self,node):
		if node not in self.no_print_set:
			node.exp.apply_visitor(self)
			self.pretty.write('=0')
		

	def inVarExp(self,node):
		if node.coeff==1:
			self.pretty.write(self.var2string[node.id])
		else:
			self.pretty.write('%s%s' % (node.coeff,self.var2string[node.id]))


	def visitFuncExp(self,node):
		if node.coeff==1:
			self.pretty.write('%s('%(node.name))
		else:
			self.pretty.write('%s%s('%(node.coeff,node.name))
		first_time = True
		for exp in node.args:
			if not first_time:
				self.pretty.write(',')
			else:
				first_time = False			
			exp.apply_visitor(self)			
		self.pretty.write(')')
			

	def visitNormExp(self,node):
		first_time = True
		for term in node.terms:
			if not first_time:
				self.pretty.write('+')
			else:
				first_time = False
			term.apply_visitor(self)
		if node.const!=0:
			self.pretty.write('+%s'%(node.const))
		

# Creates a mapping of variable names to shorter variable names
# and creates a set of equality constraints that don't need printed.
# When a variable is equal to a constant, then that equality
# is put in the no print set and the variable will be mapped to
# that constant.
# When variables are equal to each other in the constraints,
# that constraint is put in the no print set and the variables are
# mapped to the same name.
class PrettyPrintHelper(DFVisitor):
	__slots__=('var2string', 'new_name_set', 'inside_equality', 'no_print_set', 'no_print')
	
	def __init__(self):
		self.var2string = {}
		self.new_name_set = set()
		self.inside_equality = False
		self.no_print_set = set()
		self.no_print = False
		self.func_depth = 0
		self.in_var_tuple = False
	
	def getVarMap(self):
		return self.var2string
		
	def getNoPrintSet(self):
		return self.no_print_set
		
	def inVarTuple(self,node):
		self.in_var_tuple = True
	def outVarTuple(self,node):
		self.in_var_tuple = False
	

	def inVarExp(self,node):
		# look var up in dictionary
		# if not already there 
		if self.in_var_tuple and not self.var2string.has_key(node.id):
			legal = False
			count = 1
			while (not legal and count<=len(node.id)):
				# then come up with candidate shorter name
				new_name = node.id[0:count]
				# check if shorter name is in new name set
				if new_name not in self.new_name_set:
					legal = True
				else:
					count = count + 1
					
			# if still have name conflict then append underscores
			# to var until no conflict occurs
			if not legal:
				while not legal:
					new_name = new_name + '_'
					if new_name not in self.new_name_set:
						legal = True
					
			# map var to a shorter name
			self.new_name_set.add(new_name)
			self.var2string[node.id] = new_name

		# for other non tuple var uses check that the var has mapping
		if not self.var2string.has_key(node.id):
			print "#### id not legal, existentially quantified var"
			print "node.id = ", node.id
			print "new_name_set = ", self.new_name_set
			assert 0

		
	def outVarExp(self,node):
		self.defaultOut(node)


	def inEquality(self,node):
		# entering equality
		self.inside_equality = True
		
	def outEquality(self,node):
		self.inside_equality = False
		if self.no_print:
			self.no_print = False
			self.no_print_set.add(node)

	# We have to keep track of the function depth so that we
	# don't "find" equalities in NormExp that are embedded
	# in FuncExp.
	def inFuncExp(self,node):
		self.func_depth += 1
	
	def outFuncExp(self,node):
		self.func_depth -= 1
	
	def inNormExp(self,node):
		# if inside an equality
		if self.inside_equality and self.func_depth==0:
			# if only one VarExp, then we could have a var equal to a constant
			if len(node.terms)==1 and isinstance(node.terms[0],VarExp):
				if node.terms[0].coeff == -1:
					# map var name to string for constant
					self.var2string[node.terms[0].id] = "%d" % (node.const)
					self.no_print = True
					
				if node.terms[0].coeff == 1:
					# map var name to string for negative of constant
					self.var2string[node.terms[0].id] = "%d" % (-node.const)
					self.no_print = True
					
			# if only two VarExpr and one has -1 coeff and the other 1 coeff
			if (len(node.terms)==2 and node.const==0
				and isinstance(node.terms[0], VarExp) 
				and isinstance(node.terms[1], VarExp)
				and (  (node.terms[0].coeff==-1 
						and node.terms[1].coeff==1)
					or (node.terms[0].coeff==1 
						and node.terms[1].coeff==-1)
					)
				):
					# set one of the variables pretty string to the 
					# other guy's
					self.var2string[node.terms[0].id] = \
						self.var2string[node.terms[1].id]
					self.no_print = True

