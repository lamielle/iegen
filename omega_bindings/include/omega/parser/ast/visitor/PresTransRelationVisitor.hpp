#ifndef _OMEGA_BINDINGS_PARSER_AST_VISITOR_PRES_TRANS_RELATION_VISITOR_H_
#define _OMEGA_BINDINGS_PARSER_AST_VISITOR_PRES_TRANS_RELATION_VISITOR_H_

#include "PresUtil.hpp"
#include "PresTransVisitor.hpp"
#include "Relation.hpp"

namespace omega { namespace bindings { namespace parser { namespace ast { namespace visitor {

	//Presburger AST visitor that prints an ASTs python representation
	class PresTransRelationVisitor : public PresTransVisitor
	{
		public:
			PresTransRelationVisitor();
			PresTransRelationVisitor(PresTransRelationVisitor const& o);
			PresTransRelationVisitor& operator=(PresTransRelationVisitor const& o);

			void compose(PresTransRelationVisitor const& o);
			void inverse();

			int arity_in() const;
			int arity_out() const;

			//Relation nodes
			virtual void inPresRelation(PresRelation const& v);
			virtual void outPresRelation(PresRelation const& v);

			//Variable nodes
			virtual void inPresVarID(PresVarID const& v);
			virtual void outPresVarID(PresVarID const& v);

			sptr<Relation> relation() const;
			virtual sptr<Formula> formula() const;

		private:
			void relation(sptr<Relation> const& set);

			sptr<Relation> m_relation;
	};

}}}}}//end namespace omega::bindings::parser::ast::visitor

#endif
