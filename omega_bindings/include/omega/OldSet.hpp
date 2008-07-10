#ifndef _OMEGA_BINDINGS_OLD_SET_H_
#define _OMEGA_BINDINGS_OLD_SET_H_

#include <boost/python.hpp>
#include <omega.h>
#include <string>
#include "TupleCollection.hpp"

namespace python=boost::python;
namespace omega { namespace bindings {

	class OldRelation;

	//Wraps the omega::Relation class as a set of tuples
	class OldSet : public TupleCollection
	{
		public:
			OldSet(int arity);
			OldSet(OldSet const& s);
			OldSet(OldSet const& s,omega::Relation const& r);
			OldSet(std::string name);
			OldSet(python::tuple const& names);
			OldSet& operator=(OldSet const& s);
			int arity() const;
			void name(int i,std::string const& name);
			void name(python::tuple const& names);
			std::string name(int i);
			python::tuple names();
			void get_vars();
			void clear_vars(python::object type,python::object value,python::object traceback);
			void apply(OldRelation const& r);

			//Python iterator support
			PyObject* iter();
			std::string code();
	};

}}//end namespace omega::bindings

#endif
