#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_NORM_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_EXPR_NORM_H_

#include "PresUtil.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//This class represents a expression in 'normalized' form:
	//The sum of a collection of variables and their coefficients, functions and their coefficients, and a single constant value
	//A map of PresExprs contains both the variables (PresExprID) and the functions (PresExprFunc).
	//Consider it and exceptional case if something other than these two node types are in the list of terms
	class PresExprNorm
	{
		public:
			PresExprNorm(int const_val);
			PresExprNorm(norm_map const& terms);
			PresExprNorm(norm_map const& terms,int const_val);
			PresExprNorm(PresExprNorm const& o);
			PresExprNorm& operator=(PresExprNorm const& o);

			bool empty() const;
			bool has_terms() const;

			std::string str() const;

			norm_map const& terms() const;
			int const_val() const;

		private:
			void terms(norm_map const& terms);
			norm_map m_terms;

			void const_val(int const_val);
			int m_const_val;
	};

	//Operators
	PresExprNorm operator+(PresExprNorm const& e1,PresExprNorm const& e2);
	PresExprNorm operator-(PresExprNorm const& e1,PresExprNorm const& e2);
	PresExprNorm operator*(PresExprNorm const& e1,PresExprNorm const& e2);
	PresExprNorm operator*(int const_val,PresExprNorm const& e);
	PresExprNorm operator*(PresExprNorm const& e,int const_val);

}}}}//end namespace omega::bindings::parser::ast

#endif
