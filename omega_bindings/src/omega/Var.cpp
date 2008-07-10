#include <boost/python.hpp>
#include <omega.h>
#include <string>
#include "util.hpp"
#include "Var.hpp"
#include "FVar.hpp"
#include "FStmt.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	//--------------------------------------------------
	//Constructors/Destructor/Operators
	//--------------------------------------------------
	Var::Var(Var_Decl* var):m_var(var){}
	Var::Var():m_var(NULL){}
	Var::Var(Var const& o):m_var(o.m_var){}
	Var::~Var() {}

	Var& Var::operator=(Var const& o)
	{
		this->m_var=o.m_var;
		return *this;
	}
	//--------------------------------------------------

	//Name of this variable
	std::string Var::name() const
	{
		if(NULL!=this->m_var)
			return std::string((const char*)this->m_var->base_name);
		else
			return "{Empty Var}";
	}

	//Python string representation
	std::string Var::str() const
	{
		return this->name();
	}

	//Obtains a pointer to the Var_Decl that this class class wraps
	Var_Decl* Var::var_ptr() const
	{
		return this->m_var;
	}

}}//end namespace omega::bindings
