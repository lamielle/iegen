#include "PresUtil.hpp"
#include "PresNode.hpp"
#include "PresConstr.hpp"
#include "PresConstrAndOr.hpp"
#include "PresStmt.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	PresConstrAndOr::PresConstrAndOr(NodeType::PresConstrAndOrType quant_type,constr_vect const& constrs,stmt_vect const& stmts) : PresConstr(NodeType::AndOr),m_quant_type(quant_type),m_constrs(constrs),m_stmts(stmts) {}

	PresConstrAndOr::PresConstrAndOr(PresConstrAndOr const& o) : PresConstr(o.type()),m_quant_type(o.quant_type()),m_constrs(o.constrs()),m_stmts(o.stmts()) {}

	PresConstrAndOr& PresConstrAndOr::operator=(PresConstrAndOr const& o)
	{
		this->PresConstr::operator=(o);
		this->quant_type(o.quant_type());
		this->constrs(o.constrs());
		this->stmts(o.stmts());
		return *this;
	}

	NodeType::PresConstrAndOrType PresConstrAndOr::quant_type() const {return this->m_quant_type;}
	void PresConstrAndOr::quant_type(NodeType::PresConstrAndOrType quant_type) {this->m_quant_type=quant_type;}
	constr_vect PresConstrAndOr::constrs() const {return this->m_constrs;}
	void PresConstrAndOr::constrs(constr_vect const& constrs) {this->m_constrs=constrs;}
	stmt_vect PresConstrAndOr::stmts() const {return this->m_stmts;}
	void PresConstrAndOr::stmts(stmt_vect const& stmts) {this->m_stmts=stmts;}

	template node_vect get_pres_node_vector(constr_vect const& v);
	template node_vect get_pres_node_vector(stmt_vect const& v);
	std::string PresConstrAndOr::str() const
	{
		std::stringstream s;
		//Only return something if this constraint is not empty
		if(!this->empty())
		{
			//Trim out all empty constraints and combine statements and constraints
			node_vect nodes;
			foreach(sptr<PresConstr> constr,this->constrs())
				if(!constr->empty())
					nodes.push_back(constr);
			foreach(sptr<PresStmt> stmt,this->stmts())
				nodes.push_back(stmt);

			std::string sep=" "+this->sep()+" ";
			s<<get_string_from_vector(nodes,sep);
		}
		return s.str();
	}

	//empty if no statments and (no constrs or all constrs empty)
	//-OR- (by De Morgan)
	//not empty if any constraints or (any constraints and not all empty)
	bool PresConstrAndOr::empty() const
	{
		bool empty=true;
		if(0!=this->stmts().size()) empty=false;
		if(0!=this->constrs().size())
			foreach(sptr<PresConstr> constr,this->constrs())
				if(!constr->empty()) empty=false;
		return empty;
	}

}}}}//end namespace omega::bindings::parser::ast
