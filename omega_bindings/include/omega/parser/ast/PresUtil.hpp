#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_UTIL_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_UTIL_H_

#include "util.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Subtypes for the main node types
	namespace NodeType {
		enum PresFormulaType {Set,Relation};
		enum PresVarTupleType {SetVars,InVars,OutVars};
		enum PresVarType {VarID,VarUnnamed,VarExpr,VarRange,VarStride};
		enum PresConstrType {AndOr,Not,ExistsForall,ConstrParen};
		enum PresConstrAndOrType {And,Or};
		enum PresConstrExistsForallType {Exists,Forall};
		enum PresStmtType {EQ,NEQ,LT,LTE,GT,GTE};
		enum PresExprType {Int,ID,Func,UnOp,BinOp,List,ExprParen};
		enum PresExprUnOpType {Neg};
		enum PresExprBinOpType {Add,Sub,Mult};
	}//end namespace NodeType

	//Forward declarations of all AST related classes
	class PresNode;

	class PresFormula;
	class PresSet;
	class PresRelation;

	class PresVarTupleSet;
	class PresVarTupleIn;
	class PresVarTupleOut;

	class PresVar;
	class PresVarID;
	class PresVarUnnamed;
	class PresVarRange;
	class PresVarStride;
	class PresVarExpr;

	class PresConstr;
	class PresConstrAndOr;
	class PresConstrAnd;
	class PresConstrOr;
	class PresConstrNot;
	class PresConstrExistsForall;
	class PresConstrExists;
	class PresConstrForall;
	class PresConstrParen;

	class PresStmt;
	class PresStmtEQ;
	class PresStmtNEQ;
	class PresStmtGT;
	class PresStmtGTE;
	class PresStmtLT;
	class PresStmtLTE;

	class PresExpr;
	class PresExprInt;
	class PresExprID;
	class PresExprUnOp;
	class PresExprNeg;
	class PresExprBinOp;
	class PresExprAdd;
	class PresExprSub;
	class PresExprMult;
	class PresExprList;
	class PresExprFunc;
	class PresExprParen;
	class PresExprNorm;

	namespace visitor {
		class IPresVisitor;
		class IPresVisitable;
		class PresDepthFirstVisitor;
	}//end namespace visitor

	//Define types for vectors of various nodes
	typedef std::vector<sptr<PresNode> > node_vect;
	typedef std::vector<sptr<PresVar> > var_vect;
	typedef std::vector<sptr<PresVarID> > varid_vect;
	typedef std::vector<sptr<PresConstr> > constr_vect;
	typedef std::vector<sptr<PresStmt> > stmt_vect;
	typedef std::vector<sptr<PresExpr> > expr_vect;
	typedef std::vector<std::string> str_vect;

	typedef boost::tuple<int,sptr<PresExpr> > norm_tuple;
	typedef std::map<std::string,norm_tuple> norm_map;

	typedef std::stack<PresExprNorm> norm_stack;

	template <typename T>
	node_vect get_pres_node_vector(std::vector<sptr<T> > const& v)
	{
		node_vect new_v;
		foreach(sptr<PresNode> node,v)
			new_v.push_back(node);
		return new_v;
	}

	std::string get_string_from_vector(node_vect const& items,std::string const& sep);
	std::string get_string_from_strings(str_vect const& strings,std::string const& sep);


#if 0
namespace omega { namespace bindings { namespace parser { namespace ast {

//Method for typedefing a templated class
//Goal of these two classes is to change using
//boost::shared_ptr/weak_ptr<T> to sptr<T>::t
template <class T> class sptr
{
	public:
		typedef boost::shared_ptr<T> t;
};

template <class T> class wptr
{
	public:
		typedef boost::weak_ptr<T> t;
};

#endif

}}}}//end namespace omega::bindings::parser::ast

#endif
