#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_RELATION_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_RELATION_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresFormula.hpp"
#include "PresConstr.hpp"
#include "PresVar.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Relation AST node
	class PresRelation : public PresFormula
	{
		public:
			PresRelation(sptr<PresVarTupleIn> const& in_vars,sptr<PresVarTupleOut> const& out_vars,sptr<PresConstr> constr);
			static sptr<PresRelation> new_(sptr<PresVarTupleIn> const& in_vars,sptr<PresVarTupleOut> const& out_vars,sptr<PresConstr> const& constr);
			PresRelation(PresRelation const& o);
			PresRelation& operator=(PresRelation const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			sptr<PresVarTupleIn> in_vars() const;
			sptr<PresVarTupleOut> out_vars() const;

			void apply(IPresVisitor& v);

		private:
			void in_vars(sptr<PresVarTupleIn> const& in_vars);
			void out_vars(sptr<PresVarTupleOut> const& out_vars);
			sptr<PresVarTupleIn> m_in_vars;
			sptr<PresVarTupleOut> m_out_vars;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
