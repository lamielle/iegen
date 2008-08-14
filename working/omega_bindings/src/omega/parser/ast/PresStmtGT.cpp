#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresStmt.hpp"
#include "PresStmtGT.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresStmtGT::PresStmtGT(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr) : PresStmt(NodeType::GT,lexpr,rstmt,rexpr) {}

	sptr<PresStmtGT> PresStmtGT::new_(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt) {return sptr<PresStmtGT>(new PresStmtGT(lexpr,rstmt,sptr<PresExpr>()));}

	sptr<PresStmtGT> PresStmtGT::new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) {return sptr<PresStmtGT>(new PresStmtGT(lexpr,sptr<PresStmt>(),rexpr));}

	PresStmtGT::PresStmtGT(PresStmtGT const& o) : PresStmt(o.type(),o.rexpr(),o.rstmt(),o.lexpr()) {}

	PresStmtGT& PresStmtGT::operator=(PresStmtGT const& o)
	{
		this->PresStmt::operator=(o);
		return *this;
	}

	std::string PresStmtGT::str() const {return this->PresStmt::str();}
	std::string PresStmtGT::op() const {return ">";}

	void PresStmtGT::apply(IPresVisitor& v) {v.visitPresStmtGT(*this);}

	std::string PresStmtGT::name() const {return "PresStmtGT";}

}}}}//end namespace omega::bindings::parser::ast
