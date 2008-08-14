#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVar.hpp"
#include "PresVarID.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresVarID::PresVarID(std::string const& id):PresVar(NodeType::VarID),m_id(id) {}

	sptr<PresVarID> PresVarID::new_(std::string const& id){return sptr<PresVarID>(new PresVarID(id));}

	PresVarID::PresVarID(PresVarID const& o) : PresVar(o.type()),m_id(o.id()) {}

	PresVarID& PresVarID::operator=(PresVarID const& o)
	{
		this->PresVar::operator=(o);
		this->id(o.id());
		return *this;
	}

	std::string PresVarID::id() const {return this->m_id;}
	void PresVarID::id(std::string const& id) {this->m_id=id;}

	std::string PresVarID::str() const {return this->id();}

	void PresVarID::apply(IPresVisitor& v) {v.visitPresVarID(*this);}

	std::string PresVarID::name() const {return "PresVarID";}

}}}}//end namespace omega::bindings::parser::ast
