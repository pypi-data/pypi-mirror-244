import itertools

import numpy as np
import sympy as sp
from pgmpy.factors.discrete import TabularCPD

from ananke.factors import SymCPD, SymDiscreteFactor


class TestSymDiscreteFactor:
    def test_initialize(self):
        variables = ["A", "B"]
        cardinality = [2, 3]
        a = sp.Symbol("a")
        b = sp.Symbol("b")
        values = sp.Array([2, b + 1, b + 0.5, a - 3, b / a, b + a])
        result = SymDiscreteFactor(variables, cardinality, values)
        assert len(values) == 6
        assert result.values.shape == (2, 3)

    def test_marginalize(self):
        variables = ["A", "B"]
        cardinality = [2, 3]
        a = sp.Symbol("a")
        b = sp.Symbol("b")
        values = sp.Array([2, b + 1, b + 0.5, a - 3, b / a, b + a])
        result = SymDiscreteFactor(variables, cardinality, values)

        result = result.marginalize(["A"])
        truth = SymDiscreteFactor(
            ["B"], [3], sp.Array([2 + a - 3, b + 1 + b / a, b + 0.5 + b + a])
        )
        assert truth == result

    def test_product(self):
        a = sp.Symbol("a")
        b = sp.Symbol("b")
        c = sp.Symbol("c")
        d = sp.Symbol("d")

        variables1 = ["C", "A", "B"]
        cardinality1 = [2, 2, 3]
        # (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)
        values1 = sp.Array(
            [
                2,
                b + 1,
                b + 0.5,
                a - 3,
                b / a,
                b + a,
                2,
                b + 1,
                b + 0.5,
                a - 3,
                b / a,
                b + a,
            ]
        )
        factor1 = SymDiscreteFactor(variables1, cardinality1, values1)

        variables2 = ["D", "B", "C"]
        cardinality2 = [2, 3, 2]
        # (0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)
        values2 = sp.Array(
            [
                1,
                d,
                d**2,
                d**3,
                d**4,
                d**5,
                1,
                c,
                c**2,
                c**3,
                c**4,
                c**5,
            ]
        )
        factor2 = SymDiscreteFactor(variables2, cardinality2, values2)

        result = factor1.product(factor2)

        # 000, 001, 010, 011, 020, 021, 100, 101, 110, 111, 120, 121
        rvalues1 = values1.reshape(2, 2, 3)
        rvalues2 = values2.reshape(2, 3, 2)
        final_values = list()
        for i in itertools.product(*[range(2), range(3), range(2), range(2)]):
            final_values.append(
                rvalues1[i[2], i[0], i[1]] * rvalues2[i[3], i[1], i[2]]
            )
        truth = SymDiscreteFactor(
            variables=["A", "B", "C", "D"],
            cardinality=[2, 3, 2, 2],
            values=sp.Array(final_values),
        )
        assert result == truth

    def test_product_no_intersection(self):
        a = sp.Symbol("a")
        b = sp.Symbol("b")
        factor1 = SymDiscreteFactor(
            variables=["A"], cardinality=[2], values=sp.Array([a, a + 1])
        )
        factor2 = SymDiscreteFactor(
            variables=["B"], cardinality=[2], values=sp.Array([b, b + 1])
        )
        truth = SymDiscreteFactor(
            variables=["A", "B"],
            cardinality=[2, 2],
            values=sp.Array(
                [a * b, a * (b + 1), (a + 1) * b, (a + 1) * (b + 1)]
            ),
        )
        assert factor1.product(factor2) == truth

    def test_reduce(self):
        a = sp.Symbol("a")
        b = sp.Symbol("b")
        factor = SymDiscreteFactor(
            variables=["A", "B"],
            cardinality=[2, 2],
            values=sp.Array(
                [a * b, a * (b + 1), (a + 1) * b, (a + 1) * (b + 1)]
            ),
        )

        truth = SymDiscreteFactor(
            variables=["A"],
            cardinality=[2],
            values=sp.Array(
                [
                    a * b,
                    (a + 1) * b,
                ]
            ),
        )

        assert factor.reduce([("B", 0)]) == truth

    def test_divide(self):
        a = sp.Symbol("a")
        b = sp.Symbol("b")
        factor = SymDiscreteFactor(
            variables=["A", "B"],
            cardinality=[2, 2],
            values=sp.Array(
                [a * b, a * (b + 1), (a + 1) * b, (a + 1) * (b + 1)]
            ),
        )
        truth = SymDiscreteFactor(
            variables=["A", "B"],
            cardinality=[2, 2],
            values=sp.Array([1] * 4),
        )

        assert factor.divide(factor) == truth

    def test_marginalize_from_cpd(self):
        x1 = sp.Symbol("x1")
        y1 = sp.Symbol("y1")
        cpd_a = SymCPD(
            "A", 2, sp.Array([[x1, y1], [1 - x1, 1 - y1]]), ["B"], [2]
        )
        factor = cpd_a.to_factor()
        result = factor.marginalize(["B"])
        truth = SymDiscreteFactor(
            variables=["A"],
            cardinality=[2],
            values=sp.Array([x1 + y1, 2 - x1 - y1]),
        )

        result2 = factor.marginalize([])
        assert result2 == factor

    def test_empty_factor(self):
        a = sp.Symbol("a")
        factor = SymDiscreteFactor(
            variables=["A"], cardinality=[2], values=sp.Array([a, 1 - a])
        )
        result = factor.marginalize(["A"])

        truth = SymDiscreteFactor(variables=[], cardinality=[], values=1)

        assert result == truth
        assert factor.product(truth) == factor

    def test_get_value(self):
        x1 = sp.Symbol("x1")
        y1 = sp.Symbol("y1")
        cpd_a = SymCPD(
            "A", 2, sp.Array([[x1, y1], [1 - x1, 1 - y1]]), ["B"], [2]
        )

        result = cpd_a.get_value(A=0, B=1)
        truth = y1
        assert result == truth

    def test_to_pgmpy(self):
        cpd_a = SymCPD("A", 2, sp.Array([[1, 1], [0, 0]]), ["B"], [2])
        result = cpd_a.to_pgmpy()
        truth = TabularCPD("A", 2, np.array([[1, 1], [0, 0]]), ["B"], [2])

        assert result == truth
