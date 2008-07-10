#include <boost/python.hpp>
#include <omega.h>
#include <string>

#include "util.hpp"

#include "PresUtil.hpp"

#include "IPresVisitor.hpp"
#include "PresDepthFirstVisitor.hpp"

#include "IPresVisitable.hpp"
#include "PresNode.hpp"
#include "PresTypedNode.hpp"

#include "PresFormula.hpp"
#include "PresSet.hpp"
#include "PresRelation.hpp"

#include "PresVarTupleSet.hpp"
#include "PresVarTupleIn.hpp"
#include "PresVarTupleOut.hpp"

#include "PresVar.hpp"
#include "PresVarID.hpp"
#include "PresVarUnnamed.hpp"
#include "PresVarExpr.hpp"
#include "PresVarRange.hpp"
#include "PresVarStride.hpp"

#include "PresConstr.hpp"
#include "PresConstrAndOr.hpp"
#include "PresConstrAnd.hpp"
#include "PresConstrOr.hpp"
#include "PresConstrNot.hpp"
#include "PresConstrExistsForall.hpp"
#include "PresConstrExists.hpp"
#include "PresConstrForall.hpp"
#include "PresConstrParen.hpp"

#include "PresStmt.hpp"
#include "PresStmtEQ.hpp"
#include "PresStmtNEQ.hpp"
#include "PresStmtGT.hpp"
#include "PresStmtGTE.hpp"
#include "PresStmtLT.hpp"
#include "PresStmtLTE.hpp"

#include "PresExpr.hpp"
#include "PresExprInt.hpp"
#include "PresExprID.hpp"
#include "PresExprUnOp.hpp"
#include "PresExprNeg.hpp"
#include "PresExprBinOp.hpp"
#include "PresExprAdd.hpp"
#include "PresExprSub.hpp"
#include "PresExprMult.hpp"
#include "PresExprFunc.hpp"
#include "PresExprList.hpp"
#include "PresExprParen.hpp"

using namespace boost::python;

namespace omega { namespace bindings { namespace parser { namespace ast {

	template <typename T>
	void export_container_conversion()
	{
		omega::bindings::from_python_sequence<std::vector<T>,omega::bindings::variable_capacity_policy>();
	}

	void export_pres_root_nodes()
	{
		class_<IPresVisitable,boost::noncopyable>("IPresVisitable",no_init);
		class_<PresNode,bases<IPresVisitable>,boost::noncopyable>("PresNode",no_init)
			.def("__str__",pure_virtual(&PresNode::str))
			.def("name",pure_virtual(&PresNode::name));
	}

	template <typename T>
	void export_root_typed_node(std::string const& name)
	{
		class_<PresTypedNode<T>,bases<PresNode>,boost::noncopyable>(("PresTypedNode_"+name).c_str(),no_init)
			.def("type",(T (PresTypedNode<T>::*)(void)const)&PresTypedNode<T>::type)
			.def("__str__",pure_virtual(&PresTypedNode<T>::str))
			.def("name",pure_virtual(&PresTypedNode<T>::name));
	}

	template <typename T,typename B>
	void export_internal_node(std::string const& name)
	{
		class_<T,bases<B>,boost::noncopyable>(name.c_str(),no_init)
			.def("__str__",&T::str)
			.def("name",&T::name);
	}

	template <typename T,typename B>
	void export_leaf_node(std::string const& name)
	{
		class_<T,bases<B> >(name.c_str(),no_init)
			.def("new",&T::new_)
			.staticmethod("new")
			.def("__str__",&T::str)
			.def("name",&T::name);
		boost::python::register_ptr_to_python<sptr<T> >();
	}

	template <typename T>
	void export_stmt_leaf_node(std::string const& name)
	{
		class_<T,bases<PresStmt> >(name.c_str(),no_init)
			.def("new",(sptr<T> (*)(sptr<PresExpr> const&,sptr<PresStmt> const&))&T::new_)
			.def("new",(sptr<T> (*)(sptr<PresExpr> const&,sptr<PresExpr> const&))&T::new_)
			.staticmethod("new")
			.def("__str__",&T::str)
			.def("name",&T::name);
		boost::python::register_ptr_to_python<sptr<T> >();
	}

	void export_pres_expr_mult()
	{
		class_<PresExprMult,bases<PresExpr> >("PresExprMult",no_init)
			.def("new",(sptr<PresExprMult> (*)(sptr<PresExpr> const&,sptr<PresExpr> const&))&PresExprMult::new_)
			.def("new",(sptr<PresExprMult> (*)(sptr<PresExpr> const&,sptr<PresExpr> const&,bool))&PresExprMult::new_)
			.staticmethod("new")
			.def("__str__",&PresExprMult::str)
			.def("name",&PresExprMult::name)
			.def("simple",(bool (PresExprMult::*)(void) const)&PresExprMult::simple);
		boost::python::register_ptr_to_python<sptr<PresExprMult> >();
	}

	void export_pres_node_type_enums()
	{
		//PresFormulaType
		enum_<NodeType::PresFormulaType>("PresFormulaType")
			.value("Set",NodeType::Set)
			.value("Relation",NodeType::Relation);

		//PresVarType
		enum_<NodeType::PresVarType>("PresVarType")
			.value("Var",NodeType::VarID)
			.value("Unnamed",NodeType::VarUnnamed)
			.value("Expr",NodeType::VarExpr)
			.value("Range",NodeType::VarRange)
			.value("RangeRestrict",NodeType::VarStride);

		//PresConstrType
		enum_<NodeType::PresConstrType>("PresConstrType")
			.value("AndOr",NodeType::AndOr)
			.value("Not",NodeType::Not)
			.value("ExistsForall",NodeType::ExistsForall);

		//PresStmtType
		enum_<NodeType::PresStmtType>("PresStmtType")
			.value("EQ",NodeType::EQ)
			.value("NEQ",NodeType::NEQ)
			.value("LT",NodeType::LT)
			.value("LTE",NodeType::LTE)
			.value("GT",NodeType::GT)
			.value("GTE",NodeType::GTE);

		//PresExprType
		enum_<NodeType::PresExprType>("PresExprType")
			.value("Int",NodeType::Int)
			.value("ID",NodeType::ID)
			.value("Func",NodeType::Func)
			.value("UnOp",NodeType::UnOp)
			.value("BinOp",NodeType::BinOp)
			.value("List",NodeType::List);

		//PresExprUnOpType
		enum_<NodeType::PresExprUnOpType>("PresExprUnOpType")
			.value("Neg",NodeType::Neg);

		//PresExprBinOpType
		enum_<NodeType::PresExprBinOpType>("PresExprBinOpType")
			.value("Add",NodeType::Add)
			.value("Sub",NodeType::Sub)
			.value("Mult",NodeType::Mult);
	}

	void export_pres_formula_nodes()
	{
		export_root_typed_node<NodeType::PresFormulaType>("PresFormulaType");
		export_internal_node<PresFormula,PresTypedNode<NodeType::PresFormulaType> >("PresFormula");

		export_leaf_node<PresSet,PresFormula>("PresSet");
		export_leaf_node<PresRelation,PresFormula>("PresRelation");
	}

	void export_pres_var_tuple_nodes()
	{
		export_root_typed_node<NodeType::PresVarTupleType>("PresVarTupleType");
		export_internal_node<PresVarTuple,PresTypedNode<NodeType::PresVarTupleType> >("PresVarTuple");
		export_leaf_node<PresVarTupleSet,PresVarTuple>("PresVarTupleSet");
		export_leaf_node<PresVarTupleIn,PresVarTuple>("PresVarTupleIn");
		export_leaf_node<PresVarTupleOut,PresVarTuple>("PresVarTupleOut");
		export_container_conversion<sptr<PresVarTuple> >();
	}

	void export_pres_var_nodes()
	{
		export_root_typed_node<NodeType::PresVarType>("PresVarType");
		export_internal_node<PresVar,PresTypedNode<NodeType::PresVarType> >("PresVar");
		export_leaf_node<PresVarID,PresVar>("PresVarID");
		export_leaf_node<PresVarUnnamed,PresVar>("PresVarUnnamed");
		export_leaf_node<PresVarExpr,PresVar>("PresVarExpr");
		export_leaf_node<PresVarRange,PresVar>("PresVarRange");
		export_leaf_node<PresVarStride,PresVar>("PresVarStride");
		export_container_conversion<sptr<PresVar> >();
		export_container_conversion<sptr<PresVarID> >();
	}

	void export_pres_constr_nodes()
	{
		export_root_typed_node<NodeType::PresConstrType>("PresConstrType");
		export_internal_node<PresConstr,PresTypedNode<NodeType::PresConstrType> >("PresConstr");
		export_internal_node<PresConstrAndOr,PresConstr>("PresConstrAndOr");
		export_leaf_node<PresConstrAnd,PresConstrAndOr>("PresConstrAnd");
		export_leaf_node<PresConstrOr,PresConstrAndOr>("PresConstrOr");
		export_leaf_node<PresConstrNot,PresConstr>("PresConstrNot");
		export_internal_node<PresConstrExistsForall,PresConstr>("PresConstrExistsForall");
		export_leaf_node<PresConstrExists,PresConstrExistsForall>("PresConstrExists");
		export_leaf_node<PresConstrForall,PresConstrExistsForall>("PresConstrForall");
		export_leaf_node<PresConstrParen,PresConstr>("PresConstrParen");
		export_container_conversion<sptr<PresConstr> >();
	}

	void export_pres_stmt_nodes()
	{
		export_root_typed_node<NodeType::PresStmtType>("PresStmtType");
		export_internal_node<PresStmt,PresTypedNode<NodeType::PresStmtType> >("PresStmt");
		export_stmt_leaf_node<PresStmtEQ>("PresStmtEQ");
		export_stmt_leaf_node<PresStmtNEQ>("PresStmtNEQ");
		export_stmt_leaf_node<PresStmtGT>("PresStmtGT");
		export_stmt_leaf_node<PresStmtGTE>("PresStmtGTE");
		export_stmt_leaf_node<PresStmtLT>("PresStmtLT");
		export_stmt_leaf_node<PresStmtLTE>("PresStmtLTE");
		export_container_conversion<sptr<PresStmt> >();
	}

	void export_pres_expr_nodes()
	{
		export_root_typed_node<NodeType::PresExprType>("PresExprType");
		export_internal_node<PresExpr,PresTypedNode<NodeType::PresExprType> >("PresExpr");
		export_leaf_node<PresExprInt,PresExpr>("PresExprInt");
		export_leaf_node<PresExprID,PresExpr>("PresExprID");
		export_internal_node<PresExprUnOp,PresExpr>("PresExprUnOp");
		export_leaf_node<PresExprNeg,PresExprUnOp>("PresExprNeg");
		export_internal_node<PresExprBinOp,PresExpr>("PresExprBinOp");
		export_leaf_node<PresExprAdd,PresExprBinOp>("PresExprAdd");
		export_leaf_node<PresExprSub,PresExprBinOp>("PresExprSub");
		export_pres_expr_mult();
		export_leaf_node<PresExprList,PresExpr>("PresExprList");
		export_leaf_node<PresExprFunc,PresExpr>("PresExprFunc");
		export_leaf_node<PresExprParen,PresExpr>("PresExprParen");
		export_container_conversion<sptr<PresExpr> >();
		export_container_conversion<std::string>();
	}

	BOOST_PYTHON_MODULE(_ast)
	{
		export_pres_node_type_enums();
		export_pres_root_nodes();
		export_pres_formula_nodes();
		export_pres_var_tuple_nodes();
		export_pres_var_nodes();
		export_pres_constr_nodes();
		export_pres_stmt_nodes();
		export_pres_expr_nodes();
	}

}}}}//end namespace omega::bindings::parser::ast
