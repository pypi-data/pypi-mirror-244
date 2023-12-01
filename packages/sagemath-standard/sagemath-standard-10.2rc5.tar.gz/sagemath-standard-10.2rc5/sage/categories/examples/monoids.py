r"""
Examples of monoids
"""
#*****************************************************************************
#  Copyright (C) 2008-2009 Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.misc.cachefunc import cached_method
from sage.structure.parent import Parent
from sage.structure.element_wrapper import ElementWrapper
from sage.categories.monoids import Monoids
from .semigroups import FreeSemigroup
from sage.sets.family import Family

class FreeMonoid(FreeSemigroup):
    r"""
    An example of a monoid: the free monoid

    This class illustrates a minimal implementation of a monoid. For a
    full featured implementation of free monoids, see :func:`FreeMonoid`.

    EXAMPLES::

        sage: S = Monoids().example(); S
        An example of a monoid: the free monoid generated by ('a', 'b', 'c', 'd')

        sage: S.category()
        Category of monoids

    This is the free semigroup generated by::

        sage: S.semigroup_generators()
        Family ('a', 'b', 'c', 'd')

    with product rule given by concatenation of words::

        sage: S('dab') * S('acb')
        'dabacb'

    and unit given by the empty word::

        sage: S.one()
        ''

    We conclude by running systematic tests on this monoid::

        sage: TestSuite(S).run(verbose = True)
        running ._test_an_element() . . . pass
        running ._test_associativity() . . . pass
        running ._test_cardinality() . . . pass
        running ._test_category() . . . pass
        running ._test_construction() . . . pass
        running ._test_elements() . . .
          Running the test suite of self.an_element()
          running ._test_category() . . . pass
          running ._test_eq() . . . pass
          running ._test_new() . . . pass
          running ._test_not_implemented_methods() . . . pass
          running ._test_pickling() . . . pass
          pass
        running ._test_elements_eq_reflexive() . . . pass
        running ._test_elements_eq_symmetric() . . . pass
        running ._test_elements_eq_transitive() . . . pass
        running ._test_elements_neq() . . . pass
        running ._test_eq() . . . pass
        running ._test_new() . . . pass
        running ._test_not_implemented_methods() . . . pass
        running ._test_one() . . . pass
        running ._test_pickling() . . . pass
        running ._test_prod() . . . pass
        running ._test_some_elements() . . . pass
    """

    def __init__(self, alphabet=('a','b','c','d')):
        r"""
        The free monoid

        INPUT:

        - ``alphabet`` -- a tuple of strings: the generators of the monoid

        EXAMPLES::

            sage: M = Monoids().example(alphabet=('a','b','c')); M
            An example of a monoid: the free monoid generated by ('a', 'b', 'c')

        TESTS::

            sage: TestSuite(M).run()

        """
        self.alphabet = alphabet
        Parent.__init__(self, category=Monoids())

    def _repr_(self):
        r"""
        TESTS::

            sage: M = Monoids().example(alphabet=('a','b','c'))
            sage: M._repr_()
            "An example of a monoid: the free monoid generated by ('a', 'b', 'c')"

        """
        return "An example of a monoid: the free monoid generated by %s" % (self.alphabet,)

    @cached_method
    def one(self):
        r"""
        Returns the one of the monoid, as per :meth:`Monoids.ParentMethods.one`.

        EXAMPLES::

            sage: M = Monoids().example(); M
            An example of a monoid: the free monoid generated by ('a', 'b', 'c', 'd')
            sage: M.one()
            ''

        """
        return self("")

    @cached_method
    def monoid_generators(self):
        r"""
        Return the generators of this monoid.

        EXAMPLES::

            sage: M = Monoids().example(); M
            An example of a monoid: the free monoid generated by ('a', 'b', 'c', 'd')
            sage: M.monoid_generators()
            Finite family {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd'}
            sage: a,b,c,d = M.monoid_generators()
            sage: a*d*c*b
            'adcb'
        """
        return Family(self.alphabet, self)

    class Element (ElementWrapper):
        wrapped_class = str


Example = FreeMonoid
