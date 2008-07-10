#ifndef _OMEGA_BINDINGS_PARSER_AST_VISITOR_PRES_DEPTH_FIRST_VISITOR_H_
#define _OMEGA_BINDINGS_PARSER_AST_VISITOR_PRES_DEPTH_FIRST_VISITOR_H_

#include "PresUtil.hpp"

#include "IPresVisitor.hpp"
#include "PresDepthFirstVisitor.hpp"

#include "IPresVisitable.hpp"
#include "PresNode.hpp"
#include "PresTypedNode.hpp"

#include "PresFormula.hpp"
#include "PresSet.hpp"
#include "PresRelation.hpp"

#include "PresVarTupleSet.hpp"
#include "PresVarTupleIn.hpp"
#include "PresVarTupleOut.hpp"

#include "PresVar.hpp"
#include "PresVarID.hpp"
#include "PresVarUnnamed.hpp"
#include "PresVarExpr.hpp"
#include "PresVarRange.hpp"
#include "PresVarStride.hpp"

#include "PresConstr.hpp"
#include "PresConstrAndOr.hpp"
#include "PresConstrAnd.hpp"
#include "PresConstrOr.hpp"
#include "PresConstrNot.hpp"
#include "PresConstrExistsForall.hpp"
#include "PresConstrExists.hpp"
#include "PresConstrForall.hpp"
#include "PresConstrParen.hpp"

#include "PresStmt.hpp"
#include "PresStmtEQ.hpp"
#include "PresStmtNEQ.hpp"
#include "PresStmtGT.hpp"
#include "PresStmtGTE.hpp"
#include "PresStmtLT.hpp"
#include "PresStmtLTE.hpp"

#include "PresExpr.hpp"
#include "PresExprInt.hpp"
#include "PresExprID.hpp"
#include "PresExprUnOp.hpp"
#include "PresExprNeg.hpp"
#include "PresExprBinOp.hpp"
#include "PresExprAdd.hpp"
#include "PresExprSub.hpp"
#include "PresExprMult.hpp"
#include "PresExprFunc.hpp"
#include "PresExprList.hpp"
#include "PresExprParen.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	//Depth first Presburger AST visitor
	class PresDepthFirstVisitor : public IPresVisitor
	{
		public:
			PresDepthFirstVisitor();
			PresDepthFirstVisitor(PresDepthFirstVisitor const& o);
			PresDepthFirstVisitor& operator=(PresDepthFirstVisitor const& o);
			virtual ~PresDepthFirstVisitor();

			//---------- In/Out/Between methods ----------
			//These methods should be overridden as needed
			virtual void defaultIn(PresNode const& v);
			virtual void defaultOut(PresNode const& v);
			virtual void defaultBetween();

			//Set/Relation nodes
			virtual void inPresSet(PresSet const& v);
			virtual void outPresSet(PresSet const& v);

			virtual void inPresRelation(PresRelation const& v);
			virtual void outPresRelation(PresRelation const& v);

			virtual void betweenPresVarTuplePresConstr();
			virtual void betweenPresVarTuples();

			//Variable tuple nodes
			virtual void inPresVarTupleSet(PresVarTupleSet const& v);
			virtual void outPresVarTupleSet(PresVarTupleSet const& v);

			virtual void inPresVarTupleIn(PresVarTupleIn const& v);
			virtual void outPresVarTupleIn(PresVarTupleIn const& v);

			virtual void inPresVarTupleOut(PresVarTupleOut const& v);
			virtual void outPresVarTupleOut(PresVarTupleOut const& v);

			virtual void betweenPresVars();

			//Variable nodes
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

			virtual void betweenPresExprPresExprInt();

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

			virtual void betweenPresConstrs();
			virtual void betweenPresConstrPresStmt(constr_vect const& v);
			virtual void betweenPresVarsPresConstr(varid_vect const& vars);

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

			virtual void betweenPresStmts();
			virtual void betweenPresStmtPresExpr();

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

			virtual void betweenPresExprs();
			virtual void betweenPresVarPresVars();

			//---------- Visit methods ----------
			void visit(sptr<IPresVisitable> const& v);

			void visitPresNodes(PresNode const& v,node_vect const& nodes,void (PresDepthFirstVisitor::*between)(void));

			//Set/Relation nodes
			void visitPresSet(PresSet const& v);
			void visitPresRelation(PresRelation const& v);

			//Variable tuple nodes
			void visitPresVars(PresNode const& v,var_vect const& vars);
			void visitPresVars(PresNode const& v,varid_vect const& vars);
			template <typename T>
			void visitPresVarTuple(T const& v,void (PresDepthFirstVisitor::*in)(T const&),void (PresDepthFirstVisitor::*out)(T const&));
			void visitPresVarTupleSet(PresVarTupleSet const& v);
			void visitPresVarTupleIn(PresVarTupleIn const& v);
			void visitPresVarTupleOut(PresVarTupleOut const& v);

			//Variable nodes
			void visitPresVarID(PresVarID const& v);
			void visitPresVarUnnamed(PresVarUnnamed const& v);
			void visitPresVarRange(PresVarRange const& v);
			void visitPresVarStride(PresVarStride const& v);
			void visitPresVarExpr(PresVarExpr const& v);

			//Constraint nodes
		private:
			template <typename T>
			void visitPresConstrAndOr(T const& v,void (PresDepthFirstVisitor::*in)(T const&),void (PresDepthFirstVisitor::*out)(T const&));
			template <typename T>
			void visitPresConstrExistsForall(T const& v,void (PresDepthFirstVisitor::*in)(T const&),void (PresDepthFirstVisitor::*out)(T const&));
		public:
			void visitPresConstrAnd(PresConstrAnd const& v);
			void visitPresConstrOr(PresConstrOr const& v);
			void visitPresConstrNot(PresConstrNot const& v);
			void visitPresConstrForall(PresConstrForall const& v);
			void visitPresConstrExists(PresConstrExists const& v);
			void visitPresConstrParen(PresConstrParen const& v);

			//Statement nodes
		private:
			template <typename T>
			void visitPresStmt(T const& v,void (PresDepthFirstVisitor::*in)(T const&),void (PresDepthFirstVisitor::*out)(T const&));
		public:
			void visitPresStmtEQ(PresStmtEQ const& v);
			void visitPresStmtNEQ(PresStmtNEQ const& v);
			void visitPresStmtGT(PresStmtGT const& v);
			void visitPresStmtGTE(PresStmtGTE const& v);
			void visitPresStmtLT(PresStmtLT const& v);
			void visitPresStmtLTE(PresStmtLTE const& v);

			//Expression nodes
		private:
			void visitPresExprs(PresNode const& v,expr_vect const& exprs);
			template <typename T>
			void visitPresExprBinOp(T const& v,void (PresDepthFirstVisitor::*in)(T const&),void (PresDepthFirstVisitor::*out)(T const&));
		public:
			void visitPresExprInt(PresExprInt const& v);
			void visitPresExprID(PresExprID const& v);
			void visitPresExprNeg(PresExprNeg const& v);
			void visitPresExprAdd(PresExprAdd const& v);
			void visitPresExprSub(PresExprSub const& v);
			void visitPresExprMult(PresExprMult const& v);
			void visitPresExprList(PresExprList const& v);
			void visitPresExprFunc(PresExprFunc const& v);
			void visitPresExprParen(PresExprParen const& v);

		protected:
			std::string const& curr_node_name() const;
			void curr_node_name(std::string const& curr_node_name);
			std::string m_curr_node_name;

			//Current variable tuple
			bool at_set_vars() const;
			void at_set_vars(bool at_set_vars);
			bool at_in_vars() const;
			void at_in_vars(bool at_in_vars);
			bool at_out_vars() const;
			void at_out_vars(bool at_out_vars);
			bool at_vars() const;

			bool m_at_set_vars,m_at_in_vars,m_at_out_vars;
	};

}}}}}//end namespace omega::bindings::parser::ast::visitor

#endif
