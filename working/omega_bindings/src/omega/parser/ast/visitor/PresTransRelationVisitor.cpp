#include "PresTransRelationVisitor.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	PresTransRelationVisitor::PresTransRelationVisitor() : PresTransVisitor(),m_relation() {}

	PresTransRelationVisitor::PresTransRelationVisitor(PresTransRelationVisitor const& o) : m_relation(o.relation()) {}

	PresTransRelationVisitor::PresTransRelationVisitor& PresTransRelationVisitor::operator=(PresTransRelationVisitor const& o)
	{
		this->PresTransVisitor::operator=(o);
		this->relation(o.relation());
		return *this;
	}

	void PresTransRelationVisitor::compose(PresTransRelationVisitor const& o)
	{
		this->relation()->compose(o.relation());
	}

	void PresTransRelationVisitor::inverse()
	{
		this->relation()->inverse();
	}

	int PresTransRelationVisitor::arity_in() const {return this->relation()->arity_in();}
	int PresTransRelationVisitor::arity_out() const {return this->relation()->arity_out();}

	sptr<Relation> PresTransRelationVisitor::relation() const {return this->m_relation;}
	sptr<Formula> PresTransRelationVisitor::formula() const {return this->m_relation;}
	void PresTransRelationVisitor::relation(sptr<Relation> const& relation) {this->m_relation=relation;}

	//Relation nodes
	void PresTransRelationVisitor::inPresRelation(PresRelation const& v)
	{
		this->relation(sptr<Relation>(new Relation(v.in_vars()->vars().size(),v.out_vars()->vars().size())));
	}
	void PresTransRelationVisitor::outPresRelation(PresRelation const& v) {}

	//Variable nodes
	void PresTransRelationVisitor::inPresVarID(PresVarID const& v)
	{
		if(this->at_in_vars())
			this->relation()->name_in(this->curr_var(),v.id());
		else if(this->at_out_vars())
			this->relation()->name_out(this->curr_var(),v.id());
		else if(!this->at_func())
			throw OmegaException("Visited a PresVarID but not at in or out vars.");
	}
	void PresTransRelationVisitor::outPresVarID(PresVarID const& v) {this->next_var();}

}}}}}//end namespace omega::bindings::parser::ast::visitor
