#ifndef _OMEGA_BINDINGS_PARSER_AST_VISITOR_PRES_TRANS_SET_VISITOR_H_
#define _OMEGA_BINDINGS_PARSER_AST_VISITOR_PRES_TRANS_SET_VISITOR_H_

#include "PresUtil.hpp"
#include "PresTransVisitor.hpp"
#include "Set.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	//Presburger AST visitor that prints an ASTs python representation
	class PresTransSetVisitor : public PresTransVisitor
	{
		public:
			PresTransSetVisitor();
			PresTransSetVisitor(PresTransSetVisitor const& o);
			PresTransSetVisitor& operator=(PresTransSetVisitor const& o);

			//Set nodes
			virtual void inPresSet(PresSet const& v);
			virtual void outPresSet(PresSet const& v);

			//Variable nodes
			virtual void inPresVarID(PresVarID const& v);
			virtual void outPresVarID(PresVarID const& v);

			sptr<Set> set() const;
			virtual sptr<Formula> formula() const;

		private:
			void set(sptr<Set> const& set);

			sptr<Set> m_set;
	};

}}}}}//end namespace omega::bindings::parser::ast::visitor

#endif
