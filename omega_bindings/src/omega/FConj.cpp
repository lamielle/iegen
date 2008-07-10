#include <string>
#include <vector>
#include <iterator>
#include "FConj.hpp"
#include "FStmt.hpp"

namespace omega { namespace bindings {

	FConj::FConj() : m_type(And),m_stmts(),m_conjs() {}
	FConj::FConj(FConj_Type type) : m_type(type),m_stmts(),m_conjs() {}
	FConj::FConj(FConj_Type type,FStmt const& stmt) : m_type(type),m_stmts(),m_conjs()
	{
		this->add_stmt(stmt);
	}

	FConj::FConj(FConj_Type type,FStmt const& stmt1,FStmt const& stmt2) : m_type(type),m_stmts(),m_conjs()
	{
		this->add_stmt(stmt1);
		this->add_stmt(stmt2);
	}

	FConj::FConj(FConj_Type type,FConj const& conj,FStmt const& stmt) : m_type(type),m_stmts(),m_conjs()
	{
		this->add_conj(conj);
		this->add_stmt(stmt);
	}

	FConj::FConj(FConj_Type type,FConj const& conj1,FConj const& conj2) : m_type(type),m_stmts(),m_conjs()
	{
		this->add_conj(conj1);
		this->add_conj(conj2);
	}

	FConj::FConj(FConj const& o) : m_type(o.type()),m_stmts(o.m_stmts),m_conjs(o.m_conjs) {}

	FConj& FConj::operator=(FConj const& o)
	{
		this->type(o.type());
		this->stmts(o.stmts());
		this->conjs(o.conjs());
		return *this;
	}

	//Python string representation
	std::string FConj::str() const
	{
		std::string conj;
		std::stringstream s;
		if(Not==this->type())
		{
			s<<"NOT ( ";
			s<<this->get_all_parts()[0]->str();
			s<<" )";
		}
		else
		{
			if(And==this->type())conj=" AND ";
			else conj=" OR ";
			std::vector<FPart const*> parts=this->get_all_parts();
			s<<"( ";
			std::vector<FPart const*>::iterator i=parts.begin();
			while(i!=parts.end())
			{
				s<<(*i)->str();
				i++;
				if(i!=parts.end())
					s<<conj;
			}
			s<<" )";
		}
		return s.str();
	}

	FConj::FConj_Type FConj::type() const {return this->m_type;}
	void FConj::type(FConj::FConj_Type type) {this->m_type=type;}
	std::vector<FStmt> FConj::stmts() const {return this->m_stmts;}
	void FConj::stmts(std::vector<FStmt> stmts) {this->m_stmts=stmts;}
	std::vector<FConj> FConj::conjs() const {return this->m_conjs;}
	void FConj::conjs(std::vector<FConj> conjs) {this->m_conjs=conjs;}

	//Collects all FStmts and FConjs and returns them in a single collection
	std::vector<FPart const*> const FConj::get_all_parts() const
	{
		std::vector<FPart const*> parts;
		for(std::vector<FStmt>::const_iterator i=this->m_stmts.begin(); i!=this->m_stmts.end(); i++)
			parts.push_back(&(*i));
		for(std::vector<FConj>::const_iterator i=this->m_conjs.begin(); i!=this->m_conjs.end(); i++)
			parts.push_back(&(*i));
		return parts;
	}

	void FConj::add_stmt(FStmt const& stmt)
	{
		this->m_stmts.push_back(stmt);
	}

	void FConj::add_conj(FConj const& conj)
	{
		this->m_conjs.push_back(conj);
	}

}}//end namespace omega::bindings
