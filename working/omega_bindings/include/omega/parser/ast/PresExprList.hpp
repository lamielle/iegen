#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_LIST_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_LIST_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger List AST node
	class PresExprList : public PresExpr
	{
		public:
			PresExprList(expr_vect const& exprs);
			static sptr<PresExprList> new_(expr_vect const& exprs);
			PresExprList(PresExprList const& o);
			PresExprList& operator=(PresExprList const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			expr_vect exprs() const;

			void apply(IPresVisitor& v);

		private:
			void exprs(expr_vect const& exprs);
			expr_vect m_exprs;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
