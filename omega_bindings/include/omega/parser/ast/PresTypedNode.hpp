#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_TYPED_NODE_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_TYPED_NODE_H_

#include "PresUtil.hpp"
#include "PresNode.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Base class for all typed Presburger formula AST nodes
	template <typename T>
	class PresTypedNode : public PresNode
	{
		protected:
			PresTypedNode(T type);
			PresTypedNode(PresTypedNode const& o);
			virtual PresTypedNode& operator=(PresTypedNode const& o);
			virtual ~PresTypedNode();

		public:
			T type() const;
			virtual std::string str() const=0;

		private:
			void type(T type);
			T m_type;

	};

}}}}//end namespace omega::bindings::parser::ast

#endif
