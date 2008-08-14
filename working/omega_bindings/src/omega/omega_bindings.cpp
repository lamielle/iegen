#include <boost/python.hpp>
#include <omega.h>
#include <string>
#include "Var.hpp"
#include "FreeVar.hpp"
#include "FPart.hpp"
#include "FConj.hpp"
#include "OldSet.hpp"
#include "OldRelation.hpp"
#include "Formula.hpp"
#include "Set.hpp"
#include "Relation.hpp"
#include "OmegaException.hpp"
#include "util.hpp"

using namespace boost::python;
using namespace omega::bindings;

namespace omega { namespace bindings {

	void export_omega_enums()
	{
		//TupleType
		enum_<omega::Argument_Tuple>("TupleType")
			.value("inp",omega::Input_Tuple)
			.value("outp",omega::Output_Tuple)
			.value("set",omega::Set_Tuple);

		//ConjType
		enum_<FConj::FConj_Type>("ConjType")
			.value("And",FConj::And)
			.value("Or",FConj::Or)
			.value("Not",FConj::Not);

		//StmtType
		enum_<FStmt::FStmt_Type>("StmtType")
			.value("EQ",FStmt::EQ)
			.value("GEQ",FStmt::GEQ)
			.value("Stride",FStmt::Stride);
	}

	void export_omega_formula_building()
	{
		//--------------------------------------------------
		//Formula Class Definitions
		//--------------------------------------------------
		//FPart
		class_<FPart>("FPart",no_init);
		//FConj
		class_<FConj,bases<FPart> >("FConj",no_init)
			.def("__str__",&FConj::str)
			.def("__repr__",&FConj::str)
			.def("type",(FConj::FConj_Type (FConj::*)(void) const)&FConj::type)
			.def(FStmt() & self).def(self & FStmt())
			.def(FStmt() | self).def(self | FStmt())
			.def(self | FConj()).def(FConj() | self)
			.def(self & FConj()).def(FConj() & self);
		//FStmt
		class_<FStmt,bases<FPart> >("FStmt",no_init)
			.def("__str__",&FStmt::str)
			.def("__repr__",&FStmt::str)
			.def("type",(FStmt::FStmt_Type (FStmt::*)(void) const)&FStmt::type)
			.def("expr",(FExpr (FStmt::*)(void) const)&FStmt::expr)
			.def(self & FStmt()).def(FStmt() & self)
			.def(self | FStmt()).def(FStmt() | self);
		//FExpr
		class_<FExpr,bases<FPart> >("FExpr",no_init)
			.def("__str__",&FExpr::str)
			.def("__repr__",&FExpr::str)
			.def("vars",&FExpr::vars_tuple)
			.def("const",(int (FExpr::*)(void) const)&FExpr::constant)

			.def(self+int()) .def(int()+self)
			.def(self-int()) .def(int()-self)
			.def(self+Var()) .def(Var()+self)
			.def(self-Var()) .def(Var()-self)
			.def(self+FVar()).def(FVar()+self)
			.def(self-FVar()).def(FVar()-self)
			.def(self+FExpr())
			.def(self-FExpr())

			.def(self*int()) .def(int()*self)

			.def(self==int()).def(int()==self)
			.def(self!=int()).def(int()!=self)
			.def(self>=int()).def(int()>=self)
			.def(self<=int()).def(int()<=self)
			.def(self>int()) .def(int()>self)
			.def(self<int()) .def(int()<self)

			.def(self==Var()).def(Var()==self)
			.def(self!=Var()).def(Var()!=self)
			.def(self>=Var()).def(Var()>=self)
			.def(self<=Var()).def(Var()<=self)
			.def(self>Var()) .def(Var()>self)
			.def(self<Var()) .def(Var()<self)

			.def(self==FVar()).def(FVar()==self)
			.def(self!=FVar()).def(FVar()!=self)
			.def(self>=FVar()).def(FVar()>=self)
			.def(self<=FVar()).def(FVar()<=self)
			.def(self>FVar()) .def(FVar()>self)
			.def(self<FVar()) .def(FVar()<self)

			.def(self==FExpr())
			.def(self!=FExpr())
			.def(self>=FExpr())
			.def(self<=FExpr())
			.def(self>FExpr())
			.def(self<FExpr())

			.def(-self);

		//FVar
		class_<FVar,bases<FPart> >("FVar",no_init)
			.def("__str__",&FVar::str)
			.def("__repr__",&FVar::str)
			.def("name",&FVar::name)
			.def("coeff",(int (FVar::*)(void) const)&FVar::coeff)

			.def(self+int()) .def(int()+self)
			.def(self-int()) .def(int()-self)
			.def(self+Var()) .def(Var()+self)
			.def(self-Var()) .def(Var()-self)
			.def(self+FVar())
			.def(self-FVar())

			.def(self*int()) .def(int()*self)

			.def(self==int()).def(int()==self)
			.def(self!=int()).def(int()==self)
			.def(self>=int()).def(int()>=self)
			.def(self<=int()).def(int()<=self)
			.def(self>int()) .def(int()>self)
			.def(self<int()) .def(int()<self)

			.def(self==Var()).def(Var()==self)
			.def(self!=Var()).def(Var()!=self)
			.def(self>=Var()).def(Var()>=self)
			.def(self<=Var()).def(Var()<=self)
			.def(self>Var()) .def(Var()>self)
			.def(self<Var()) .def(Var()<self)

			.def(self==FVar())
			.def(self!=FVar())
			.def(self>=FVar())
			.def(self<=FVar())
			.def(self>FVar())
			.def(self<FVar())

			.def(-self);

		//Var
		class_<Var>("Var",no_init)
			.def("__str__",&Var::str)
			.def("__repr__",&Var::str)
			.def("name",&Var::name)

			.def(self+int()) .def(int()+self)
			.def(self-int()) .def(int()-self)
			.def(self+Var())
			.def(self-Var())

			.def(self*int()) .def(int()*self)

			.def(self==int()).def(int()==self)
			.def(self!=int()).def(int()!=self)
			.def(self>=int()).def(int()>=self)
			.def(self<=int()).def(int()<=self)
			.def(self>int()) .def(int()>self)
			.def(self<int()) .def(int()<self)

			.def(self==Var())
			.def(self!=Var())
			.def(self>=Var())
			.def(self<=Var())
			.def(self>Var())
			.def(self<Var())

			.def(-self);

		//FreeVar
		class_<FreeVar>("FreeVar",no_init)
			.def("__str__",&FreeVar::str)
			.def("__repr__",&FreeVar::str);
	}

	void export_omega_old_formulas()
	{
		//TupleCollection
		class_<TupleCollection>("TupleCollection",no_init)
			.def("__getitem__",(Var (TupleCollection::*)(std::string const&))&TupleCollection::getitem)
			.def("__getitem__",(Var (TupleCollection::*)(python::tuple const&))&TupleCollection::getitem)
			.def("__setitem__",&TupleCollection::setitem)
			.def("append",(void (TupleCollection::*)(FStmt const&,FConj::FConj_Type))&TupleCollection::append)
			.def("append",(void (TupleCollection::*)(FConj const&,FConj::FConj_Type))&TupleCollection::append)
			.def("set_formula",(void (TupleCollection::*)(void))&TupleCollection::set_formula)
			.def("set_formula",(void (TupleCollection::*)(FStmt const&))&TupleCollection::set_formula)
			.def("set_formula",(void (TupleCollection::*)(FConj const&))&TupleCollection::set_formula)
			.add_property("formula",&TupleCollection::get_formula,(void (TupleCollection::*)(FConj const&))&TupleCollection::set_formula);

		//OldSet
		class_<OldSet,bases<TupleCollection> >("OldSet",init<int>())
			.def(init<std::string const&>())
			.def(init<python::tuple const&>())
			.def("__str__",&OldSet::str)
			.def("__repr__",&OldSet::str)
			.def("arity",&OldSet::arity)
			.def("name",(void (OldSet::*)(int,std::string const&))&OldSet::name)
			.def("name",(void (OldSet::*)(python::tuple const&))&OldSet::name)
			.def("name",(std::string (OldSet::*)(int i))&OldSet::name)
			.def("names",&OldSet::names)
			.def("apply",&OldSet::apply)
			.def("__iter__",&OldSet::iter)
			.def("code",&OldSet::code)
			.def("__enter__",&OldSet::get_vars)
			.def("__exit__",&OldSet::clear_vars);

		//OldRelation
		class_<bindings::OldRelation,bases<TupleCollection> >("OldRelation",init<int,int>())
			.def(init<std::string const&,std::string const&>())
			.def(init<python::tuple const&,python::tuple const&>())
			.def(init<OldSet>())
			.def("__str__",&bindings::OldRelation::str)
			.def("__repr__",&bindings::OldRelation::str)
			.def("arity_in",&bindings::OldRelation::arity_in)
			.def("arity_out",&bindings::OldRelation::arity_out)
			.def("name_in",(void (bindings::OldRelation::*)(int,std::string const&))&bindings::OldRelation::name_in)
			.def("name_in",(void (bindings::OldRelation::*)(python::tuple const&))&bindings::OldRelation::name_in)
			.def("name_in",(std::string (bindings::OldRelation::*)(int i))&bindings::OldRelation::name_in)
			.def("names_in",&bindings::OldRelation::names_in)
			.def("name_out",(void (bindings::OldRelation::*)(int,std::string const&))&bindings::OldRelation::name_out)
			.def("name_out",(void (bindings::OldRelation::*)(python::tuple const&))&bindings::OldRelation::name_out)
			.def("name_out",(std::string (bindings::OldRelation::*)(int))&bindings::OldRelation::name_out)
			.def("names_out",&bindings::OldRelation::names_out)
			.def("names",&bindings::OldRelation::names)
			.def("identity",(bindings::OldRelation (*)(long))&bindings::OldRelation::identity)
			.staticmethod("identity")
			.def("scale",(bindings::OldRelation (*)(long,long))&bindings::OldRelation::scale)
			.def("scale",(bindings::OldRelation (*)(long,long,long))&bindings::OldRelation::scale)
			.staticmethod("scale")
			.def("skew",&OldRelation::skew)
			.staticmethod("skew")
			.def("translate",&OldRelation::translate)
			.staticmethod("translate")
			.def("__enter__",&OldRelation::get_vars)
			.def("__exit__",&OldRelation::clear_vars);
	}

	void export_omega_formulas()
	{
		class_<Formula,boost::noncopyable>("OmegaFormula",no_init)
			.def("__str__",&Formula::str);

		class_<Set,bases<Formula> >("OmegaSet",no_init);
		boost::python::register_ptr_to_python<sptr<Set> >();

		class_<Relation,bases<Formula> >("OmegaRelation",no_init);
		boost::python::register_ptr_to_python<sptr<Relation> >();
	}

	BOOST_PYTHON_MODULE(_omega)
	{
		register_exception_translator<OmegaException>(&translate_exception);

		export_omega_enums();
		export_omega_formula_building();
		export_omega_old_formulas();
		export_omega_formulas();
	}

}}//end namespace omega::bindings
