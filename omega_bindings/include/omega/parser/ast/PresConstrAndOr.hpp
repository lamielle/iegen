#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_AND_OR_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_CONSTR_AND_OR_H_

#include "PresUtil.hpp"
#include "PresConstr.hpp"
#include "PresStmt.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger AndOr AST node
	class PresConstrAndOr : public PresConstr
	{
		protected:
			PresConstrAndOr(NodeType::PresConstrAndOrType quant_type,constr_vect const& constrs,stmt_vect const& stmts);
			PresConstrAndOr(PresConstrAndOr const& o);
			PresConstrAndOr& operator=(PresConstrAndOr const& o);

			virtual std::string sep() const=0;

		public:
			virtual std::string str() const;
			virtual bool empty() const;

			NodeType::PresConstrAndOrType quant_type() const;
			constr_vect constrs() const;
			stmt_vect stmts() const;

		private:
			void quant_type(NodeType::PresConstrAndOrType quant_type);
			void constrs(constr_vect const& constrs);
			void stmts(stmt_vect const& stmts);
			NodeType::PresConstrAndOrType m_quant_type;
			constr_vect m_constrs;
			stmt_vect m_stmts;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
