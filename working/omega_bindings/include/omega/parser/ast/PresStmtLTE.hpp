#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_STMT_LTE_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_STMT_LTE_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresStmt.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger LTE AST node
	class PresStmtLTE : public PresStmt
	{
		public:
			PresStmtLTE(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr);
			static sptr<PresStmtLTE> new_(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt);
			static sptr<PresStmtLTE> new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr);
			PresStmtLTE(PresStmtLTE const& o);
			PresStmtLTE& operator=(PresStmtLTE const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			virtual std::string op() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
