#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresConstrForall.hpp"
#include "PresConstrExistsForall.hpp"
#include "PresConstr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresConstrForall::PresConstrForall(varid_vect const& vars,sptr<PresConstr> const& constr) : PresConstrExistsForall(NodeType::Forall,vars,constr) {}

	sptr<PresConstrForall> PresConstrForall::new_(varid_vect const& vars,sptr<PresConstr> const& constr) {return sptr<PresConstrForall>(new PresConstrForall(vars,constr));}

	PresConstrForall::PresConstrForall(PresConstrForall const& o) : PresConstrExistsForall(o.quant_type(),o.vars(),o.constr()) {}

	PresConstrForall& PresConstrForall::operator=(PresConstrForall const& o)
	{
		this->PresConstrExistsForall::operator=(o);
		return *this;
	}

	std::string PresConstrForall::str() const {return this->PresConstrExistsForall::str();}
	std::string PresConstrForall::quant() const {return "FORALL";}

	void PresConstrForall::apply(IPresVisitor& v) {v.visitPresConstrForall(*this);}

	std::string PresConstrForall::name() const {return "PresConstrForall";}

}}}}//end namespace omega::bindings::parser::ast
