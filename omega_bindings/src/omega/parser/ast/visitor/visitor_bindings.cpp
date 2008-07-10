#include <boost/python.hpp>
#include <omega.h>
#include <string>

#include "util.hpp"

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "IPresVisitable.hpp"
#include "PresDepthFirstVisitor.hpp"
#include "PresReprVisitor.hpp"
#include "PresTransVisitor.hpp"
#include "PresTransSetVisitor.hpp"
#include "PresTransRelationVisitor.hpp"

using namespace boost::python;

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	void export_pres_visitors()
	{
		class_<IPresVisitor,boost::noncopyable>("IPresVisitor",no_init);

		class_<PresDepthFirstVisitor,bases<IPresVisitor> >("PresDepthFirstVisitor",no_init)
			.def("visit",&PresDepthFirstVisitor::visit);

		class_<PresReprVisitor,bases<PresDepthFirstVisitor> >("PresReprVisitor",init<>())
			.def("__str__",(std::string (PresReprVisitor::*)(void) const)&PresReprVisitor::str)
			.def("__repr__",(std::string (PresReprVisitor::*)(void) const)&PresReprVisitor::str);

		class_<PresTransVisitor,bases<PresDepthFirstVisitor>,boost::noncopyable>("PresTransVisitor",no_init)
			.def("__str__",&PresTransVisitor::str)
			.def("union",&PresTransVisitor::union_);

		class_<PresTransSetVisitor,bases<PresTransVisitor> >("PresTransSetVisitor",init<>())
			.def("set",(sptr<Set> (PresTransSetVisitor::*)(void) const)&PresTransSetVisitor::set);

		class_<PresTransRelationVisitor,bases<PresTransVisitor> >("PresTransRelationVisitor",init<>())
			.def("relation",(sptr<Relation> (PresTransRelationVisitor::*)(void) const)&PresTransRelationVisitor::relation);
	}

	BOOST_PYTHON_MODULE(_visitor)
	{
		register_exception_translator<OmegaException>(&translate_exception);
		export_pres_visitors();
	}

}}}}}//end namespace omega::bindings::parser::ast::visitor
