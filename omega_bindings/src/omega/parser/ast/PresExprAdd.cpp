#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"
#include "PresExprBinOp.hpp"
#include "PresExprAdd.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprAdd::PresExprAdd(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) : PresExprBinOp(NodeType::Add,lexpr,rexpr) {}

	sptr<PresExprAdd> PresExprAdd::new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) {return sptr<PresExprAdd>(new PresExprAdd(lexpr,rexpr));}

	PresExprAdd::PresExprAdd(PresExprAdd const& o) : PresExprBinOp(o.op_type(),o.lexpr(),o.rexpr()) {}

	PresExprAdd& PresExprAdd::operator=(PresExprAdd const& o)
	{
		this->PresExprBinOp::operator=(o);
		return *this;
	}

	std::string PresExprAdd::str() const {return this->PresExprBinOp::str();}
	std::string PresExprAdd::op() const {return "+";}

	void PresExprAdd::apply(IPresVisitor& v) {v.visitPresExprAdd(*this);}

	std::string PresExprAdd::name() const {return "PresExprAdd";}

}}}}//end namespace omega::bindings::parser::ast
