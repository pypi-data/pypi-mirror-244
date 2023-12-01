"""
Finitely and Freely Generated Lie Conformal Algebras.

AUTHORS:

- Reimundo Heluani (2019-08-09): Initial implementation.
"""

#******************************************************************************
#       Copyright (C) 2019 Reimundo Heluani <heluani@potuz.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.categories.lie_conformal_algebras import LieConformalAlgebras
from .freely_generated_lie_conformal_algebra import \
                                            FreelyGeneratedLieConformalAlgebra

class FinitelyFreelyGeneratedLCA(FreelyGeneratedLieConformalAlgebra):
    """
    Abstract base class for finitely generated Lie conformal
    algebras.

    This class provides minimal functionality, simply sets the
    number of generators.
    """
    def __init__(self, R, index_set=None, central_elements=None, category=None,
                 element_class=None, prefix=None, names=None, latex_names=None,
                 **kwds):
        """
        Initialize self.

        TESTS::

            sage: V = lie_conformal_algebras.Virasoro(QQ)
            sage: TestSuite(V).run()
        """
        default_category = LieConformalAlgebras(R).FinitelyGenerated()
        try:
            category = default_category.or_subcategory(category)
        except ValueError:
            category = default_category.Super().or_subcategory(category)

        from sage.categories.sets_cat import Sets
        if index_set not in Sets().Finite():
            raise TypeError("index_set must be a finite set")

        super().__init__(R,
                         index_set=index_set, central_elements=central_elements,
                         category=category, element_class=element_class,
                         prefix=prefix, **kwds)
        self._ngens = len(self._generators)
        self._names = names
        self._latex_names = latex_names

    def _repr_(self):
        """
        The name of this Lie conformal algebra.

        EXAMPLES::

            sage: bosondict = {('a','a'):{1:{('K',0):1}}}
            sage: R = LieConformalAlgebra(QQ,bosondict,names=('a',),central_elements=('K',))
            sage: R
            Lie conformal algebra with generators (a, K) over Rational Field
        """
        if self._ngens == 1:
            return "Lie conformal algebra generated by {0} over {1}".format(
                self.gen(0), self.base_ring())
        return "Lie conformal algebra with generators {0} over {1}".format(
            self.gens(), self.base_ring())

    def _an_element_(self):
        """
        An element of this Lie conformal algebra.

        EXAMPLES::

            sage: R = lie_conformal_algebras.NeveuSchwarz(QQ); R.an_element()
            L + G + C
        """
        return self.sum(self.gens())

    def ngens(self):
        """
        The number of generators of this Lie conformal algebra.

        EXAMPLES::

            sage: Vir = lie_conformal_algebras.Virasoro(QQ); Vir.ngens()
            2
            sage: V = lie_conformal_algebras.Affine(QQ, 'A1'); V.ngens()
            4
        """
        return self._ngens

    @cached_method
    def gens(self):
        """
        The generators for this Lie conformal algebra.

        OUTPUT:

        This method returns a tuple with the (finite) generators
        of this Lie conformal algebra.

        EXAMPLES::

            sage: Vir = lie_conformal_algebras.Virasoro(QQ);
            sage: Vir.gens()
            (L, C)

        .. SEEALSO::

            :meth:`lie_conformal_algebra_generators<\
            FreelyGeneratedLieConformalAlgebra.\
            lie_conformal_algebra_generators>`
        """
        return self.lie_conformal_algebra_generators()

    @cached_method
    def central_elements(self):
        """
        The central elements of this Lie conformal algebra.

        EXAMPLES::

            sage: R = lie_conformal_algebras.NeveuSchwarz(QQ); R.central_elements()
            (C,)
        """
        return tuple(FreelyGeneratedLieConformalAlgebra.central_elements(self))
