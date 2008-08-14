#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_FUNC_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_FUNC_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Func AST node
	class PresExprFunc : public PresExpr
	{
		public:
			PresExprFunc(sptr<PresVarID> const& func_name,varid_vect const& args);
			static sptr<PresExprFunc> new_(sptr<PresVarID> const& func_name,varid_vect const& args);
			PresExprFunc(PresExprFunc const& o);
			PresExprFunc& operator=(PresExprFunc const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			sptr<PresVarID> func_name() const;
			varid_vect args() const;

			void apply(IPresVisitor& v);

		private:
			void func_name(sptr<PresVarID> const& func_name);
			void args(varid_vect const& args);
			sptr<PresVarID> m_func_name;
			varid_vect m_args;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
