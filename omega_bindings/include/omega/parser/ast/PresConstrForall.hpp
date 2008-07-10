#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_FORALL_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_FORALL_H_

#include "PresUtil.hpp"
#include "PresConstrExistsForall.hpp"
#include "PresConstr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Forall AST node
	class PresConstrForall : public PresConstrExistsForall
	{
		public:
			PresConstrForall(varid_vect const& vars,sptr<PresConstr> const& constr);
			static sptr<PresConstrForall> new_(varid_vect const& vars,sptr<PresConstr> const& constr);
			PresConstrForall(PresConstrForall const& o);
			PresConstrForall& operator=(PresConstrForall const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			virtual std::string quant() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
