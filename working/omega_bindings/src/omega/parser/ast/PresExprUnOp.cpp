#include "PresUtil.hpp"
#include "PresExpr.hpp"
#include "PresExprUnOp.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprUnOp::PresExprUnOp(NodeType::PresExprUnOpType op_type,sptr<PresExpr> const& expr) : PresExpr(NodeType::UnOp),m_op_type(op_type),m_expr(expr) {}

	PresExprUnOp::PresExprUnOp(PresExprUnOp const& o) : PresExpr(o.type()),m_op_type(o.op_type()),m_expr(o.expr()) {}

	PresExprUnOp& PresExprUnOp::operator=(PresExprUnOp const& o)
	{
		this->PresExpr::operator=(o);
		this->op_type(o.op_type());
		this->expr(o.expr());
		return *this;
	}

	NodeType::PresExprUnOpType PresExprUnOp::op_type() const {return this->m_op_type;}
	void PresExprUnOp::op_type(NodeType::PresExprUnOpType op_type) {this->m_op_type=op_type;}
	sptr<PresExpr> PresExprUnOp::expr() const {return this->m_expr;}
	void PresExprUnOp::expr(sptr<PresExpr> const& expr) {this->m_expr=expr;}

	std::string PresExprUnOp::str() const
	{
		std::stringstream s;
		s<<this->op();
		s<<this->expr()->str();
		return s.str();
	}

}}}}//end namespace omega::bindings::parser::ast
