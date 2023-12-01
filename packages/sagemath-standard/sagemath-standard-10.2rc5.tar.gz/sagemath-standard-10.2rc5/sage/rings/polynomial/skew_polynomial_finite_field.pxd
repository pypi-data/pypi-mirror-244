from sage.rings.polynomial.skew_polynomial_finite_order cimport SkewPolynomial_finite_order_dense

cdef class SkewPolynomial_finite_field_dense (SkewPolynomial_finite_order_dense):
    cdef _norm_factor
    cdef dict _types
    cdef _factorization

    cdef inline _reduced_norm_factored(self) noexcept

    # Finding divisors
    cdef SkewPolynomial_finite_field_dense _rdivisor_c(P, N) noexcept

    # Finding factorizations
    cdef _factor_c(self) noexcept
    cdef _factor_uniform_c(self) noexcept

cdef inline SkewPolynomial_finite_field_dense mul_op(SkewPolynomial_finite_field_dense P, SkewPolynomial_finite_field_dense Q) noexcept:
    return Q * P
