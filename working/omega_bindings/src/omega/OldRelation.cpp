#include <boost/python.hpp>
#include <boost/python/detail/api_placeholder.hpp>
#include <omega.h>
#include <string>
#include <vector>
#include "OldRelation.hpp"
#include "OldSet.hpp"
#include "Var.hpp"
#include "FConj.hpp"
#include "OmegaException.hpp"
#include "util.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	OldRelation::OldRelation(int in,int out):TupleCollection(in,out){}

	OldRelation::OldRelation(std::string const& in_name,std::string const& out_name):TupleCollection(1,1)
	{
		this->name_in(1,in_name);
		this->name_out(1,out_name);
	}

	OldRelation::OldRelation(python::tuple const& in_names,python::tuple const& out_names):TupleCollection(python::len(in_names),python::len(out_names))
	{
		this->name_in(in_names);
		this->name_out(out_names);
	}

	//Copy Constructor
	OldRelation::OldRelation(OldRelation const& r):TupleCollection(r) {}

	//Constructs a trivial relation based on the given set
	//In and out arity is equal to the set's arity
	//In names are the same as the set's names
	//Out names are the same as the set's names appended with 'p'
	//The relation maps directly from input var to the corresponding output var
	OldRelation::OldRelation(OldSet set):TupleCollection(set.arity(),set.arity())
	{
		python::tuple names=set.names();
		int len=python::len(names);
		std::vector<std::string> in(len),out(len);
		for(int i=0;i<len;i++)
		{
			std::string s=python::extract<std::string>(names[i]);
			in[i]=s;
			out[i]=s+"p";
			this->name_in(i+1,in[i]);
			this->name_out(i+1,out[i]);
		}
		FConj conj(FConj::And);
		for(int i=0;i<len;i++)
		{
			std::string ins=in[i];
			std::string outs=out[i];
			Var in=this->TupleCollection::getitem(ins);
			FVar out=this->TupleCollection::getitem(outs)*-1;
			conj=conj&(out+in==0);
		}
		this->set_formula(conj);
	}

	//Arity of the input tuples
	int OldRelation::arity_in() const
	{
		return this->m_r.n_inp();
	}

	//Arity of the output tuples
	int OldRelation::arity_out() const
	{
		return this->m_r.n_out();
	}

	//Name the input variable at position i
	void OldRelation::name_in(int i,std::string const& name)
	{
		this->TupleCollection::name(i,this->m_r.n_inp(),name,&omega::Relation::name_input_var,&omega::Relation::input_var);
	}

	//Name the first len(names) input variables
	void OldRelation::name_in(python::tuple const& names)
	{
		this->TupleCollection::name(names,this->m_r.n_inp(),&omega::Relation::name_input_var,&omega::Relation::input_var);
	}

	//Gets the name of the input variable at position i
	std::string OldRelation::name_in(int i)
	{
		return this->TupleCollection::name(i,this->arity_in(),&omega::Relation::input_var);
	}

	//Gets a tuple of the input variable names for this set
	python::tuple OldRelation::names_in()
	{
		return this->TupleCollection::names(this->arity_in(),&omega::Relation::input_var);
	}

	//Name the output variable at position i
	void OldRelation::name_out(int i,std::string const& name)
	{
		this->TupleCollection::name(i,this->m_r.n_out(),name,&omega::Relation::name_output_var,&omega::Relation::output_var);
	}

	//Name the first len(names) output variables
	void OldRelation::name_out(python::tuple const& names)
	{
		this->TupleCollection::name(names,this->m_r.n_out(),&omega::Relation::name_output_var,&omega::Relation::output_var);
	}

	//Gets the name of the output variable at position i
	std::string OldRelation::name_out(int i)
	{
		return this->TupleCollection::name(i,this->arity_out(),&omega::Relation::output_var);
	}

	//Gets a tuple of the output variable names for this set
	python::tuple OldRelation::names_out()
	{
		return this->TupleCollection::names(this->arity_out(),&omega::Relation::output_var);
	}

	//Gets a tuple of two tuples: the input var names and the output var names
	python::tuple OldRelation::names()
	{
		return python::make_tuple(this->names_in(),this->names_out());
	}

	void OldRelation::get_vars()
	{
		TupleCollection::vars(TupleCollection::VARS_GET,this->arity_in(),&omega::Relation::input_var);
		TupleCollection::vars(TupleCollection::VARS_GET,this->arity_out(),&omega::Relation::output_var);
	}
	void OldRelation::clear_vars(python::object type,python::object value,python::object traceback)
	{
		TupleCollection::vars(TupleCollection::VARS_CLEAR,this->arity_in(),&omega::Relation::input_var);
		TupleCollection::vars(TupleCollection::VARS_CLEAR,this->arity_out(),&omega::Relation::output_var);
	}

	//Predefined identity relation of arity 'dim'
	//input and output variables are named
	//no constraints are added
	OldRelation OldRelation::identity(long dim)
	{
		//Make sure the dimension is a sane value
		if(dim<1)
			throw OmegaException("Dimension must be >0");

		std::vector<long> ignore_dims(dim);
		for(long i=0;i<dim;i++)ignore_dims[i]=i+1;

		return OldRelation::identity(dim,ignore_dims,false);
	}

	//Predefined identity relation of arity 'dim'
	//ignore_dims is a collection of dimensions to not add constraints for
	//If apply is true, sets the formula, otherwise it must be done later
	OldRelation OldRelation::identity(long dim,std::vector<long> ignore_dims,bool apply)
	{
		//Make sure the dimension is a sane value
		if(dim<1)
			throw OmegaException("Dimension must be >0");

		//The relation that is being created
		OldRelation r(dim,dim);

		//Get unique input and output variable names
		std::vector<std::string> in_vars=OldRelation::get_names(dim,"","");
		std::vector<std::string> out_vars=OldRelation::get_names(dim,"","p");

		//Name the relation variables and add in_var=out_var for each
		for(long i=0;i<dim;i++)
		{
			//Name the variables
			r.name_in(i+1,in_vars[i]);
			r.name_out(i+1,out_vars[i]);
			Var v=r.getitem(in_vars[i]);
			Var vp=r.getitem(out_vars[i]);
			if(OldRelation::add_constraint(i+1,ignore_dims))
				r.append(vp==v,FConj::And);
		}

		if(apply) r.set_formula();

		return r;
	}

	//Lame linear search through 'ignore_dims' for 'dim'.
	bool OldRelation::add_constraint(long dim,std::vector<long> ignore_dims)
	{
		foreach(long i,ignore_dims)
			if(dim==i) return false;
		return true;
	}

	//Predefined scaling relation of arity 'dim'.
	//Scales 'scale_dim' by 'factor'.
	OldRelation OldRelation::scale(long dim,long scale_dim,long factor)
	{
		//Make sure the scale dimension is a sane value
		if(scale_dim<1)
			throw OmegaException("Scale Dimension must be >0");
		if(scale_dim>dim)
			throw OmegaException("Scale Dimension must be <= Relation Dimension");

		OldRelation r=OldRelation::identity(dim,std::vector<long>(1,scale_dim),false);

		//Apply the scaling to the specified dimension
		Var v=r.getitem(r.name_in(scale_dim));
		Var vp=r.getitem(r.name_out(scale_dim));
		r.append(vp==(factor*v),FConj::And);

		r.set_formula();
		return r;
	}

	//Predefined scaling relation of arity 'dim'.
	//Scales all dimentions by 'factor'.
	OldRelation OldRelation::scale(long dim,long factor)
	{
		OldRelation r=OldRelation::identity(dim);

		//Add scaling constraints for each dimension
		for(long i=1;i<=dim;i++)
		{
			Var v=r.getitem(r.name_in(i));
			Var vp=r.getitem(r.name_out(i));
			r.append(vp==(factor*v),FConj::And);
		}

		r.set_formula();
		return r;
	}

	//Predefined skew transformation of arity 'dim'.
	//Skews the dimension 'skew_dim' by 'factor' with respect to 'base_dim'
	OldRelation OldRelation::skew(long dim,long skew_dim,long base_dim,long factor)
	{
		//Make sure the dimensions are sane values
		if(dim<2)
			throw OmegaException("Relation Dimension must be >1");
		if(skew_dim<1)
			throw OmegaException("Skew Dimension must be >0");
		if(skew_dim>dim)
			throw OmegaException("Skew Dimension must be <= Relation Dimension");
		if(base_dim<1)
			throw OmegaException("Base Dimension must be >0");
		if(base_dim>dim)
			throw OmegaException("Base Dimension must be <= Relation Dimension");

		//The relation that is being created
		OldRelation r=OldRelation::identity(dim,std::vector<long>(1,skew_dim),false);

		//Add the skewing constraint to the relation's formula
		Var v=r.getitem(r.name_in(skew_dim));
		Var vp=r.getitem(r.name_out(skew_dim));
		Var b=r.getitem(r.name_in(base_dim));
		r.append(vp==b*factor+v,FConj::And);

		r.set_formula();

		return r;
	}

	//Predefined translation transformation of arity 'dim'.
	//Translates in the 'trans_dim' dimension by 'factor'.
	OldRelation OldRelation::translate(long dim,long trans_dim,long factor)
	{
		if(trans_dim<1)
			throw OmegaException("Translation Dimension must be >0");
		if(trans_dim>dim)
			throw OmegaException("Translation Dimension must be <= Relation Dimension");

		//The relation that is being created
		OldRelation r=OldRelation::identity(dim,std::vector<long>(1,trans_dim),false);

		//Add the translation constraint to the relation's formula
		Var v=r.getitem(r.name_in(trans_dim));
		Var vp=r.getitem(r.name_out(trans_dim));
		r.append(vp==v+factor,FConj::And);

		r.set_formula();

		return r;
	}

	//Gets a vector of unique strings for use as relation variable names
	//Each name has the string 'prepend' prepended to it and 'append' appended to it
	std::vector<std::string> OldRelation::get_names(unsigned long num,std::string prepend,std::string append)
	{
		std::vector<std::string> names(num);
		for(unsigned long i=0;i<num;i++)
			names[i]=prepend+OldRelation::get_id(i)+append;
		return names;
	}

	//Gets the ith string id in base 26 using symbols a-z
	//Essentially does a base 10 to base 26 conversion
	std::string OldRelation::get_id(unsigned long i)
	{
		unsigned long len=1;
		if(i>0)
			len+=((unsigned long)(log(i)/log(26)));
		std::string s(len,'\0');

		//Start with the highest needed power of 26 (place value)
		unsigned long place=(unsigned long)pow((double)26,(double)s.size()-1);

		//Determine the character for each position in the string
		for(unsigned long pos=0;pos<s.size();pos++)
		{
			unsigned long val=i/place;
			s[pos]='a'+(char)val;
			i-=val*place;
			place=place/26;
		}

		return s;
	}

}}//end namespace omega::bindings
