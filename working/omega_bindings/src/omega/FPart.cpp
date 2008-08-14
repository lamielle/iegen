#include <string>
#include "FPart.hpp"
#include "OmegaException.hpp"

namespace omega { namespace bindings {

	FPart::FPart() {}
	FPart::~FPart() {}

	std::string FPart::str() const
	{
		throw OmegaException("Unsupported Operation: No string representation exists for an FPart.");
	}

}}//end namespace omega::bindings
