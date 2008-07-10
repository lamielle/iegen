#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_UN_OP_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_UN_OP_H_

#include "PresUtil.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger UnOp AST node
	class PresExprUnOp : public PresExpr
	{
		protected:
			PresExprUnOp(NodeType::PresExprUnOpType op_type,sptr<PresExpr> const& expr);
			PresExprUnOp(PresExprUnOp const& o);
			PresExprUnOp& operator=(PresExprUnOp const& o);

		public:
			virtual std::string str() const;
			virtual std::string op() const=0;

			NodeType::PresExprUnOpType op_type() const;
			sptr<PresExpr> expr() const;

		private:
			void op_type(NodeType::PresExprUnOpType op_type);
			void expr(sptr<PresExpr> const& expr);
			NodeType::PresExprUnOpType m_op_type;
			sptr<PresExpr> m_expr;

	};

}}}}//end namespace omega::bindings::parser::ast

#endif
