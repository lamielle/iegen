#include "PresUtil.hpp"
#include "PresTypedNode.hpp"
#include "PresFormula.hpp"
#include "PresConstr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresFormula::PresFormula(NodeType::PresFormulaType type) : PresTypedNode<NodeType::PresFormulaType>(type),m_constr() {}

	PresFormula::PresFormula(NodeType::PresFormulaType type,sptr<PresConstr> constr) : PresTypedNode<NodeType::PresFormulaType>(type),m_constr(constr) {}

	PresFormula::PresFormula(PresFormula const& o) : PresTypedNode<NodeType::PresFormulaType>(o.type()),m_constr(o.constr()) {}

	PresFormula& PresFormula::operator=(PresFormula const& o)
	{
		this->PresTypedNode<NodeType::PresFormulaType>::operator=(o);
		this->constr(o.constr());
		return *this;
	}

	sptr<PresConstr> PresFormula::constr() const {return sptr<PresConstr>(this->m_constr);}
	void PresFormula::constr(sptr<PresConstr> constr) {this->m_constr=sptr<PresConstr>(constr);}

}}}}//end namespace omega::bindings::parser::ast
