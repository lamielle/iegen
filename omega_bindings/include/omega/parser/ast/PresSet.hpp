#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_SET_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_SET_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresFormula.hpp"
#include "PresConstr.hpp"
#include "PresVar.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Set AST node
	class PresSet : public PresFormula
	{
		public:
			PresSet(sptr<PresVarTupleSet> const& set_vars,sptr<PresConstr> const& constr);
			static sptr<PresSet> new_(sptr<PresVarTupleSet> const& set_vars,sptr<PresConstr> const& constr);
			PresSet(PresSet const& o);
			PresSet& operator=(PresSet const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			sptr<PresVarTupleSet> set_vars() const;

			void apply(IPresVisitor& v);

		private:
			void set_vars(sptr<PresVarTupleSet> const& set_vars);
			sptr<PresVarTupleSet> m_set_vars;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
