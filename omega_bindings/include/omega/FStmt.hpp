#ifndef _OMEGA_BINDINGS_FSTMT_H_
#define _OMEGA_BINDINGS_FSTMT_H_

#include <string>
#include "FPart.hpp"
#include "FExpr.hpp"

namespace omega { namespace bindings {

	class FConj;

	//Represents a formula statement
	//Either FExpr>=0 (GEQ)
	//Or FExpr==0 (EQ)
	//Or n divides FExpr (Stride)
	class FStmt : public FPart
	{
		public:
			friend void export_omega_formula_building();
			enum FStmt_Type {EQ,GEQ,Stride};
			FStmt(FExpr expr,FStmt_Type type);
			virtual std::string str() const;
			FStmt_Type type() const;
			FExpr expr() const;

		protected:
			FStmt();

		private:
			void type(FStmt_Type type);
			void expr(FExpr const& expr);

		private:
			FStmt_Type m_type;
			FExpr m_expr;
	};

}}//end namespace omega::bindings

#endif
