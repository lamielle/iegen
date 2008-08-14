#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresConstrAnd.hpp"
#include "PresConstrAndOr.hpp"
#include "PresConstr.hpp"
#include "PresStmt.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresConstrAnd::PresConstrAnd(constr_vect const& constrs,stmt_vect const& stmts) : PresConstrAndOr(NodeType::And,constrs,stmts) {}

	sptr<PresConstrAnd> PresConstrAnd::new_(constr_vect const& constrs,stmt_vect const& stmts) {return sptr<PresConstrAnd>(new PresConstrAnd(constrs,stmts));}

	PresConstrAnd::PresConstrAnd(PresConstrAnd const& o) : PresConstrAndOr(o.quant_type(),o.constrs(),o.stmts()) {}

	PresConstrAnd& PresConstrAnd::operator=(PresConstrAnd const& o)
	{
		this->PresConstrAndOr::operator=(o);
		return *this;
	}

	std::string PresConstrAnd::str() const {return this->PresConstrAndOr::str();}
	std::string PresConstrAnd::sep() const {return "AND";}

	void PresConstrAnd::apply(IPresVisitor& v) {v.visitPresConstrAnd(*this);}

	std::string PresConstrAnd::name() const {return "PresConstrAnd";}

}}}}//end namespace omega::bindings::parser::ast
