#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_RANGE_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_RANGE_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVar.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger VarRange AST node
	class PresVarRange : public PresVar
	{
		public:
			PresVarRange(sptr<PresExpr> const& start,sptr<PresExpr> const& end);
			static sptr<PresVarRange> new_(sptr<PresExpr> const& start,sptr<PresExpr> const& end);
			PresVarRange(PresVarRange const& o);
			PresVarRange& operator=(PresVarRange const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			sptr<PresExpr> start() const;
			sptr<PresExpr> end() const;

			void apply(IPresVisitor& v);

		private:
			void start(sptr<PresExpr> const& start);
			void end(sptr<PresExpr> const& end);
			sptr<PresExpr> m_start,m_end;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
