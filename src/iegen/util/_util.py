#Defines a property called m_name
#This property is assigned to the given class
#The getter and setter access a member of the class called _'name'
def define_properties(class_name,names):
	for each name in names:
		#Define the getter and setter methods themselves
		exec '''
	def _get(self): return self._%s
	def _set(self,value): self._%s=value'''%(name,name)

		#Create a property from these methods and assign it to the class
		exec '''%s.m_%s=property(_get,_set)'''%(class_name,name)

class DimensionalityError(Exception):
	pass
