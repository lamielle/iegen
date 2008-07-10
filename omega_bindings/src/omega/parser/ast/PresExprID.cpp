#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"
#include "PresExprID.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprID::PresExprID(std::string const& id) : PresExpr(NodeType::ID),m_id(id) {}

	sptr<PresExprID> PresExprID::new_(std::string const& id) {return sptr<PresExprID>(new PresExprID(id));}

	PresExprID::PresExprID(PresExprID const& o) : PresExpr(o.type()),m_id(o.id()) {}

	PresExprID& PresExprID::operator=(PresExprID const& o)
	{
		this->PresExpr::operator=(o);
		this->id(o.id());
		return *this;
	}

	std::string PresExprID::id() const {return this->m_id;}
	void PresExprID::id(std::string const& id) {this->m_id=id;}

	std::string PresExprID::str() const {return this->id();}

	void PresExprID::apply(IPresVisitor& v) {v.visitPresExprID(*this);}

	std::string PresExprID::name() const {return "PresExprID";}

}}}}//end namespace omega::bindings::parser::ast
