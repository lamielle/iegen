#include "PresExprNorm.hpp"
#include "PresExprID.hpp"
#include "PresExprFunc.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprNorm::PresExprNorm(int const_val) : m_terms(),m_const_val(const_val) {}
	PresExprNorm::PresExprNorm(norm_map const& terms) : m_terms(terms),m_const_val(0) {}
	PresExprNorm::PresExprNorm(norm_map const& terms,int const_val) : m_terms(terms),m_const_val(const_val) {}

	PresExprNorm::PresExprNorm(PresExprNorm const& o) : m_terms(o.terms()),m_const_val(o.const_val()) {}

	PresExprNorm& PresExprNorm::operator=(PresExprNorm const& o)
	{
		this->terms(o.terms());
		this->const_val(o.const_val());
		return *this;
	}

	norm_map const& PresExprNorm::terms() const {return this->m_terms;}
	void PresExprNorm::terms(norm_map const& terms) {this->m_terms=terms;}

	int PresExprNorm::const_val() const {return this->m_const_val;}
	void PresExprNorm::const_val(int const_val) {this->m_const_val=const_val;}

	bool PresExprNorm::empty() const
	{
		return 0==this->terms().size()&&0==this->const_val();
	}

	bool PresExprNorm::has_terms() const
	{
		return 0!=this->terms().size();
	}

	std::string PresExprNorm::str() const
	{
		std::stringstream s;
		norm_map::size_type num_terms,curr_pos;
		num_terms=this->terms().size();

		//Terms
		curr_pos=0;
		foreach(norm_map::value_type kv,this->terms())
		{
			norm_tuple v=kv.second;
			int coeff=v.get<0>();
			sptr<PresExpr> expr=v.get<1>();
			s<<coeff<<"*"<<expr->str();
			if(curr_pos<num_terms-1)
				s<<"+";
			++curr_pos;

			//Sanity check
			if(NodeType::ID!=expr->type()&&NodeType::Func!=expr->type())
				throw OmegaException("Normal maps should only contain PresExprIDs and PresExprFuncs!");
		}

		//Func/const separator
		if(this->has_terms())
		{
			if(0!=this->const_val())
				s<<"+"<<this->const_val();
		}
		else
			s<<this->const_val();

		return s.str();
	}

	PresExprNorm operator+(PresExprNorm const& e1,PresExprNorm const& e2)
	{
		norm_map new_terms(e1.terms());

		foreach(norm_map::value_type kv,e2.terms())
		{
			std::string k=kv.first;
			norm_tuple v=kv.second;
			if(map_contains_key(new_terms,k))
				new_terms[k]=norm_tuple(new_terms[k].get<0>()+v.get<0>(),new_terms[k].get<1>());
			else
				new_terms[k]=norm_tuple(v.get<0>(),v.get<1>());
		}

		return PresExprNorm(new_terms,e1.const_val()+e2.const_val());
	}

	PresExprNorm operator-(PresExprNorm const& e1,PresExprNorm const& e2)
	{
		return e1+(-1*e2);
	}

	PresExprNorm operator*(PresExprNorm const& e1,PresExprNorm const& e2)
	{
		//Make sure one of the terms is only a constant and has no terms
		//Multiplication of variablies is undefined here
		if(e1.has_terms()&&e2.has_terms())
			throw OmegaException("Multiplication of variables/functions with other variables/functions is not defined.");

		norm_map terms,new_terms;
		int coeff,const_val;
		if(!e1.has_terms())
		{
			terms=e2.terms();
			coeff=e1.const_val();
			const_val=e2.const_val();
		}
		else
		{
			new_terms=e1.terms();
			coeff=e2.const_val();
			const_val=e1.const_val();
		}

		foreach(norm_map::value_type kv,terms)
		{
			std::string k=kv.first;
			norm_tuple v=kv.second;
			new_terms[k]=norm_tuple(coeff*v.get<0>(),v.get<1>());
		}

		return PresExprNorm(new_terms,coeff*const_val);
	}

	PresExprNorm operator*(int const_val,PresExprNorm const& e)
	{
		return PresExprNorm(const_val)*e;
	}
	PresExprNorm operator*(PresExprNorm const& e,int const_val)
	{
		return const_val*e;
	}

}}}}//end namespace omega::bindings::parser::ast
