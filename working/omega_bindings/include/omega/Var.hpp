#ifndef _OMEGA_BINDINGS_VAR_H_
#define _OMEGA_BINDINGS_VAR_H_

#include <boost/python.hpp>
#include <string>
#include <omega.h>
#include "FVar.hpp"
#include "FExpr.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	//Forward declaration of FVar so Var will compile
	class FVar;
	class FExpr;
	class FStmt;

	//Represents a local (constrained) variable
	class Var
	{
		public:
			friend class TupleCollection;
			friend void export_omega_formula_building();
			Var(Var_Decl* var);
			Var(Var const& o);
			Var& operator=(Var const& o);
			virtual ~Var();
			std::string name() const;
			virtual std::string str() const;
			Var_Decl* var_ptr() const;

		protected:
			Var();

		private:
			Var_Decl* m_var;
	};

}}//end namespace omega::bindings

#endif
