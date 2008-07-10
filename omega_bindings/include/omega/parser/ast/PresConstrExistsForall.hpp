#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_EXISTS_FORALL_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_EXISTS_FORALL_H_

#include "PresUtil.hpp"
#include "PresConstr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger ExistsForall AST node
	class PresConstrExistsForall : public PresConstr
	{
		protected:
			PresConstrExistsForall(NodeType::PresConstrExistsForallType quant_type,varid_vect const& vars,sptr<PresConstr> const& constr);
			PresConstrExistsForall(PresConstrExistsForall const& o);
			PresConstrExistsForall& operator=(PresConstrExistsForall const& o);

			virtual std::string quant() const=0;

		public:
			virtual std::string str() const;
			virtual bool empty() const;

			NodeType::PresConstrExistsForallType quant_type() const;
			varid_vect vars() const;
			sptr<PresConstr> constr() const;

		private:
			void quant_type(NodeType::PresConstrExistsForallType quant_type);
			void vars(varid_vect const& vars);
			void constr(sptr<PresConstr> const& constr);
			NodeType::PresConstrExistsForallType m_quant_type;
			varid_vect m_vars;
			sptr<PresConstr> m_constr;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
