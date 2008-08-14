#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_H_

#include "PresUtil.hpp"
#include "PresTypedNode.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger tuple variable node
	class PresVar : public PresTypedNode<NodeType::PresVarType>
	{
		protected:
			PresVar(NodeType::PresVarType type);
			PresVar(PresVar const& o);
			PresVar& operator=(PresVar const& o);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
