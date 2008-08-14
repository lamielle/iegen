#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_PAREN_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_PAREN_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresConstr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Paren AST node
	class PresConstrParen : public PresConstr
	{
		public:
			PresConstrParen(sptr<PresConstr> const& constr);
			static sptr<PresConstrParen> new_(sptr<PresConstr> const& constr);
			PresConstrParen(PresConstrParen const& o);
			PresConstrParen& operator=(PresConstrParen const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			virtual bool empty() const;

			sptr<PresConstr> constr() const;

			void apply(IPresVisitor& v);

		private:
			void constr(sptr<PresConstr> const& constr);
			sptr<PresConstr> m_constr;
	};


}}}}//end namespace omega::bindings::parser::ast

#endif
