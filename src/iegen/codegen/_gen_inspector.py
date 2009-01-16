#Generates code for the inspector
def gen_inspector(mapir):
	from iegen.codegen import Function
	from iegen.idg.visitor import ParamVisitor,DeclVisitor,CodegenVisitor

	#Create the inspector function with the necessary parameters
	inspector=Function('inspector','void',ParamVisitor().visit(mapir.idg).params)

	#Add the necessary variable declarations
	inspector.body.extend(DeclVisitor().visit(mapir.idg).decls)

	#Add the code for the body of the inspector
	inspector.body.extend(CodegenVisitor().visit(mapir.idg).stmts)

#	#Create the declare/create the index array wrappers
#	inspector.body.extend(gen_declare_index_array_wrappers(mapir))
#	inspector.newline()
#	inspector.body.extend(gen_create_index_array_wrappers(mapir))
#	inspector.newline()
#
#	#Create a sigma_ER variable
#	inspector.body.extend(gen_declare_sigma_er())
#	inspector.newline()
#
#	#Step 1a) generate code that creates an explicit representation of the access relation artt at runtime
#	inspector.body.extend(gen_create_artt(mapir))
#	inspector.newline()
#
#	#Step 1b) Generate code that passes explicit relation to ERG
#	inspector.body.extend(gen_create_sigma(mapir))
#	inspector.newline()
#
#	#Step 1c) Generate code that does data reordering
#	inspector.body.extend(gen_reorder_data(mapir,data_reordering))
#	inspector.newline()
#
#	#Destroy the index array wrappers
#	inspector.body.extend(gen_destroy_index_array_wrappers(mapir))

	return inspector
