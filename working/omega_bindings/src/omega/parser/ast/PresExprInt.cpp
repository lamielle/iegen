#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"
#include "PresExprInt.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprInt::PresExprInt(int value) : PresExpr(NodeType::Int),m_value(value) {}

	sptr<PresExprInt> PresExprInt::new_(int value) {return sptr<PresExprInt>(new PresExprInt(value));}

	PresExprInt::PresExprInt(PresExprInt const& o) : PresExpr(o.type()),m_value(o.value()) {}

	PresExprInt& PresExprInt::operator=(PresExprInt const& o)
	{
		this->PresExpr::operator=(o);
		this->value(o.value());
		return *this;
	}

	int PresExprInt::value() const {return this->m_value;}
	void PresExprInt::value(int value) {this->m_value=value;}

	std::string PresExprInt::str() const
	{
		std::stringstream s;
		s<<this->value();
		return s.str();
	}

	void PresExprInt::apply(IPresVisitor& v) {v.visitPresExprInt(*this);}

	std::string PresExprInt::name() const {return "PresExprInt";}

}}}}//end namespace omega::bindings::parser::ast
