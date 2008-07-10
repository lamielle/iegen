#include <boost/python.hpp>
#include <omega.h>
#include "util.hpp"
#include "Formula.hpp"
#include "util.hpp"
#include "OmegaException.hpp"
#include "PresExprNorm.hpp"
#include "PresExprInt.hpp"
#include "PresExprID.hpp"
#include "PresExprFunc.hpp"
#include "PresVarID.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	Formula::~Formula() {}

	Formula::Formula(int arity) : m_relation(omega::Relation(arity)),m_free_vars(),m_funcs(),m_formula_stack(),m_expr_stack()
	{
		if(arity<0)
			throw OmegaException("Tuples must have arity greater than or equal to 0.");
	}

	Formula::Formula(int arity_in,int arity_out) : m_relation(Relation(arity_in,arity_out)),m_free_vars(),m_funcs(),m_formula_stack(),m_expr_stack()
	{
		if(arity_in<0||arity_out<0)
			throw OmegaException("Tuples must have arity greater than or equal to 0.");
	}

	Formula::Formula(Formula const& o) : m_relation(omega::copy(o.const_relation())),m_free_vars(o.const_free_vars()),m_funcs(o.const_funcs()),m_formula_stack(o.const_formula_stack()),m_expr_stack(o.const_expr_stack()) {}

	Formula& Formula::operator=(Formula const& o)
	{
		this->relation(o.const_relation());
		this->free_vars(o.const_free_vars());
		this->funcs(o.const_funcs());
		this->formula_stack(o.const_formula_stack());
		this->expr_stack(o.const_expr_stack());
		return *this;
	}

	//Python string representation of this Formula
	std::string Formula::str()
	{
//		return (std::string)((const char*)this->relation().print_to_string());
		std::string s=(const char*)this->relation().print_with_subs_to_string(true);
		return s.substr(0,s.length()-1);
	}

	void Formula::union_(sptr<Formula> const& o)
	{
		cout<<"before union: "<<this->str()<<endl;
		omega::Relation this_copy=omega::copy(this->const_relation());
		omega::Relation o_copy=omega::copy(o->const_relation());
		omega::Relation unioned=omega::Union(this_copy,o_copy);

		this->relation(omega::Relation(unioned));
		cout<<"after union: "<<this->str()<<endl;
	}

	omega::Relation const& Formula::const_relation() const {return this->m_relation;}
	omega::Relation& Formula::relation() {return this->m_relation;}
	void Formula::relation(omega::Relation const& relation) {this->m_relation=omega::copy(relation);}

	//---------- Variable members ----------
	//Name the variable at position 'i' using the given naming method
	void Formula::name(
		int i,
		int max_vars,
		std::string const& name,
		void (omega::Relation::*name_var)(int,omega::Const_String),
		Variable_ID (omega::Relation::*get_var)(int))
	{
		//Verify that the position to be named is within the valid range
		if(i<1||i>max_vars)
		{
			std::stringstream s;
			s<<"Cannot set name of variable at position "<<i<<": Position out of range 1:"<<max_vars<<".";
			throw OmegaException(s.str());
		}

		//Name the variable at position i using the given method pointer
		((this->relation()).*name_var)(i,name.c_str());
	}

	//Gets the name of the variable at position i
	std::string Formula::name(
		int i,
		int max_vars,
		Variable_ID (omega::Relation::*get_var)(int))
	{
		//Verify that the position is within the valid range
		if(i<1||i>max_vars)
		{
			std::stringstream s;
			s<<"Cannot get name of variable at position "<<i<<": Position out of range 1:"<<max_vars<<".";
			throw OmegaException(s.str());
		}

		//Get the name of the variable at postition i
		return std::string((const char*)(((this->relation()).*get_var)(i))->base_name);
	}

	template bool map_contains_key(std::map<std::string,sptr<Free_Var_Decl> > const& m,std::string const& k);
	Variable_ID Formula::get_local_var(std::string const& name)
	{
		if(!map_contains_key<std::string,sptr<Free_Var_Decl> >(this->free_vars(),name))
			this->free_vars()[name]=sptr<Free_Var_Decl>(new Free_Var_Decl(Const_String(name.c_str())));
		return this->relation().get_local(this->free_vars()[name].get());
	}

	Variable_ID Formula::get_func(std::string name,str_vect::size_type arity)
	{
		if(!map_contains_key<std::string,sptr<Free_Var_Decl> >(this->funcs(),name))
			this->funcs()[name]=sptr<Free_Var_Decl>(new Free_Var_Decl(Const_String(name.c_str()),arity));
		return this->relation().get_local(this->funcs()[name].get(),Output_Tuple);
	}
	//--------------------------------------

	//---------- Free variable members ----------
	std::map<std::string,sptr<Free_Var_Decl> > Formula::const_free_vars() const {return this->m_free_vars;}
	std::map<std::string,sptr<Free_Var_Decl> >& Formula::free_vars() {return this->m_free_vars;}
	void Formula::free_vars(std::map<std::string,sptr<Free_Var_Decl> > const& free_vars) {this->m_free_vars=free_vars;}
	//--------------------------------------------

	//---------- Func members ----------
	std::map<std::string,sptr<Free_Var_Decl> > Formula::const_funcs() const {return this->m_funcs;}
	std::map<std::string,sptr<Free_Var_Decl> >& Formula::funcs() {return this->m_funcs;}
	void Formula::funcs(std::map<std::string,sptr<Free_Var_Decl> > const& funcs) {this->m_funcs=funcs;}
	//--------------------------------------------

	//---------- Formula stack members ----------
	form_stack const& Formula::const_formula_stack() const {return this->m_formula_stack;}
	form_stack& Formula::formula_stack() {return this->m_formula_stack;}
	void Formula::formula_stack(form_stack const& formula_stack) {this->m_formula_stack=formula_stack;}

	omega::Formula* Formula::curr_formula()
	{
		if(this->formula_stack().empty())
			throw OmegaException("Formula stack empty.");
		return this->formula_stack().top();
	}

	omega::F_And* Formula::curr_formula_and()
	{
		//If the current formula is not an 'And', add an and first
		//This is needed as statements can only be added to an 'And' formula node
		F_And* f_and;
		if(this->curr_formula()->node_type()!=omega::Op_And)
			f_and=this->curr_formula()->add_and();
		else
			f_and=(F_And*)this->curr_formula();
		return f_and;
	}

	void Formula::push_and()
	{
		if(this->formula_stack().empty())
			this->formula_stack().push(this->relation().add_and());
		else
			this->formula_stack().push(this->curr_formula()->add_and());
	}

	void Formula::push_or()
	{
		if(this->formula_stack().empty())
			this->formula_stack().push(this->relation().add_or());
		else
			this->formula_stack().push(this->curr_formula()->add_or());
	}

	void Formula::push_not()
	{
		if(this->formula_stack().empty())
			this->formula_stack().push(this->relation().add_not());
		else
			this->formula_stack().push(this->curr_formula()->add_not());
	}

	void Formula::pop_formula() {this->formula_stack().pop();}
	//-------------------------------------------

	//---------- Statement adding members ----------
	void Formula::add_eq()
	{
		PresExprNorm expr=-1*this->curr_expr();
		this->pop_expr();
		expr=expr+this->curr_expr();

		this->setup_constr(expr,this->curr_formula_and()->add_EQ());
	}

	void Formula::add_neq()
	{
		PresExprNorm expr=this->curr_expr();
		this->push_or();
		this->add_lt();
		this->push_expr(expr);
		this->add_gt();
		this->pop_formula();
	}

	void Formula::add_gt()
	{
		PresExprNorm expr=-1*this->curr_expr();
		this->pop_expr();
		expr=expr+this->curr_expr();
		expr=expr-1;

		this->setup_constr(expr,this->curr_formula_and()->add_GEQ());
	}

	void Formula::add_gte()
	{
		PresExprNorm expr=-1*this->curr_expr();
		this->pop_expr();
		expr=expr+this->curr_expr();

		this->setup_constr(expr,this->curr_formula_and()->add_GEQ());
	}

	void Formula::add_lt()
	{
		PresExprNorm expr=this->curr_expr();
		this->pop_expr();
		expr=expr+(-1*this->curr_expr());
		expr=expr-1;

		this->setup_constr(expr,this->curr_formula_and()->add_GEQ());
	}

	void Formula::add_lte()
	{
		PresExprNorm expr=this->curr_expr();
		this->pop_expr();
		expr=expr+(-1*this->curr_expr());

		this->setup_constr(expr,this->curr_formula_and()->add_GEQ());
	}

	void Formula::setup_constr(PresExprNorm const& norm_expr,Constraint_Handle constr)
	{
		constr.update_const(norm_expr.const_val());

		foreach(norm_map::value_type kv,norm_expr.terms())
		{
			norm_tuple v=kv.second;
			int coeff=v.get<0>();
			sptr<PresExpr> expr=v.get<1>();

			if(NodeType::ID==expr->type())
			{
				PresExprID* id((PresExprID*)expr.get());
				constr.update_coef(this->get_formula_var(id->id()),coeff);
			}
			else if(NodeType::Func==expr->type())
			{
				PresExprFunc* func((PresExprFunc*)expr.get());
				constr.update_coef(this->get_func(func->func_name()->id(),func->args().size()),coeff);
			}
			else
				throw OmegaException("Normal maps should only contain PresExprIDs and PresExprFuncs!");
		}
	}
	//----------------------------------------------

	//---------- Normalized expression stack members ----------
	norm_stack const& Formula::const_expr_stack() const {return this->m_expr_stack;}
	norm_stack& Formula::expr_stack() {return this->m_expr_stack;}
	void Formula::expr_stack(norm_stack const& expr_stack) {this->m_expr_stack=expr_stack;}

	PresExprNorm Formula::curr_expr()
	{
		if(this->expr_stack().empty())
			throw OmegaException("Expression stack empty.");
		return this->expr_stack().top();
	}

	void Formula::push_int(PresExprInt const& int_expr)
	{
		this->push_expr(PresExprNorm(int_expr.value()));
	}

	void Formula::push_id(PresExprID const& id_expr)
	{
		norm_map terms;
		sptr<PresExprID> id(new PresExprID(id_expr));

		terms[id->str()]=norm_tuple(1,id);
		this->push_expr(PresExprNorm(terms));
	}

	void Formula::push_func(PresExprFunc const& func_expr)
	{
		norm_map terms;
		sptr<PresExprFunc> func(new PresExprFunc(func_expr));

		terms[func->str()]=norm_tuple(1,func);
		this->push_expr(PresExprNorm(terms));
	}

	void Formula::push_expr(PresExprNorm const& norm_expr) {this->expr_stack().push(norm_expr);}

	void Formula::pop_expr() {this->expr_stack().pop();}
	//---------------------------------------------------------

#if 0
	//Sets the given statement as the formula
	void Formula::set_formula(FStmt const& stmt)
	{
		this->formula()=FConj(FConj::And,stmt);
		this->set_formula();
	}

	//Sets the given conjunction as the formula
	void Formula::set_formula(FConj const& conj)
	{
		this->formula()=conj;
		this->set_formula();
	}

	//Boolean flag as to whether a formula has yet been set
	bool& Formula::formula_set(){return this->m_formula_set;}

	//Sets the formula based on the current conjunction
	void Formula::set_formula()
	{
		if(this->formula_set())
			throw OmegaException("Cannot set formula: A formula has already been set.");

		//Add the conjunction based on it's type
		switch(this->formula().type())
		{
			case(FConj::And):Formula::add_conj(this->m_r.add_and(),this->formula());break;
			case(FConj::Or):Formula::add_conj(this->m_r.add_or(),this->formula());break;
			case(FConj::Not):Formula::add_conj(this->m_r.add_not(),this->formula());break;
		}
		this->formula_set()=true;
	}

	//Adds the statements and conjunctions that are a part of the given conjunction to the given formula node
	void Formula::add_conj(Formula* form,FConj const& conj)
	{
		//Add all statements in the given conjunction
		//If the formula is not an 'And', add an and first
		//This is needed as statements can only be added to an 'And' formula node
		F_And* f_and;
		if(form->node_type()!=omega::Op_And)
			f_and=form->add_and();
		else
			f_and=(F_And*)form;
		std::vector<FStmt> stmts=conj.stmts();
		for(std::vector<FStmt>::const_iterator i=stmts.begin(); i!=stmts.end(); i++)
		{
			Formula::add_stmt(f_and,*i);
		}

		//Add all conjunctions in the given conjunction
		std::vector<FConj> conjs=conj.conjs();
		for(std::vector<FConj>::const_iterator i=conjs.begin(); i!=conjs.end(); i++)
		{
			//Add the conjunction based on it's type
			switch(i->type())
			{
				case(FConj::And):Formula::add_conj(form->add_and(),*i);break;
				case(FConj::Or):Formula::add_conj(form->add_or(),*i);break;
				case(FConj::Not):Formula::add_conj(form->add_not(),*i);break;
			}
		}
	}

	//Adds the given statement to the given formula
	void Formula::add_stmt(omega::F_And* form,FStmt const& stmt)
	{
		Constraint_Handle* constraint;
		GEQ_Handle geq;
		EQ_Handle eq;
		switch(stmt.type())
		{
			case(FStmt::GEQ):
				geq=form->add_GEQ();
				constraint=&geq;
				break;
			case(FStmt::EQ):
				eq=form->add_EQ();
				constraint=&eq;
				break;
			case(FStmt::Stride):throw OmegaException("Stride statements are not yet supported.");
		}

		FExpr expr=stmt.expr();

		//Set the constant for the constraint
		constraint->update_const(expr.constant());

		//Add all vars of the expression to the constraint
		std::vector<FVar> vars=expr.vars();
		for(std::vector<FVar>::iterator i=vars.begin(); i!=vars.end(); i++)
			constraint->update_coef((*i).var(),(*i).coeff());
	}
	//--------------------------------------------------
	// End Formula Translation Methods
	//--------------------------------------------------
#endif

}}//end namespace omega::bindings
