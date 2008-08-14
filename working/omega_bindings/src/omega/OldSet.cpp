#include <boost/python.hpp>
#include <boost/python/detail/api_placeholder.hpp>
#include <omega.h>
#include <code_gen/code_gen.h>
#include <string>
#include "OldSet.hpp"
#include "OldRelation.hpp"
#include "TupleCollection.hpp"
#include "OmegaException.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	OldSet::OldSet(int arity):TupleCollection(arity) {}
	OldSet::OldSet(OldSet const& s):TupleCollection(s) {}
	OldSet::OldSet(OldSet const& s,omega::Relation const& r):TupleCollection(s,r) {}

	OldSet::OldSet(std::string name):TupleCollection(1)
	{
		this->name(1,name);
	}

	OldSet::OldSet(python::tuple const& names):TupleCollection(python::len(names))
	{
		this->name(names);
	}

	//Assignment operator
	OldSet& OldSet::operator=(OldSet const& s)
	{
		TupleCollection *thisp;
		TupleCollection const* sp;

		//Get pointers to the objects as TupleCollections
		thisp=this;
		sp=&s;

		//Use TupleCollection::operator= to do the assignment
		*thisp=*sp;
		return *this;
	}

	//Arity of the tuples in the set
	int OldSet::arity() const
	{
		return this->m_r.n_set();
	}

	//Name the set variable at position i
	void OldSet::name(int i,std::string const& name)
	{
		this->TupleCollection::name(i,this->m_r.n_set(),name,&omega::Relation::name_set_var,&omega::Relation::set_var);
	}

	//Name the first len(names) set variables
	void OldSet::name(python::tuple const& names)
	{
		this->TupleCollection::name(names,this->m_r.n_set(),&omega::Relation::name_set_var,&omega::Relation::set_var);
	}

	//Gets the name of the variable at position i
	std::string OldSet::name(int i)
	{
		return this->TupleCollection::name(i,this->arity(),&omega::Relation::set_var);
	}

	//Gets a tuple of the variable names for this set
	python::tuple OldSet::names()
	{
		return this->TupleCollection::names(this->arity(),&omega::Relation::set_var);
	}

	//Applies the given relation to this set
	//The input arity of the given relation must match the arity of this set
	void OldSet::apply(OldRelation const& r)
	{
		//Make sure the arities are correct
		if(this->arity()!=r.arity_in())
			throw OmegaException("Cannot apply the relation to the set: Set arity does not match the input arity of the relation.");

		//Make a copy of the given relation
		OldRelation rcopy(r);

		//Apply the composition rcopy(this)
		omega::Relation new_set=Composition(rcopy.m_r,omega::copy(this->m_r));

		//Create a new set from the result and assign it to *this
		*this=OldSet(*this,new_set);
	}

	void OldSet::get_vars()
	{
		TupleCollection::vars(TupleCollection::VARS_GET,this->arity(),&omega::Relation::set_var);
	}
	void OldSet::clear_vars(python::object type,python::object value,python::object traceback)
	{
		TupleCollection::vars(TupleCollection::VARS_CLEAR,this->arity(),&omega::Relation::set_var);
	}

	//Python iterator support
	//Returns a generator object based on the python code produced by Omega
	PyObject* OldSet::iter()
	{
		PyObject *generator;

		//Run python code to define the generator function iterating over the tuples in this relation
		//The code is obtained from this->code()
		PyRun_String((std::string("def generate():\n")+
		             this->code()).c_str(),
		             Py_file_input,PyEval_GetGlobals(),PyEval_GetLocals());

		//Create a new generator object from the previous definition
		PyRun_String("generator=generate()",Py_file_input,PyEval_GetGlobals(),PyEval_GetLocals());

		//Obtain the created generator object
		generator=PyDict_GetItemString(PyEval_GetLocals(),"generator");

		//Make sure to increment the reference count of the generator
		Py_INCREF(generator);

		//Remove the variable and the generator function from the names dictionary
		PyRun_String("del generator",Py_file_input,PyEval_GetGlobals(),PyEval_GetLocals());
		PyRun_String("del generate",Py_file_input,PyEval_GetGlobals(),PyEval_GetLocals());

		//Return the generator
		return generator;
	}

	//Generates python code to iterate over the tuples in this set
	std::string OldSet::code()
	{
		Tuple<omega::Relation> transformations,original_IS;

		//Known relation, using Relation::True (Nothing is known)
		omega::Relation known=omega::Relation::True(this->arity());

		//Create and use a trivial transformation for this set
		transformations.append(omega::bindings::OldRelation(*this).m_r);

		//The iteration space is this set itself
		original_IS.append(this->m_r);

		//Return the std::string version of the result of MMGeneratePythonCode
		return std::string((const char*)MMGeneratePythonCode(transformations,original_IS,known));
	}

}}//end namespace omega::bindings
