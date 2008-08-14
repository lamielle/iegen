#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_TUPLE_OUT_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_TUPLE_OUT_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVarTuple.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger set variable tuple AST node
	class PresVarTupleOut : public PresVarTuple
	{
		public:
			PresVarTupleOut(var_vect const& vars);
			static sptr<PresVarTupleOut> new_(var_vect const& vars);
			PresVarTupleOut(PresVarTupleOut const& o);
			PresVarTupleOut& operator=(PresVarTupleOut const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
