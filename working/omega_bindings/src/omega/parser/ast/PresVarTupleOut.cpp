#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVarTupleOut.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresVarTupleOut::PresVarTupleOut(var_vect const& vars):PresVarTuple(NodeType::OutVars,vars) {}

	sptr<PresVarTupleOut> PresVarTupleOut::new_(var_vect const& vars){return sptr<PresVarTupleOut>(new PresVarTupleOut(vars));}

	PresVarTupleOut::PresVarTupleOut(PresVarTupleOut const& o) : PresVarTuple(o.type(),o.vars()) {}

	PresVarTupleOut& PresVarTupleOut::operator=(PresVarTupleOut const& o)
	{
		this->PresVarTuple::operator=(o);
		return *this;
	}

	std::string PresVarTupleOut::str() const {return this->PresVarTuple::str();}

	void PresVarTupleOut::apply(IPresVisitor& v) {v.visitPresVarTupleOut(*this);}

	std::string PresVarTupleOut::name() const {return "PresVarTupleOut";}

}}}}//end namespace omega::bindings::parser::ast
