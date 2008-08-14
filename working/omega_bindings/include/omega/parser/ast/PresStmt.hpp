#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_STMT_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_STMT_H_

#include "PresUtil.hpp"
#include "PresTypedNode.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger expression AST node: Either Int, ID, Func, UnOp, BinOp, or List
	class PresStmt : public PresTypedNode<NodeType::PresStmtType>
	{
		protected:
			PresStmt(NodeType::PresStmtType type,sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr);
			PresStmt(PresStmt const& o);
			PresStmt& operator=(PresStmt const& o);

		public:
			virtual std::string str() const; virtual std::string op() const=0;

			sptr<PresExpr> lexpr() const;
			sptr<PresStmt> rstmt() const;
			bool has_rstmt() const;
			sptr<PresExpr> rexpr() const;

		private:
			void lexpr(sptr<PresExpr> const& lexpr);
			void rstmt(sptr<PresStmt> const& rstmt);
			void rexpr(sptr<PresExpr> const& rexpr);
			sptr<PresExpr> m_lexpr;
			sptr<PresStmt> m_rstmt;
			sptr<PresExpr> m_rexpr;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
