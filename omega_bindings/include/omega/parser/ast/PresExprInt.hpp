#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_INT_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_INT_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Int AST node
	class PresExprInt : public PresExpr
	{
		public:
			PresExprInt(int value);
			static sptr<PresExprInt> new_(int value);
			PresExprInt(PresExprInt const& o);
			PresExprInt& operator=(PresExprInt const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			int value() const;

			void apply(IPresVisitor& v);

		private:
			void value(int value);
			int m_value;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
