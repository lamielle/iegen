#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_ADD_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_ADD_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"
#include "PresExprBinOp.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Add AST node
	class PresExprAdd : public PresExprBinOp
	{
		public:
			PresExprAdd(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr);
			static sptr<PresExprAdd> new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr);
			PresExprAdd(PresExprAdd const& o);
			PresExprAdd& operator=(PresExprAdd const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			virtual std::string op() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
