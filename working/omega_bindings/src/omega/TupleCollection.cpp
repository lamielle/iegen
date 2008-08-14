#include <boost/python.hpp>
#include <boost/python/detail/api_placeholder.hpp>
#include <omega.h>
#include <string>
#include <map>
#include "TupleCollection.hpp"
#include "OmegaException.hpp"
#include "Var.hpp"
#include "FreeVar.hpp"
#include "FConj.hpp"
#include "FStmt.hpp"
#include "util.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	//m_global_vars init
	python::dict TupleCollection::m_global_vars=python::dict();

	//Constructors
	TupleCollection::TupleCollection(int arity):m_local_vars(),m_formula(FConj::And),m_formula_set(false)
	{
		if(arity<0)
			throw OmegaException("Tuples must have arity greater than or equal to 0.");
		this->m_r=Relation(arity);
	}

	TupleCollection::TupleCollection(int arity_in,int arity_out):m_local_vars(),m_formula(FConj::And),m_formula_set(false)
	{
		if(arity_in<0||arity_out<0)
			throw OmegaException("Tuples must have arity greater than or equal to 0.");
		this->m_r=Relation(arity_in,arity_out);
	}

	//Copy constructor
	TupleCollection::TupleCollection(TupleCollection const& c):m_r(copy(c.m_r)),m_local_vars(c.m_local_vars),m_formula(c.m_formula),m_formula_set(c.m_formula_set) {}

	//Copy constructor++ (assigns the given omega::Relation rather than the one in the given TupleCollection)
	TupleCollection::TupleCollection(TupleCollection const& c,omega::Relation const& r):m_r(copy(r)),m_local_vars(c.m_local_vars),m_formula(c.m_formula),m_formula_set(c.m_formula_set) {}

	//Assignment operator
	TupleCollection& TupleCollection::operator=(TupleCollection const& c)
	{
		this->m_r=omega::copy(c.m_r);
		this->m_local_vars=c.m_local_vars;
		this->m_formula=c.m_formula;
		return *this;
	}

	//Python string representation of this TupleCollection
	std::string TupleCollection::str()
	{
//		return (std::string)((const char*)this->m_r.print_to_string());
		std::string s=(const char*)this->m_r.print_with_subs_to_string(true);
		return s.substr(0,s.length()-1);
	}

	//Name the variable at position 'i' using the given naming method
	void TupleCollection::name(
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

		//Verify that no other local or global variable has the new name
		if(this->m_local_vars.has_key(name))
		{
			std::stringstream s;
			s<<"Cannot set name of variable at position "<<i<<" to '"+name+"': Another variable of the same name is already in use.";
			throw OmegaException(s.str());
		}

		//Name the variable at position i using the given method pointer
		(this->m_r.*name_var)(i,name.c_str());

		//Create a Var associated with this variable
		this->m_local_vars[name]=Var((this->m_r.*get_var)(i));
	}

	//Name the first len(names) variables using the given naming method
	void TupleCollection::name(
		python::tuple const& names,
		int max_vars,
		void (omega::Relation::*name_var)(int,omega::Const_String),
		Variable_ID (omega::Relation::*get_var)(int))
	{
		int len=python::len(names);

		//Verify that we were not given too many names
		if(len>max_vars)
		{
			std::stringstream s;
			s<<"Too many variable names ("<<len<<") supplied (maximum: "<<max_vars<<").";
			throw OmegaException(s.str());
		}

		//Iterate over the given names naming the associated variables
		for(int i=0;i<len;i++)
			this->name(i+1,max_vars,python::extract<std::string>(names[i]),name_var,get_var);
	}

	//Gets the name of the variable at position i
	std::string TupleCollection::name(
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
		return std::string((const char*)(((this->m_r.*get_var)(i))->base_name));
	}
	
	//Gets a tuple of the variable names for this TupleCollection
	python::tuple TupleCollection::names(
		int max_vars,
		Variable_ID (omega::Relation::*get_var)(int))
	{
		python::list names;
		for(int i=1;i<=max_vars;i++)
			names.append(this->name(i,max_vars,get_var));
		return python::tuple(names);
	}

	//This method does one of two things, based on the given action parameter
	//If action is VARS_GET:
	//  Gets each of the variables using the given method and
	//  assigns a python variable their associated Var object
	//  Example:
	//  s=OldSet("a")
	//  a=s["a"]
	//   ---OR---
	//  s=OldSet("a")
	//  s.get_vars()
	//  #The variable a is now the same as it would be after executing the first snippet
	//
	//If action is VARS_CLEAR:
	//  Clears each of the variables using the given method for obtaining names
	void TupleCollection::vars(
		TupleCollection::VarAction action,
		int max_vars,
		Variable_ID (omega::Relation::*get_var)(int))
	{
		//Get the global name dictionary
		PyObject *globals=PyEval_GetGlobals();

		//Loop through each variable
		for(int i=1;i<=max_vars;i++)
		{
			//Get its name
			std::string name=this->name(i,max_vars,get_var);

			if(VARS_GET==action)
			{
				//Get the Var object associate with the name
				Var v=this->getitem(name);
				python::object o=python::object(v);
				//Set a python variable of the same name equal to the Var object
				PyDict_SetItemString(globals,name.c_str(),o.ptr());
			}
			else
			{
				//Remove the entry from the globals dictionary
				PyDict_DelItemString(globals,name.c_str());
			}
		}
	}

	//Gets the Var of the variable with the given name
	//If the name does not exist in the set of local vars,
	//a global FreeVar is created with the given name and
	//the corresponding local Var is returned.
	Var TupleCollection::getitem(std::string const& name)
	{
		return this->getitem(python::make_tuple(name,0));
	}

	//Gets the Var of the variable matching the given tuple
	//of the form (var name,[function arity[,function tuple target]])
	//
	//Examples:
	// getitem(("a")): Gets the local or free variable with name "a".
	//   If "a" does not exist, this method creates it.
	// getitem(("a",0)): Equivalent to getitem(("a"))
	// getitem(("f",1,TupleType.inp)): Gets or creates an uninterpreted
	//   function symbol with name "f" of arity one as a function of
	//   the input tuple
	// getitem(("g",2)): Gets or creates an ininterpreted function
	//   symbol with name "g" of arity 2 as a function of the Set's tuple
	//   (if the relation is a Set) or the Relation's input tuple (if the
	//   relation is a Relation).
	Var TupleCollection::getitem(python::tuple const& var_def)
	{
		int len=python::len(var_def);

		//Verify that the tuple of of a valid length
		if(len<1||len>3)
			throw OmegaException("Index value must be a string or tuple of length 1, 2, or 3.");

		//Get the name from position 0 in the tuple
		std::string name=python::extract<std::string>(var_def[0]);

		//Was just the name given?
		if(1==len)
			return this->get_local_or_global(name);
		else
		{
			//Get the arity that was specified
			int arity=python::extract<int>(var_def[1]);

			//If arity is 0, do the same as if it wasn't specified
			if(!arity)
				return this->get_local_or_global(name);

			//Otherwise we are creating an uninterpreted function symbol
			//Assume the tuple that the UFS is being applied to is Set
			Argument_Tuple type=Set_Tuple;

			//The third position in the tuple specifies differently if given
			if(len==3)
				type=python::extract<Argument_Tuple>(var_def[2]);

			return this->get_local_ufs(name,arity,type);
		}
	}

	//Setting items is not supported
	void TupleCollection::setitem(std::string const& name,python::object const& o) const
	{
		throw OmegaException("Assignment to variable dictionary not permitted.");
	}

	//Gets the local (constrained) or global (free) variable with the given name
	//This method also creates the global and/or local variable if necessary
	Var TupleCollection::get_local_or_global(std::string const& name)
	{
		Var v;
		//Determine if a Var with the given name already exists
		if(this->m_local_vars.has_key(name))
		{
			//Get the local var associated with the given name
			v=python::extract<Var>(this->m_local_vars[name]);
		}
		else
		{
			FreeVar fv;
			//Determine if a Global var with the given name already exists
			if(this->m_global_vars.has_key(name))
			{
				//Get the global FreeVar associated with the given name
				fv=python::extract<FreeVar>(this->m_global_vars[name]);
			}
			else
			{
				//Create a global FreeVar and associate it with the given name
				fv=FreeVar(name);
				this->m_global_vars[name]=fv;
			}

			//Create a Var from the global FreeVar
			v=Var(this->m_r.get_local(fv.fvar_ptr()));

			//Associate the Var with the given name
			this->m_local_vars[name]=v;
		}

		return v;
	}

	//Gets the local uninterpreted function symbol of the given name and arity for the given type
	//This method also creates the global and local UFS if necessary
	Var TupleCollection::get_local_ufs(std::string const& name,int arity,Argument_Tuple type)
	{
		//Has the UFS already been created? (If not create it)
		if(!this->m_global_vars.has_key(name))
			this->m_global_vars[name]=FreeVar(name,arity);

		//Create the (name,type) tuple that is used as the key for UFSs
		python::tuple key_tuple=python::make_tuple(name,type);

		Var v;
		//Is the local UFS already present in the local vars? (If not create it)
		if(this->m_local_vars.has_key(key_tuple))
		{
			//Get the local var associated with the key_tuple
			v=python::extract<Var>(this->m_local_vars[key_tuple]);
		}
		else
		{
			//Get the global FreeVar associated with the given name
			FreeVar fv=python::extract<FreeVar>(this->m_global_vars[name]);

			//Create a local Var from the global FreeVar
			v=Var(this->m_r.get_local(fv.fvar_ptr(),type));

			//Associate the Var with the key_tuple
			this->m_local_vars[key_tuple]=v;
		}

		//Return the extracted Var associated with the key_tuple
		return v;
	}

	//--------------------------------------------------
	//Formula related methods
	//--------------------------------------------------

	FConj& TupleCollection::formula(){return this->m_formula;}
	FConj TupleCollection::get_formula(){return this->m_formula;}

	//Append the given statement to the current formula
	void TupleCollection::append(FStmt const& stmt,FConj::FConj_Type type)
	{
		if(this->formula_set())
			throw OmegaException("Cannot append statement: Formula has already been set.");

		switch(type)
		{
			case(FConj::And):this->formula()=this->formula()&stmt;break;
			case(FConj::Or):this->formula()=this->formula()|stmt;break;
			default: throw OmegaException("Must append a statement with either And or Or."); break;
		}
	}

	//Append the given conjunction to the current formula
	void TupleCollection::append(FConj const& conj,FConj::FConj_Type type)
	{
		if(this->formula_set())
			throw OmegaException("Cannot append conjunction: Formula has already been set.");

		switch(type)
		{
			case(FConj::And):this->formula()=this->formula()&conj;break;
			case(FConj::Or):this->formula()=this->formula()|conj;break;
			default: throw OmegaException("Must append a statement with either And or Or."); break;
		}
	}

	//Sets the given statement as the formula
	void TupleCollection::set_formula(FStmt const& stmt)
	{
		this->formula()=FConj(FConj::And,stmt);
		this->set_formula();
	}

	//Sets the given conjunction as the formula
	void TupleCollection::set_formula(FConj const& conj)
	{
		this->formula()=conj;
		this->set_formula();
	}

	//Boolean flag as to whether a formula has yet been set
	bool& TupleCollection::formula_set(){return this->m_formula_set;}

	//Sets the formula based on the current conjunction
	void TupleCollection::set_formula()
	{
		if(this->formula_set())
			throw OmegaException("Cannot set formula: A formula has already been set.");

		//Add the conjunction based on it's type
		switch(this->formula().type())
		{
			case(FConj::And):TupleCollection::add_conj(this->m_r.add_and(),this->formula());break;
			case(FConj::Or):TupleCollection::add_conj(this->m_r.add_or(),this->formula());break;
			case(FConj::Not):TupleCollection::add_conj(this->m_r.add_not(),this->formula());break;
		}
		this->formula_set()=true;
	}

	//Adds the statements and conjunctions that are a part of the given conjunction to the given formula node
	void TupleCollection::add_conj(Formula* form,FConj const& conj)
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
			TupleCollection::add_stmt(f_and,*i);
		}

		//Add all conjunctions in the given conjunction
		std::vector<FConj> conjs=conj.conjs();
		for(std::vector<FConj>::const_iterator i=conjs.begin(); i!=conjs.end(); i++)
		{
			//Add the conjunction based on it's type
			switch(i->type())
			{
				case(FConj::And):TupleCollection::add_conj(form->add_and(),*i);break;
				case(FConj::Or):TupleCollection::add_conj(form->add_or(),*i);break;
				case(FConj::Not):TupleCollection::add_conj(form->add_not(),*i);break;
			}
		}
	}

	//Adds the given statement to the given formula
	void TupleCollection::add_stmt(omega::F_And* form,FStmt const& stmt)
	{
		Constraint_Handle* constraint=NULL;
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

}}//end namespace omega::bindings
