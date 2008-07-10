#ifndef _OMEGA_BINDINGS_UTIL_H_
#define _OMEGA_BINDINGS_UTIL_H_

//STL includes
#include <string>
#include <vector>
#include <stack>
#include <map>

//Define shorter names for shared and weak pointers
#define sptr boost::shared_ptr
#define wptr boost::weak_ptr

#include <boost/tuple/tuple.hpp>
#include <boost/python.hpp>
#include <boost/python/list.hpp>
#include <boost/python/tuple.hpp>
#include <boost/python/extract.hpp>
#include <boost/python/to_python_converter.hpp>
#include <boost/foreach.hpp>
#include <omega.h>
#include "OmegaException.hpp"
#include "Var.hpp"
#include "FVar.hpp"
#include "FExpr.hpp"
#include "FStmt.hpp"
#include "FConj.hpp"

#undef foreach
#define foreach BOOST_FOREACH

namespace omega { namespace bindings {

	typedef std::stack<omega::Formula*> form_stack;

	void translate_exception(OmegaException const& e);

	template<typename K,typename V>
	bool map_contains_key(std::map<K,V> const& m,K const& k)
	{
		return m.find(k)!=m.end();
	}

	//--------------------------------------------------
	// Formula Building Operators
	//--------------------------------------------------

	//Addition and Subtraction
	FExpr operator+(Var const& v,long c);
	FExpr operator+(long c,Var const& v);
	FExpr operator-(Var const& v,long c);
	FExpr operator-(long c,Var const& v);

	FExpr operator+(Var const& v1,Var const& v2);
	FExpr operator-(Var const& v1,Var const& v2);

	FExpr operator+(FVar const& v,long c);
	FExpr operator+(long c,FVar const& v);
	FExpr operator-(FVar const& v,long c);
	FExpr operator-(long c,FVar const& v);

	FExpr operator+(FVar const& v1,Var const& v2);
	FExpr operator+(Var const& v1,FVar const& v2);
	FExpr operator-(FVar const& v1,Var const& v2);
	FExpr operator-(Var const& v1,FVar const& v2);

	FExpr operator+(FVar const& v1,FVar const& v2);
	FExpr operator-(FVar const& v1,FVar const& v2);
	
	FExpr operator+(FExpr const& e,long c);
	FExpr operator+(long c,FExpr const& e);
	FExpr operator-(FExpr const& e,long c);
	FExpr operator-(long c,FExpr const& e);

	FExpr operator+(FExpr const& e,Var const& v);
	FExpr operator+(Var const& v,FExpr const& e);
	FExpr operator-(FExpr const& e,Var const& v);
	FExpr operator-(Var const& v,FExpr const& e);

	FExpr operator+(FExpr const& e,FVar const& v);
	FExpr operator+(FVar const& v,FExpr const& e);
	FExpr operator-(FExpr const& e,FVar const& v);
	FExpr operator-(FVar const& v,FExpr const& e);

	FExpr operator+(FExpr const& e1,FExpr const& e2);
	FExpr operator-(FExpr const& e1,FExpr const& e2);

	//Multiplication
	FVar operator*(Var const& v,long c) ;
	FVar operator*(long c,Var const& v) ;

	FVar operator*(FVar const& v,long c);
	FVar operator*(long c,FVar const& v);

	FExpr operator*(FExpr const& e,long c);
	FExpr operator*(long c,FExpr const& e);

	//Equality (==)
	FStmt operator==(Var const& v,long c);
	FStmt operator==(long c,Var const& v);

	FStmt operator==(FVar const& v,long c);
	FStmt operator==(long c,FVar const& v);

	FStmt operator==(FExpr const& e,long c);
	FStmt operator==(long c,FExpr const& e);

	FStmt operator==(Var const& v1,Var const& v2);

	FStmt operator==(FVar const& v1,Var const& v2);
	FStmt operator==(Var const& v1,FVar const& v2);

	FStmt operator==(FExpr const& e,Var const& v);
	FStmt operator==(Var const& v,FExpr const& e);

	FStmt operator==(FVar const& v1,FVar const& v2);

	FStmt operator==(FExpr const& e,FVar const& v);
	FStmt operator==(FVar const& v,FExpr const& e);

	FStmt operator==(FExpr const& e1,FExpr const& e2);

	//Equality (!=)
	FConj operator!=(Var const& v,long c);
	FConj operator!=(long c,Var const& v);

	FConj operator!=(FVar const& v,long c);
	FConj operator!=(long c,FVar const& v);

	FConj operator!=(FExpr const& e,long c);
	FConj operator!=(long c,FExpr const& e);

	FConj operator!=(Var const& v1,Var const& v2);

	FConj operator!=(FVar const& v1,Var const& v2);
	FConj operator!=(Var const& v1,FVar const& v2);

	FConj operator!=(FExpr const& e,Var const& v);
	FConj operator!=(Var const& v,FExpr const& e);

	FConj operator!=(FVar const& v1,FVar const& v2);

	FConj operator!=(FExpr const& e,FVar const& v);
	FConj operator!=(FVar const& v,FExpr const& e);

	FConj operator!=(FExpr const& e1,FExpr const& e2);

	//Inequality (>= and <=)
	FStmt operator>=(Var const& v,long c);
	FStmt operator<=(long c,Var const& v);
	FStmt operator>=(long c,Var const& v);
	FStmt operator<=(Var const& v,long c);

	FStmt operator>=(FVar const& v,long c);
	FStmt operator<=(long c,FVar const& v);
	FStmt operator>=(long c,FVar const& v);
	FStmt operator<=(FVar const& v,long c);

	FStmt operator>=(FExpr const& e,long c);
	FStmt operator<=(long c,FExpr const& e);
	FStmt operator>=(long c,FExpr const& e);
	FStmt operator<=(FExpr const& e,long c);

	FStmt operator>=(Var const& v1,Var const& v2);
	FStmt operator<=(Var const& v1,Var const& v2);

	FStmt operator>=(FVar const& v1,Var const& v2);
	FStmt operator<=(Var const& v1,FVar const& v2);
	FStmt operator>=(Var const& v1,FVar const& v2);
	FStmt operator<=(FVar const& v1,Var const& v2);

	FStmt operator>=(FExpr const& e,Var const& v);
	FStmt operator<=(Var const& v,FExpr const& e);
	FStmt operator>=(Var const& v,FExpr const& e);
	FStmt operator<=(FExpr const& e,Var const& v);

	FStmt operator>=(FVar const& v1,FVar const& v2);
	FStmt operator<=(FVar const& v1,FVar const& v2);

	FStmt operator>=(FExpr const& e,FVar const& v);
	FStmt operator<=(FVar const& v,FExpr const& e);
	FStmt operator>=(FVar const& v,FExpr const& e);
	FStmt operator<=(FExpr const& e,FVar const& v);

	FStmt operator>=(FExpr const& e1,FExpr const& e2);
	FStmt operator<=(FExpr const& e1,FExpr const& e2);

	//Inequality (> and <)
	FStmt operator>(Var const& v,long c);
	FStmt operator<(long c,Var const& v);
	FStmt operator>(long c,Var const& v);
	FStmt operator<(Var const& v,long c);

	FStmt operator>(FVar const& v,long c);
	FStmt operator<(long c,FVar const& v);
	FStmt operator>(long c,FVar const& v);
	FStmt operator<(FVar const& v,long c);

	FStmt operator>(FExpr const& e,long c);
	FStmt operator<(long c,FExpr const& e);
	FStmt operator>(long c,FExpr const& e);
	FStmt operator<(FExpr const& e,long c);

	FStmt operator>(Var const& v1,Var const& v2);
	FStmt operator<(Var const& v1,Var const& v2);

	FStmt operator>(FVar const& v1,Var const& v2);
	FStmt operator<(Var const& v1,FVar const& v2);
	FStmt operator>(Var const& v1,FVar const& v2);
	FStmt operator<(FVar const& v1,Var const& v2);

	FStmt operator>(FExpr const& e,Var const& v);
	FStmt operator<(Var const& v,FExpr const& e);
	FStmt operator>(Var const& v,FExpr const& e);
	FStmt operator<(FExpr const& e,Var const& v);

	FStmt operator>(FVar const& v1,FVar const& v2);
	FStmt operator<(FVar const& v1,FVar const& v2);

	FStmt operator>(FExpr const& e,FVar const& v);
	FStmt operator<(FVar const& v,FExpr const& e);
	FStmt operator>(FVar const& v,FExpr const& e);
	FStmt operator<(FExpr const& e,FVar const& v);

	FStmt operator>(FExpr const& e1,FExpr const& e2);
	FStmt operator<(FExpr const& e1,FExpr const& e2);

	//Conjunction Building (& and |)
	FConj operator&(FStmt const& stmt1,FStmt const& stmt2);
	FConj operator&(FConj const& conj,FStmt const& stmt);
	FConj operator&(FStmt const& stmt,FConj const& conj);
	FConj operator&(FConj const& conj1,FConj const& conj2);

	FConj operator|(FStmt const& stmt1,FStmt const& stmt2);
	FConj operator|(FConj const& conj,FStmt const& stmt);
	FConj operator|(FStmt const& stmt,FConj const& conj);
	FConj operator|(FConj const& conj1,FConj const& conj2);

	//Negation
	FVar operator-(Var const& v);
	FVar operator-(FVar const& v);
	FExpr operator-(FExpr const& e);

	//--------------------------------------------------
	// Container conversion routines
	// Taken from CCTBX project (http://cctbx.sourceforge.net)
	// Original file was called container_conversions.h
	//--------------------------------------------------
	template <typename ContainerType>
	struct to_tuple
	{
		static PyObject* convert(ContainerType const& a)
		{
			boost::python::list result;
			typedef typename ContainerType::const_iterator const_iter;
			for(const_iter p=a.begin();p!=a.end();p++) {
				result.append(boost::python::object(*p));
			}
		return boost::python::incref(boost::python::tuple(result).ptr());
		}

		static const PyTypeObject* get_pytype() { return &PyTuple_Type; }
	};

	struct default_policy
	{
		static bool check_convertibility_per_element() { return false; }

		template <typename ContainerType>
		static bool check_size(boost::type<ContainerType>, std::size_t /*sz*/)
		{
			return true;
		}

		template <typename ContainerType>
		static void assert_size(boost::type<ContainerType>, std::size_t /*sz*/) {}

		template <typename ContainerType>
		static void reserve(ContainerType& a, std::size_t sz) {}
	};

	struct fixed_size_policy
	{
		static bool check_convertibility_per_element() { return true; }

		template <typename ContainerType>
		static bool check_size(boost::type<ContainerType>, std::size_t sz)
		{
			return ContainerType::size() == sz;
		}

		template <typename ContainerType>
		static void assert_size(boost::type<ContainerType>, std::size_t sz)
		{
			if (!check_size(boost::type<ContainerType>(), sz)) {
				PyErr_SetString(PyExc_RuntimeError,
				                "Insufficient elements for fixed-size array.");
				boost::python::throw_error_already_set();
			}
		}

		template <typename ContainerType>
		static void reserve(ContainerType& /*a*/, std::size_t sz)
		{
			if (sz > ContainerType::size()) {
				PyErr_SetString(PyExc_RuntimeError,
				                "Too many elements for fixed-size array.");
				boost::python::throw_error_already_set();
			}
		}

		template <typename ContainerType, typename ValueType>
		static void set_value(ContainerType& a, std::size_t i, ValueType const& v)
		{
			reserve(a, i+1);
			a[i] = v;
		}
	};

	struct variable_capacity_policy : default_policy
	{
		template <typename ContainerType>
		static void reserve(ContainerType& a, std::size_t sz)
		{
			a.reserve(sz);
		}

		template <typename ContainerType, typename ValueType>
		static void set_value(
			ContainerType& a,
			std::size_t
			#if !defined(NDEBUG)
			i
			#endif
			,
			ValueType const& v)
		{
			assert(a.size() == i);
			a.push_back(v);
		}
	};

	struct fixed_capacity_policy : variable_capacity_policy
	{
		template <typename ContainerType>
		static bool check_size(boost::type<ContainerType>, std::size_t sz)
		{
			return ContainerType::max_size() >= sz;
		}
	};

	struct linked_list_policy : default_policy
	{
		template <typename ContainerType, typename ValueType>
		static void
		set_value(ContainerType& a, std::size_t /*i*/, ValueType const& v)
		{
			a.push_back(v);
		}
	};

	struct set_policy : default_policy
	{
		template <typename ContainerType, typename ValueType>
		static void
		set_value(ContainerType& a, std::size_t /*i*/, ValueType const& v)
		{
			a.insert(v);
		}
	};

	template <typename ContainerType, typename ConversionPolicy>
	struct from_python_sequence
	{
		typedef typename ContainerType::value_type container_element_type;

		from_python_sequence()
		{
			boost::python::converter::registry::push_back(
				&convertible,
				&construct,
				boost::python::type_id<ContainerType>());
		}

		static void* convertible(PyObject* obj_ptr)
		{
			if (!(   PyList_Check(obj_ptr)
			    || PyTuple_Check(obj_ptr)
			    || PyIter_Check(obj_ptr)
			    || PyRange_Check(obj_ptr)
			    || (   !PyString_Check(obj_ptr)
			    && !PyUnicode_Check(obj_ptr)
			    && (   obj_ptr->ob_type == 0
			    || obj_ptr->ob_type->ob_type == 0
			    || obj_ptr->ob_type->ob_type->tp_name == 0
			    || std::strcmp(
			    obj_ptr->ob_type->ob_type->tp_name,
			    "Boost.Python.class") != 0)
			    && PyObject_HasAttrString(obj_ptr, "__len__")
			    && PyObject_HasAttrString(obj_ptr, "__getitem__")))) return 0;
			boost::python::handle<> obj_iter(
				boost::python::allow_null(PyObject_GetIter(obj_ptr)));
			if (!obj_iter.get()) { // must be convertible to an iterator
				PyErr_Clear();
				return 0;
			}
			if (ConversionPolicy::check_convertibility_per_element()) {
				std::size_t obj_size = PyObject_Length(obj_ptr);
				if (obj_size < 0) { // must be a measurable sequence
					PyErr_Clear();
					return 0;
				}
				if (!ConversionPolicy::check_size(
				    boost::type<ContainerType>(), obj_size)) return 0;
				bool is_range = PyRange_Check(obj_ptr);
				std::size_t i=0;
				if (!all_elements_convertible(obj_iter, is_range, i)) return 0;
				if (!is_range) assert(i == obj_size);
			}
			return obj_ptr;
		}

		// This loop factored out by Achim Domma to avoid Visual C++
		// Internal Compiler Error.
		static bool
		all_elements_convertible(
		                         boost::python::handle<>& obj_iter,
		                         bool is_range,
		                         std::size_t& i)
		{
			for(;;i++) {
				boost::python::handle<> py_elem_hdl(
				boost::python::allow_null(PyIter_Next(obj_iter.get())));
				if (PyErr_Occurred()) {
					PyErr_Clear();
					return false;
				}
				if (!py_elem_hdl.get()) break; // end of iteration
				boost::python::object py_elem_obj(py_elem_hdl);
				boost::python::extract<container_element_type>
				elem_proxy(py_elem_obj);
				if (!elem_proxy.check()) return false;
				if (is_range) break; // in a range all elements are of the same type
			}
			return true;
		}

		static void construct(
		                      PyObject* obj_ptr,
		                      boost::python::converter::rvalue_from_python_stage1_data* data)
		{
			boost::python::handle<> obj_iter(PyObject_GetIter(obj_ptr));
			void* storage = (
			                 (boost::python::converter::rvalue_from_python_storage<ContainerType>*)
			                 data)->storage.bytes;
			new (storage) ContainerType();
			data->convertible = storage;
			ContainerType& result = *((ContainerType*)storage);
			std::size_t i=0;
			for(;;i++) {
				boost::python::handle<> py_elem_hdl(
				boost::python::allow_null(PyIter_Next(obj_iter.get())));
				if (PyErr_Occurred()) boost::python::throw_error_already_set();
				if (!py_elem_hdl.get()) break; // end of iteration
				boost::python::object py_elem_obj(py_elem_hdl);
				boost::python::extract<container_element_type> elem_proxy(py_elem_obj);
				ConversionPolicy::set_value(result, i, elem_proxy());
			}
			ConversionPolicy::assert_size(boost::type<ContainerType>(), i);
		}
	};

	template <typename ContainerType>
	struct to_tuple_mapping
	{
		to_tuple_mapping() {
			boost::python::to_python_converter<
			ContainerType,
			to_tuple<ContainerType>
			#ifdef BOOST_PYTHON_SUPPORTS_PY_SIGNATURES
			, true
			#endif
			>();
		}
	};

	template <typename ContainerType, typename ConversionPolicy>
	struct tuple_mapping : to_tuple_mapping<ContainerType>
	{
		tuple_mapping() {
			from_python_sequence<
			ContainerType,
			ConversionPolicy>();
		}
	};

	template <typename ContainerType>
	struct tuple_mapping_fixed_size
	{
		tuple_mapping_fixed_size() {
			tuple_mapping<
			ContainerType,
			fixed_size_policy>();
		}
	};

	template <typename ContainerType>
	struct tuple_mapping_fixed_capacity
	{
		tuple_mapping_fixed_capacity() {
			tuple_mapping<
			ContainerType,
			fixed_capacity_policy>();
		}
	};

	template <typename ContainerType>
	struct tuple_mapping_variable_capacity
	{
		tuple_mapping_variable_capacity() {
			tuple_mapping<
			ContainerType,
			variable_capacity_policy>();
		}
	};

	template <typename ContainerType>
	struct tuple_mapping_set
	{
		tuple_mapping_set() {
			tuple_mapping<
			ContainerType,
			set_policy>();
		}
	};
}}//end namespace omega::bindings
#endif
