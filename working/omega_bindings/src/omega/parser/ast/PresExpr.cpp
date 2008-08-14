#include "PresUtil.hpp"
#include "PresTypedNode.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExpr::PresExpr(NodeType::PresExprType type) : PresTypedNode<NodeType::PresExprType>(type) {}

	PresExpr::PresExpr(PresExpr const& o) : PresTypedNode<NodeType::PresExprType>(o.type()) {}

	PresExpr& PresExpr::operator=(PresExpr const& o)
	{
		this->PresTypedNode<NodeType::PresExprType>::operator=(o);
		return *this;
	}

}}}}//end namespace omega::bindings::parser::ast
