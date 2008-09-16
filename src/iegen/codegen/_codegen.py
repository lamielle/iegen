#Given a collection of Statement objects, calculates the combined iteration space of all statements
def full_iter_space(statements):
	#Get the iteration space of the first statement
	statement=statements[0]
	full_iter=statement.iter_space.apply(statement.scatter)

	#Now union this with the rest of the statement's iteration spaces
	for statement in statements[1:]:
		full_iter=full_iter.union(statement.iter_space.apply(statement.scatter))

	return full_iter

def calc_artt(mapir,data_permute):
	from iegen import AccessRelation
	#Iteration Sub Space Relation
	issr=data_permute.iter_sub_space_relation

	#Calculate the iteration space to data space relation
	iter_to_data=None
	for stmt in mapir.statements:
		if not iter_to_data:
			iter_to_data=issr.compose(stmt.scatter.compose(stmt.access_relations[0].iter_to_data.inverse())).inverse()
		else:
			iter_to_data=iter_to_data.union(issr.compose(stmt.scatter.compose(stmt.access_relations[0].iter_to_data.inverse())).inverse())

		for ar in stmt.access_relations[1:]:
			iter_to_data=iter_to_data.union(issr.compose(stmt.scatter.compose(ar.iter_to_data.inverse())).inverse())

	print mapir.full_iter_space
	print data_permute.iter_sub_space_relation
	print iter_to_data

	artt=AccessRelation(
              name='A_I_sub_to_%s'%(data_permute.target_data_space.name),
              iter_space=mapir.full_iter_space.apply(data_permute.iter_sub_space_relation),
              data_space=data_permute.target_data_space,
              iter_to_data=iter_to_data)
	return artt

#---------- Public Interface Function ----------
def codegen(mapir,data_permute,iter_permute,code):
	#Step 0) Calculate the full iteration space based on the iteration spaces of the statements
	mapir.full_iter_space=full_iter_space(mapir.statements)

	#Put the full iteration space in the iter permute rtrt
#	iter_permute.iter_space=mapir.full_iter_space

	print 'Full iteration space for all statements: %s'%mapir.full_iter_space

	#Step 1a) generate an AccessRelation specification that will be the input for data reordering
	mapir.artt=calc_artt(mapir,data_permute)
#-----------------------------------------------
