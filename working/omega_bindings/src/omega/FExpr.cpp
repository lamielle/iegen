#include <boost/python.hpp>
#include <string>
#include <vector>
#include <iterator>
#include "util.hpp"
#include "FExpr.hpp"
#include "FVar.hpp"
#include "Var.hpp"
#include "FStmt.hpp"
#include "OmegaException.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	FExpr::FExpr() : m_const(0),m_vars() {}
	FExpr::FExpr(int constant) : m_const(constant),m_vars() {}
	FExpr::FExpr(Var const& var) : m_const(0),m_vars(1,FVar(var)) {}
	FExpr::FExpr(FVar const& var) : m_const(0),m_vars(1,var) {}
	FExpr::FExpr(Var const& var,int constant) : m_const(constant),m_vars(1,FVar(var)) {}
	FExpr::FExpr(FVar const& var,int constant) : m_const(constant),m_vars(1,var) {}

	FExpr::FExpr(Var const& var1,Var const& var2) : m_const(0),m_vars()
	{
		this->add_var(FVar(var1));
		this->add_var(FVar(var2));
	}

	FExpr::FExpr(FVar const& var1,Var const& var2) : m_const(0),m_vars()
	{
		this->add_var(var1);
		this->add_var(FVar(var2));
	}

	FExpr::FExpr(FVar const& var1,FVar const& var2) : m_const(0),m_vars()
	{
		this->add_var(var1);
		this->add_var(var2);
	}

	FExpr::FExpr(FExpr const& e) : m_const(e.constant()),m_vars(e.m_vars) {}
	FExpr::FExpr(FExpr const& e,int constant,FExpr_CopyOp op) : m_const(e.constant()),m_vars(e.m_vars)
	{
		switch(op)
		{
			case(Add):
				this->constant(this->constant()+constant);
				break;
			case(Multiply):
				this->constant(this->constant()*constant);
				for(unsigned i=0;i<this->vars().size();i++)
					this->m_vars[i]=FVar(constant,this->m_vars[i]);
				break;
		}
	}
	FExpr::FExpr(FExpr const& e,FVar const& var) : m_const(e.constant()),m_vars(e.m_vars)
	{
		this->add_var(var);
	}
	FExpr::FExpr(FExpr const& e1,FExpr const& e2) : m_const(e1.constant()),m_vars(e1.m_vars)
	{
		this->add_vars(e2.vars());
		this->constant(this->constant()+e2.constant());
	}
	
	int FExpr::constant() const {return this->m_const;}
	void FExpr::constant(int constant) {this->m_const=constant;}
	std::vector<FVar> FExpr::vars() const {return this->m_vars;}
	python::tuple FExpr::vars_tuple() const
	{
		python::list l=python::list();
		for(std::vector<FVar>::const_iterator i=this->m_vars.begin(); i!=this->m_vars.end(); i++)
			l.append(*i);
		return python::tuple(l);
	}

	void FExpr::vars(std::vector<FVar> const& vars) {this->m_vars=vars;}
	
	//Python string representation
	std::string FExpr::str() const
	{
		std::stringstream s;
		std::vector<FVar>::const_iterator i=this->m_vars.begin();
		while(i!=this->m_vars.end())
		{
			s<<(*i).str();
			i++;
			if(i!=this->m_vars.end())
				s<<"+";
		}
		if(this->m_const)
			s<<"+"<<this->m_const;
		return s.str();
	}

	void FExpr::add_var(FVar const& v)
	{
		this->m_vars.push_back(v);
	}

	void FExpr::add_vars(std::vector<FVar> const& vars)
	{
		this->m_vars.insert(this->m_vars.end(),vars.begin(),vars.end());
	}

}}//end namespace omega::bindings
