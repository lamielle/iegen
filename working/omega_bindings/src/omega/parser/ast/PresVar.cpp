#include "PresUtil.hpp"
#include "PresTypedNode.hpp"
#include "PresVar.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresVar::PresVar(NodeType::PresVarType type) : PresTypedNode<NodeType::PresVarType>(type) {}

	PresVar::PresVar(PresVar const& o) : PresTypedNode<NodeType::PresVarType>(o.type()) {}

	PresVar& PresVar::operator=(PresVar const& o)
	{
		this->PresTypedNode<NodeType::PresVarType>::operator=(o);
		return *this;
	}

}}}}//end namespace omega::bindings::parser::ast
