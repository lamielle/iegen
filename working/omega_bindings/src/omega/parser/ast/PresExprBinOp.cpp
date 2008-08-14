#include "PresUtil.hpp"
#include "PresExpr.hpp"
#include "PresExprBinOp.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprBinOp::PresExprBinOp(NodeType::PresExprBinOpType op_type,sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) : PresExpr(NodeType::BinOp),m_op_type(op_type),m_lexpr(lexpr),m_rexpr(rexpr) {}

	PresExprBinOp::PresExprBinOp(PresExprBinOp const& o) : PresExpr(o.type()),m_op_type(o.op_type()),m_lexpr(o.lexpr()),m_rexpr(o.rexpr()) {}

	PresExprBinOp& PresExprBinOp::operator=(PresExprBinOp const& o)
	{
		this->PresExpr::operator=(o);
		this->op_type(o.op_type());
		this->lexpr(o.lexpr());
		this->rexpr(o.rexpr());
		return *this;
	}

	NodeType::PresExprBinOpType PresExprBinOp::op_type() const {return this->m_op_type;}
	void PresExprBinOp::op_type(NodeType::PresExprBinOpType op_type) {this->m_op_type=op_type;}
	sptr<PresExpr> PresExprBinOp::lexpr() const {return this->m_lexpr;}
	sptr<PresExpr> PresExprBinOp::rexpr() const {return this->m_rexpr;}
	void PresExprBinOp::lexpr(sptr<PresExpr> const& lexpr) {this->m_lexpr=lexpr;}
	void PresExprBinOp::rexpr(sptr<PresExpr> const& rexpr) {this->m_rexpr=rexpr;}

	std::string PresExprBinOp::str() const
	{
		std::stringstream s;
		s<<this->lexpr()->str();
		s<<this->op();
		s<<this->rexpr()->str();
		return s.str();
	}

}}}}//end namespace omega::bindings::parser::ast
