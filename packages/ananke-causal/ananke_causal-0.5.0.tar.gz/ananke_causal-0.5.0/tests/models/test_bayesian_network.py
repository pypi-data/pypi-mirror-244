import numpy as np
import sympy as sp
from pgmpy.factors.discrete import TabularCPD

from ananke.factors import SymCPD
from ananke.graphs import DAG
from ananke.models import BayesianNetwork, bayesian_network


def test_fixing_in_bayesian_network_chain():
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
    bayesian_network.fix({"A": 0})

    assert bayesian_network.cpds["A"] == SymCPD(
        variable="A", variable_card=2, values=sp.Array([[1], [0]])
    )

    assert set(bayesian_network.di_edges) == set([("C", "B")])


def test_fixing_in_bayesian_network_collider():
    x1 = sp.Symbol("x1")
    y1 = sp.Symbol("y1")
    y2 = sp.Symbol("y2")
    y3 = sp.Symbol("y3")
    y4 = sp.Symbol("y4")
    x3 = sp.Symbol("x3")
    cpd_a = SymCPD("A", 2, sp.Array([[x1], [1 - x1]]))
    cpd_b = SymCPD(
        "B",
        2,
        sp.Array([[y1, y2, y3, y4], [1 - y1, 1 - y2, 1 - y3, 1 - y4]]),
        ["A", "C"],
        [2, 2],
    )
    cpd_c = SymCPD("C", 2, sp.Array([[x3], [1 - x3]]))

    graph = DAG(
        vertices={"A": 2, "B": 2, "C": 2},
        di_edges=[("C", "B"), ("B", "A")],
    )
    cpds = {"A": cpd_a, "B": cpd_b, "C": cpd_c}
    net = BayesianNetwork(graph, cpds)
    net.fix({"B": 0})
    truth = SymCPD(
        variable="B",
        variable_card=2,
        values=sp.Array([[1], [0]]),
    )

    assert net.cpds["B"] == truth


def test_fixing_using_pgmpy_cpds():
    x1 = 0.3
    y1 = 0.2
    y2 = 0.3
    y3 = 0.5
    y4 = 0.7
    x3 = 0.2

    cpd_a = TabularCPD("A", 2, np.array([[x1], [1 - x1]]))
    cpd_b = TabularCPD(
        "B",
        2,
        np.array([[y1, y2, y3, y4], [1 - y1, 1 - y2, 1 - y3, 1 - y4]]),
        ["A", "C"],
        [2, 2],
    )
    cpd_c = TabularCPD("C", 2, np.array([[x3], [1 - x3]]))

    graph = DAG(
        vertices={"A": 2, "B": 2, "C": 2},
        di_edges=[("C", "B"), ("B", "A")],
    )
    cpds = {"A": cpd_a, "B": cpd_b, "C": cpd_c}
    bayesian_network = BayesianNetwork(graph, cpds)
    bayesian_network.fix({"B": 0})
    truth = TabularCPD(
        variable="B",
        variable_card=2,
        values=np.array([[1], [0]]),
    )
    assert bayesian_network.cpds["B"] == truth


def test_bayesian_network_to_pgmpy():
    x1 = 0.3
    y1 = 0.2
    y2 = 0.3
    y3 = 0.5
    y4 = 0.7
    x3 = 0.2

    cpd_a = TabularCPD("A", 2, np.array([[x1], [1 - x1]]))
    cpd_b = TabularCPD(
        "B",
        2,
        np.array([[y1, y2, y3, y4], [1 - y1, 1 - y2, 1 - y3, 1 - y4]]),
        ["A", "C"],
        [2, 2],
    )
    cpd_c = TabularCPD("C", 2, np.array([[x3], [1 - x3]]))

    graph = DAG(
        vertices={"A": 2, "B": 2, "C": 2},
        di_edges=[("C", "B"), ("B", "A")],
    )
    cpds = {"A": cpd_a, "B": cpd_b, "C": cpd_c}
    net = BayesianNetwork(graph, cpds)
    pgmpy_net = net.to_pgmpy()
    assert set(pgmpy_net.edges()) == set(graph.di_edges)
    assert set(pgmpy_net.nodes()) == set(graph.vertices)
    assert set(cpds.values()) == set(pgmpy_net.get_cpds())


def test_symbolic_cpd_generation():

    graph = DAG(
        vertices={"A": 2, "B": 2, "C": 2},
        di_edges=[("C", "B"), ("B", "A")],
    )
    cpds, all_vars = bayesian_network.create_symbolic_cpds(graph)
    assert set(all_vars) == {
        sp.Symbol("q_C_0"),
        sp.Symbol("q_B_0_0"),
        sp.Symbol("q_B_0_1"),
        sp.Symbol("q_A_0_0"),
        sp.Symbol("q_A_0_1"),
    }
    assert cpds["A"] == SymCPD(
        "A",
        2,
        sp.Array(
            [
                [sp.Symbol("q_A_0_0"), sp.Symbol("q_A_0_1")],
                [1 - sp.Symbol("q_A_0_0"), 1 - sp.Symbol("q_A_0_1")],
            ]
        ),
        ["B"],
        [2],
    )
