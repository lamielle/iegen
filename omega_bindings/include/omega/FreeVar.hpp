#ifndef _OMEGA_BINDINGS_FREEVAR_H_
#define _OMEGA_BINDINGS_FREEVAR_H_

#include <boost/python.hpp>
#include <boost/shared_ptr.hpp>
#include <omega.h>
#include <string>

namespace python=boost::python;
namespace omega { namespace bindings {

	//Class wrapping an omega::Free_Var_Decl used to represent global variables
	class FreeVar
	{
		public:
			friend class TupleCollection;
			FreeVar(std::string const& name);
			FreeVar(std::string const& name,int arity);
			FreeVar(FreeVar const& o);
			FreeVar();
			~FreeVar();
			FreeVar& operator=(FreeVar const& o);
			std::string str() const;

		protected:
			Free_Var_Decl* fvar_ptr();

		private:
			boost::shared_ptr<Free_Var_Decl> m_fvar;
	};

}}//end namespace omega::bindings

#endif
