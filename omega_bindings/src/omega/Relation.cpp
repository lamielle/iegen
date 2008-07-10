#include <boost/python.hpp>
#include <omega.h>
#include "Relation.hpp"
#include "Formula.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	Relation::Relation(int arity_in,int arity_out) : Formula(arity_in,arity_out),m_in_var_names(),m_out_var_names() {}

	Relation::Relation(Relation const& o) : Formula(o),m_in_var_names(o.const_in_var_names()),m_out_var_names(o.const_out_var_names()) {}

	Relation& Relation::operator=(Relation const& o)
	{
		this->Formula::operator=(o);
		this->in_var_names(o.const_in_var_names());
		this->out_var_names(o.const_out_var_names());
		return *this;
	}

	//Arity of the input and output tuples
	int Relation::arity_in() const {return this->const_relation().n_inp();}
	int Relation::arity_out() const {return this->const_relation().n_out();}

	//Name the input variable at position i
	void Relation::name_in(int i,std::string const& name)
	{
		this->Formula::name(i,this->arity_in(),name,&omega::Relation::name_input_var,&omega::Relation::input_var);
		this->in_var_names()[i]=name;
	}

	//Gets the name of the input variable at position i
	std::string Relation::name_in(int i)
	{
		return this->Formula::name(i,this->arity_in(),&omega::Relation::input_var);
	}

	//Name the output variable at position i
	void Relation::name_out(int i,std::string const& name)
	{
		this->Formula::name(i,this->arity_out(),name,&omega::Relation::name_output_var,&omega::Relation::output_var);
		this->out_var_names()[i]=name;
	}

	//Gets the name of the output variable at position i
	std::string Relation::name_out(int i)
	{
		return this->Formula::name(i,this->arity_out(),&omega::Relation::output_var);
	}

	bool Relation::is_var_name(std::string const& name)
	{
		return this->is_in_var_name(name)||this->is_out_var_name(name);
	}

	bool Relation::is_in_var_name(std::string const& name)
	{
		return this->find_in_var(name)>0;
	}

	bool Relation::is_out_var_name(std::string const& name)
	{
		return this->find_out_var(name)>0;
	}

	template bool map_contains_key(std::map<int,std::string> const& m,int const& k);
	int Relation::find_in_var(std::string const& name)
	{
		int in_var_pos=0;

		for(int i=1;i<=this->arity_in();i++)
		{
			if(map_contains_key(this->in_var_names(),i))
			{
				if(name==this->in_var_names()[i])
				{
					in_var_pos=i;
					break;
				}
			}
		}
		return in_var_pos;
	}

	int Relation::find_out_var(std::string const& name)
	{
		int out_var_pos=0;

		for(int i=1;i<=this->arity_out();i++)
		{
			if(map_contains_key(this->out_var_names(),i))
			{
				if(name==this->out_var_names()[i])
				{
					out_var_pos=i;
					break;
				}
			}
		}
		return out_var_pos;
	}

	Variable_ID Relation::get_formula_var(std::string const& name)
	{
		if(this->is_in_var_name(name))
			return this->relation().input_var(this->find_in_var(name));
		else if(this->is_out_var_name(name))
			return this->relation().output_var(this->find_out_var(name));
		else
			return this->get_local_var(name);
	}

	std::map<int,std::string> Relation::const_in_var_names() const {return this->m_in_var_names;}
	std::map<int,std::string>& Relation::in_var_names() {return this->m_in_var_names;}
	void Relation::in_var_names(std::map<int,std::string> const& in_var_names) {this->m_in_var_names=in_var_names;}

	std::map<int,std::string> Relation::const_out_var_names() const {return this->m_out_var_names;}
	std::map<int,std::string>& Relation::out_var_names() {return this->m_out_var_names;}
	void Relation::out_var_names(std::map<int,std::string> const& out_var_names) {this->m_out_var_names=out_var_names;}

}}//end namespace omega::bindings
