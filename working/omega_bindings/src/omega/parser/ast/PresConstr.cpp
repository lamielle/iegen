#include "PresUtil.hpp"
#include "PresTypedNode.hpp"
#include "PresConstr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresConstr::PresConstr(NodeType::PresConstrType type) : PresTypedNode<NodeType::PresConstrType>(type) {}

	PresConstr::PresConstr(PresConstr const& o) : PresTypedNode<NodeType::PresConstrType>(o.type()) {}

	PresConstr& PresConstr::operator=(PresConstr const& o)
	{
		this->PresTypedNode<NodeType::PresConstrType>::operator=(o);
		return *this;
	}

}}}}//end namespace omega::bindings::parser::ast
