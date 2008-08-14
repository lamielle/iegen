#ifndef _OMEGA_BINDINGS_FORMULA_H_
#define _OMEGA_BINDINGS_FORMULA_H_

#include <boost/python.hpp>
#include <omega.h>
#include "util.hpp"
#include "PresUtil.hpp"
#include "PresExprNorm.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	using namespace omega::bindings::parser::ast;

	//Parent class of both Relation and Set
	//A generalization of both.
	//Contains the omega::Relation object that these classes wrap
	class Formula
	{
		public:
			virtual ~Formula();
			Formula(Formula const& c);
			Formula& operator=(Formula const& c);

			std::string str();

			void union_(sptr<Formula> const& o);

		protected:
			Formula(int arity);
			Formula(int arity_in,int arity_out);

			omega::Relation const& const_relation() const;
			omega::Relation& relation();

			void relation(omega::Relation const& relation);

		private:
			omega::Relation m_relation;

		//---------- Variable members ----------
		protected:
			void name(int i,int max_vars,std::string const& name,void (omega::Relation::*name_var)(int,omega::Const_String),Variable_ID (omega::Relation::*get_var)(int));
			std::string name(int i,int max_vars,Variable_ID (omega::Relation::*get_var)(int));
			virtual bool is_var_name(std::string const& name)=0;

		protected:
			virtual Variable_ID get_formula_var(std::string const& name)=0;
			Variable_ID get_local_var(std::string const& name);
			Variable_ID get_func(std::string name,str_vect::size_type arity);
		//---------------------------------------------

		//---------- Free variable members ----------
		public:
			std::map<std::string,sptr<Free_Var_Decl> > const_free_vars() const;

		protected:
			std::map<std::string,sptr<Free_Var_Decl> >& free_vars();

		private:
			void free_vars(std::map<std::string,sptr<Free_Var_Decl> > const& free_vars);
			std::map<std::string,sptr<Free_Var_Decl> > m_free_vars;
		//--------------------------------------------

		//---------- Func members ----------
		public:
			std::map<std::string,sptr<Free_Var_Decl> > const_funcs() const;

		protected:
			std::map<std::string,sptr<Free_Var_Decl> >& funcs();

		private:
			void funcs(std::map<std::string,sptr<Free_Var_Decl> > const& funcs);
			std::map<std::string,sptr<Free_Var_Decl> > m_funcs;
		//--------------------------------------------

		//---------- Formula stack members ----------
		private:
			form_stack m_formula_stack;

			form_stack const& const_formula_stack() const;
			form_stack& formula_stack();
			void formula_stack(form_stack const& formula_stack);

		public:
			omega::Formula* curr_formula();
			omega::F_And* curr_formula_and();
			void push_and();
			void push_or();
			void push_not();
			void pop_formula();
		//-------------------------------------------

		//---------- Statement adding members ----------
		public:
			void add_eq();
			void add_neq();
			void add_gt();
			void add_gte();
			void add_lt();
			void add_lte();

		private:
			void setup_constr(PresExprNorm const& norm_expr,Constraint_Handle constr);
		//---------------------------------------

		//---------- Normalized expression stack members ----------
		public:
			PresExprNorm curr_expr();
			void push_int(PresExprInt const& int_expr);
			void push_id(PresExprID const& id_expr);
			void push_func(PresExprFunc const& func_expr);
			void push_expr(PresExprNorm const& norm_expr);
			void pop_expr();

		private:
			norm_stack m_expr_stack;

			norm_stack const& const_expr_stack() const;
			norm_stack& expr_stack();
			void expr_stack(norm_stack const& expr_stack);
		//---------------------------------------------------------

	};

}}//end namespace omega::bindings

#endif
