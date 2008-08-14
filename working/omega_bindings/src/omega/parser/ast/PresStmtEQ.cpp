#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresStmt.hpp"
#include "PresStmtEQ.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresStmtEQ::PresStmtEQ(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr) : PresStmt(NodeType::EQ,lexpr,rstmt,rexpr) {}

	sptr<PresStmtEQ> PresStmtEQ::new_(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt) {return sptr<PresStmtEQ>(new PresStmtEQ(lexpr,rstmt,sptr<PresExpr>()));}

	sptr<PresStmtEQ> PresStmtEQ::new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) {return sptr<PresStmtEQ>(new PresStmtEQ(lexpr,sptr<PresStmt>(),rexpr));}

	PresStmtEQ::PresStmtEQ(PresStmtEQ const& o) : PresStmt(o.type(),o.rexpr(),o.rstmt(),o.lexpr()) {}

	PresStmtEQ& PresStmtEQ::operator=(PresStmtEQ const& o)
	{
		this->PresStmt::operator=(o);
		return *this;
	}

	std::string PresStmtEQ::str() const {return this->PresStmt::str();}
	std::string PresStmtEQ::op() const {return "=";}

	void PresStmtEQ::apply(IPresVisitor& v) {v.visitPresStmtEQ(*this);}

	std::string PresStmtEQ::name() const {return "PresStmtEQ";}

}}}}//end namespace omega::bindings::parser::ast
