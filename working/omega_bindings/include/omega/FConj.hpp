#ifndef _OMEGA_BINDINGS_FCONJ_H_
#define _OMEGA_BINDINGS_FCONJ_H_

#include <string>
#include <vector>
#include "FPart.hpp"
#include "FStmt.hpp"

namespace omega { namespace bindings {

	//Represents a formula conjunction:
	//Either FPart AND FPart AND ... AND FPart
	//or FPart OR FPart OR ... OR FPart
	//or NOT FPart
	class FConj : public FPart
	{
		public:
			enum FConj_Type {And,Or,Not};
			friend void export_omega_formula_building();
			friend FConj combine(FConj_Type type,FConj const& conj,FStmt const& stmt);
			friend FConj combine(FConj_Type type,FConj const& conj1,FConj const& conj2);
			FConj(FConj_Type type);
			FConj(FConj_Type type,FStmt const& stmt);
			FConj(FConj_Type type,FStmt const& stmt1,FStmt const& stmt2);
			FConj(FConj_Type type,FConj const& conj,FStmt const& stmt);
			FConj(FConj_Type type,FConj const& conj1,FConj const& conj2);
			FConj(FConj const& o);
			FConj& operator=(FConj const& o);
			virtual std::string str() const;
			FConj_Type type() const;
			std::vector<FStmt> stmts() const;
			std::vector<FConj> conjs() const;

		protected:
			FConj();

		private:
			void type(FConj_Type type);
			void stmts(std::vector<FStmt> stmts);
			void conjs(std::vector<FConj> conjs);

			std::vector<FPart const*> const get_all_parts() const;
			void add_stmt(FStmt const& stmt);
			void add_conj(FConj const& conj);

		private:
			FConj_Type m_type;
			std::vector<FStmt> m_stmts;
			std::vector<FConj> m_conjs;
	};

}}//end namespace omega::bindings

#endif
