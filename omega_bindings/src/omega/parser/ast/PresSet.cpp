#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresFormula.hpp"
#include "PresVarTupleSet.hpp"
#include "PresConstr.hpp"
#include "PresSet.hpp"
#include "PresVar.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresSet::PresSet(sptr<PresVarTupleSet> const& set_vars,sptr<PresConstr> const& constr) : PresFormula(NodeType::Set,constr),m_set_vars(set_vars) {}

	sptr<PresSet> PresSet::new_(sptr<PresVarTupleSet> const& set_vars,sptr<PresConstr> const& constr){return sptr<PresSet>(new PresSet(set_vars,constr));}

	PresSet::PresSet(PresSet const& o) : PresFormula(NodeType::Set,o.constr()),m_set_vars(o.set_vars()) {}

	PresSet& PresSet::operator=(PresSet const& o)
	{
		this->PresFormula::operator=(o);
		this->set_vars(o.set_vars());
		return *this;
	}

	std::string PresSet::str() const
	{
		std::stringstream s;
		s<<"{[";
		s<<this->set_vars()->str();
		s<<"]";
		if(!this->constr()->empty())
		{
			s<<":";
			s<<this->constr()->str();
		}
		s<<"}";
		return s.str();
	}

	sptr<PresVarTupleSet> PresSet::set_vars() const {return this->m_set_vars;}
	void PresSet::set_vars(sptr<PresVarTupleSet> const& set_vars){this->m_set_vars=set_vars;}

	void PresSet::apply(IPresVisitor& v) {v.visitPresSet(*this);}

	std::string PresSet::name() const {return "PresSet";}

}}}}//end namespace omega::bindings::parser::ast
