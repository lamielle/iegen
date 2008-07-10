#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresStmt.hpp"
#include "PresStmtLT.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresStmtLT::PresStmtLT(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr) : PresStmt(NodeType::LT,lexpr,rstmt,rexpr) {}

	sptr<PresStmtLT> PresStmtLT::new_(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt) {return sptr<PresStmtLT>(new PresStmtLT(lexpr,rstmt,sptr<PresExpr>()));}

	sptr<PresStmtLT> PresStmtLT::new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) {return sptr<PresStmtLT>(new PresStmtLT(lexpr,sptr<PresStmt>(),rexpr));}

	PresStmtLT::PresStmtLT(PresStmtLT const& o) : PresStmt(o.type(),o.rexpr(),o.rstmt(),o.lexpr()) {}

	PresStmtLT& PresStmtLT::operator=(PresStmtLT const& o)
	{
		this->PresStmt::operator=(o);
		return *this;
	}

	std::string PresStmtLT::str() const {return this->PresStmt::str();}
	std::string PresStmtLT::op() const {return "<";}

	void PresStmtLT::apply(IPresVisitor& v) {v.visitPresStmtLT(*this);}

	std::string PresStmtLT::name() const {return "PresStmtLT";}

}}}}//end namespace omega::bindings::parser::ast
