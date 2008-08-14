#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_STMT_LT_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_STMT_LT_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresStmt.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger LT AST node
	class PresStmtLT : public PresStmt
	{
		public:
			PresStmtLT(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr);
			static sptr<PresStmtLT> new_(sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt);
			static sptr<PresStmtLT> new_(sptr<PresExpr> const& lexpr,sptr<PresExpr> const& rexpr);
			PresStmtLT(PresStmtLT const& o);
			PresStmtLT& operator=(PresStmtLT const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			virtual std::string op() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
