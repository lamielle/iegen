#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_TUPLE_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_TUPLE_H_

#include "PresUtil.hpp"
#include "PresTypedNode.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger variable tuple
	class PresVarTuple : public PresTypedNode<NodeType::PresVarTupleType>
	{
		protected:
			PresVarTuple(NodeType::PresVarTupleType type,var_vect const& vars);
			PresVarTuple(PresVarTuple const& o);
			PresVarTuple& operator=(PresVarTuple const& o);

		public:
			var_vect vars() const;
			virtual std::string str() const;

		private:
			void vars(var_vect const& vars);
			var_vect m_vars;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
