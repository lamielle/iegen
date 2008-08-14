#include <string>
#include "OmegaException.hpp"

namespace omega { namespace bindings {

	OmegaException::OmegaException(std::string const& msg):m_msg(msg){}

	OmegaException::~OmegaException() throw() {};

	std::string const& OmegaException::get_msg() const
	{
		return this->m_msg;
	}

}}//end namespace omega::bindings
