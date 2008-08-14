#ifndef _OMEGA_BINDINGS_PARSER_AST_VISITOR_PRES_REPR_VISITOR_H_
#define _OMEGA_BINDINGS_PARSER_AST_VISITOR_PRES_REPR_VISITOR_H_

#include "PresUtil.hpp"
#include "PresDepthFirstVisitor.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	//Presburger AST visitor that prints an ASTs python representation
	class PresReprVisitor : public PresDepthFirstVisitor
	{
		public:
			PresReprVisitor();
			PresReprVisitor(PresReprVisitor const& o);
			PresReprVisitor& operator=(PresReprVisitor const& o);

			//Default in/out/between methods
			virtual void defaultIn(PresNode const& v);
			virtual void defaultOut(PresNode const& v);
			virtual void defaultBetween();

			//Set/Relation nodes
			virtual void inPresSet(PresSet const& v);
			virtual void outPresSet(PresSet const& v);

			virtual void inPresRelation(PresRelation const& v);
			virtual void outPresRelation(PresRelation const& v);

			//Variable tuple nodes
			virtual void inPresVarTupleSet(PresVarTupleSet const& v);
			virtual void outPresVarTupleSet(PresVarTupleSet const& v);

			virtual void inPresVarTupleIn(PresVarTupleIn const& v);
			virtual void outPresVarTupleIn(PresVarTupleIn const& v);

			virtual void inPresVarTupleOut(PresVarTupleOut const& v);
			virtual void outPresVarTupleOut(PresVarTupleOut const& v);

			//Variable nodes
		private:
			void inVar(PresVar const& v);
			void outVar();
		public:
			virtual void inPresVarID(PresVarID const& v);
			virtual void outPresVarID(PresVarID const& v);

			virtual void inPresVarUnnamed(PresVarUnnamed const& v);
			virtual void outPresVarUnnamed(PresVarUnnamed const& v);

			virtual void inPresVarRange(PresVarRange const& v);
			virtual void outPresVarRange(PresVarRange const& v);

			virtual void inPresVarStride(PresVarStride const& v);
			virtual void outPresVarStride(PresVarStride const& v);

			virtual void inPresVarExpr(PresVarExpr const& v);
			virtual void outPresVarExpr(PresVarExpr const& v);

			//Constraint nodes
			virtual void inPresConstrAnd(PresConstrAnd const& v);
			virtual void outPresConstrAnd(PresConstrAnd const& v);

			virtual void inPresConstrOr(PresConstrOr const& v);
			virtual void outPresConstrOr(PresConstrOr const& v);

			virtual void inPresConstrNot(PresConstrNot const& v);
			virtual void outPresConstrNot(PresConstrNot const& v);

			virtual void inPresConstrForall(PresConstrForall const& v);
			virtual void outPresConstrForall(PresConstrForall const& v);

			virtual void inPresConstrExists(PresConstrExists const& v);
			virtual void outPresConstrExists(PresConstrExists const& v);

			virtual void inPresConstrParen(PresConstrParen const& v);
			virtual void outPresConstrParen(PresConstrParen const& v);

			virtual void betweenPresConstrPresStmt(constr_vect const& v);
			virtual void betweenPresVarsPresConstr(varid_vect const& v);

			//Statement nodes
			virtual void inPresStmtEQ(PresStmtEQ const& v);
			virtual void outPresStmtEQ(PresStmtEQ const& v);

			virtual void inPresStmtNEQ(PresStmtNEQ const& v);
			virtual void outPresStmtNEQ(PresStmtNEQ const& v);

			virtual void inPresStmtGT(PresStmtGT const& v);
			virtual void outPresStmtGT(PresStmtGT const& v);

			virtual void inPresStmtGTE(PresStmtGTE const& v);
			virtual void outPresStmtGTE(PresStmtGTE const& v);

			virtual void inPresStmtLT(PresStmtLT const& v);
			virtual void outPresStmtLT(PresStmtLT const& v);

			virtual void inPresStmtLTE(PresStmtLTE const& v);
			virtual void outPresStmtLTE(PresStmtLTE const& v);

			//Expression nodes
			virtual void inPresExprInt(PresExprInt const& v);
			virtual void outPresExprInt(PresExprInt const& v);

			virtual void inPresExprID(PresExprID const& v);
			virtual void outPresExprID(PresExprID const& v);

			virtual void inPresExprNeg(PresExprNeg const& v);
			virtual void outPresExprNeg(PresExprNeg const& v);

			virtual void inPresExprAdd(PresExprAdd const& v);
			virtual void outPresExprAdd(PresExprAdd const& v);

			virtual void inPresExprSub(PresExprSub const& v);
			virtual void outPresExprSub(PresExprSub const& v);

			virtual void inPresExprMult(PresExprMult const& v);
			virtual void outPresExprMult(PresExprMult const& v);

			virtual void inPresExprList(PresExprList const& v);
			virtual void outPresExprList(PresExprList const& v);

			virtual void inPresExprFunc(PresExprFunc const& v);
			virtual void outPresExprFunc(PresExprFunc const& v);

			virtual void inPresExprParen(PresExprParen const& v);
			virtual void outPresExprParen(PresExprParen const& v);

			virtual void betweenPresVarPresVars();

			std::string str() const;

		private:
			std::stringstream& repr();
			void str(std::string const& str);
			std::stringstream m_repr;
	};

}}}}}//end namespace omega::bindings::parser::ast::visitor

#endif
