#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_EXISTS_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_EXISTS_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresConstrExistsForall.hpp"
#include "PresConstr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger Exists AST node
	class PresConstrExists : public PresConstrExistsForall
	{
		public:
			PresConstrExists(varid_vect const& vars,sptr<PresConstr> const& constr);
			static sptr<PresConstrExists> new_(varid_vect const& vars,sptr<PresConstr> const& constr);
			PresConstrExists(PresConstrExists const& o);
			PresConstrExists& operator=(PresConstrExists const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			virtual std::string quant() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
