#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresStmt.hpp"
#include "PresStmtLTE.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresStmtLTE::PresStmtLTE(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr) : PresStmt(NodeType::LTE,lexpr,rstmt,rexpr) {}

	sptr<PresStmtLTE> PresStmtLTE::new_(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt) {return sptr<PresStmtLTE>(new PresStmtLTE(lexpr,rstmt,sptr<PresExpr>()));}

	sptr<PresStmtLTE> PresStmtLTE::new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) {return sptr<PresStmtLTE>(new PresStmtLTE(lexpr,sptr<PresStmt>(),rexpr));}

	PresStmtLTE::PresStmtLTE(PresStmtLTE const& o) : PresStmt(o.type(),o.rexpr(),o.rstmt(),o.lexpr()) {}

	PresStmtLTE& PresStmtLTE::operator=(PresStmtLTE const& o)
	{
		this->PresStmt::operator=(o);
		return *this;
	}

	std::string PresStmtLTE::str() const {return this->PresStmt::str();}
	std::string PresStmtLTE::op() const {return "<=";}

	void PresStmtLTE::apply(IPresVisitor& v) {v.visitPresStmtLTE(*this);}

	std::string PresStmtLTE::name() const {return "PresStmtLTE";}

}}}}//end namespace omega::bindings::parser::ast
