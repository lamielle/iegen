#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_ID_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_ID_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger ID AST node
	class PresExprID : public PresExpr
	{
		public:
			PresExprID(std::string const& id);
			static sptr<PresExprID> new_(std::string const& id);
			PresExprID(PresExprID const& o);
			PresExprID& operator=(PresExprID const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			std::string id() const;

			void apply(IPresVisitor& v);

		private:
			void id(std::string const& id);
			std::string m_id;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
