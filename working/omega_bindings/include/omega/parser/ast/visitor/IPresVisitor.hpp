#ifndef _OMEGA_BINDINGS_PARSER_AST_VISITOR_I_PRES_VISITOR_H_
#define _OMEGA_BINDINGS_PARSER_AST_VISITOR_I_PRES_VISITOR_H_

#include "PresUtil.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	//Visitable AST node interface
	class IPresVisitor
	{
		public:
			virtual ~IPresVisitor()=0;

			virtual void visit(sptr<IPresVisitable> const& v)=0;

			//Set/Relation nodes
			virtual void visitPresSet(PresSet const& v)=0;
			virtual void visitPresRelation(PresRelation const& v)=0;

			//Variable tuple nodes
			virtual void visitPresVarTupleSet(PresVarTupleSet const& v)=0;
			virtual void visitPresVarTupleIn(PresVarTupleIn const& v)=0;
			virtual void visitPresVarTupleOut(PresVarTupleOut const& v)=0;

			//Variable nodes
			virtual void visitPresVarID(PresVarID const& v)=0;
			virtual void visitPresVarUnnamed(PresVarUnnamed const& v)=0;
			virtual void visitPresVarRange(PresVarRange const& v)=0;
			virtual void visitPresVarStride(PresVarStride const& v)=0;
			virtual void visitPresVarExpr(PresVarExpr const& v)=0;

			//Constraint nodes
			virtual void visitPresConstrAnd(PresConstrAnd const& v)=0;
			virtual void visitPresConstrOr(PresConstrOr const& v)=0;
			virtual void visitPresConstrNot(PresConstrNot const& v)=0;
			virtual void visitPresConstrForall(PresConstrForall const& v)=0;
			virtual void visitPresConstrExists(PresConstrExists const& v)=0;
			virtual void visitPresConstrParen(PresConstrParen const& v)=0;

			//Statement nodes
			virtual void visitPresStmtEQ(PresStmtEQ const& v)=0;
			virtual void visitPresStmtNEQ(PresStmtNEQ const& v)=0;
			virtual void visitPresStmtGT(PresStmtGT const& v)=0;
			virtual void visitPresStmtGTE(PresStmtGTE const& v)=0;
			virtual void visitPresStmtLT(PresStmtLT const& v)=0;
			virtual void visitPresStmtLTE(PresStmtLTE const& v)=0;

			//Expression nodes
			virtual void visitPresExprInt(PresExprInt const& v)=0;
			virtual void visitPresExprID(PresExprID const& v)=0;
			virtual void visitPresExprNeg(PresExprNeg const& v)=0;
			virtual void visitPresExprAdd(PresExprAdd const& v)=0;
			virtual void visitPresExprSub(PresExprSub const& v)=0;
			virtual void visitPresExprMult(PresExprMult const& v)=0;
			virtual void visitPresExprList(PresExprList const& v)=0;
			virtual void visitPresExprFunc(PresExprFunc const& v)=0;
			virtual void visitPresExprParen(PresExprParen const& v)=0;
	};

}}}}}//end namespace omega::bindings::parser::ast::visitor

#endif
