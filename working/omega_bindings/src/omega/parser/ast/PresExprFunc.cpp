#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresExpr.hpp"
#include "PresExprFunc.hpp"
#include "PresVarID.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresExprFunc::PresExprFunc(sptr<PresVarID> const& func_name,varid_vect const& args) : PresExpr(NodeType::Func),m_func_name(func_name),m_args(args) {}

	sptr<PresExprFunc> PresExprFunc::new_(sptr<PresVarID> const& func_name,varid_vect const& args) {return sptr<PresExprFunc>(new PresExprFunc(func_name,args));}

	PresExprFunc::PresExprFunc(PresExprFunc const& o) : PresExpr(o.type()),m_func_name(o.func_name()),m_args(o.args()) {}

	PresExprFunc& PresExprFunc::operator=(PresExprFunc const& o)
	{
		this->PresExpr::operator=(o);
		this->func_name(o.func_name());
		this->args(o.args());
		return *this;
	}

	sptr<PresVarID> PresExprFunc::func_name() const {return this->m_func_name;}
	void PresExprFunc::func_name(sptr<PresVarID> const& func_name) {this->m_func_name=func_name;}
	varid_vect PresExprFunc::args() const {return this->m_args;}
	void PresExprFunc::args(varid_vect const& args) {this->m_args=args;}

	std::string PresExprFunc::str() const
	{
		std::stringstream s;
		s<<this->func_name()->str();
		s<<"(";
		s<<get_string_from_vector(get_pres_node_vector(this->args()),",");
		s<<")";
		return s.str();
	}

	void PresExprFunc::apply(IPresVisitor& v) {v.visitPresExprFunc(*this);}

	std::string PresExprFunc::name() const {return "PresExprFunc";}

}}}}//end namespace omega::bindings::parser::ast
