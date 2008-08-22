#Runs all of the IEGen tests
def run_tests():
	import iegen,nose
	nose.run(argv=['','-v','-s','-w%s'%iegen.dir])

#Given a MapIR object, calculates the combined iteration space of all statements
def full_iter_space(statements):
	#Get the iteration space of the first statement
	statement=statements[0]
	full_iter=statement.scatter.compose(statement.iter_space)

	#Now union this with the rest of the statement's iteration spaces
	for statement in statements[1:]:
		full_iter=full_iter.union(statement.scatter.compose(statement.iter_space))

	return full_iter

#Defines a property called m_name
#This property is assigned to the given class
#The getter and setter access a member of the class called _'name'
def define_properties(add_to_class,names):
	for name in names:
		#Define the getter and setter methods themselves
		exec '''
def _get(self): return self._%s
def _set(self,value): self._%s=value'''%(name,name)

		#Create a property from these methods and assign it to the class
		exec '''add_to_class.m_%s=property(_get,_set)'''%(name,)

class DimensionalityError(Exception):
	pass
