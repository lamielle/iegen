#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_NEG_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_NEG_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExprUnOp.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Neg AST node
	class PresExprNeg : public PresExprUnOp
	{
		public:
			PresExprNeg(sptr<PresExpr> const& expr);
			static sptr<PresExprNeg> new_(sptr<PresExpr> const& expr);
			PresExprNeg(PresExprNeg const& o);
			PresExprNeg& operator=(PresExprNeg const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			virtual std::string op() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
