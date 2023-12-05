import functools

import sympy as sp

from ananke.factors import SymCPD
from ananke.graphs import DAG
from ananke.inference.variable_elimination import variable_elimination
from ananke.models import BayesianNetwork


def test_variable_elimination_on_three_var_chain():
    x1 = sp.Symbol("x1")
    y1 = sp.Symbol("y1")
    y2 = sp.Symbol("y2")
    x2 = sp.Symbol("x2")
    x3 = sp.Symbol("x3")
    cpd_a = SymCPD("A", 2, sp.Array([[x1, y1], [1 - x1, 1 - y1]]), ["B"], [2])
    cpd_b = SymCPD("B", 2, sp.Array([[x2, y2], [1 - x2, 1 - y2]]), ["C"], [2])
    cpd_c = SymCPD("C", 2, sp.Array([[x3], [1 - x3]]))

    graph = DAG(
        vertices={"A": 2, "B": 2, "C": 2},
        di_edges=[("C", "B"), ("B", "A")],
    )
    cpds = {"A": cpd_a, "B": cpd_b, "C": cpd_c}
    bayesian_network = BayesianNetwork(graph, cpds)
    marginal = variable_elimination(bayesian_network, variables=["A"])
    truth = functools.reduce(
        lambda x, y: x.product(y), [cpd.to_factor() for cpd in cpds.values()]
    ).marginalize(["B", "C"])
    assert sp.simplify(sp.tensorcontraction(marginal.values, (0,))) == 1
    assert marginal == truth
