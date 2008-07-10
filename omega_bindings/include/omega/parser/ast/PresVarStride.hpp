#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_STRIDE_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_STRIDE_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVar.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger VarStride AST node
	class PresVarStride : public PresVar
	{
		public:
			PresVarStride(sptr<PresExpr> const& start,sptr<PresExpr> const& end,sptr<PresExprInt> const& stride);
			static sptr<PresVarStride> new_(sptr<PresExpr> const& start,sptr<PresExpr> const& end,sptr<PresExprInt> const& stride);
			PresVarStride(PresVarStride const& o);
			PresVarStride& operator=(PresVarStride const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			sptr<PresExpr> start() const;
			sptr<PresExpr> end() const;
			sptr<PresExprInt> stride() const;

			void apply(IPresVisitor& v);

		private:
			void start(sptr<PresExpr> const& start);
			void end(sptr<PresExpr> const& end);
			void stride(sptr<PresExprInt> const& stride);
			sptr<PresExpr> m_start,m_end;
			sptr<PresExprInt> m_stride;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
