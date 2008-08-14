#include "PresUtil.hpp"
#include "PresTypedNode.hpp"
#include "PresNode.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	template <typename T>
	PresTypedNode<T>::PresTypedNode(T type) : m_type(type) {}

	template <typename T>
	PresTypedNode<T>::PresTypedNode(PresTypedNode const& o) : m_type(o.type()) {}

	template <typename T>
	PresTypedNode<T>& PresTypedNode<T>::operator=(PresTypedNode<T> const& o)
	{
		this->PresNode::operator=(o);
		this->type(o.type());
		return *this;
	}

	template <typename T>
	PresTypedNode<T>::~PresTypedNode() {}

	template <typename T>
	T PresTypedNode<T>::type() const {return this->m_type;}

	template <typename T>
	void PresTypedNode<T>::type(T type) {this->m_type=type;}

	//Explicitly instantiate the following PresTypedNode template classes
	template class PresTypedNode<NodeType::PresFormulaType>;
	template class PresTypedNode<NodeType::PresVarTupleType>;
	template class PresTypedNode<NodeType::PresVarType>;
	template class PresTypedNode<NodeType::PresConstrType>;
	template class PresTypedNode<NodeType::PresStmtType>;
	template class PresTypedNode<NodeType::PresExprType>;

}}}}//end namespace omega::bindings::parser::ast
