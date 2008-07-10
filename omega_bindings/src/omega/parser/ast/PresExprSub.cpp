#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"
#include "PresExprBinOp.hpp"
#include "PresExprSub.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprSub::PresExprSub(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) : PresExprBinOp(NodeType::Sub,lexpr,rexpr) {}

	sptr<PresExprSub> PresExprSub::new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) {return sptr<PresExprSub>(new PresExprSub(lexpr,rexpr));}

	PresExprSub::PresExprSub(PresExprSub const& o) : PresExprBinOp(o.op_type(),o.lexpr(),o.rexpr()) {}

	PresExprSub& PresExprSub::operator=(PresExprSub const& o)
	{
		this->PresExprBinOp::operator=(o);
		return *this;
	}

	std::string PresExprSub::str() const {return this->PresExprBinOp::str();}
	std::string PresExprSub::op() const {return "-";}

	void PresExprSub::apply(IPresVisitor& v) {v.visitPresExprSub(*this);}

	std::string PresExprSub::name() const {return "PresExprSub";}

}}}}//end namespace omega::bindings::parser::ast
