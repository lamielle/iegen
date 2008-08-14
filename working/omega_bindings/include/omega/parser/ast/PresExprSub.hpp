#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_SUB_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_SUB_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"
#include "PresExprBinOp.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Sub AST node
	class PresExprSub : public PresExprBinOp
	{
		public:
			PresExprSub(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr);
			static sptr<PresExprSub> new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr);
			PresExprSub(PresExprSub const& o);
			PresExprSub& operator=(PresExprSub const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			virtual std::string op() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
