#ifndef _OMEGA_BINDINGS_FEXPR_H_
#define _OMEGA_BINDINGS_FEXPR_H_

#include <boost/python.hpp>
#include <string>
#include <vector>
#include "FPart.hpp"
#include "FVar.hpp"
#include "Var.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	class FVar;
	class Var;
	class FStmt;

	//Represents a formula expression
	// FVar + FVar + ... + FVar + constant
	class FExpr : public FPart
	{
		public:
			enum FExpr_CopyOp {Add,Multiply};
			FExpr();
			FExpr(int constant);
			FExpr(Var const& var);
			FExpr(Var const& var1,Var const& var2);
			FExpr(FVar const& var);
			FExpr(FVar const& var1,Var const& var2);
			FExpr(FVar const& var1,FVar const& var2);
			FExpr(Var const& var,int constant);
			FExpr(FVar const& var,int constant);
			FExpr(FExpr const& e);
			FExpr(FExpr const& e,int constant,FExpr_CopyOp op);
			FExpr(FExpr const& e,FVar const& var);
			FExpr(FExpr const& e1,FExpr const& e2);

			virtual std::string str() const;
			int constant() const;
			std::vector<FVar> vars() const;
			python::tuple vars_tuple() const;

		private:
			void add_var(FVar const& v);
			void add_vars(std::vector<FVar> const& vars);
			void constant(int constant);
			void vars(std::vector<FVar> const& vars);

		private:
			int m_const;
			std::vector<FVar> m_vars;
	};

}}//end namespace omega::bindings

#endif
