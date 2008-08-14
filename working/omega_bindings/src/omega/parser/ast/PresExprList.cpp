#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"
#include "PresExprList.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprList::PresExprList(expr_vect const& exprs) : PresExpr(NodeType::List),m_exprs(exprs) {}

	sptr<PresExprList> PresExprList::new_(expr_vect const& exprs) {return sptr<PresExprList>(new PresExprList(exprs));}

	PresExprList::PresExprList(PresExprList const& o) : PresExpr(o.type()),m_exprs(o.exprs()) {}

	PresExprList& PresExprList::operator=(PresExprList const& o)
	{
		this->PresExpr::operator=(o);
		this->exprs(o.exprs());
		return *this;
	}

	expr_vect PresExprList::exprs() const {return this->m_exprs;}
	void PresExprList::exprs(expr_vect const& exprs) {this->m_exprs=exprs;}

	std::string PresExprList::str() const {return get_string_from_vector(get_pres_node_vector(this->exprs()),",");}

	void PresExprList::apply(IPresVisitor& v) {v.visitPresExprList(*this);}

	std::string PresExprList::name() const {return "PresExprList";}

}}}}//end namespace omega::bindings::parser::ast
