#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVarTupleSet.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresVarTupleSet::PresVarTupleSet(var_vect const& vars):PresVarTuple(NodeType::SetVars,vars) {}

	sptr<PresVarTupleSet> PresVarTupleSet::new_(var_vect const& vars){return sptr<PresVarTupleSet>(new PresVarTupleSet(vars));}

	PresVarTupleSet::PresVarTupleSet(PresVarTupleSet const& o) : PresVarTuple(o.type(),o.vars()) {}

	PresVarTupleSet& PresVarTupleSet::operator=(PresVarTupleSet const& o)
	{
		this->PresVarTuple::operator=(o);
		return *this;
	}

	std::string PresVarTupleSet::str() const {return this->PresVarTuple::str();}

	void PresVarTupleSet::apply(IPresVisitor& v) {v.visitPresVarTupleSet(*this);}

	std::string PresVarTupleSet::name() const {return "PresVarTupleSet";}

}}}}//end namespace omega::bindings::parser::ast
