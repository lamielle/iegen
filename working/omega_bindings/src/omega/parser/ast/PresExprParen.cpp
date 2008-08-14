#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExprParen.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprParen::PresExprParen(sptr<PresExpr> const& expr) : PresExpr(NodeType::ExprParen),m_expr(expr) {}

	sptr<PresExprParen> PresExprParen::new_(sptr<PresExpr> const& expr) {return sptr<PresExprParen>(new PresExprParen(expr));}

	PresExprParen::PresExprParen(PresExprParen const& o) : PresExpr(o.type()),m_expr(o.expr()) {}

	PresExprParen& PresExprParen::operator=(PresExprParen const& o)
	{
		this->PresExpr::operator=(o);
		this->expr(o.expr());
		return *this;
	}

	sptr<PresExpr> PresExprParen::expr() const {return this->m_expr;}
	void PresExprParen::expr(sptr<PresExpr> const& expr) {this->m_expr=expr;}

	std::string PresExprParen::str() const
	{
		std::stringstream s;
		s<<"(";
		s<<this->expr()->str();
		s<<")";
		return s.str();
	}

	void PresExprParen::apply(IPresVisitor& v) {v.visitPresExprParen(*this);}

	std::string PresExprParen::name() const {return "PresExprParen";}

}}}}//end namespace omega::bindings::parser::ast
