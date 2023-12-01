from sage.structure.element cimport Element, MonoidElement, MultiplicativeGroupElement

cdef class SemimonomialTransformation(MultiplicativeGroupElement):
    cdef tuple v
    cdef object perm, alpha

    cdef _new_c(self) noexcept
    cpdef _mul_(self, other) noexcept
