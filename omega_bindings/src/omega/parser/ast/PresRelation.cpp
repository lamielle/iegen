#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresFormula.hpp"
#include "PresVarTupleIn.hpp"
#include "PresVarTupleOut.hpp"
#include "PresConstr.hpp"
#include "PresRelation.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresRelation::PresRelation(sptr<PresVarTupleIn> const& in_vars,sptr<PresVarTupleOut> const& out_vars,sptr<PresConstr> constr) : PresFormula(NodeType::Relation,constr),m_in_vars(in_vars),m_out_vars(out_vars) {}

	sptr<PresRelation> PresRelation::new_(sptr<PresVarTupleIn> const& in_vars,sptr<PresVarTupleOut> const& out_vars,sptr<PresConstr> const& constr){return sptr<PresRelation>(new PresRelation(in_vars,out_vars,constr));}

	PresRelation::PresRelation(PresRelation const& o) : PresFormula(NodeType::Relation,o.constr()),m_in_vars(o.in_vars()),m_out_vars(o.out_vars()) {}

	PresRelation& PresRelation::operator=(PresRelation const& o)
	{
		this->PresFormula::operator=(o);
		this->in_vars(o.in_vars());
		this->out_vars(o.out_vars());
		return *this;
	}

	std::string PresRelation::str() const
	{
		std::stringstream s;
		s<<"{[";
		s<<this->in_vars()->str();
		s<<"]->[";
		s<<this->out_vars()->str();
		s<<"]";
		if(!this->constr()->empty())
		{
			s<<":";
			s<<this->constr()->str();
		}
		s<<"}";
		return s.str();
	}

	sptr<PresVarTupleIn> PresRelation::in_vars() const {return this->m_in_vars;}
	void PresRelation::in_vars(sptr<PresVarTupleIn> const& in_vars){this->m_in_vars=in_vars;}
	sptr<PresVarTupleOut> PresRelation::out_vars() const {return this->m_out_vars;}
	void PresRelation::out_vars(sptr<PresVarTupleOut> const& out_vars){this->m_out_vars=out_vars;}

	void PresRelation::apply(IPresVisitor& v) {v.visitPresRelation(*this);}

	std::string PresRelation::name() const {return "PresRelation";}

}}}}//end namespace omega::bindings::parser::ast
