#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_EXPR_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_EXPR_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVar.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger VarExpr AST node
	class PresVarExpr : public PresVar
	{
		public:
			PresVarExpr(sptr<PresExpr> const& expr);
			static sptr<PresVarExpr> new_(sptr<PresExpr> const& expr);
			PresVarExpr(PresVarExpr const& o);
			PresVarExpr& operator=(PresVarExpr const& o);

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
