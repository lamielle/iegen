#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_H_

#include "PresUtil.hpp"
#include "PresTypedNode.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger constraint AST node: Either And, Or, Not, Exists, or Forall
	class PresConstr : public PresTypedNode<NodeType::PresConstrType>
	{
		protected:
			PresConstr(NodeType::PresConstrType type);
			PresConstr(PresConstr const& o);
			PresConstr& operator=(PresConstr const& o);

		public:
			virtual bool empty() const=0;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
