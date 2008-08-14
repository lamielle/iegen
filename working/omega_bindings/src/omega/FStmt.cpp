#include <string>
#include "FStmt.hpp"
#include "FConj.hpp"
#include "OmegaException.hpp"

namespace omega { namespace bindings {

	FStmt::FStmt(FExpr expr,FStmt_Type type) : m_type(type),m_expr(expr) {}
	FStmt::FStmt() : m_type(EQ),m_expr() {}


	FStmt::FStmt_Type FStmt::type() const {return this->m_type;}
	void FStmt::type(FStmt::FStmt_Type type) {this->m_type=type;}
	FExpr FStmt::expr() const {return this->m_expr;}
	void FStmt::expr(FExpr const& expr) {this->m_expr=expr;}

	//Python string representation
	std::string FStmt::str() const
	{
		std::stringstream s;
		s<<this->expr().str();
		if(EQ==this->type())
			s<<"=0";
		else if(GEQ==this->type())
			s<<">=0";
		else
			throw OmegaException("Stride statements not yet supported.");
		return s.str();
	}

}}//end namespace omega::bindings
