#include "PresTransSetVisitor.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	PresTransSetVisitor::PresTransSetVisitor() : PresTransVisitor(),m_set() {}

	PresTransSetVisitor::PresTransSetVisitor(PresTransSetVisitor const& o) : m_set(o.set()) {}

	PresTransSetVisitor::PresTransSetVisitor& PresTransSetVisitor::operator=(PresTransSetVisitor const& o)
	{
		this->PresTransVisitor::operator=(o);
		this->set(o.set());
		return *this;
	}

	sptr<Set> PresTransSetVisitor::set() const {return this->m_set;}
	sptr<Formula> PresTransSetVisitor::formula() const {return this->m_set;}
	void PresTransSetVisitor::set(sptr<Set> const& set) {this->m_set=set;}

	//Set nodes
	void PresTransSetVisitor::inPresSet(PresSet const& v)
	{
		this->set(sptr<Set>(new Set(v.set_vars()->vars().size())));
	}
	void PresTransSetVisitor::outPresSet(PresSet const& v) {}

	//Variable nodes
	void PresTransSetVisitor::inPresVarID(PresVarID const& v) {if(!this->at_func()) this->set()->name(this->curr_var(),v.id());}
	void PresTransSetVisitor::outPresVarID(PresVarID const& v) {if(!this->at_func())this->next_var();}

}}}}}//end namespace omega::bindings::parser::ast::visitor
