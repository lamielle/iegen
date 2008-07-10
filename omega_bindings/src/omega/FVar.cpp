#include <string>
#include <boost/shared_ptr.hpp>
#include "util.hpp"
#include "FVar.hpp"
#include "Var.hpp"
#include "FStmt.hpp"
#include "OmegaException.hpp"

namespace omega { namespace bindings {

	//--------------------------------------------------
	//Constructors/Destructors/Operators
	//--------------------------------------------------
	FVar::FVar() : m_coeff(1),m_v() {}
	FVar::FVar(Var const& v) : m_coeff(1),m_v(new Var(v)) {}
	FVar::FVar(int coeff,Var const& v) : m_coeff(coeff),m_v(new Var(v)) {}
	FVar::FVar(int coeff,FVar const& o) : m_coeff(coeff*o.coeff()),m_v(o.m_v) {}

	FVar::FVar(FVar const& o) : m_coeff(o.coeff()),m_v(o.m_v) {}

	FVar::~FVar() {}

	FVar& FVar::operator=(FVar const& o)
	{
		this->m_coeff=o.coeff();
		this->m_v=o.m_v;
		return *this;
	}

	int FVar::coeff() const {return this->m_coeff;}
	Var_Decl* FVar::var() const {return this->m_v->var_ptr();}
	void FVar::coeff(int coeff) {this->m_coeff=coeff;}
	
	std::string FVar::name() const
	{
		return this->m_v->name();
	}

	//Python string representation
	std::string FVar::str() const
	{
		std::stringstream s;
		if(this->coeff())
		{
			if(1!=this->coeff())
				s<<this->coeff()<<"*";
			s<<this->m_v->str();
		}
		else
			s<<"0";
		return s.str();
	}

}}//end namespace omega::bindings
