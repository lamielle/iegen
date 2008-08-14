#include "PresTransVisitor.hpp"
#include "Set.hpp"
#include "Relation.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	PresTransVisitor::PresTransVisitor() : PresDepthFirstVisitor(),m_curr_var(0),m_at_func(false),m_stmt_count(0) {}

	PresTransVisitor::PresTransVisitor(PresTransVisitor const& o) : PresDepthFirstVisitor(),m_curr_var(o.curr_var()),m_at_func(false),m_stmt_count(o.stmt_count()) {}

	PresTransVisitor::PresTransVisitor& PresTransVisitor::operator=(PresTransVisitor const& o)
	{
		this->PresTransVisitor::operator=(o);
		this->curr_var(o.curr_var());
		this->at_func(o.at_func());
		this->stmt_count(o.stmt_count());
		return *this;
	}

	std::string PresTransVisitor::str()
	{
		return this->formula()->str();
	}

	void PresTransVisitor::union_(PresTransVisitor const& o)
	{
		this->formula()->union_(o.formula());
	}

	//---------- Current variable members ----------
	int PresTransVisitor::curr_var() const {return this->m_curr_var;}
	void PresTransVisitor::curr_var(int curr_var) {this->m_curr_var=curr_var;}
	void PresTransVisitor::next_var() {this->curr_var(this->curr_var()+1);}
	//----------------------------------------------

	//---------- At function members ----------
	bool PresTransVisitor::at_func() const {return this->m_at_func;}
		void PresTransVisitor::at_func(bool at_func) {this->m_at_func=at_func;}
	//-----------------------------------------

	//---------- Current statement members ----------
	void PresTransVisitor::next_stmt() {this->stmt_count(this->stmt_count()+1);}
	void PresTransVisitor::prev_stmt() {this->stmt_count(this->stmt_count()-1);}
	int PresTransVisitor::stmt_count() const {return this->m_stmt_count;}
	void PresTransVisitor::stmt_count(int stmt_count) {this->m_stmt_count=stmt_count;}
	//-----------------------------------------------

	//---------- Visitor members ----------
	//Default in/out/between methods
	void PresTransVisitor::defaultIn(PresNode const& v) {}
	void PresTransVisitor::defaultOut(PresNode const& v) {}
	void PresTransVisitor::defaultBetween() {}

	//Set/Relation nodes
	void PresTransVisitor::inPresSet(PresSet const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresSet(PresSet const& v) {this->defaultOut(v);}

	void PresTransVisitor::inPresRelation(PresRelation const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresRelation(PresRelation const& v) {this->defaultOut(v);}

	void PresTransVisitor::betweenPresVarTuplePresConstr() {this->defaultBetween();}

	//Variable tuple nodes
	void PresTransVisitor::inPresVarTupleSet(PresVarTupleSet const& v)
	{
		this->curr_var(1);
	}
	void PresTransVisitor::outPresVarTupleSet(PresVarTupleSet const& v) {}

	void PresTransVisitor::inPresVarTupleIn(PresVarTupleIn const& v)
	{
		this->curr_var(1);
	}
	void PresTransVisitor::outPresVarTupleIn(PresVarTupleIn const& v) {this->defaultOut(v);}

	void PresTransVisitor::inPresVarTupleOut(PresVarTupleOut const& v)
	{
		this->curr_var(1);
	}
	void PresTransVisitor::outPresVarTupleOut(PresVarTupleOut const& v) {this->defaultOut(v);}

	//Variable nodes
	void PresTransVisitor::inPresVarID(PresVarID const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresVarID(PresVarID const& v) {this->defaultOut(v);}

	//Do nothing (no name to set)
	void PresTransVisitor::inPresVarUnnamed(PresVarUnnamed const& v) {this->next_var();}
	void PresTransVisitor::outPresVarUnnamed(PresVarUnnamed const& v) {}

	void PresTransVisitor::inPresVarRange(PresVarRange const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresVarRange(PresVarRange const& v) {this->defaultOut(v);}

	void PresTransVisitor::inPresVarStride(PresVarStride const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresVarStride(PresVarStride const& v) {this->defaultOut(v);}

	void PresTransVisitor::inPresVarExpr(PresVarExpr const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresVarExpr(PresVarExpr const& v) {this->defaultOut(v);}

	//Constraint nodes
	void PresTransVisitor::inPresConstrAnd(PresConstrAnd const& v) {if(!v.empty()) this->formula()->push_and();}
	void PresTransVisitor::outPresConstrAnd(PresConstrAnd const& v) {if(!v.empty()) this->formula()->pop_formula();}

	void PresTransVisitor::inPresConstrOr(PresConstrOr const& v) {if(!v.empty()) this->formula()->push_or();}
	void PresTransVisitor::outPresConstrOr(PresConstrOr const& v) {if(!v.empty()) this->formula()->pop_formula();}

	void PresTransVisitor::inPresConstrNot(PresConstrNot const& v) {if(!v.empty()) this->formula()->push_not();}
	void PresTransVisitor::outPresConstrNot(PresConstrNot const& v) {if(!v.empty()) this->formula()->pop_formula();}

	void PresTransVisitor::inPresConstrForall(PresConstrForall const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresConstrForall(PresConstrForall const& v) {this->defaultOut(v);}

	void PresTransVisitor::inPresConstrExists(PresConstrExists const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresConstrExists(PresConstrExists const& v) {this->defaultOut(v);}

	void PresTransVisitor::inPresConstrParen(PresConstrParen const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresConstrParen(PresConstrParen const& v) {this->defaultOut(v);}

	void PresTransVisitor::betweenPresConstrPresStmt(constr_vect const& v) {}
	void PresTransVisitor::betweenPresVarsPresConstr(varid_vect const& v) {}

	//Statement nodes
	void PresTransVisitor::inPresStmt() {this->next_stmt();}

	void PresTransVisitor::outPresStmt()
	{
		this->prev_stmt();
		if(this->stmt_count()<0)
			throw OmegaException("Statement count should always be >=0!");
		if(0==this->stmt_count())
			this->formula()->pop_expr();
	}

	void PresTransVisitor::inPresStmtEQ(PresStmtEQ const& v) {this->inPresStmt();}
	void PresTransVisitor::outPresStmtEQ(PresStmtEQ const& v) {this->formula()->add_eq(); this->outPresStmt();}

	void PresTransVisitor::inPresStmtNEQ(PresStmtNEQ const& v) {this->inPresStmt();}
	void PresTransVisitor::outPresStmtNEQ(PresStmtNEQ const& v) {this->formula()->add_neq(); this->outPresStmt();}

	void PresTransVisitor::inPresStmtGT(PresStmtGT const& v) {this->inPresStmt();}
	void PresTransVisitor::outPresStmtGT(PresStmtGT const& v) {this->formula()->add_gt(); this->outPresStmt();}

	void PresTransVisitor::inPresStmtGTE(PresStmtGTE const& v) {this->inPresStmt();}
	void PresTransVisitor::outPresStmtGTE(PresStmtGTE const& v) {this->formula()->add_gte(); this->outPresStmt();}

	void PresTransVisitor::inPresStmtLT(PresStmtLT const& v) {this->inPresStmt();}
	void PresTransVisitor::outPresStmtLT(PresStmtLT const& v) {this->formula()->add_lt(); this->outPresStmt();}

	void PresTransVisitor::inPresStmtLTE(PresStmtLTE const& v) {this->inPresStmt();}
	void PresTransVisitor::outPresStmtLTE(PresStmtLTE const& v) {this->formula()->add_lte(); this->outPresStmt();}

	//Expression nodes
	void PresTransVisitor::inPresExprInt(PresExprInt const& v) {this->formula()->push_int(v);}
	void PresTransVisitor::outPresExprInt(PresExprInt const& v) {}

	void PresTransVisitor::inPresExprID(PresExprID const& v) {this->formula()->push_id(v);}
	void PresTransVisitor::outPresExprID(PresExprID const& v) {}

	void PresTransVisitor::inPresExprNeg(PresExprNeg const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresExprNeg(PresExprNeg const& v) {this->defaultOut(v);}

	void PresTransVisitor::inPresExprAdd(PresExprAdd const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresExprAdd(PresExprAdd const& v) {this->defaultOut(v);}

	void PresTransVisitor::inPresExprSub(PresExprSub const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresExprSub(PresExprSub const& v) {this->defaultOut(v);}

	void PresTransVisitor::inPresExprMult(PresExprMult const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresExprMult(PresExprMult const& v)
	{
		this->defaultOut(v);
	}

	void PresTransVisitor::inPresExprList(PresExprList const& v)
	{
		this->defaultIn(v);
	}
	void PresTransVisitor::outPresExprList(PresExprList const& v)
	{
		this->defaultOut(v);
	}


	void PresTransVisitor::inPresExprFunc(PresExprFunc const& v)
	{
		this->at_func(true);
		this->formula()->push_func(v);
	}
	void PresTransVisitor::outPresExprFunc(PresExprFunc const& v) {this->at_func(false);}

	void PresTransVisitor::inPresExprParen(PresExprParen const& v) {this->defaultIn(v);}
	void PresTransVisitor::outPresExprParen(PresExprParen const& v) {this->defaultOut(v);}

	void PresTransVisitor::betweenPresVarPresVars()
	{
	}
	//-------------------------------------

}}}}}//end namespace omega::bindings::parser::ast::visitor
