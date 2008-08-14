#ifndef _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_UNNAMED_H_
#define _OMEGA_BINDINGS_PARSER_AST_PRES_VAR_UNNAMED_H_

#include "PresUtil.hpp"
#include "IPresVisitor.hpp"
#include "PresVar.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast {

	//Presburger VarUnnamed AST node
	class PresVarUnnamed : public PresVar
	{
		public:
			PresVarUnnamed();
			static sptr<PresVarUnnamed> new_();
			PresVarUnnamed(PresVarUnnamed const& o);
			PresVarUnnamed& operator=(PresVarUnnamed const& o);

			virtual std::string str() const;
			virtual std::string name() const;

			void apply(IPresVisitor& v);
	};

}}}}//end namespace omega::bindings::parser::ast

#endif
