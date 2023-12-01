r"""
Examples of filtered algebra with basis
"""
#*****************************************************************************
#  Copyright (C) 2014 Travis Scrimshaw <tscrim at ucdavis.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.categories.filtered_algebras_with_basis import FilteredAlgebrasWithBasis
from sage.combinat.free_module import CombinatorialFreeModule
from sage.monoids.indexed_free_monoid import IndexedFreeAbelianMonoid
from sage.sets.family import Family

class PBWBasisCrossProduct(CombinatorialFreeModule):
    r"""
    This class illustrates an implementation of a filtered algebra
    with basis: the universal enveloping algebra of the Lie algebra
    of `\RR^3` under the cross product.

    The Lie algebra is generated by `x,y,z` with brackets defined by
    `[x, y] = z`, `[y, z] = x`, and `[x, z] = -y`. The universal enveloping
    algebra has a (PBW) basis consisting of monomials `x^i y^j z^k`.
    Despite these monomials not commuting with each other, we
    nevertheless label them by the elements of the free abelian monoid
    on three generators.

    INPUT:

    - ``R`` -- base ring

    The implementation involves the following:

    - A set of algebra generators -- the set of generators `x,y,z`.

    - The index of the unit element -- the unit element in the monoid
      of monomials.

    - A product -- this is given on basis elements by using
      :meth:`product_on_basis`.

    - A degree function -- this is determined on the basis elements
      by using :meth:`degree_on_basis` which returns the sum of exponents
      of the monomial.
    """
    def __init__(self, base_ring):
        """
        EXAMPLES::

            sage: A = AlgebrasWithBasis(QQ).Filtered().example()
            sage: x,y,z = A.algebra_generators()
            sage: TestSuite(A).run(elements=[x*y+z])
        """
        I = IndexedFreeAbelianMonoid(['x', 'y', 'z'], prefix='U')

        CombinatorialFreeModule.__init__(self, base_ring, I, bracket=False,
                                         prefix='',
                                         sorting_key=self._sort_key,
                                         category=FilteredAlgebrasWithBasis(base_ring))

    def _sort_key(self, x):
        """
        Return the key used to sort the terms.

        INPUT:

        - ``x`` -- a basis index (here an element in a free Abelian monoid)

        EXAMPLES::

            sage: A = AlgebrasWithBasis(QQ).Filtered().example()
            sage: S = sorted(A.an_element().support()); S
            [1, U['x'], U['x']^2*U['y']^2*U['z']^3, U['y']]
            sage: [A._sort_key(m) for m in S]
            [(0, []), (-1, ['x']), (-7, ['x', 'x', 'y', 'y', 'z', 'z', 'z']),
            (-1, ['y'])]
        """
        return (-len(x), x.to_word_list())

    def _repr_(self):
        """
        Return a string representation of ``self``.

        EXAMPLES::

            sage: AlgebrasWithBasis(QQ).Filtered().example()
            An example of a filtered algebra with basis:
             the universal enveloping algebra of
             Lie algebra of RR^3 with cross product over Rational Field
        """
        return "An example of a filtered algebra with basis: the universal enveloping algebra of Lie algebra of RR^3 with cross product over {}".format(self.base_ring())

    def algebra_generators(self):
        """
        Return the algebra generators of ``self``.

        EXAMPLES::

            sage: A = AlgebrasWithBasis(QQ).Filtered().example()
            sage: list(A.algebra_generators())
            [U['x'], U['y'], U['z']]
        """
        G = self._indices.monoid_generators()
        I = sorted(G.keys())
        return Family(I, lambda x: self.monomial(G[x]))

    def one_basis(self):
        """
        Return the index of the unit of ``self``.

        EXAMPLES::

            sage: A = AlgebrasWithBasis(QQ).Filtered().example()
            sage: A.one_basis()
            1
        """
        return self._indices.one()

    def degree_on_basis(self, m):
        """
        The degree of the basis element of ``self`` labelled by ``m``.

        INPUT:

        - ``m`` -- an element of the free abelian monoid

        OUTPUT: an integer, the degree of the corresponding basis element

        EXAMPLES::

            sage: A = AlgebrasWithBasis(QQ).Filtered().example()
            sage: x = A.algebra_generators()['x']
            sage: A.degree_on_basis((x^4).leading_support())
            4
            sage: a = A.an_element(); a
            U['x']^2*U['y']^2*U['z']^3 + 2*U['x'] + 3*U['y'] + 1
            sage: A.degree_on_basis(a.leading_support())
            1
            sage: s = sorted(a.support(), key=str)[2]; s
            U['x']^2*U['y']^2*U['z']^3
            sage: A.degree_on_basis(s)
            7
        """
        return len(m)

    # TODO: This is a general procedure of expanding multiplication defined
    #  on generators to arbitrary monomials and could likely be factored out
    #  and be useful elsewhere.
    def product_on_basis(self, s, t):
        """
        Return the product of two basis elements indexed by ``s`` and ``t``.

        EXAMPLES::

            sage: A = AlgebrasWithBasis(QQ).Filtered().example()
            sage: G = A.algebra_generators()
            sage: x,y,z = G['x'], G['y'], G['z']
            sage: A.product_on_basis(x.leading_support(), y.leading_support())
            U['x']*U['y']
            sage: y*x
            U['x']*U['y'] - U['z']
            sage: x*y*x
            U['x']^2*U['y'] - U['x']*U['z']
            sage: z*y*x
            U['x']*U['y']*U['z'] - U['x']^2 + U['y']^2 - U['z']^2
        """
        if len(s) == 0:
            return self.monomial(t)
        if len(t) == 0:
            return self.monomial(s)
        if s.trailing_support() <= t.leading_support():
            return self.monomial(s*t)

        if len(t) == 1:
            if len(s) == 1:
                # Do the product of the generators
                a = s.leading_support()
                b = t.leading_support()
                cur = self.monomial(s*t)
                if a <= b:
                    return cur
                if a == 'z':
                    if b == 'y':
                        return cur - self.monomial(self._indices.gen('x'))
                    # b == 'x'
                    return cur + self.monomial(self._indices.gen('y'))
                # a == 'y' and b == 'x'
                return cur - self.monomial(self._indices.gen('z'))

            cur = self.monomial(t)
            for a in reversed(s.to_word_list()):
                cur = self.monomial(self._indices.gen(a)) * cur
            return cur

        cur = self.monomial(s)
        for a in t.to_word_list():
            cur = cur * self.monomial(self._indices.gen(a))
        return cur


Example = PBWBasisCrossProduct
