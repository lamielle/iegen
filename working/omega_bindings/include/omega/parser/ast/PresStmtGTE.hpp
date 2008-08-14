#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_STMT_GTE_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_STMT_GTE_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresStmt.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger GTE AST node
	class PresStmtGTE : public PresStmt
	{
		public:
			PresStmtGTE(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr);
			static sptr<PresStmtGTE> new_(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt);
			static sptr<PresStmtGTE> new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr);
			PresStmtGTE(PresStmtGTE const& o);
			PresStmtGTE& operator=(PresStmtGTE const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			virtual std::string op() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
