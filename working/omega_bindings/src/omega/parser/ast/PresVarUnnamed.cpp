#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVar.hpp"
#include "PresVarUnnamed.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresVarUnnamed::PresVarUnnamed() : PresVar(NodeType::VarUnnamed) {}

	sptr<PresVarUnnamed> PresVarUnnamed::new_() {return sptr<PresVarUnnamed>(new PresVarUnnamed());}

	PresVarUnnamed::PresVarUnnamed(PresVarUnnamed const& o) : PresVar(o.type()) {}

	PresVarUnnamed& PresVarUnnamed::operator=(PresVarUnnamed const& o)
	{
		this->PresVar::operator=(o);
		return *this;
	}

	std::string PresVarUnnamed::str() const {return "*";}

	void PresVarUnnamed::apply(IPresVisitor& v) {v.visitPresVarUnnamed(*this);}

	std::string PresVarUnnamed::name() const {return "PresVarUnnamed";}

}}}}//end namespace omega::bindings::parser::ast
