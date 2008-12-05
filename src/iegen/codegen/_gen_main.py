def gen_main(mapir):
	from iegen.codegen import Function

	#Create the main function
	main=Function('main','int',[])
#
#	#Add a declaration of the symbolic variables
#	main.body.append(Comment('Declare the symbolics'))
#	main.body.extend(gen_symbolics_decl(mapir))
#	main.newline()
#
#	#Add declarations for the non-index array data spaces
#	main.body.append(Comment('Declare the data spaces'))
#	data_array_vars=VarDecl('double');
#	for data_array in mapir.get_data_arrays():
#		data_array_vars.var_names.append('*'+data_array.name)
#		data_array_vars.values.append('NULL');
#	main.body.append(data_array_vars);
#	main.newline()
#
#	#Add declarations of the index arrays
#	main.body.append(Comment('Declare the index arrays'))
#	index_array_vars=VarDecl('int')
#	for index_array in mapir.get_index_arrays():
#		index_array_vars.var_names.append('*'+index_array.name)
#		index_array_vars.values.append('NULL')
#	main.body.append(index_array_vars)
#	main.newline()
#
#	#Add declarations of sigma and delta
#	main.body.append(Comment('Declare pointers for sigma and delta'))
#	er_vars=VarDecl('ExplicitRelation')
#	er_vars.var_names.append('*sigma')
#	er_vars.values.append('NULL')
#	er_vars.var_names.append('*delta')
#	er_vars.values.append('NULL')
#	main.body.append(er_vars)
#	main.newline()
#
#	#Allocate memory for the data spaces
#	main.body.append(Comment('Allocate memory for the data spaces'))
#	for data_array in mapir.get_data_arrays():
#		main.body.append(Statement('%s=(double*)malloc(sizeof(double)*10);'%data_array.name))
#	main.newline()
#
#	#Allocate memory for the index arrays
#	main.body.append(Comment('Allocate memory for the index arrays'))
#	for index_array in mapir.get_index_arrays():
#		main.body.append(Statement('%s=(int*)malloc(sizeof(int)*10);'%(index_array.name)))
#	main.newline()
#
#	#Set index arrays to be 'identity' index arrays
#	main.body.append(Comment("Set index arrays to be 'identity' index arrays"))
#	for index_array in mapir.get_index_arrays():
#		main.body.append(Statement('for(int i=0;i<10;i++) %s[i]=i;'%(index_array.name)))
#	main.newline()
#
#	#Call the inspector
#	main.body.append(Comment('Call the inspector'))
#	main.body.append(Statement('inspector(%s);'%(calc_ie_arg_names_string(mapir))))
#	main.newline()
#
#	#Call the executor
#	main.body.append(Comment('Call the executor'))
#	main.body.append(Statement('executor(%s);'%(calc_ie_arg_names_string(mapir))))
#	main.newline()
#
#	#Debug printing of the data spaces
#	main.body.append(Comment('Debug printing of the data arrays'))
#	main.body.append(Statement('for(int i=0;i<10;i++)'))
#	main.body.append(Statement('{'))
#	main.body.append(Statement('  printf("inter1[%d]=%d\\n",i,inter1[1]);'))
#	main.body.append(Statement('  printf("inter2[%d]=%d\\n",i,inter1[1]);'))
#	main.body.append(Statement('  printf("x[%d]=%d\\n",i,inter1[1]);'))
#	main.body.append(Statement('  printf("fx[%d]=%d\\n",i,inter1[1]);'))
#
#	main.body.append(Statement('}'))
#	main.body.append(Statement(''))
#
#	#Free the data space memory
#	main.body.append(Comment('Free the data space memory'))
#	for data_array in mapir.get_data_arrays():
#		main.body.append(Statement('free(%s);'%data_array.name))
#	main.newline()
#
#	#Free the data space memory
#	main.body.append(Comment('Free the index array memory'))
#	for index_array in mapir.get_index_arrays():
#		main.body.append(Statement('free(%s);'%index_array.name))
#	main.newline()
#
#	main.body.append(Statement('return 0;'))
#
	return main
