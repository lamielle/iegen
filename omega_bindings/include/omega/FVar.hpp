#ifndef _OMEGA_BINDINGS_FVAR_H_
#define _OMEGA_BINDINGS_FVAR_H_

#include <string>
#include <boost/shared_ptr.hpp>
#include "FPart.hpp"
#include "FExpr.hpp"
#include "Var.hpp"

namespace omega { namespace bindings {

	class Var;
	class FExpr;
	class FStmt;

	//Represents a formula variable of the form:
	// c*Var
	class FVar : public FPart
	{
		public:
			friend void export_omega_formula_building();
			FVar(Var const& v);
			FVar(int coeff,Var const& v);
			FVar(FVar const& o);
			FVar(int coeff,FVar const& o);
			~FVar();
			FVar& operator=(FVar const& o);
			std::string name() const;
			virtual std::string str() const;
			int coeff() const;
			Var_Decl* var() const;

		protected:
			FVar();

		private:
			void coeff(int coeff);

		private:
			int m_coeff;
			boost::shared_ptr<Var> m_v;
	};

}}//end namespace omega::bindings

#endif
