#ifndef _OMEGA_BINDINGS_TUPLECOLLECTION_H_
#define _OMEGA_BINDINGS_TUPLECOLLECTION_H_

#include <boost/python.hpp>
#include <omega.h>
#include <string>
#include <map>
#include "Var.hpp"
#include "FConj.hpp"
#include "FStmt.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	//Parent class of both Relation and Set:
	//A generalization of both.
	//Contains the omega::Relation object that these classes wrap
	//along with naming functionality and the ability to set formulas
	class TupleCollection
	{
		public:
			enum VarAction {VARS_GET,VARS_CLEAR};
			TupleCollection(TupleCollection const& c);
			TupleCollection(TupleCollection const& c,omega::Relation const& r);
			TupleCollection& operator=(TupleCollection const& c);
			Var getitem(std::string const& name);
			Var getitem(python::tuple const& var_def);
			void setitem(std::string const& name,python::object const& o) const;
			std::string str();

		//Formula related methods
		public:
			void append(FStmt const& stmt,FConj::FConj_Type type);
			void append(FConj const& conj,FConj::FConj_Type type);
			FConj get_formula();
			void set_formula(FStmt const& stmt);
			void set_formula(FConj const& conj);
			void set_formula();
		private:
			static void add_conj(omega::Formula* form,FConj const& conj);
			static void add_stmt(omega::F_And* form,FStmt const& stmt);

		protected:
			TupleCollection(int arity);
			TupleCollection(int arity_in,int arity_out);

			void name(int i,int max_vars,std::string const& name,void (omega::Relation::*name_var)(int,omega::Const_String),Variable_ID (omega::Relation::*get_var)(int));
			void name(python::tuple const& names,int max_vars,void (omega::Relation::*name_var)(int,omega::Const_String),Variable_ID (omega::Relation::*get_var)(int));
			std::string name(int i,int max_vars,Variable_ID (omega::Relation::*get_var)(int));
			python::tuple names(int max_vars,Variable_ID (omega::Relation::*get_var)(int));
		void vars(TupleCollection::VarAction action,int max_vars,Variable_ID (omega::Relation::*get_var)(int));

		private:
			Var get_local_or_global(std::string const& name);
			Var get_local_ufs(std::string const& name,int arity,Argument_Tuple type);

		protected:
			omega::Relation m_r;

		private:
			python::dict m_local_vars;
			static python::dict m_global_vars;

			FConj& formula();
			FConj m_formula;
			bool& formula_set();
			bool m_formula_set;
	};

}}//end namespace omega::bindings

#endif
