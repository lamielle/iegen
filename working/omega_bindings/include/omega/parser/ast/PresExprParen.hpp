#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_PAREN_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_PAREN_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Paren AST node
	class PresExprParen : public PresExpr
	{
		public:
			PresExprParen(sptr<PresExpr> const& expr);
			static sptr<PresExprParen> new_(sptr<PresExpr> const& expr);
			PresExprParen(PresExprParen const& o);
			PresExprParen& operator=(PresExprParen const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			sptr<PresExpr> expr() const;

			void apply(IPresVisitor& v);

		private:
			void expr(sptr<PresExpr> const& expr);
			sptr<PresExpr> m_expr;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
