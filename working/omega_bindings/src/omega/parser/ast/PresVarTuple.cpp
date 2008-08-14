#include "PresUtil.hpp"
#include "PresVarTuple.hpp"
#include "PresVar.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresVarTuple::PresVarTuple(NodeType::PresVarTupleType type,var_vect const& vars) : PresTypedNode<NodeType::PresVarTupleType>(type),m_vars(vars) {}

	PresVarTuple::PresVarTuple(PresVarTuple const& o) : PresTypedNode<NodeType::PresVarTupleType>(o.type()),m_vars(o.vars()) {}

	PresVarTuple& PresVarTuple::operator=(PresVarTuple const& o)
	{
		this->PresTypedNode<NodeType::PresVarTupleType>::operator=(o);
		this->vars(o.vars());
		return *this;
	}

	var_vect PresVarTuple::vars() const {return this->m_vars;}
	void PresVarTuple::vars(var_vect const& vars) {this->m_vars=vars;}

	std::string PresVarTuple::str() const
	{
		return get_string_from_vector(get_pres_node_vector(this->vars()),",");
	}

}}}}//end namespace omega::bindings::parser::ast
