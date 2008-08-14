#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresConstrParen.hpp"
#include "PresConstr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresConstrParen::PresConstrParen(sptr<PresConstr> const& constr) : PresConstr(NodeType::ConstrParen),m_constr(constr) {}

	sptr<PresConstrParen> PresConstrParen::new_(sptr<PresConstr> const& constr) {return sptr<PresConstrParen>(new PresConstrParen(constr));}

	PresConstrParen::PresConstrParen(PresConstrParen const& o) : PresConstr(o.type()),m_constr(o.constr()) {}

	PresConstrParen& PresConstrParen::operator=(PresConstrParen const& o)
	{
		this->PresConstr::operator=(o);
		this->constr(o.constr());
		return *this;
	}

	sptr<PresConstr> PresConstrParen::constr() const {return this->m_constr;}
	void PresConstrParen::constr(sptr<PresConstr> const& constr) {this->m_constr=constr;}

	std::string PresConstrParen::str() const
	{
		std::stringstream s;
		if(!this->empty())
		{
			s<<"(";
			s<<this->constr()->str();
			s<<")";
		}
		return s.str();
	}

	bool PresConstrParen::empty() const
	{
		return this->constr()->empty();
	}

	void PresConstrParen::apply(IPresVisitor& v) {v.visitPresConstrParen(*this);}

	std::string PresConstrParen::name() const {return "PresConstrParen";}

}}}}//end namespace omega::bindings::parser::ast
