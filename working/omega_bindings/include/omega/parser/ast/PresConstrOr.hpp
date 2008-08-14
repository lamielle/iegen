#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_OR_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_OR_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresConstrAndOr.hpp"
#include "PresConstr.hpp"
#include "PresStmt.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Or AST node
	class PresConstrOr : public PresConstrAndOr
	{
		public:
			PresConstrOr(constr_vect const& constrs,stmt_vect const& stmts);
			static sptr<PresConstrOr> new_(constr_vect const& constrs,stmt_vect const& stmts);
			PresConstrOr(PresConstrOr const& o);
			PresConstrOr& operator=(PresConstrOr const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			void apply(IPresVisitor& v);

		protected:
			virtual std::string sep() const;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
