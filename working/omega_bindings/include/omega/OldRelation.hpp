#ifndef _OMEGA_BINDINGS_OLD_RELATION_H_
#define _OMEGA_BINDINGS_OLD_RELATION_H_

#include <boost/python.hpp>
#include <omega.h>
#include <string>
#include "TupleCollection.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	class OldSet;

	//Wraps the omega::Relation class as a true relation (a mapping from tuples to tuples)
	class OldRelation : public TupleCollection
	{
		public:
			friend void export_omega_old_formulas();
			friend class OldSet;
			OldRelation(int in,int out);
			OldRelation(std::string const& in_name,std::string const& out_name);
			OldRelation(python::tuple const& in_names,python::tuple const& out_names);
			OldRelation(OldRelation const& r);
			OldRelation(OldSet set);
			int arity_in() const;
			int arity_out() const;
			void name_in(int i,std::string const& name);
			void name_in(python::tuple const& names);
			std::string name_in(int i);
			python::tuple names_in();
			void name_out(int i,std::string const& name);
			void name_out(python::tuple const& names);
			std::string name_out(int i);
			python::tuple names_out();
			python::tuple names();

			void get_vars();
			void clear_vars(python::object type,python::object value,python::object traceback);

			//Predefined transformations
			static OldRelation identity(long dim);
			static OldRelation identity(long dim,std::vector<long> ignore_dims,bool apply);
			static OldRelation scale(long dim,long scale_dim,long factor);
			static OldRelation scale(long dim,long factor);
			static OldRelation skew(long dim,long skew_dim,long base_dim,long factor);
			static OldRelation translate(long dim,long trans_dim,long factor);

		private:
			static std::vector<std::string> get_names(unsigned long num);
			static std::vector<std::string> get_names(unsigned long num,std::string prepend,std::string append);
			static std::string get_id(unsigned long i);
			static bool add_constraint(long dim,std::vector<long> ignore_dims);
	};

}}//end namespace omega::bindings

#endif
