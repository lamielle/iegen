#include "PresDepthFirstVisitor.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	PresDepthFirstVisitor::PresDepthFirstVisitor() : m_curr_node_name(),m_at_set_vars(false),m_at_in_vars(false),m_at_out_vars(false) {}

	PresDepthFirstVisitor::PresDepthFirstVisitor(PresDepthFirstVisitor const& o) : m_curr_node_name(o.curr_node_name()),m_at_set_vars(o.at_set_vars()),m_at_in_vars(o.at_in_vars()),m_at_out_vars(o.at_out_vars()) {}

	PresDepthFirstVisitor::PresDepthFirstVisitor& PresDepthFirstVisitor::operator=(PresDepthFirstVisitor const& o)
	{
		this->curr_node_name(o.curr_node_name());
		this->at_set_vars(false);
		this->at_in_vars(false);
		this->at_out_vars(false);
		return *this;
	}

	PresDepthFirstVisitor::~PresDepthFirstVisitor() {}

	std::string const& PresDepthFirstVisitor::curr_node_name() const {return this->m_curr_node_name;}
	void PresDepthFirstVisitor::curr_node_name(std::string const& curr_node_name) {this->m_curr_node_name=curr_node_name;}

	//Current variable tuple
	bool PresDepthFirstVisitor::at_set_vars() const {return this->m_at_set_vars;}
	void PresDepthFirstVisitor::at_set_vars(bool at_set_vars) {this->m_at_set_vars=at_set_vars;}

	bool PresDepthFirstVisitor::at_in_vars() const {return this->m_at_in_vars;}
	void PresDepthFirstVisitor::at_in_vars(bool at_in_vars) {this->m_at_in_vars=at_in_vars;}

	bool PresDepthFirstVisitor::at_out_vars() const {return this->m_at_out_vars;}
	void PresDepthFirstVisitor::at_out_vars(bool at_out_vars) {this->m_at_out_vars=at_out_vars;}

	bool PresDepthFirstVisitor::at_vars() const {return this->at_set_vars()||this->at_in_vars()||this->at_out_vars();}

	//---------- In/Out/Between methods ----------
	//Default in/out/between methods
	void PresDepthFirstVisitor::defaultIn(PresNode const& v) {}
	void PresDepthFirstVisitor::defaultOut(PresNode const& v) {}
	void PresDepthFirstVisitor::defaultBetween() {}

	//Set/Relation nodes
	void PresDepthFirstVisitor::inPresSet(PresSet const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresSet(PresSet const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresRelation(PresRelation const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresRelation(PresRelation const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::betweenPresVarTuplePresConstr() {this->defaultBetween();}
	void PresDepthFirstVisitor::betweenPresVarTuples() {this->defaultBetween();}

	//Variable tuple nodes
	void PresDepthFirstVisitor::inPresVarTupleSet(PresVarTupleSet const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresVarTupleSet(PresVarTupleSet const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresVarTupleIn(PresVarTupleIn const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresVarTupleIn(PresVarTupleIn const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresVarTupleOut(PresVarTupleOut const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresVarTupleOut(PresVarTupleOut const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::betweenPresVars() {this->defaultBetween();}

	//Variable nodes
	void PresDepthFirstVisitor::inPresVarID(PresVarID const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresVarID(PresVarID const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresVarUnnamed(PresVarUnnamed const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresVarUnnamed(PresVarUnnamed const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresVarRange(PresVarRange const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresVarRange(PresVarRange const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresVarStride(PresVarStride const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresVarStride(PresVarStride const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresVarExpr(PresVarExpr const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresVarExpr(PresVarExpr const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::betweenPresExprPresExprInt() {this->defaultBetween();}

	//Constraint nodes
	void PresDepthFirstVisitor::inPresConstrAnd(PresConstrAnd const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresConstrAnd(PresConstrAnd const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresConstrOr(PresConstrOr const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresConstrOr(PresConstrOr const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresConstrNot(PresConstrNot const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresConstrNot(PresConstrNot const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresConstrForall(PresConstrForall const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresConstrForall(PresConstrForall const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresConstrExists(PresConstrExists const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresConstrExists(PresConstrExists const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresConstrParen(PresConstrParen const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresConstrParen(PresConstrParen const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::betweenPresConstrs() {this->defaultBetween();}
	void PresDepthFirstVisitor::betweenPresConstrPresStmt(constr_vect const& v) {this->defaultBetween();}
	void PresDepthFirstVisitor::betweenPresVarsPresConstr(varid_vect const& v) {this->defaultBetween();}

	//Statement nodes
	void PresDepthFirstVisitor::inPresStmtEQ(PresStmtEQ const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresStmtEQ(PresStmtEQ const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresStmtNEQ(PresStmtNEQ const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresStmtNEQ(PresStmtNEQ const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresStmtGT(PresStmtGT const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresStmtGT(PresStmtGT const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresStmtGTE(PresStmtGTE const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresStmtGTE(PresStmtGTE const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresStmtLT(PresStmtLT const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresStmtLT(PresStmtLT const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresStmtLTE(PresStmtLTE const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresStmtLTE(PresStmtLTE const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::betweenPresStmts() {this->defaultBetween();}
	void PresDepthFirstVisitor::betweenPresStmtPresExpr() {this->defaultBetween();}

	//Expression nodes
	void PresDepthFirstVisitor::inPresExprInt(PresExprInt const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresExprInt(PresExprInt const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresExprID(PresExprID const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresExprID(PresExprID const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresExprNeg(PresExprNeg const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresExprNeg(PresExprNeg const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresExprAdd(PresExprAdd const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresExprAdd(PresExprAdd const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresExprSub(PresExprSub const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresExprSub(PresExprSub const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresExprMult(PresExprMult const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresExprMult(PresExprMult const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresExprList(PresExprList const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresExprList(PresExprList const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresExprFunc(PresExprFunc const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresExprFunc(PresExprFunc const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::inPresExprParen(PresExprParen const& v) {this->defaultIn(v);}
	void PresDepthFirstVisitor::outPresExprParen(PresExprParen const& v) {this->defaultOut(v);}

	void PresDepthFirstVisitor::betweenPresExprs() {this->defaultBetween();}
	void PresDepthFirstVisitor::betweenPresVarPresVars() {this->defaultBetween();}

	//---------- Visit methods ----------
	void PresDepthFirstVisitor::visit(sptr<IPresVisitable> const& v) {v->apply(*this);}

	void PresDepthFirstVisitor::visitPresNodes(PresNode const& v,node_vect const& nodes,void (PresDepthFirstVisitor::*between)(void))
	{
		node_vect::size_type num_nodes,curr_node;

		//Visit the nodes
		num_nodes=nodes.size();
		curr_node=0;
		foreach(sptr<PresNode> node,nodes)
		{
			node->apply(*this);
			if(num_nodes>1&&curr_node<num_nodes)
			{
				((*this).*(between))();
			}
			++curr_node;
		}
	}

	//Set/Relation nodes
	void PresDepthFirstVisitor::visitPresSet(PresSet const& v)
	{
		this->curr_node_name(v.name());
		this->inPresSet(v);

		//Visit the tuple variables
		v.set_vars()->apply(*this);

		this->betweenPresVarTuplePresConstr();

		//Visit the constraints
		v.constr()->apply(*this);

		this->curr_node_name(v.name());
		this->outPresSet(v);
	}

	void PresDepthFirstVisitor::visitPresRelation(PresRelation const& v)
	{
		this->curr_node_name(v.name());
		this->inPresRelation(v);

		//Visit the input tuple variables
		v.in_vars()->apply(*this);

		this->betweenPresVarTuples();

		//Visit the output tuple variables
		v.out_vars()->apply(*this);

		this->betweenPresVarTuplePresConstr();

		//Visit the constraints
		v.constr()->apply(*this);

		this->curr_node_name(v.name());
		this->outPresRelation(v);
	}

	template <typename T>
	void PresDepthFirstVisitor::visitPresVarTuple(T const& v,void (PresDepthFirstVisitor::*in)(T const&),void (PresDepthFirstVisitor::*out)(T const&))
	{
		this->curr_node_name(v.name());
		((*this).*(in))(v);

		this->visitPresNodes(v,get_pres_node_vector(v.vars()),&PresDepthFirstVisitor::betweenPresVars);

		this->curr_node_name(v.name());
		((*this).*(out))(v);
	}

	void PresDepthFirstVisitor::visitPresVarTupleSet(PresVarTupleSet const& v)
	{
		this->at_set_vars(true);
		this->visitPresVarTuple(v,&PresDepthFirstVisitor::inPresVarTupleSet,&PresDepthFirstVisitor::outPresVarTupleSet);
		this->at_set_vars(false);
	}

	void PresDepthFirstVisitor::visitPresVarTupleIn(PresVarTupleIn const& v)
	{
		this->at_in_vars(true);
		this->visitPresVarTuple(v,&PresDepthFirstVisitor::inPresVarTupleIn,&PresDepthFirstVisitor::outPresVarTupleIn);
		this->at_in_vars(false);
	}

	void PresDepthFirstVisitor::visitPresVarTupleOut(PresVarTupleOut const& v)
	{
		this->at_out_vars(true);
		this->visitPresVarTuple(v,&PresDepthFirstVisitor::inPresVarTupleOut,&PresDepthFirstVisitor::outPresVarTupleOut);
		this->at_out_vars(false);
	}

	//Variable nodes
	void PresDepthFirstVisitor::visitPresVarID(PresVarID const& v)
	{
		this->curr_node_name(v.name());
		this->inPresVarID(v);
		this->curr_node_name(v.name());
		this->outPresVarID(v);
	}

	void PresDepthFirstVisitor::visitPresVarUnnamed(PresVarUnnamed const& v)
	{
		this->curr_node_name(v.name());
		this->inPresVarUnnamed(v);
		this->curr_node_name(v.name());
		this->outPresVarUnnamed(v);
	}

	void PresDepthFirstVisitor::visitPresVarRange(PresVarRange const& v)
	{
		this->curr_node_name(v.name());
		this->inPresVarRange(v);

		//Visit the start expression
		v.start()->apply(*this);

		this->betweenPresExprs();

		//Visit the end expression
		v.end()->apply(*this);

		this->curr_node_name(v.name());
		this->outPresVarRange(v);
	}

	void PresDepthFirstVisitor::visitPresVarStride(PresVarStride const& v)
	{
		this->curr_node_name(v.name());
		this->inPresVarStride(v);

		//Visit the start expression
		v.start()->apply(*this);

		this->betweenPresExprs();

		//Visit the end expression
		v.end()->apply(*this);

		this->betweenPresExprPresExprInt();

		//Visit the stride
		v.stride()->apply(*this);

		this->curr_node_name(v.name());
		this->outPresVarStride(v);
	}

	void PresDepthFirstVisitor::visitPresVarExpr(PresVarExpr const& v)
	{
		this->curr_node_name(v.name());
		this->inPresVarExpr(v);

		//Visit the expression
		v.expr()->apply(*this);

		this->curr_node_name(v.name());
		this->outPresVarExpr(v);
	}

	//Constraint nodes
	template <typename T>
	void PresDepthFirstVisitor::visitPresConstrAndOr(T const& v,void (PresDepthFirstVisitor::*in)(T const&),void (PresDepthFirstVisitor::*out)(T const&))
	{
		this->curr_node_name(v.name());
		((*this).*(in))(v);

		//Visit each of the constraints
		this->visitPresNodes(v,get_pres_node_vector(v.constrs()),&PresDepthFirstVisitor::betweenPresConstrs);

		this->betweenPresConstrPresStmt(v.constrs());

		//Visit each of the statements
		this->visitPresNodes(v,get_pres_node_vector(v.stmts()),&PresDepthFirstVisitor::betweenPresStmts);

		this->curr_node_name(v.name());
		((*this).*(out))(v);
	}

	template <typename T>
	void PresDepthFirstVisitor::visitPresConstrExistsForall(T const& v,void (PresDepthFirstVisitor::*in)(T const&),void (PresDepthFirstVisitor::*out)(T const&))
	{
		this->curr_node_name(v.name());
		((*this).*(in))(v);

		this->visitPresNodes(v,get_pres_node_vector(v.vars()),&PresDepthFirstVisitor::betweenPresVars);

		this->betweenPresVarsPresConstr(v.vars());

		//Visit the constraint
		v.constr()->apply(*this);

		this->curr_node_name(v.name());
		((*this).*(out))(v);
	}

	void PresDepthFirstVisitor::visitPresConstrAnd(PresConstrAnd const& v)
	{
		this->visitPresConstrAndOr(v,&PresDepthFirstVisitor::inPresConstrAnd,&PresDepthFirstVisitor::outPresConstrAnd);
	}

	void PresDepthFirstVisitor::visitPresConstrOr(PresConstrOr const& v)
	{
		this->visitPresConstrAndOr(v,&PresDepthFirstVisitor::inPresConstrOr,&PresDepthFirstVisitor::outPresConstrOr);
	}

	void PresDepthFirstVisitor::visitPresConstrNot(PresConstrNot const& v)
	{
		this->curr_node_name(v.name());
		this->inPresConstrNot(v);

		//Visit the constraint
		v.constr()->apply(*this);

		this->curr_node_name(v.name());
		this->outPresConstrNot(v);
	}

	void PresDepthFirstVisitor::visitPresConstrForall(PresConstrForall const& v)
	{
		this->visitPresConstrExistsForall(v,&PresDepthFirstVisitor::inPresConstrForall,&PresDepthFirstVisitor::outPresConstrForall);
	}

	void PresDepthFirstVisitor::visitPresConstrExists(PresConstrExists const& v)
	{
		this->visitPresConstrExistsForall(v,&PresDepthFirstVisitor::inPresConstrExists,&PresDepthFirstVisitor::outPresConstrExists);
	}

	void PresDepthFirstVisitor::visitPresConstrParen(PresConstrParen const& v)
	{
		this->curr_node_name(v.name());
		this->inPresConstrParen(v);

		//Visit the constraint
		v.constr()->apply(*this);

		this->curr_node_name(v.name());
		this->outPresConstrParen(v);
	}

	//Statement nodes
	template <typename T>
	void PresDepthFirstVisitor::visitPresStmt(T const& v,void (PresDepthFirstVisitor::*in)(T const&),void (PresDepthFirstVisitor::*out)(T const&))
	{
		this->curr_node_name(v.name());
		((*this).*(in))(v);

		//Visit the left expression
		v.lexpr()->apply(*this);

		//Visit the right expression or statement
		if(v.has_rstmt())
		{
			this->betweenPresStmts();
			v.rstmt()->apply(*this);
		}
		else
		{
			this->betweenPresStmtPresExpr();
			v.rexpr()->apply(*this);
		}

		this->curr_node_name(v.name());
		((*this).*(out))(v);
	}

	void PresDepthFirstVisitor::visitPresStmtEQ(PresStmtEQ const& v)
	{
		this->visitPresStmt(v,&PresDepthFirstVisitor::inPresStmtEQ,&PresDepthFirstVisitor::outPresStmtEQ);
	}

	void PresDepthFirstVisitor::visitPresStmtNEQ(PresStmtNEQ const& v)
	{
		this->visitPresStmt(v,&PresDepthFirstVisitor::inPresStmtNEQ,&PresDepthFirstVisitor::outPresStmtNEQ);
	}

	void PresDepthFirstVisitor::visitPresStmtGT(PresStmtGT const& v)
	{
		this->visitPresStmt(v,&PresDepthFirstVisitor::inPresStmtGT,&PresDepthFirstVisitor::outPresStmtGT);
	}

	void PresDepthFirstVisitor::visitPresStmtGTE(PresStmtGTE const& v)
	{
		this->visitPresStmt(v,&PresDepthFirstVisitor::inPresStmtGTE,&PresDepthFirstVisitor::outPresStmtGTE);
	}

	void PresDepthFirstVisitor::visitPresStmtLT(PresStmtLT const& v)
	{
		this->visitPresStmt(v,&PresDepthFirstVisitor::inPresStmtLT,&PresDepthFirstVisitor::outPresStmtLT);
	}

	void PresDepthFirstVisitor::visitPresStmtLTE(PresStmtLTE const& v)
	{
		this->visitPresStmt(v,&PresDepthFirstVisitor::inPresStmtLTE,&PresDepthFirstVisitor::outPresStmtLTE);
	}

	//Expression nodes
	template <typename T>
	void PresDepthFirstVisitor::visitPresExprBinOp(T const& v,void (PresDepthFirstVisitor::*in)(T const&),void (PresDepthFirstVisitor::*out)(T const&))
	{
		this->curr_node_name(v.name());
		((*this).*(in))(v);

		//Visit the left expression
		v.lexpr()->apply(*this);

		this->betweenPresExprs();

		//Visit the right expression
		v.rexpr()->apply(*this);

		this->curr_node_name(v.name());
		((*this).*(out))(v);
	}

	void PresDepthFirstVisitor::visitPresExprInt(PresExprInt const& v)
	{
		this->curr_node_name(v.name());
		this->inPresExprInt(v);
		this->curr_node_name(v.name());
		this->outPresExprInt(v);
	}

	void PresDepthFirstVisitor::visitPresExprID(PresExprID const& v)
	{
		this->curr_node_name(v.name());
		this->inPresExprID(v);
		this->curr_node_name(v.name());
		this->outPresExprID(v);
	}

	void PresDepthFirstVisitor::visitPresExprNeg(PresExprNeg const& v)
	{
		this->curr_node_name(v.name());
		this->inPresExprNeg(v);

		//Visit the expression
		v.expr()->apply(*this);

		this->curr_node_name(v.name());
		this->outPresExprNeg(v);
	}

	void PresDepthFirstVisitor::visitPresExprAdd(PresExprAdd const& v)
	{
		this->visitPresExprBinOp(v,&PresDepthFirstVisitor::inPresExprAdd,&PresDepthFirstVisitor::outPresExprAdd);
	}

	void PresDepthFirstVisitor::visitPresExprSub(PresExprSub const& v)
	{
		this->visitPresExprBinOp(v,&PresDepthFirstVisitor::inPresExprSub,&PresDepthFirstVisitor::outPresExprSub);
	}

	void PresDepthFirstVisitor::visitPresExprMult(PresExprMult const& v)
	{
		this->visitPresExprBinOp(v,&PresDepthFirstVisitor::inPresExprMult,&PresDepthFirstVisitor::outPresExprMult);
	}

	void PresDepthFirstVisitor::visitPresExprList(PresExprList const& v)
	{
		this->curr_node_name(v.name());
		this->inPresExprList(v);

		this->visitPresNodes(v,get_pres_node_vector(v.exprs()),&PresDepthFirstVisitor::betweenPresExprs);

		this->curr_node_name(v.name());
		this->outPresExprList(v);
	}

	void PresDepthFirstVisitor::visitPresExprFunc(PresExprFunc const& v)
	{
		this->curr_node_name(v.name());
		this->inPresExprFunc(v);

		v.func_name()->apply(*this);

		this->betweenPresVarPresVars();

		this->visitPresNodes(v,get_pres_node_vector(v.args()),&PresDepthFirstVisitor::betweenPresVars);

		this->curr_node_name(v.name());
		this->outPresExprFunc(v);
	}

	void PresDepthFirstVisitor::visitPresExprParen(PresExprParen const& v)
	{
		this->curr_node_name(v.name());
		this->inPresExprParen(v);

		//Visit the constraint
		v.expr()->apply(*this);

		this->curr_node_name(v.name());
		this->outPresExprParen(v);
	}

}}}}}//end namespace omega::bindings::parser::ast::visitor
