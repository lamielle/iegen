#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExprNeg.hpp"
#include "PresExprUnOp.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprNeg::PresExprNeg(sptr<PresExpr> const& expr) : PresExprUnOp(NodeType::Neg,expr) {}

	sptr<PresExprNeg> PresExprNeg::new_(sptr<PresExpr> const& expr) {return sptr<PresExprNeg>(new PresExprNeg(expr));}

	PresExprNeg::PresExprNeg(PresExprNeg const& o) : PresExprUnOp(o.op_type(),o.expr()) {}

	PresExprNeg& PresExprNeg::operator=(PresExprNeg const& o)
	{
		this->PresExprUnOp::operator=(o);
		return *this;
	}

	std::string PresExprNeg::str() const {return this->PresExprUnOp::str();}
	std::string PresExprNeg::op() const {return "-";}

	void PresExprNeg::apply(IPresVisitor& v) {v.visitPresExprNeg(*this);}

	std::string PresExprNeg::name() const {return "PresExprNeg";}

}}}}//end namespace omega::bindings::parser::ast
