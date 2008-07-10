#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresStmt.hpp"
#include "PresStmtGTE.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresStmtGTE::PresStmtGTE(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr) : PresStmt(NodeType::GTE,lexpr,rstmt,rexpr) {}

	sptr<PresStmtGTE> PresStmtGTE::new_(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt) {return sptr<PresStmtGTE>(new PresStmtGTE(lexpr,rstmt,sptr<PresExpr>()));}

	sptr<PresStmtGTE> PresStmtGTE::new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) {return sptr<PresStmtGTE>(new PresStmtGTE(lexpr,sptr<PresStmt>(),rexpr));}

	PresStmtGTE::PresStmtGTE(PresStmtGTE const& o) : PresStmt(o.type(),o.rexpr(),o.rstmt(),o.lexpr()) {}

	PresStmtGTE& PresStmtGTE::operator=(PresStmtGTE const& o)
	{
		this->PresStmt::operator=(o);
		return *this;
	}

	std::string PresStmtGTE::str() const {return this->PresStmt::str();}
	std::string PresStmtGTE::op() const {return ">=";}

	void PresStmtGTE::apply(IPresVisitor& v) {v.visitPresStmtGTE(*this);}

	std::string PresStmtGTE::name() const {return "PresStmtGTE";}

}}}}//end namespace omega::bindings::parser::ast
