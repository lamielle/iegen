#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_BIN_OP_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_BIN_OP_H_

#include "PresUtil.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger BinOp AST node
	class PresExprBinOp : public PresExpr
	{
		protected:
			PresExprBinOp(NodeType::PresExprBinOpType op_type,sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr);
			PresExprBinOp(PresExprBinOp const& o);
			PresExprBinOp& operator=(PresExprBinOp const& o);

		public:
			virtual std::string str() const;
			virtual std::string op() const=0;

			NodeType::PresExprBinOpType op_type() const;
			sptr<PresExpr> lexpr() const;
			sptr<PresExpr> rexpr() const;

		private:
			void op_type(NodeType::PresExprBinOpType op_type);
			void lexpr(sptr<PresExpr> const& lexpr);
			void rexpr(sptr<PresExpr> const& rexpr);
			NodeType::PresExprBinOpType m_op_type;
			sptr<PresExpr> m_lexpr,m_rexpr;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
