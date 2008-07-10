#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_AND_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_AND_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresConstrAndOr.hpp"
#include "PresConstr.hpp"
#include "PresStmt.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger And AST node
	class PresConstrAnd : public PresConstrAndOr
	{
		public:
			PresConstrAnd(constr_vect const& constrs,stmt_vect const& stmts);
			static sptr<PresConstrAnd> new_(constr_vect const& constrs,stmt_vect const& stmts);
			PresConstrAnd(PresConstrAnd const& o);
			PresConstrAnd& operator=(PresConstrAnd const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			void apply(IPresVisitor& v);

		protected:
			virtual std::string sep() const;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
