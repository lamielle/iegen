#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresConstrOr.hpp"
#include "PresConstrAndOr.hpp"
#include "PresConstr.hpp"
#include "PresStmt.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresConstrOr::PresConstrOr(constr_vect const& constrs,stmt_vect const& stmts) : PresConstrAndOr(NodeType::Or,constrs,stmts) {}

	sptr<PresConstrOr> PresConstrOr::new_(constr_vect const& constrs,stmt_vect const& stmts) {return sptr<PresConstrOr>(new PresConstrOr(constrs,stmts));}

	PresConstrOr::PresConstrOr(PresConstrOr const& o) : PresConstrAndOr(o.quant_type(),o.constrs(),o.stmts()) {}

	PresConstrOr& PresConstrOr::operator=(PresConstrOr const& o)
	{
		this->PresConstrAndOr::operator=(o);
		return *this;
	}

	std::string PresConstrOr::str() const {return this->PresConstrAndOr::str();}
	std::string PresConstrOr::sep() const {return "OR";}

	void PresConstrOr::apply(IPresVisitor& v) {v.visitPresConstrOr(*this);}

	std::string PresConstrOr::name() const {return "PresConstrOr";}

}}}}//end namespace omega::bindings::parser::ast
