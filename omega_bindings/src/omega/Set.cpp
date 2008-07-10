#include <boost/python.hpp>
#include <omega.h>
#include "util.hpp"
#include "Set.hpp"
#include "Formula.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	Set::Set(int arity) : Formula(arity),m_var_names() {}

	Set::Set(Set const& o) : Formula(o),m_var_names(o.const_var_names()) {}

	Set& Set::operator=(Set const& o)
	{
		this->Formula::operator=(o);
		this->var_names(o.const_var_names());
		return *this;
	}

	//Arity of the tuples in the set
	int Set::arity() const {return this->const_relation().n_set();}

	//Name the set variable at position i
	void Set::name(int i,std::string const& name)
	{
		this->Formula::name(i,this->arity(),name,&omega::Relation::name_set_var,&omega::Relation::set_var);
		this->var_names()[i]=name;
	}

	//Gets the name of the variable at position i
	std::string Set::name(int i)
	{
		return this->Formula::name(i,this->arity(),&omega::Relation::set_var);
	}

	bool Set::is_var_name(std::string const& name)
	{
		return this->find_var(name)>0;
	}

	template bool map_contains_key(std::map<int,std::string> const& m,int const& k);
	int Set::find_var(std::string const& name)
	{
		int var_pos=0;

		for(int i=1;i<=this->arity();i++)
		{
			if(map_contains_key<int,std::string>(this->var_names(),i))
			{
				if(name==this->var_names()[i])
				{
					var_pos=i;
					break;
				}
			}
		}

		return var_pos;
	}

	Variable_ID Set::get_formula_var(std::string const& name)
	{
		if(this->is_var_name(name))
			return this->relation().set_var(this->find_var(name));
		else
			return this->get_local_var(name);
	}

	//---------- Variable names members ----------
	std::map<int,std::string> Set::const_var_names() const {return this->m_var_names;}
	std::map<int,std::string>& Set::var_names() {return this->m_var_names;}
	void Set::var_names(std::map<int,std::string> const& var_names) {this->m_var_names=var_names;}
	//--------------------------------------------

}}//end namespace omega::bindings
