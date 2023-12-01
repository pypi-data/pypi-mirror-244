# -*- coding: utf-8 -*-
r"""
Value groups of discrete valuations

This file defines additive sub(semi-)groups of `\QQ` and related structures.

AUTHORS:

- Julian Rüth (2013-09-06): initial version

EXAMPLES::

    sage: v = ZZ.valuation(2)
    sage: v.value_group()
    Additive Abelian Group generated by 1
    sage: v.value_semigroup()
    Additive Abelian Semigroup generated by 1

"""
# ****************************************************************************
#       Copyright (C) 2013-2018 Julian Rüth <julian.rueth@fsfe.org>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation
from sage.rings.integer_ring import ZZ
from sage.rings.rational_field import QQ
from sage.rings.infinity import infinity
from sage.misc.cachefunc import cached_method


class DiscreteValuationCodomain(UniqueRepresentation, Parent):
    r"""
    The codomain of discrete valuations, the rational numbers extended by
    `\pm\infty`.

    EXAMPLES::

        sage: from sage.rings.valuation.value_group import DiscreteValuationCodomain
        sage: C = DiscreteValuationCodomain(); C
        Codomain of Discrete Valuations

    TESTS::

        sage: TestSuite(C).run() # long time

    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.rings.valuation.value_group import DiscreteValuationCodomain
            sage: isinstance(QQ.valuation(2).codomain(), DiscreteValuationCodomain)
            True

        """
        from sage.sets.finite_enumerated_set import FiniteEnumeratedSet
        from sage.categories.additive_monoids import AdditiveMonoids
        UniqueRepresentation.__init__(self)
        Parent.__init__(self, facade=(QQ, FiniteEnumeratedSet([infinity, -infinity])), category=AdditiveMonoids())

    def _element_constructor_(self, x):
        r"""
        Create an element from ``x``.

        INPUT:

        - ``x`` -- a rational number or `\infty`

        TESTS::

            sage: from sage.rings.valuation.value_group import DiscreteValuationCodomain
            sage: DiscreteValuationCodomain()(0)
            0
            sage: DiscreteValuationCodomain()(infinity)
            +Infinity
            sage: DiscreteValuationCodomain()(-infinity)
            -Infinity

        """
        if x is infinity:
            return x
        if x is -infinity:
            return x
        if x not in QQ:
            raise ValueError("must be a rational number or infinity")
        return QQ.coerce(x)

    def _repr_(self):
        r"""
        Return a printable representation.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValuationCodomain
            sage: DiscreteValuationCodomain() # indirect doctest
            Codomain of Discrete Valuations

        """
        return "Codomain of Discrete Valuations"


class DiscreteValueGroup(UniqueRepresentation, Parent):
    r"""
    The value group of a discrete valuation, an additive subgroup of `\QQ`
    generated by ``generator``.

    INPUT:

    - ``generator`` -- a rational number

    .. NOTE::

        We do not rely on the functionality provided by additive abelian groups
        in Sage since these require the underlying set to be the integers.
        Therefore, we roll our own \Z-module here.
        We could have used :class:`AdditiveAbelianGroupWrapper` here, but it
        seems to be somewhat outdated. In particular, generic group
        functionality should now come from the category and not from the
        super-class. A facade of \Q appeared to be the better approach.

    EXAMPLES::

        sage: from sage.rings.valuation.value_group import DiscreteValueGroup
        sage: D1 = DiscreteValueGroup(0); D1
        Trivial Additive Abelian Group
        sage: D2 = DiscreteValueGroup(4/3); D2
        Additive Abelian Group generated by 4/3
        sage: D3 = DiscreteValueGroup(-1/3); D3
        Additive Abelian Group generated by 1/3

    TESTS::

        sage: TestSuite(D1).run()  # long time
        sage: TestSuite(D2).run()  # long time
        sage: TestSuite(D3).run()  # long time

    """
    @staticmethod
    def __classcall__(cls, generator):
        r"""
        Normalizes ``generator`` to a positive rational so that this is a
        unique parent.

        TESTS::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: DiscreteValueGroup(1) is DiscreteValueGroup(-1)
            True

        """
        generator = QQ.coerce(generator).abs()
        return super().__classcall__(cls, generator)

    def __init__(self, generator):
        r"""
        TESTS::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: isinstance(DiscreteValueGroup(0), DiscreteValueGroup)
            True

        """
        from sage.categories.modules import Modules
        self._generator = generator

        # We can not set the facade to DiscreteValuationCodomain since there
        # are some issues with iterated facades currently
        UniqueRepresentation.__init__(self)
        Parent.__init__(self, facade=QQ, category=Modules(ZZ))

    def _element_constructor_(self, x):
        r"""
        Create an element in this group from ``x``.

        INPUT:

        - ``x`` -- a rational number

        TESTS::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: DiscreteValueGroup(0)(0)
            0
            sage: DiscreteValueGroup(0)(1)
            Traceback (most recent call last):
            ...
            ValueError: `1` is not in Trivial Additive Abelian Group.
            sage: DiscreteValueGroup(1)(1)
            1
            sage: DiscreteValueGroup(1)(1/2)
            Traceback (most recent call last):
            ...
            ValueError: `1/2` is not in Additive Abelian Group generated by 1.

        """
        x = QQ.coerce(x)
        if x == 0 or (self._generator != 0 and x / self._generator in ZZ):
            return x

        raise ValueError("`{0}` is not in {1}.".format(x, self))

    def _repr_(self):
        r"""
        Return a printable representation for this group.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: DiscreteValueGroup(0) # indirect doctest
            Trivial Additive Abelian Group

        """
        if self.is_trivial():
            return "Trivial Additive Abelian Group"
        return "Additive Abelian Group generated by %r" % (self._generator,)

    def __add__(self, other):
        r"""
        Return the subgroup of `\QQ` generated by this group and ``other``.

        INPUT:

        - ``other`` -- a discrete value group or a rational number

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: D = DiscreteValueGroup(1/2)
            sage: D + 1/3
            Additive Abelian Group generated by 1/6
            sage: D + D
            Additive Abelian Group generated by 1/2
            sage: D + 1
            Additive Abelian Group generated by 1/2
            sage: DiscreteValueGroup(2/7) + DiscreteValueGroup(4/9)
            Additive Abelian Group generated by 2/63

        """
        if isinstance(other, DiscreteValueGroup):
            return DiscreteValueGroup(self._generator.gcd(other._generator))
        if isinstance(other, DiscreteValueSemigroup):
            return other + self
        from sage.structure.element import is_Element
        if is_Element(other) and QQ.has_coerce_map_from(other.parent()):
            return self + DiscreteValueGroup(other)
        raise ValueError("`other` must be a DiscreteValueGroup or a rational number")

    def _mul_(self, other, switch_sides=False):
        r"""
        Return the group generated by ``other`` times the generator of this
        group.

        INPUT:

        - ``other`` -- a rational number

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: D = DiscreteValueGroup(1/2)
            sage: 1/2 * D
            Additive Abelian Group generated by 1/4
            sage: D * (1/2)
            Additive Abelian Group generated by 1/4
            sage: D * 0
            Trivial Additive Abelian Group
        """
        other = QQ.coerce(other)
        return DiscreteValueGroup(self._generator * other)

    def index(self, other):
        r"""
        Return the index of ``other`` in this group.

        INPUT:

        - ``other`` -- a subgroup of this group

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: DiscreteValueGroup(3/8).index(DiscreteValueGroup(3))
            8
            sage: DiscreteValueGroup(3).index(DiscreteValueGroup(3/8))
            Traceback (most recent call last):
            ...
            ValueError: other must be a subgroup of this group
            sage: DiscreteValueGroup(3).index(DiscreteValueGroup(0))
            Traceback (most recent call last):
            ...
            ValueError: other must have finite index in this group
            sage: DiscreteValueGroup(0).index(DiscreteValueGroup(0))
            1
            sage: DiscreteValueGroup(0).index(DiscreteValueGroup(3))
            Traceback (most recent call last):
            ...
            ValueError: other must be a subgroup of this group

        """
        if not isinstance(other, DiscreteValueGroup):
            raise ValueError("other must be a DiscreteValueGroup")
        if other._generator not in self:
            raise ValueError("other must be a subgroup of this group")
        if other._generator == 0:
            if self._generator == 0:
                return ZZ(1)
            else:
                raise ValueError("other must have finite index in this group")
        return ZZ(other._generator / self._generator)

    def numerator(self):
        r"""
        Return the numerator of a generator of this group.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: DiscreteValueGroup(3/8).numerator()
            3

        """
        return self._generator.numerator()

    def denominator(self):
        r"""
        Return the denominator of a generator of this group.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: DiscreteValueGroup(3/8).denominator()
            8

        """
        return self._generator.denominator()

    def gen(self):
        r"""
        Return a generator of this group.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: DiscreteValueGroup(-3/8).gen()
            3/8

        """
        return self._generator

    def some_elements(self):
        r"""
        Return some typical elements in this group.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: DiscreteValueGroup(-3/8).some_elements()
            [3/8, -3/8, 0, 42, 3/2, -3/2, 9/8, -9/8]

        """
        return [self._generator, -self._generator] + [x for x in QQ.some_elements() if x in self]

    def is_trivial(self):
        r"""
        Return whether this is the trivial additive abelian group.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: DiscreteValueGroup(-3/8).is_trivial()
            False
            sage: DiscreteValueGroup(0).is_trivial()
            True

        """
        return self._generator.is_zero()

    def _element_with_valuation(self, subgroup, s):
        r"""
        Return exponents such that `\pi^a+\psi^b` has valuation `s` where `\pi`
        is a unformizer corresponding to this value group and `\psi` a
        unformizer corresponding to its ``subgroup``.

        The returned values are such that ``a`` is minimal.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueGroup
            sage: DiscreteValueGroup(3/8)._element_with_valuation(DiscreteValueGroup(3), 15/8)
            (-3, 1)
            sage: DiscreteValueGroup(3/8)._element_with_valuation(DiscreteValueGroup(3), 33/8)
            (3, 1)

        """
        if s not in self:
            raise ValueError("s must be in the value group but %r is not in %r." % (s, self))

        i = self.index(subgroup)
        x = s/self.gen()
        a = x % i
        if abs(a-i) < a:
            a -= i
        b = (x-a)/i
        return a, b


class DiscreteValueSemigroup(UniqueRepresentation, Parent):
    r"""
    The value semigroup of a discrete valuation, an additive subsemigroup of
    `\QQ` generated by ``generators``.

    INPUT:

    - ``generators`` -- rational numbers

    EXAMPLES::

        sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
        sage: D1 = DiscreteValueSemigroup(0); D1
        Trivial Additive Abelian Semigroup
        sage: D2 = DiscreteValueSemigroup(4/3); D2
        Additive Abelian Semigroup generated by 4/3
        sage: D3 = DiscreteValueSemigroup([-1/3, 1/2]); D3
        Additive Abelian Semigroup generated by -1/3, 1/2

    TESTS::

        sage: TestSuite(D1).run()               # long time
        sage: TestSuite(D2).run()               # long time                             # needs sage.geometry.polyhedron
        sage: TestSuite(D3).run()               # long time                             # needs sage.numerical.mip

    """
    @staticmethod
    def __classcall__(cls, generators):
        r"""
        Normalize ``generators``.

        TESTS:

        We do not find minimal generators or something like that but just sort the
        generators and drop generators that are trivially contained in the
        semigroup generated by the remaining generators::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
            sage: DiscreteValueSemigroup([1,2]) is DiscreteValueSemigroup([1])
            True

        In this case, the normalization is not sufficient to determine that
        these are the same semigroup::

            sage: DiscreteValueSemigroup([1,-1,1/3]) is DiscreteValueSemigroup([1/3,-1/3])
            False

        """
        if generators in QQ:
            generators = [generators]
        generators = list(set([QQ.coerce(g) for g in generators if g != 0]))
        generators.sort()
        simplified_generators = generators

        # this is not very efficient but there should never be more than a
        # couple of generators
        for g in generators:
            for h in generators:
                if g == h:
                    continue
                from sage.rings.semirings.non_negative_integer_semiring import NN
                if h/g in NN:
                    simplified_generators.remove(h)
                    break

        return super().__classcall__(cls, tuple(simplified_generators))

    def __init__(self, generators):
        r"""
        TESTS::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
            sage: isinstance(DiscreteValueSemigroup([0]), DiscreteValueSemigroup)
            True

        """
        from sage.categories.additive_magmas import AdditiveMagmas
        self._generators = generators

        category = AdditiveMagmas().AdditiveAssociative().AdditiveUnital()
        if all(-g in generators for g in generators):
            # check whether this is trivially a group
            # is_group() performs a complete check that is very costly and
            # refines the category
            category = category.AdditiveInverse()

        # We can not set the facade to DiscreteValuationCodomain since there
        # are some issues with iterated facades currently
        Parent.__init__(self, facade=QQ, category=category)

    def _solve_linear_program(self, target):
        r"""
        Return the coefficients of a linear combination to write ``target`` in
        terms of the generators of this semigroup.

        Return ``None`` if no such combination exists.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
            sage: D = DiscreteValueSemigroup([2,3,5])
            sage: D._solve_linear_program(12)                                           # needs sage.numerical.mip
            {0: 1, 1: 0, 2: 2}
            sage: 1*2 + 0*3 + 2*5
            12

        """
        if len(self._generators) == 0:
            if target == 0:
                return {}
            else:
                return None

        if len(self._generators) == 1:
            from sage.rings.semirings.non_negative_integer_semiring import NN
            exp = target / self._generators[0]
            if exp not in NN:
                return None
            return {0: exp}

        if len(self._generators) == 2 and self._generators[0] == - self._generators[1]:
            from sage.rings.integer_ring import ZZ
            exp = target / self._generators[0]
            if exp not in ZZ:
                return None
            return {0: exp, 1: 0}

        from sage.numerical.mip import MixedIntegerLinearProgram, MIPSolverException
        P = MixedIntegerLinearProgram(maximization=False, solver="ppl")
        x = P.new_variable(integer=True, nonnegative=True)
        constraint = sum([g * x[i]
                          for i, g in enumerate(self._generators)]) == target
        P.add_constraint(constraint)
        P.set_objective(None)
        try:
            P.solve()
        except MIPSolverException:
            return None
        return P.get_values(x)

    def _element_constructor_(self, x):
        r"""
        Create an element in this group from ``x``.

        INPUT:

        - ``x`` -- a rational number

        TESTS::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
            sage: DiscreteValueSemigroup([])(0)
            0
            sage: DiscreteValueSemigroup([])(1)
            Traceback (most recent call last):
            ...
            ValueError: `1` is not in Trivial Additive Abelian Semigroup.
            sage: DiscreteValueSemigroup([1])(1)
            1
            sage: DiscreteValueSemigroup([1])(-1)
            Traceback (most recent call last):
            ...
            ValueError: `-1` is not in Additive Abelian Semigroup generated by 1.
        """
        x = QQ.coerce(x)
        if x in self._generators or self._solve_linear_program(x) is not None:
            return x

        raise ValueError("`{0}` is not in {1}.".format(x, self))

    def _repr_(self):
        r"""
        Return a printable representation for this semigroup.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
            sage: DiscreteValueSemigroup(0) # indirect doctest
            Trivial Additive Abelian Semigroup

        """
        if self.is_trivial():
            return "Trivial Additive Abelian Semigroup"
        return "Additive Abelian Semigroup generated by %s" % (', '.join([repr(g) for g in self._generators]),)

    def __add__(self, other):
        r"""
        Return the subsemigroup of `\QQ` generated by this semigroup and ``other``.

        INPUT:

        - ``other`` -- a discrete value (semi-)group or a rational number

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup, DiscreteValueGroup
            sage: D = DiscreteValueSemigroup(1/2)
            sage: D + 1/3
            Additive Abelian Semigroup generated by 1/3, 1/2
            sage: D + D
            Additive Abelian Semigroup generated by 1/2
            sage: D + 1
            Additive Abelian Semigroup generated by 1/2
            sage: DiscreteValueGroup(2/7) + DiscreteValueSemigroup(4/9)
            Additive Abelian Semigroup generated by -2/7, 2/7, 4/9

        """
        if isinstance(other, DiscreteValueSemigroup):
            return DiscreteValueSemigroup(self._generators + other._generators)
        if isinstance(other, DiscreteValueGroup):
            return DiscreteValueSemigroup(self._generators + (other._generator, -other._generator))
        from sage.structure.element import is_Element
        if is_Element(other) and QQ.has_coerce_map_from(other.parent()):
            return self + DiscreteValueSemigroup(other)
        raise ValueError("`other` must be a DiscreteValueGroup, a DiscreteValueSemigroup or a rational number")

    def _mul_(self, other, switch_sides=False):
        r"""
        Return the semigroup generated by ``other`` times the generators of this
        semigroup.

        INPUT:

        - ``other`` -- a rational number

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
            sage: D = DiscreteValueSemigroup(1/2)
            sage: 1/2 * D
            Additive Abelian Semigroup generated by 1/4
            sage: D * (1/2)
            Additive Abelian Semigroup generated by 1/4
            sage: D * 0
            Trivial Additive Abelian Semigroup

        """
        other = QQ.coerce(other)
        return DiscreteValueSemigroup([g*other for g in self._generators])

    def gens(self):
        r"""
        Return the generators of this semigroup.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
            sage: DiscreteValueSemigroup(-3/8).gens()
            (-3/8,)

        """
        return tuple(self._generators)

    def some_elements(self):
        r"""
        Return some typical elements in this semigroup.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
            sage: list(DiscreteValueSemigroup([-3/8,1/2]).some_elements())              # needs sage.numerical.mip
            [0, -3/8, 1/2, ...]
        """
        yield self(0)
        if self.is_trivial():
            return
        yield from self._generators
        from sage.rings.integer_ring import ZZ
        for x in (ZZ**len(self._generators)).some_elements():
            yield QQ.coerce(sum([abs(c) * g
                                 for c, g in zip(x, self._generators)]))

    def is_trivial(self):
        r"""
        Return whether this is the trivial additive abelian semigroup.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
            sage: DiscreteValueSemigroup(-3/8).is_trivial()
            False
            sage: DiscreteValueSemigroup([]).is_trivial()
            True

        """
        return len(self._generators) == 0

    @cached_method
    def is_group(self):
        r"""
        Return whether this semigroup is a group.

        EXAMPLES::

            sage: from sage.rings.valuation.value_group import DiscreteValueSemigroup
            sage: DiscreteValueSemigroup(1).is_group()
            False
            sage: D = DiscreteValueSemigroup([-1, 1])
            sage: D.is_group()
            True

        Invoking this method also changes the category of this semigroup if it
        is a group::

            sage: D in AdditiveMagmas().AdditiveAssociative().AdditiveUnital().AdditiveInverse()
            True
        """
        for x in self._generators:
            if -x not in self:
                return False
        self._refine_category_(self.category().AdditiveInverse())
        return True
