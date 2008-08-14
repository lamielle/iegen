#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_STMT_NEQ_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_STMT_NEQ_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresStmt.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger NEQ AST node
	class PresStmtNEQ : public PresStmt
	{
		public:
			PresStmtNEQ(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr);
			static sptr<PresStmtNEQ> new_(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt);
			static sptr<PresStmtNEQ> new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr);
			PresStmtNEQ(PresStmtNEQ const& o);
			PresStmtNEQ& operator=(PresStmtNEQ const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			virtual std::string op() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
