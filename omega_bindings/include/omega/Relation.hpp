#ifndef _OMEGA_BINDINGS_RELATION_H_
#define _OMEGA_BINDINGS_RELATION_H_

#include <boost/python.hpp>
#include <omega.h>
#include "Formula.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	//Wraps the omega::Relation class as a true relation (a mapping from tuples to tuples)
	class Relation : public Formula
	{
		public:
			Relation(int arity_in,int arity_out);
			Relation(Relation const& r);
			Relation& operator=(Relation const& c);
			int arity_in() const;
			int arity_out() const;

			void compose(sptr<Relation> const& o);
			void inverse();

			void name_in(int i,std::string const& name);
			std::string name_in(int i);
			void name_out(int i,std::string const& name);
			std::string name_out(int i);

			bool is_var_name(std::string const& name);
			bool is_in_var_name(std::string const& name);
			bool is_out_var_name(std::string const& name);
			int find_in_var(std::string const& name);
			int find_out_var(std::string const& name);
			Variable_ID get_formula_var(std::string const& name);

			std::map<int,std::string> const_in_var_names() const;
			std::map<int,std::string> const_out_var_names() const;

		private:
			std::map<int,std::string>& in_var_names();
			void in_var_names(std::map<int,std::string> const& in_var_names);
			std::map<int,std::string>& out_var_names();
			void out_var_names(std::map<int,std::string> const& out_var_names);
			std::map<int,std::string> m_in_var_names,m_out_var_names;
	};

}}//end namespace omega::bindings

#endif
