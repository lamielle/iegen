#include "PresReprVisitor.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	PresReprVisitor::PresReprVisitor() : PresDepthFirstVisitor() {}

	PresReprVisitor::PresReprVisitor(PresReprVisitor const& o)
	{
		this->str(o.str());
	}

	PresReprVisitor::PresReprVisitor& PresReprVisitor::operator=(PresReprVisitor const& o)
	{
		this->PresReprVisitor::operator=(o);
		this->str(o.str());
		return *this;
	}

	std::stringstream& PresReprVisitor::repr() {return this->m_repr;}
	std::string PresReprVisitor::str() const {return this->m_repr.str();}
	void PresReprVisitor::str(std::string const& str)
	{
		this->repr().str(str);
	}

	//Default in/out/between methods
	void PresReprVisitor::defaultIn(PresNode const& v)
	{
		this->repr()<<v.name()<<".new(";
	}
	void PresReprVisitor::defaultOut(PresNode const& v)
	{
		this->repr()<<")";
	}
	void PresReprVisitor::defaultBetween() {this->repr()<<",";}

	//Set/Relation nodes
	void PresReprVisitor::inPresSet(PresSet const& v) {this->str(""); this->defaultIn(v);}
	void PresReprVisitor::outPresSet(PresSet const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresRelation(PresRelation const& v) {this->str(""); this->defaultIn(v);}
	void PresReprVisitor::outPresRelation(PresRelation const& v) {this->defaultOut(v);}

	//Variable tuple nodes
	void PresReprVisitor::inPresVarTupleSet(PresVarTupleSet const& v)
	{
		this->defaultIn(v);
		this->repr()<<"(";
	}
	void PresReprVisitor::outPresVarTupleSet(PresVarTupleSet const& v)
	{
		if(1==v.vars().size())
			this->repr()<<",";
		this->repr()<<")";
		this->defaultOut(v);
	}

	void PresReprVisitor::inPresVarTupleIn(PresVarTupleIn const& v)
	{
		this->defaultIn(v);
		this->repr()<<"(";
	}
	void PresReprVisitor::outPresVarTupleIn(PresVarTupleIn const& v)
	{
		if(1==v.vars().size())
			this->repr()<<",";
		this->repr()<<")";
		this->defaultOut(v);
	}

	void PresReprVisitor::inPresVarTupleOut(PresVarTupleOut const& v)
	{
		this->defaultIn(v);
		this->repr()<<"(";
	}
	void PresReprVisitor::outPresVarTupleOut(PresVarTupleOut const& v)
	{
		if(1==v.vars().size())
			this->repr()<<",";
		this->repr()<<")";
		this->defaultOut(v);
	}

	//Variable nodes
	void PresReprVisitor::inPresVarID(PresVarID const& v)
	{
		this->defaultIn(v);
		this->repr()<<"\""<<v.id()<<"\"";
	}
	void PresReprVisitor::outPresVarID(PresVarID const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresVarUnnamed(PresVarUnnamed const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresVarUnnamed(PresVarUnnamed const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresVarRange(PresVarRange const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresVarRange(PresVarRange const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresVarStride(PresVarStride const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresVarStride(PresVarStride const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresVarExpr(PresVarExpr const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresVarExpr(PresVarExpr const& v) {this->defaultOut(v);}

	//Constraint nodes
	void PresReprVisitor::inPresConstrAnd(PresConstrAnd const& v)
	{
		this->defaultIn(v);
		this->repr()<<"(";
	}
	void PresReprVisitor::outPresConstrAnd(PresConstrAnd const& v)
	{
		if(1==v.stmts().size())
			this->repr()<<",";
		this->repr()<<")";
		this->defaultOut(v);
	}

	void PresReprVisitor::inPresConstrOr(PresConstrOr const& v)
	{
		this->defaultIn(v);
		this->repr()<<"(";
	}
	void PresReprVisitor::outPresConstrOr(PresConstrOr const& v)
	{
		if(1==v.stmts().size())
			this->repr()<<",";
		this->repr()<<")";
		this->defaultOut(v);
	}

	void PresReprVisitor::inPresConstrNot(PresConstrNot const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresConstrNot(PresConstrNot const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresConstrForall(PresConstrForall const& v)
	{
		this->defaultIn(v);
		this->repr()<<"(";
	}
	void PresReprVisitor::outPresConstrForall(PresConstrForall const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresConstrExists(PresConstrExists const& v)
	{
		this->defaultIn(v);
		this->repr()<<"(";
	}
	void PresReprVisitor::outPresConstrExists(PresConstrExists const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresConstrParen(PresConstrParen const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresConstrParen(PresConstrParen const& v) {this->defaultOut(v);}

	void PresReprVisitor::betweenPresConstrPresStmt(constr_vect const& v)
	{
		if(1==v.size())
			this->repr()<<",";
		this->repr()<<"),(";
	}
	void PresReprVisitor::betweenPresVarsPresConstr(varid_vect const& v)
	{
		if(1==v.size())
			this->repr()<<",";
		this->repr()<<"),";
	}

	//Statement nodes
	void PresReprVisitor::inPresStmtEQ(PresStmtEQ const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresStmtEQ(PresStmtEQ const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresStmtNEQ(PresStmtNEQ const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresStmtNEQ(PresStmtNEQ const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresStmtGT(PresStmtGT const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresStmtGT(PresStmtGT const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresStmtGTE(PresStmtGTE const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresStmtGTE(PresStmtGTE const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresStmtLT(PresStmtLT const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresStmtLT(PresStmtLT const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresStmtLTE(PresStmtLTE const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresStmtLTE(PresStmtLTE const& v) {this->defaultOut(v);}


	//Expression nodes
	void PresReprVisitor::inPresExprInt(PresExprInt const& v)
	{
		this->defaultIn(v);
		this->repr()<<v.value();
	}
	void PresReprVisitor::outPresExprInt(PresExprInt const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresExprID(PresExprID const& v)
	{
		this->defaultIn(v);
		this->repr()<<"\""<<v.id()<<"\"";
	}
	void PresReprVisitor::outPresExprID(PresExprID const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresExprNeg(PresExprNeg const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresExprNeg(PresExprNeg const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresExprAdd(PresExprAdd const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresExprAdd(PresExprAdd const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresExprSub(PresExprSub const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresExprSub(PresExprSub const& v) {this->defaultOut(v);}

	void PresReprVisitor::inPresExprMult(PresExprMult const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresExprMult(PresExprMult const& v)
	{
		if(v.simple())
			this->repr()<<",True";
		this->defaultOut(v);
	}

	void PresReprVisitor::inPresExprList(PresExprList const& v)
	{
		this->defaultIn(v);
		this->repr()<<"(";
	}
	void PresReprVisitor::outPresExprList(PresExprList const& v)
	{
		if(1==v.exprs().size())
			this->repr()<<",";
		this->repr()<<")";
		this->defaultOut(v);
	}

	void PresReprVisitor::inPresExprFunc(PresExprFunc const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresExprFunc(PresExprFunc const& v)
	{
		if(1==v.args().size())
			this->repr()<<",";
		this->repr()<<")";
		this->defaultOut(v);
	}

	void PresReprVisitor::inPresExprParen(PresExprParen const& v) {this->defaultIn(v);}
	void PresReprVisitor::outPresExprParen(PresExprParen const& v) {this->defaultOut(v);}

	void PresReprVisitor::betweenPresVarPresVars()
	{
		this->repr()<<",(";
	}

}}}}}//end namespace omega::bindings::parser::ast::visitor
