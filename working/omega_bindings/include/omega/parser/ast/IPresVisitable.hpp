#ifndef _OMEGA_BINDINGS_PARSER_AST_VISITOR_I_PRES_VISITABLE_H_
#define _OMEGA_BINDINGS_PARSER_AST_VISITOR_I_PRES_VISITABLE_H_

#include "PresUtil.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	//AST visitor interface
	class IPresVisitable
	{
		public:
			virtual void apply(IPresVisitor& v)=0;
			virtual ~IPresVisitable()=0;
	};

}}}}}//end namespace omega::bindings::parser::ast::visitor

#endif
