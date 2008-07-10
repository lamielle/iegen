#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_MULT_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_MULT_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"
#include "PresExprBinOp.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Mult AST node
	class PresExprMult : public PresExprBinOp
	{
		public:
			PresExprMult(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr,bool simple);
			static sptr<PresExprMult> new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr);
			static sptr<PresExprMult> new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr,bool simple);
			PresExprMult(PresExprMult const& o);
			PresExprMult& operator=(PresExprMult const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			virtual std::string op() const;

			bool simple() const;

			void apply(IPresVisitor& v);

		private:
			void simple(bool simple);
			bool m_simple;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
