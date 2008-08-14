#ifndef _OMEGA_BINDINGS_FPART_H_
#define _OMEGA_BINDINGS_FPART_H_

#include <string>

namespace omega { namespace bindings {

	//Represents a part of a formula
	//This is the base class for all formula related classes
	class FPart
	{
		public:
			virtual std::string str() const;
			virtual ~FPart();

		protected:
			FPart();
	};

}}//end namespace omega::bindings

#endif
