#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_TUPLE_SET_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_TUPLE_SET_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVarTuple.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger set variable tuple AST node
	class PresVarTupleSet : public PresVarTuple
	{
		public:
			PresVarTupleSet(var_vect const& vars);
			static sptr<PresVarTupleSet> new_(var_vect const& vars);
			PresVarTupleSet(PresVarTupleSet const& o);
			PresVarTupleSet& operator=(PresVarTupleSet const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
