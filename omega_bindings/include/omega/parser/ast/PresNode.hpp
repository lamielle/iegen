#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_NODE_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_NODE_H_

#include "PresUtil.hpp"
#include "IPresVisitable.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {
	using namespace visitor;

	//Base class for all Presburger formula AST nodes
	class PresNode : public IPresVisitable
	{
		protected:
			PresNode();
			PresNode(PresNode const& o);
			virtual PresNode& operator=(PresNode const& o);
			virtual ~PresNode();

		public:
			virtual std::string str() const=0;
			virtual std::string name() const=0;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
