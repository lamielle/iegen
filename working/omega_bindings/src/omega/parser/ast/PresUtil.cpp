#include "PresUtil.hpp"
#include "PresNode.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	std::string get_string_from_vector(node_vect const& items,std::string const& sep)
	{
		str_vect strings;
		foreach(sptr<PresNode> item,items)
			strings.push_back(item->str());
		return get_string_from_strings(strings,sep);

	}

	std::string get_string_from_strings(str_vect const& strings,std::string const& sep)
	{
		std::stringstream s;
		foreach(std::string str,strings)
			s<<str+sep;
		if(strings.size()>0)
			return s.str().substr(0,s.str().length()-sep.length());
		else
			return s.str();
	}

}}}}//end namespace omega::bindings::parser::ast
