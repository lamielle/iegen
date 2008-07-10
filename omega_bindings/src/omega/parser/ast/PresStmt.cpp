#include "PresUtil.hpp"
#include "PresTypedNode.hpp"
#include "PresStmt.hpp"
#include "PresExpr.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresStmt::PresStmt(NodeType::PresStmtType type,sptr<PresExpr> const& lexpr,sptr<PresStmt> const& rstmt,sptr<PresExpr> const& rexpr) : PresTypedNode<NodeType::PresStmtType>(type),m_lexpr(lexpr),m_rstmt(rstmt),m_rexpr(rexpr) {}

	PresStmt::PresStmt(PresStmt const& o) : PresTypedNode<NodeType::PresStmtType>(o.type()),m_lexpr(o.lexpr()),m_rstmt(o.rstmt()),m_rexpr(o.rexpr()) {}

	PresStmt& PresStmt::operator=(PresStmt const& o)
	{
		this->PresTypedNode<NodeType::PresStmtType>::operator=(o);
		this->lexpr(o.lexpr());
		this->rstmt(o.rstmt());
		this->rexpr(o.rexpr());
		return *this;
	}

	sptr<PresExpr> PresStmt::lexpr() const {return this->m_lexpr;}
	void PresStmt::lexpr(sptr<PresExpr> const& lexpr) {this->m_lexpr=lexpr;}
	sptr<PresStmt> PresStmt::rstmt() const {return this->m_rstmt;}
	void PresStmt::rstmt(sptr<PresStmt> const& rstmt) {this->m_rstmt=rstmt;}
	bool PresStmt::has_rstmt() const {return sptr<PresStmt>()!=this->rstmt();}
	sptr<PresExpr> PresStmt::rexpr() const {return this->m_rexpr;}
	void PresStmt::rexpr(sptr<PresExpr> const& rexpr) {this->m_rexpr=rexpr;}

	std::string PresStmt::str() const
	{
		std::stringstream s;
		s<<this->lexpr()->str();
		s<<this->op();
		if(this->has_rstmt())
			s<<this->rstmt()->str();
		else
			s<<this->rexpr()->str();
		return s.str();
	}

}}}}//end namespace omega::bindings::parser::ast
