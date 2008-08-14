#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVar.hpp"
#include "PresVarStride.hpp"
#include "PresExpr.hpp"
#include "PresExprInt.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresVarStride::PresVarStride(sptr<PresExpr> const& start,sptr<PresExpr> const& end,sptr<PresExprInt> const& stride) : PresVar(NodeType::VarStride),m_start(start),m_end(end),m_stride(stride) {}

	sptr<PresVarStride> PresVarStride::new_(sptr<PresExpr> const& start,sptr<PresExpr> const& end,sptr<PresExprInt> const& stride) {return sptr<PresVarStride>(new PresVarStride(start,end,stride));}

	PresVarStride::PresVarStride(PresVarStride const& o) : PresVar(o.type()),m_start(o.start()),m_end(o.end()),m_stride(o.stride()) {}

	PresVarStride& PresVarStride::operator=(PresVarStride const& o)
	{
		this->PresVar::operator=(o);
		this->start(o.start());
		this->end(o.end());
		this->stride(o.stride());
		return *this;
	}

	sptr<PresExpr> PresVarStride::start() const {return this->m_start;}
	void PresVarStride::start(sptr<PresExpr> const& start) {this->m_start=start;}
	sptr<PresExpr> PresVarStride::end() const {return this->m_end;}
	void PresVarStride::end(sptr<PresExpr> const& end) {this->m_end=end;}
	sptr<PresExprInt> PresVarStride::stride() const {return this->m_stride;}
	void PresVarStride::stride(sptr<PresExprInt> const& stride) {this->m_stride=stride;}

	std::string PresVarStride::str() const
	{
		std::stringstream s;
		s<<this->start()->str();
		s<<":";
		s<<this->end()->str();
		s<<":";
		s<<this->stride()->str();
		return s.str();
	}

	void PresVarStride::apply(IPresVisitor& v) {v.visitPresVarStride(*this);}

	std::string PresVarStride::name() const {return "PresVarStride";}

}}}}//end namespace omega::bindings::parser::ast
