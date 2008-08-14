#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_FORMULA_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_FORMULA_H_

#include "PresUtil.hpp"
#include "PresTypedNode.hpp"
#include "PresConstr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger formula AST node: Either a Set or a Relation
	class PresFormula : public PresTypedNode<NodeType::PresFormulaType>
	{
		protected:
			PresFormula(NodeType::PresFormulaType type);
			PresFormula(NodeType::PresFormulaType type,sptr<PresConstr> constr);
			PresFormula(PresFormula const& o);
			virtual PresFormula& operator=(PresFormula const& o);

		public:
			sptr<PresConstr> constr() const;

		private:
			void constr(sptr<PresConstr> constr);
			sptr<PresConstr> m_constr;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
