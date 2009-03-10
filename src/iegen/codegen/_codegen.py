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
