#include "PresUtil.hpp"
#include "PresConstr.hpp"
#include "PresConstrExistsForall.hpp"
#include "PresVarID.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresConstrExistsForall::PresConstrExistsForall(NodeType::PresConstrExistsForallType quant_type,varid_vect const& vars,sptr<PresConstr> const& constr) : PresConstr(NodeType::ExistsForall),m_quant_type(quant_type),m_vars(vars),m_constr(constr) {}

	PresConstrExistsForall::PresConstrExistsForall(PresConstrExistsForall const& o) : PresConstr(o.type()),m_quant_type(o.quant_type()),m_vars(o.vars()),m_constr(o.constr()) {}

	PresConstrExistsForall& PresConstrExistsForall::operator=(PresConstrExistsForall const& o)
	{
		this->PresConstr::operator=(o);
		this->quant_type(o.quant_type());
		this->vars(o.vars());
		this->constr(o.constr());
		return *this;
	}

	NodeType::PresConstrExistsForallType PresConstrExistsForall::quant_type() const {return this->m_quant_type;}
	void PresConstrExistsForall::quant_type(NodeType::PresConstrExistsForallType quant_type) {this->m_quant_type=quant_type;}
	varid_vect PresConstrExistsForall::vars() const {return this->m_vars;}
	void PresConstrExistsForall::vars(varid_vect const& vars) {this->m_vars=vars;}
	sptr<PresConstr> PresConstrExistsForall::constr() const {return this->m_constr;}
	void PresConstrExistsForall::constr(sptr<PresConstr> const& constr) {this->m_constr=constr;}

	std::string PresConstrExistsForall::str() const
	{
		std::stringstream s;
		if(!this->empty())
		{
			s<<this->quant();
			s<<"([";
			s<<get_string_from_vector(get_pres_node_vector(this->vars()),",");
			s<<"]:";
			s<<this->constr()->str();
			s<<")";
		}
		return s.str();
	}

	bool PresConstrExistsForall::empty() const
	{
		bool empty=true;
		if(0!=this->vars().size()) empty=false;
		if(!this->constr()->empty()) empty=false;
		return empty;
	}

}}}}//end namespace omega::bindings::parser::ast
