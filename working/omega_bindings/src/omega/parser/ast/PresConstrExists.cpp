#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresConstrExists.hpp"
#include "PresConstrExistsForall.hpp"
#include "PresConstr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresConstrExists::PresConstrExists(varid_vect const& vars,sptr<PresConstr> const& constr) : PresConstrExistsForall(NodeType::Exists,vars,constr) {}

	sptr<PresConstrExists> PresConstrExists::new_(varid_vect const& vars,sptr<PresConstr> const& constr) {return sptr<PresConstrExists>(new PresConstrExists(vars,constr));}

	PresConstrExists::PresConstrExists(PresConstrExists const& o) : PresConstrExistsForall(o.quant_type(),o.vars(),o.constr()) {}

	PresConstrExists& PresConstrExists::operator=(PresConstrExists const& o)
	{
		this->PresConstrExistsForall::operator=(o);
		return *this;
	}

	std::string PresConstrExists::str() const {return this->PresConstrExistsForall::str();}
	std::string PresConstrExists::quant() const {return "EXISTS";}

	void PresConstrExists::apply(IPresVisitor& v) {v.visitPresConstrExists(*this);}

	std::string PresConstrExists::name() const {return "PresConstrExists";}

}}}}//end namespace omega::bindings::parser::ast
