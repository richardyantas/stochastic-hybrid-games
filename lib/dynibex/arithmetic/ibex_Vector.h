//============================================================================
//                                  I B E X                                   
// File        : ibex_Vector.h
// Author      : Gilles Chabert
// Copyright   : Ecole des Mines de Nantes (France)
// License     : See the LICENSE file
// Created     : Apr 17, 2012
// Last Update : Apr 17, 2012
//============================================================================

#ifndef __IBEX_VECTOR_H__
#define __IBEX_VECTOR_H__

#include <cassert>
#include <iostream>

namespace ibex {

class Matrix; // declared only for friendship
class ExprConstant;

/**
 * \ingroup arithmetic
 *
 * \brief Vector of reals
 *
 */
class Vector {
public:
	/**
	 * \brief Create [0; ...; 0]
	 *
	 * Create a n-sized vector. All the components are 0
	 * \pre n>0
	 */
	Vector(int n);

	/**
	 * \brief Create [x; ....; x]
	 *
	 * Create a Vector of dimension \a n with
	 * all the components initialized to \a x.
	 * \pre n>0
	 */
	Vector(int n, double x);

	/**
	 * \brief Create a copy of \a x.
	 */
	Vector(const Vector& x);

	/**
	 * \brief Create the Vector [x[0]; ..; x[n]]
	 *
	 * \param a array of n doubles
	 * \pre n>0
	 */
	Vector(int n, double  x[]);

	/**
	 * \brief Delete this vector
	 */
	virtual ~Vector();

	/**
	 * \brief Return the ith double
	 *
	 * A return a const reference to the
	 * i^th double (i starts from 0)
	 */
	const double& operator[](int i) const;

	/**
	 * \brief Return the ith double
	 *
	 * A return a non-const reference to the
	 * i^th component (i starts from 0)
	 */
	double& operator[](int i);

	/**
	 * \brief Resize this Vector.
	 *
	 * If the size is increased, the existing components are not
	 * modified and the new ones are set to 0.
	 */
	void resize(int n2);

	/**
	 * \brief Return a subvector.
	 *
	 * \return [ (*this)[start_index]; ...; (*this)[end_index] ].
	 */
	Vector subvector(int start_index, int end_index) const;

	/**
	 * \brief Put a subvector into *this at a given position.
	 *
	 * \param start_index - the position where the subvector
	 * \param subvec - the subvector
	 */
	void put(int start_index, const Vector& subvec);

	/**
	 * \brief Assign this Vector to x.
	 *
	 * \pre Dimensions of this and x must match.
	 */
	Vector& operator=(const Vector& x);

	/**
	 * \brief Return true if the components of this Vector match that of \a x.
	 */
	bool operator==(const Vector& x) const;

	/**
	 * \brief Return true if one component of *this differs from \a x.
	 */
	bool operator!=(const Vector& x) const;

	/**
	 * \brief The dimension (number of components)
	 */
	int size() const;

	/**
	 * \brief The maximum of all elements
	 */
	double max() const;

	/**
	 * \brief The minimum of all elements
	 */
	double min() const;

	/**
	 * \brief ||x||.
	 */
	double norm() const;

	/**
	 * \brief (*this)+=x2.
	 */
	Vector& operator+=(const Vector& x2);

	/**
	 * \brief (*this)-=x2.
	 */
	Vector& operator-=(const Vector& x2);

	/**
	 * \brief (*this)=d*(*this) (left scalar multiplication)
	 */
	Vector& operator*=(double d);

	/**
	 * \brief Create the zero-vector of size n.
	 */
	static Vector zeros(int n);

	/**
	 * \brief Create a vector of ones of size n.
	 */
	static Vector ones(int n);

	/**
	 * \brief Cast the vector to an expression
	 */
	operator const ExprConstant&() const;

private:
	friend class Matrix;

	Vector() : n(0), vec(NULL) { } // for Matrix

	int n;             // dimension (size of vec)
	double *vec;	   // vector of elements
};

/** \ingroup arithmetic */
/*@{*/

/**
 * \brief -x.
 */
Vector operator-(const Vector& x);

/**
 * \brief x1+x2.
 */
Vector operator+(const Vector& x1, const Vector& x2);

/**
 * \brief x1-x2.
 */
Vector operator-(const Vector& x1, const Vector& x2);

/**
 * \brief x1*x2.
 */
double operator*(const Vector& x1, const Vector& x2);

/**
 * \brief Outer product of x1 and x2.
 */
Matrix outer_product(const Vector& x1, const Vector& x2);

/**
 * \brief Hadamard product of x and y.
 *
 * The Hadamard product is a component-wise multiplication:
 * z[i]=x[i]*y[i].
 */
Vector hadamard_product(const Vector& x, const Vector& y);

/**
 * \brief d*x
 */
Vector operator*(double d, const Vector& x);

/**
 * \brief |x|.
 */
Vector abs(const Vector& x);

/**
 * \brief Display the Vector \a x
 */
std::ostream& operator<<(std::ostream& os, const Vector& x);


/*@}*/

/*================================== inline implementations ========================================*/


namespace {

// the following functions are
// introduced to allow genericity
//inline bool is_empty(double x)                { return false; }
//inline bool is_empty(const Interval& x)       { return x.is_empty(); }
inline bool is_empty(const Vector& v)         { return false; }
//inline bool is_empty(const IntervalVector& v) { return v.is_empty(); }
//inline bool is_empty(const Matrix& m)         { return false; }
//inline bool is_empty(const IntervalMatrix& m) { return m.is_empty(); }
//template<class T> inline bool is_empty(const Affine2Main<T>& x)       { return x.is_empty(); }
//template<class T> inline bool is_empty(const Affine2MainVector<T>& v) { return v.is_empty(); }
//template<class T> inline bool is_empty(const Affine2MainMatrix<T>& m) { return m.is_empty(); }



//inline void set_empty(double x)          { }
//inline void set_empty(Interval& x)       { x.set_empty(); }
inline void set_empty(Vector& v)         { }
//inline void set_empty(IntervalVector& v) { v.set_empty(); }
//inline void set_empty(Matrix& m)         { }
//inline void set_empty(IntervalMatrix& m) { m.set_empty(); }
//template<class T> inline void set_empty(Affine2Main<T>& x)       { x.set_empty(); }
//template<class T> inline void set_empty(Affine2MainVector<T>& v) { v.set_empty(); }
//template<class T> inline void set_empty(Affine2MainMatrix<T>& m) { m.set_empty(); }


} // end namespace anonymous

} // end namespace ibex

#include "ibex_LinearArith.h_"

namespace ibex {



inline const double& Vector::operator[](int i) const {
	assert(i>=0 && i<n);
	return vec[i];
}

inline double& Vector::operator[](int i) {
	assert(i>=0 && i<n);
	return vec[i];
}


inline bool Vector::operator!=(const Vector& x) const {
	return !(*this==x);
}

inline int Vector::size() const {
	return n;
}

inline Vector Vector::zeros(int n) {
	return Vector(n,0.0);
}

inline Vector Vector::ones(int n) {
	return Vector(n,1.0);
}

inline Vector operator-(const Vector& x) {
	return minusV(x);
}

inline Vector& Vector::operator+=(const Vector& x) {
	return set_addV<Vector,Vector>(*this,x);
}

inline Vector& Vector::operator-=(const Vector& x) {
	return set_subV<Vector,Vector>(*this,x);
}

inline Vector& Vector::operator*=(double x) {
	return set_mulSV<double,Vector>(x,*this);
}

inline Vector operator+(const Vector& m1, const Vector& m2) {
	return Vector(m1)+=m2;
}

inline Vector operator-(const Vector& m1, const Vector& m2) {
	return Vector(m1)-=m2;
}

inline Vector operator*(double x, const Vector& v) {
	return Vector(v)*=x;
}

inline Vector hadamard_product(const Vector& v1, const Vector& v2) {
	return hadamard_prod<Vector,Vector,Vector>(v1,v2);
}

inline Vector abs(const Vector& v) {
	return absV(v);
}

inline double operator*(const Vector& v1, const Vector& v2) {
	return mulVV<Vector,Vector,double>(v1,v2);
}



} // end namespace ibex
#endif // __IBEX_VECTOR_H__