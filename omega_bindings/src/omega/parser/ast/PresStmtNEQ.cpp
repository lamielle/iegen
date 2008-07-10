#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresStmt.hpp"
#include "PresStmtNEQ.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresStmtNEQ::PresStmtNEQ(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr) : PresStmt(NodeType::NEQ,lexpr,rstmt,rexpr) {}

	sptr<PresStmtNEQ> PresStmtNEQ::new_(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt) {return sptr<PresStmtNEQ>(new PresStmtNEQ(lexpr,rstmt,sptr<PresExpr>()));}

	sptr<PresStmtNEQ> PresStmtNEQ::new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) {return sptr<PresStmtNEQ>(new PresStmtNEQ(lexpr,sptr<PresStmt>(),rexpr));}

	PresStmtNEQ::PresStmtNEQ(PresStmtNEQ const& o) : PresStmt(o.type(),o.rexpr(),o.rstmt(),o.lexpr()) {}

	PresStmtNEQ& PresStmtNEQ::operator=(PresStmtNEQ const& o)
	{
		this->PresStmt::operator=(o);
		return *this;
	}

	std::string PresStmtNEQ::str() const {return this->PresStmt::str();}
	std::string PresStmtNEQ::op() const {return "!=";}

	void PresStmtNEQ::apply(IPresVisitor& v) {v.visitPresStmtNEQ(*this);}

	std::string PresStmtNEQ::name() const {return "PresStmtNEQ";}

}}}}//end namespace omega::bindings::parser::ast
