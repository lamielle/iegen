#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_ID_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_ID_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVar.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger VarID AST node
	class PresVarID : public PresVar
	{
		public:
			PresVarID(std::string const& id);
			static sptr<PresVarID> new_(std::string const& id);
			PresVarID(PresVarID const& o);
			PresVarID& operator=(PresVarID const& o);

			virtual std::string str() const;
			virtual std::string name() const;
			std::string id() const;

			void apply(IPresVisitor& v);

		private:
			void id(std::string const& id);
			std::string m_id;
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
