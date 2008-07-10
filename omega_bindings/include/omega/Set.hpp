#ifndef _OMEGA_BINDINGS_SET_H_
#define _OMEGA_BINDINGS_SET_H_

#include <boost/python.hpp>
#include <omega.h>
#include "Formula.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	//Wraps the omega::Relation class as a set of tuples
	class Set : public Formula
	{
		public:
			Set(int arity);
			Set(Set const& s);
			Set& operator=(Set const& s);
			int arity() const;

			void name(int i,std::string const& name);
			std::string name(int i);

			bool is_var_name(std::string const& name);
			int find_var(std::string const& name);
			Variable_ID get_formula_var(std::string const& name);

		//---------- Variable names members ----------
		public:
			std::map<int,std::string> const_var_names() const;

		private:
			std::map<int,std::string>& var_names();
			void var_names(std::map<int,std::string> const& var_names);
			std::map<int,std::string> m_var_names;
		//--------------------------------------------

	};

}}//end namespace omega::bindings

#endif
