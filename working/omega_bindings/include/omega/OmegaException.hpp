#ifndef _OMEGA_BINDINGS_OMEGAEXCEPTION_H_
#define _OMEGA_BINDINGS_OMEGAEXCEPTION_H_

#include <string>

namespace omega { namespace bindings {

	//Exception class used for all exceptions thrown from the omega bindings
	class OmegaException : std::exception
	{
		public:
			OmegaException(std::string const& msg);
			~OmegaException() throw();
			const std::string& get_msg() const;

		private:
			std::string m_msg;
	};

}}//end namespace omega::bindings

#endif
