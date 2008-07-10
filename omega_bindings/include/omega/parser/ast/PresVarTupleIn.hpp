#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_TUPLE_IN_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_TUPLE_IN_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVarTuple.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger set variable tuple AST node
	class PresVarTupleIn : public PresVarTuple
	{
		public:
			PresVarTupleIn(var_vect const& vars);
			static sptr<PresVarTupleIn> new_(var_vect const& vars);
			PresVarTupleIn(PresVarTupleIn const& o);
			PresVarTupleIn& operator=(PresVarTupleIn const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
