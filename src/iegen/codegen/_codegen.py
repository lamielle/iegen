#---------- Public interface to iegen.codegen module ----------
def codegen(mapir,code):
	from iegen.codegen import do_calc,do_ito,do_gen
	from iegen.codegen.visitor import CPrintVisitor

	#---------- Calculation Phase ----------
	do_calc(mapir)
	#---------------------------------------

	#---------- ITO Phase ----------
	do_ito(mapir)
	#-------------------------------

	#---------- Code Generation Phase ----------
	program=do_gen(mapir)
	#-------------------------------------------

	#Pretty print the generated program structure
	CPrintVisitor(code,'  ').visit(program)
#--------------------------------------------------------------

def gen_tuple_vars_decl(set):
	from iegen.codegen import VarDecl

	var_decl=VarDecl('int')
	for set in set.sets:
		for var in set.tuple_set.vars:
			var_decl.var_names.append(var.id)
	return [var_decl]
