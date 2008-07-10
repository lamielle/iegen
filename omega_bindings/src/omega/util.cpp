#include <boost/python.hpp>
#include <omega.h>
#include "util.hpp"
#include "Var.hpp"
#include "FVar.hpp"
#include "FExpr.hpp"
#include "FStmt.hpp"
#include "FConj.hpp"
#include "OmegaException.hpp"

namespace omega { namespace bindings {

	//Translates the given C++ exception to a Python RuntimeError exception
	void translate_exception(OmegaException const& e)
	{
		// Use the Python 'C' API to set up an exception object
		PyErr_SetString(PyExc_RuntimeError, e.get_msg().c_str());
	}

	FConj combine(FConj::FConj_Type type,FConj const& conj,FStmt const& stmt)
	{
		if(type==conj.type())
		{
			FConj conj_new(conj);
			conj_new.add_stmt(stmt);
			return conj_new;
		}
		else
			return FConj(type,conj,stmt);
	}

	FConj combine(FConj::FConj_Type type,FConj const& conj1,FConj const& conj2)
	{
		if(FConj::Not==conj1.type()||FConj::Not==conj2.type())
			return FConj(type,conj1,conj2);
		else
		{
			if(type==conj1.type())
			{
				if(type==conj2.type())
				{
					FConj new_conj(conj1);
					std::vector<FStmt> stmts=conj2.stmts();
					for(std::vector<FStmt>::const_iterator i=stmts.begin(); i!=stmts.end(); i++)
						new_conj.add_stmt(*i);
					std::vector<FConj> conjs=conj2.conjs();
					for(std::vector<FConj>::const_iterator i=conjs.begin(); i!=conjs.end(); i++)
						new_conj.add_conj(*i);
					return new_conj;
				}
				else
				{
					FConj new_conj(conj1);
					new_conj.add_conj(conj2);
					return new_conj;
				}
			}
			else
			{
				FConj new_conj(type);
				new_conj.add_conj(conj1);
				new_conj.add_conj(conj2);
				return new_conj;
			}
		}
	}

	//--------------------------------------------------
	// Formula Building Operators
	//--------------------------------------------------

	//Addition and Subtraction
	FExpr operator+(Var const& v,long c){return FExpr(v,c);}
	FExpr operator+(long c,Var const& v){return v+c;}
	FExpr operator-(Var const& v,long c){return v+-1*c;}
	FExpr operator-(long c,Var const& v){return -1*v+c;}

	FExpr operator+(Var const& v1,Var const& v2){return FExpr(v1,v2);}
	FExpr operator-(Var const& v1,Var const& v2){return v1+-1*v2;}

	FExpr operator+(FVar const& v,long c){return FExpr(v,c);}
	FExpr operator+(long c,FVar const& v){return v+c;}
	FExpr operator-(FVar const& v,long c){return v+-1*c;}
	FExpr operator-(long c,FVar const& v){return -1*v+c;}

	FExpr operator+(FVar const& v1,Var const& v2){return FExpr(v1,v2);}
	FExpr operator+(Var const& v1,FVar const& v2){return v2+v1;}
	FExpr operator-(FVar const& v1,Var const& v2){return v1+-1*v2;}
	FExpr operator-(Var const& v1,FVar const& v2){return -1*v2+v1;}

	FExpr operator+(FVar const& v1,FVar const& v2){return FExpr(v1,v2);}
	FExpr operator-(FVar const& v1,FVar const& v2){return v1+-1*v2;}
	
	FExpr operator+(FExpr const& e,long c){return FExpr(e,c,FExpr::Add);}
	FExpr operator+(long c,FExpr const& e){return e+c;}
	FExpr operator-(FExpr const& e,long c){return e+-1*c;}
	FExpr operator-(long c,FExpr const& e){return -1*e+c;}

	FExpr operator+(FExpr const& e,Var const& v){return FExpr(e,FVar(v));}
	FExpr operator+(Var const& v,FExpr const& e){return e+v;}
	FExpr operator-(FExpr const& e,Var const& v){return e+-1*v;}
	FExpr operator-(Var const& v,FExpr const& e){return -1*e+v;}

	FExpr operator+(FExpr const& e,FVar const& v){return FExpr(e,v);}
	FExpr operator+(FVar const& v,FExpr const& e){return e+v;}
	FExpr operator-(FExpr const& e,FVar const& v){return e+-1*v;}
	FExpr operator-(FVar const& v,FExpr const& e){return -1*e+v;}

	FExpr operator+(FExpr const& e1,FExpr const& e2){return FExpr(e1,e2);}
	FExpr operator-(FExpr const& e1,FExpr const& e2){return e1+-1*e2;}

	//Multiplication
	FVar operator*(Var const& v,long c) {return FVar(c,v);}
	FVar operator*(long c,Var const& v) {return v*c;}

	FVar operator*(FVar const& v,long c){return FVar(c,v);}
	FVar operator*(long c,FVar const& v){return v*c;}

	FExpr operator*(FExpr const& e,long c){return FExpr(e,c,FExpr::Multiply);}
	FExpr operator*(long c,FExpr const& e){return e*c;}

	//Equality (==)
	FStmt operator==(Var const& v,long c){return FStmt(v+-1*c,FStmt::EQ);}
	FStmt operator==(long c,Var const& v){return v==c;}

	FStmt operator==(FVar const& v,long c){return FStmt(v+-1*c,FStmt::EQ);}
	FStmt operator==(long c,FVar const& v){return v==c;}

	FStmt operator==(FExpr const& e,long c){return FStmt(e+-1*c,FStmt::EQ);}
	FStmt operator==(long c,FExpr const& e){return e==c;}

	FStmt operator==(Var const& v1,Var const& v2){return FStmt(v1+-1*v2,FStmt::EQ);}

	FStmt operator==(FVar const& v1,Var const& v2){return FStmt(v1+-1*v2,FStmt::EQ);}
	FStmt operator==(Var const& v1,FVar const& v2){return v2==v1;}

	FStmt operator==(FExpr const& e,Var const& v){return FStmt(e+-1*v,FStmt::EQ);}
	FStmt operator==(Var const& v,FExpr const& e){return e==v;}

	FStmt operator==(FVar const& v1,FVar const& v2){return FStmt(v1+-1*v2,FStmt::EQ);}

	FStmt operator==(FExpr const& e,FVar const& v){return FStmt(e+-1*v,FStmt::EQ);}
	FStmt operator==(FVar const& v,FExpr const& e){return e==v;}

	FStmt operator==(FExpr const& e1,FExpr const& e2){return FStmt(e1+-1*e2,FStmt::EQ);}

	//Equality (!=)
	FConj operator!=(Var const& v,long c){return FConj(FConj::Or,v>=c+1,v<=c-1);}
	FConj operator!=(long c,Var const& v){return v!=c;}

	FConj operator!=(FVar const& v,long c){return FConj(FConj::Or,v>=c+1,v<=c-1);}
	FConj operator!=(long c,FVar const& v){return v!=c;}

	FConj operator!=(FExpr const& e,long c){return FConj(FConj::Or,e>=c+1,e<=c-1);}
	FConj operator!=(long c,FExpr const& e){return e!=c;}

	FConj operator!=(Var const& v1,Var const& v2){return FConj(FConj::Or,v1>=v2+1,v1<=v2-1);}

	FConj operator!=(FVar const& v1,Var const& v2){return FConj(FConj::Or,v1>=v2+1,v1<=v2-1);}
	FConj operator!=(Var const& v1,FVar const& v2){return v2!=v1;}

	FConj operator!=(FExpr const& e,Var const& v){return FConj(FConj::Or,e>=v+1,e<=v-1);}
	FConj operator!=(Var const& v,FExpr const& e){return e!=v;}

	FConj operator!=(FVar const& v1,FVar const& v2){return FConj(FConj::Or,v1>=v2+1,v1<=v2-1);}

	FConj operator!=(FExpr const& e,FVar const& v){return FConj(FConj::Or,e>=v+1,e<=v-1);}
	FConj operator!=(FVar const& v,FExpr const& e){return e!=v;}

	FConj operator!=(FExpr const& e1,FExpr const& e2){return FConj(FConj::Or,e1>=e2+1,e1<=e2-1);}

	//Inequality (>= and <=)
	FStmt operator>=(Var const& v,long c){return FStmt(v+-1*c,FStmt::GEQ);}
	FStmt operator<=(long c,Var const& v){return v>=c;}
	FStmt operator>=(long c,Var const& v){return FStmt(-1*v+c,FStmt::GEQ);}
	FStmt operator<=(Var const& v,long c){return c>=v;}

	FStmt operator>=(FVar const& v,long c){return FStmt(v+-1*c,FStmt::GEQ);}
	FStmt operator<=(long c,FVar const& v){return v>=c;}
	FStmt operator>=(long c,FVar const& v){return FStmt(-1*v+c,FStmt::GEQ);}
	FStmt operator<=(FVar const& v,long c){return c>=v;}

	FStmt operator>=(FExpr const& e,long c){return FStmt(e+-1*c,FStmt::GEQ);}
	FStmt operator<=(long c,FExpr const& e){return e>=c;}
	FStmt operator>=(long c,FExpr const& e){return FStmt(-1*e+c,FStmt::GEQ);}
	FStmt operator<=(FExpr const& e,long c){return c>=e;}

	FStmt operator>=(Var const& v1,Var const& v2){return FStmt(v1+-1*v2,FStmt::GEQ);}
	FStmt operator<=(Var const& v1,Var const& v2){return v2>=v1;}

	FStmt operator>=(FVar const& v1,Var const& v2){return FStmt(v1+-1*v2,FStmt::GEQ);}
	FStmt operator<=(Var const& v1,FVar const& v2){return v2>=v1;}
	FStmt operator>=(Var const& v1,FVar const& v2){return FStmt(-1*v2+v1,FStmt::GEQ);}
	FStmt operator<=(FVar const& v1,Var const& v2){return v2>=v1;}

	FStmt operator>=(FExpr const& e,Var const& v){return FStmt(e+-1*v,FStmt::GEQ);}
	FStmt operator<=(Var const& v,FExpr const& e){return e>=v;}
	FStmt operator>=(Var const& v,FExpr const& e){return FStmt(-1*e+v,FStmt::GEQ);}
	FStmt operator<=(FExpr const& e,Var const& v){return v>=e;}

	FStmt operator>=(FVar const& v1,FVar const& v2){return FStmt(v1+-1*v2,FStmt::GEQ);}
	FStmt operator<=(FVar const& v1,FVar const& v2){return v2>=v1;}

	FStmt operator>=(FExpr const& e,FVar const& v){return FStmt(e+-1*v,FStmt::GEQ);}
	FStmt operator<=(FVar const& v,FExpr const& e){return e>=v;}
	FStmt operator>=(FVar const& v,FExpr const& e){return FStmt(-1*e+v,FStmt::GEQ);}
	FStmt operator<=(FExpr const& e,FVar const& v){return v>=e;}

	FStmt operator>=(FExpr const& e1,FExpr const& e2){return FStmt(e1+-1*e2,FStmt::GEQ);}
	FStmt operator<=(FExpr const& e1,FExpr const& e2){return e2>=e1;}

	//Inequality (> and <)
	FStmt operator>(Var const& v,long c){return v>=c+1;}
	FStmt operator<(long c,Var const& v){return v>c;}
	FStmt operator>(long c,Var const& v){return c>=v+1;}
	FStmt operator<(Var const& v,long c){return c>v;}

	FStmt operator>(FVar const& v,long c){return v>=c+1;}
	FStmt operator<(long c,FVar const& v){return v>c;}
	FStmt operator>(long c,FVar const& v){return c>=v+1;}
	FStmt operator<(FVar const& v,long c){return c>v;}

	FStmt operator>(FExpr const& e,long c){return e>=c+1;}
	FStmt operator<(long c,FExpr const& e){return e>c;}
	FStmt operator>(long c,FExpr const& e){return c>=e+1;}
	FStmt operator<(FExpr const& e,long c){return c>e;}

	FStmt operator>(Var const& v1,Var const& v2){return v1>=v2+1;}
	FStmt operator<(Var const& v1,Var const& v2){return v2>v1;}

	FStmt operator>(FVar const& v1,Var const& v2){return v1>=v2+1;}
	FStmt operator<(Var const& v1,FVar const& v2){return v2>v1;}
	FStmt operator>(Var const& v1,FVar const& v2){return v1>=v2+1;}
	FStmt operator<(FVar const& v1,Var const& v2){return v2>v1;}

	FStmt operator>(FExpr const& e,Var const& v){return e>=v+1;}
	FStmt operator<(Var const& v,FExpr const& e){return e>v;}
	FStmt operator>(Var const& v,FExpr const& e){return v>=e+1;}
	FStmt operator<(FExpr const& e,Var const& v){return v>e;}

	FStmt operator>(FVar const& v1,FVar const& v2){return v1>=v2+1;}
	FStmt operator<(FVar const& v1,FVar const& v2){return v2>v1;}

	FStmt operator>(FExpr const& e,FVar const& v){return e>=v+1;}
	FStmt operator<(FVar const& v,FExpr const& e){return e>v;}
	FStmt operator>(FVar const& v,FExpr const& e){return v>=e+1;}
	FStmt operator<(FExpr const& e,FVar const& v){return v>e;}

	FStmt operator>(FExpr const& e1,FExpr const& e2){return e1>=e2+1;}
	FStmt operator<(FExpr const& e1,FExpr const& e2){return e2>e1;}

	//Conjunction Building (& and |)
	FConj operator&(FStmt const& stmt1,FStmt const& stmt2){return FConj(FConj::And,stmt1,stmt2);}
	FConj operator&(FConj const& conj,FStmt const& stmt){return combine(FConj::And,conj,stmt);}
	FConj operator&(FStmt const& stmt,FConj const& conj){return conj&stmt;}
	FConj operator&(FConj const& conj1,FConj const& conj2){return combine(FConj::And,conj1,conj2);}

	FConj operator|(FStmt const& stmt1,FStmt const& stmt2){return FConj(FConj::Or,stmt1,stmt2);}
	FConj operator|(FConj const& conj,FStmt const& stmt){return combine(FConj::Or,conj,stmt);}
	FConj operator|(FStmt const& stmt,FConj const& conj){return conj|stmt;}
	FConj operator|(FConj const& conj1,FConj const& conj2){return combine(FConj::Or,conj1,conj2);}

	//Negation
	FVar operator-(Var const& v){return -1*v;}
	FVar operator-(FVar const& v){return -1*v;}
	FExpr operator-(FExpr const& e){return -1*e;}

	//--------------------------------------------------

}}//end namespace omega::bindings
