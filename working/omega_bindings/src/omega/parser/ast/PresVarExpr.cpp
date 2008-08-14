#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVar.hpp"
#include "PresVarExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresVarExpr::PresVarExpr(sptr<PresExpr> const& expr) : PresVar(NodeType::VarExpr),m_expr(expr) {}

	sptr<PresVarExpr> PresVarExpr::new_(sptr<PresExpr> const& expr) {return sptr<PresVarExpr>(new PresVarExpr(expr));}

	PresVarExpr::PresVarExpr(PresVarExpr const& o) : PresVar(o.type()),m_expr(o.expr()) {}

	PresVarExpr& PresVarExpr::operator=(PresVarExpr const& o)
	{
		this->PresVar::operator=(o);
		this->expr(o.expr());
		return *this;
	}

	sptr<PresExpr> PresVarExpr::expr() const {return this->m_expr;}
	void PresVarExpr::expr(sptr<PresExpr> const& expr) {this->m_expr=expr;}

	std::string PresVarExpr::str() const {return this->expr()->str();}

	void PresVarExpr::apply(IPresVisitor& v) {v.visitPresVarExpr(*this);}

	std::string PresVarExpr::name() const {return "PresVarExpr";}

}}}}//end namespace omega::bindings::parser::ast
