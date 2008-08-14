#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVar.hpp"
#include "PresVarRange.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresVarRange::PresVarRange(sptr<PresExpr> const& start,sptr<PresExpr> const& end) : PresVar(NodeType::VarRange),m_start(start),m_end(end) {}

	sptr<PresVarRange> PresVarRange::new_(sptr<PresExpr> const& start,sptr<PresExpr> const& end) {return sptr<PresVarRange>(new PresVarRange(start,end));}

	PresVarRange::PresVarRange(PresVarRange const& o) : PresVar(o.type()),m_start(o.start()),m_end(o.end()) {}

	PresVarRange& PresVarRange::operator=(PresVarRange const& o)
	{
		this->PresVar::operator=(o);
		this->start(o.start());
		this->end(o.end());
		return *this;
	}

	sptr<PresExpr> PresVarRange::start() const {return this->m_start;}
	void PresVarRange::start(sptr<PresExpr> const& start) {this->m_start=start;}
	sptr<PresExpr> PresVarRange::end() const {return this->m_end;}
	void PresVarRange::end(sptr<PresExpr> const& end) {this->m_end=end;}

	std::string PresVarRange::str() const
	{
		std::stringstream s;
		s<<this->start()->str();
		s<<":";
		s<<this->end()->str();
		return s.str();
	}

	void PresVarRange::apply(IPresVisitor& v) {v.visitPresVarRange(*this);}

	std::string PresVarRange::name() const {return "PresVarRange";}

}}}}//end namespace omega::bindings::parser::ast
