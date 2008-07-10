#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"
#include "PresExprBinOp.hpp"
#include "PresExprMult.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprMult::PresExprMult(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr,bool simple) : PresExprBinOp(NodeType::Mult,lexpr,rexpr),m_simple(simple) {}

	sptr<PresExprMult> PresExprMult::new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr) {return sptr<PresExprMult>(new PresExprMult(lexpr,rexpr,false));}
	sptr<PresExprMult> PresExprMult::new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr,bool simple) {return sptr<PresExprMult>(new PresExprMult(lexpr,rexpr,simple));}

	PresExprMult::PresExprMult(PresExprMult const& o) : PresExprBinOp(o.op_type(),o.lexpr(),o.rexpr()),m_simple(o.simple()) {}

	PresExprMult& PresExprMult::operator=(PresExprMult const& o)
	{
		this->PresExprBinOp::operator=(o);
		this->simple(o.simple());
		return *this;
	}

	bool PresExprMult::simple() const {return this->m_simple;}
	void PresExprMult::simple(bool simple) {this->m_simple=simple;}

	std::string PresExprMult::str() const {return this->PresExprBinOp::str();}
	std::string PresExprMult::op() const {if(this->simple()) return ""; else return "*";}

	void PresExprMult::apply(IPresVisitor& v) {v.visitPresExprMult(*this);}

	std::string PresExprMult::name() const {return "PresExprMult";}

}}}}//end namespace omega::bindings::parser::ast
