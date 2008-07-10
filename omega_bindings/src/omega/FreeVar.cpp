#include <boost/python.hpp>
#include <omega.h>
#include <string>
#include "FreeVar.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	//--------------------------------------------------
	//Constructors/Destructors/Operators
	//--------------------------------------------------
	FreeVar::FreeVar(std::string const& name) : m_fvar(new Free_Var_Decl(Const_String(name.c_str()))) {}

	FreeVar::FreeVar(std::string const& name,int arity) : m_fvar(new Free_Var_Decl(Const_String(name.c_str()),arity)) {}

	FreeVar::FreeVar(FreeVar const& o) : m_fvar(o.m_fvar) {}

	FreeVar::FreeVar() {}

	FreeVar::~FreeVar() {}

	FreeVar& FreeVar::operator=(FreeVar const& o)
	{
		this->m_fvar=o.m_fvar;
		return *this;
	}
	//--------------------------------------------------

	//Python string representation
	std::string FreeVar::str() const
	{
		std::stringstream s;
		s<<"(";
		s<<std::string((const char*)this->m_fvar->base_name());
		s<<",";
		s<<this->m_fvar->arity();
		s<<")";
		return s.str();
	}

	//Get the pointer to the Free_Var_Decl that this FreeVar warps
	Free_Var_Decl* FreeVar::fvar_ptr()
	{
		return this->m_fvar.get();
	}

}}//end namespace omega::bindings
