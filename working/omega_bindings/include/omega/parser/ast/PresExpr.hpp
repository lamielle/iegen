#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_H_

#include "PresUtil.hpp"
#include "PresTypedNode.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger expression AST node: Either Int, ID, Func, UnOp, BinOp, or List
	class PresExpr : public PresTypedNode<NodeType::PresExprType>
	{
		protected:
			PresExpr(NodeType::PresExprType type);
			PresExpr(PresExpr const& o);
			PresExpr& operator=(PresExpr const& o);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
