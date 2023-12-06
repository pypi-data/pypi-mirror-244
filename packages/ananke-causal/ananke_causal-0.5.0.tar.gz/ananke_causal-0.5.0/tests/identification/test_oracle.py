import sympy as sp

from ananke.factors import SymCPD
from ananke.graphs import DAG
from ananke.identification import oracle
from ananke.models.bayesian_network import BayesianNetwork


def test_compute_effect_from_discrete_model():

    u1 = sp.Symbol("u1")
    a1 = sp.Symbol("a1")
    a2 = sp.Symbol("a2")
    y1 = sp.Symbol("y1")
    y2 = sp.Symbol("y2")
    y3 = sp.Symbol("y3")
    y4 = sp.Symbol("y4")
    cpd_u = SymCPD("U", 2, sp.Array([[u1], [1 - u1]]))
    cpd_a = SymCPD("A", 2, sp.Array([[a1, a2], [1 - a1, 1 - a2]]), ["U"], [2])

    cpd_y = SymCPD(
        "Y",
        2,
        sp.Array([[y1, y2, y3, y4], [1 - y1, 1 - y2, 1 - y3, 1 - y4]]),
        ["A", "U"],
        [2, 2],
    )
    graph = DAG(
        vertices={"A": 2, "U": 2, "Y": 2},
        di_edges=[("A", "Y"), ("U", "A"), ("U", "Y")],
    )
    cpds = {"A": cpd_a, "Y": cpd_y, "U": cpd_u}
    net = BayesianNetwork(graph, cpds)

    result = oracle.compute_effect_from_discrete_model(net, {"A": 0}, {"Y": 0})
    truth = y1 * u1 + y2 * (1 - u1)
    assert sp.simplify(result - truth) == 0
