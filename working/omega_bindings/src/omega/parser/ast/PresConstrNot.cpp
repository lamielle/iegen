#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresConstr.hpp"
#include "PresConstrNot.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresConstrNot::PresConstrNot(sptr<PresConstr> const& constr) : PresConstr(NodeType::Not),m_constr(constr) {}

	sptr<PresConstrNot> PresConstrNot::new_(sptr<PresConstr> const& constr) {return sptr<PresConstrNot>(new PresConstrNot(constr));}

	PresConstrNot::PresConstrNot(PresConstrNot const& o) : PresConstr(o.type()),m_constr(o.constr()) {}

	PresConstrNot& PresConstrNot::operator=(PresConstrNot const& o)
	{
		this->PresConstr::operator=(o);
		this->constr(o.constr());
		return *this;
	}

	sptr<PresConstr> PresConstrNot::constr() const {return this->m_constr;}
	void PresConstrNot::constr(sptr<PresConstr> const& constr) {this->m_constr=constr;}

	std::string PresConstrNot::str() const
	{
		std::stringstream s;
		if(!this->empty())
		{
			s<<"NOT ";
			s<<this->constr()->str();
		}
		return s.str();
	}

	bool PresConstrNot::empty() const
	{
		return this->constr()->empty();
	}

	void PresConstrNot::apply(IPresVisitor& v) {v.visitPresConstrNot(*this);}

	std::string PresConstrNot::name() const {return "PresConstrNot";}

}}}}//end namespace omega::bindings::parser::ast
