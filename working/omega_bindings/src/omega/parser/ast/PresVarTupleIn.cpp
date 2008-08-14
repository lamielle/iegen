#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVarTupleIn.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresVarTupleIn::PresVarTupleIn(var_vect const& vars):PresVarTuple(NodeType::InVars,vars) {}

	sptr<PresVarTupleIn> PresVarTupleIn::new_(var_vect const& vars){return sptr<PresVarTupleIn>(new PresVarTupleIn(vars));}

	PresVarTupleIn::PresVarTupleIn(PresVarTupleIn const& o) : PresVarTuple(o.type(),o.vars()) {}

	PresVarTupleIn& PresVarTupleIn::operator=(PresVarTupleIn const& o)
	{
		this->PresVarTuple::operator=(o);
		return *this;
	}

	std::string PresVarTupleIn::str() const {return this->PresVarTuple::str();}

	void PresVarTupleIn::apply(IPresVisitor& v) {v.visitPresVarTupleIn(*this);}

	std::string PresVarTupleIn::name() const {return "PresVarTupleIn";}

}}}}//end namespace omega::bindings::parser::ast
