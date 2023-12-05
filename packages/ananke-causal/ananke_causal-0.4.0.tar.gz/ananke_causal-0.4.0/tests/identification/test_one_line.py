import copy
import itertools
import unittest

import numpy as np
import pytest
import sympy as sp
from numpy.testing import assert_array_equal
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

from ananke import identification
from ananke.graphs import ADMG, DAG, Vertex
from ananke.inference.variable_elimination import variable_elimination
from ananke.models import BayesianNetwork, create_symbolic_cpds


class TestOneLine(unittest.TestCase):
    def test_id_graph(self):
        """
        Test that ADMG Y(a) is identified
        """

        vertices = ["A", "B", "C", "D", "Y"]
        di_edges = [
            ("A", "B"),
            ("A", "D"),
            ("B", "C"),
            ("C", "Y"),
            ("B", "D"),
            ("D", "Y"),
        ]
        bi_edges = [("A", "C"), ("B", "Y"), ("B", "D")]
        G = ADMG(vertices, di_edges, bi_edges)
        one_id = identification.OneLineID(G, ["A"], ["Y"])
        one_id.draw_swig()
        self.assertTrue(one_id.id())
        self.assertEqual({"Y", "C", "D", "B"}, one_id.ystar)
        one_id.export_intermediates()

    def test_BMAY_graph(self):
        vertices = ["B", "M", "A", "Y"]
        di_edges = [("B", "M"), ("M", "A"), ("A", "Y")]
        bi_edges = [("B", "A"), ("B", "Y")]
        G = ADMG(vertices, di_edges, bi_edges)
        one_id = identification.OneLineID(G, ["A"], ["Y"])
        one_id.draw_swig()
        self.assertTrue(one_id.id())

    def test_two_var_id_graph(self):
        vertices = ["A", "D", "C", "Y"]
        di_edges = [("D", "Y"), ("D", "A"), ("A", "Y"), ("C", "A"), ("C", "Y")]
        bi_edges = []
        G = ADMG(vertices, di_edges, bi_edges)
        one_id = identification.OneLineID(G, ["A"], ["Y", "D"])
        self.assertEqual({"C", "D", "Y"}, one_id.ystar)
        self.assertTrue(one_id.id())

    def test_non_id_graph(self):
        """
        Test that Y(a,b) is not identified
        """

        # non ID test
        vertices = ["A", "B", "C", "D", "Y"]
        di_edges = [
            ("A", "B"),
            ("A", "D"),
            ("B", "C"),
            ("C", "Y"),
            ("B", "D"),
            ("D", "Y"),
        ]
        bi_edges = [("A", "C"), ("B", "Y"), ("B", "D")]
        G = ADMG(vertices, di_edges, bi_edges)
        one_id = identification.OneLineID(G, ["A", "B"], ["Y"])
        self.assertFalse(one_id.id())

    def test_functional(self):
        vertices = ["M", "A", "Y"]
        di_edges = [("A", "M"), ("M", "Y")]
        bi_edges = [("A", "Y")]
        G = ADMG(vertices, di_edges, bi_edges)
        one_id = identification.OneLineID(G, ["A"], ["Y"])
        functional = one_id.functional()
        self.assertEqual("ΣM ΦAY(p(V);G) ΦAM(p(V);G) ", functional)

    def test_id_after_fixing_fails_properly(self):
        vertices = ["X1", "X2", "W", "Y"]
        di_edges = [("X1", "W"), ("W", "Y"), ("X2", "Y")]
        bi_edges = [("X1", "X2"), ("X1", "W"), ("X2", "Y")]
        G = ADMG(vertices, di_edges=di_edges, bi_edges=bi_edges)
        G.fix(["X1"])

        # This should not be identified as X_2 -> Y <-> X_2 is a bow-arc graph
        self.assertFalse(
            identification.OneLineID(G, treatments=["X2"], outcomes=["Y"]).id()
        )

        # Check that NotIdentifiedError is raised if we try to obtain functional
        with self.assertRaises(identification.NotIdentifiedError):
            identification.OneLineID(
                G, treatments=["X2"], outcomes=["Y"]
            ).functional()

    def test_id_fails_correctly(self):

        vertices = ["X1", "X2", "W", "Y"]
        di_edges = [("X1", "W"), ("W", "Y"), ("X2", "Y")]
        bi_edges = [("X1", "X2"), ("X1", "W"), ("X2", "Y")]
        G = ADMG(vertices, di_edges=di_edges, bi_edges=bi_edges)
        G.fix(["X1"])

        # This should not be identified as X_2 -> Y <-> X_2 is a bow-arc graph
        self.assertFalse(
            identification.OneLineID(G, treatments=["X2"], outcomes=["Y"]).id()
        )

        # Check that NotIdentifiedError is raised if we try to obtain functional
        with self.assertRaises(identification.NotIdentifiedError):
            identification.OneLineID(
                G, treatments=["X2"], outcomes=["Y"]
            ).functional()


class TestOneLineGID(unittest.TestCase):
    def test_is_id(self):
        vertices = ["X_1", "X_2", "W", "Y"]
        di_edges = [("X_1", "W"), ("W", "Y"), ("X_2", "Y")]
        bi_edges = [("X_1", "W"), ("X_2", "Y"), ("X_1", "X_2")]
        G = ADMG(vertices, di_edges, bi_edges)
        interventions = ["X_1", "X_2"]
        outcomes = ["Y"]
        ol = identification.OneLineGID(G, interventions, outcomes)
        status = ol.id()

        self.assertFalse(status)

        experiments = [G.copy().fix("X_1"), G.copy().fix("X_2")]
        second = ol.id(experiments)
        self.assertTrue(second)

    def test_functional(self):
        vertices = ["X_1", "X_2", "W", "Y"]
        di_edges = [("X_1", "W"), ("W", "Y"), ("X_2", "Y")]
        bi_edges = [("X_1", "W"), ("X_2", "Y"), ("X_1", "X_2")]
        G = ADMG(vertices, di_edges, bi_edges)
        interventions = ["X_1", "X_2"]
        outcomes = ["Y"]
        ol = identification.OneLineGID(G, interventions, outcomes)
        functional = ol.functional([G.copy().fix("X_1"), G.copy().fix("X_2")])
        self.assertEqual(
            "ΣW ΦX_2,Y p(W,X_2,Y | do(X_1))ΦX_1,W p(W,X_1,Y | do(X_2))",
            functional,
        )

    def test_is_id_chain(self):
        vertices = ["A", "X", "W", "Y"]
        di_edges = [("A", "X"), ("X", "W"), ("W", "Y")]
        bi_edges = [("X", "W"), ("W", "Y")]
        G = ADMG(vertices, di_edges, bi_edges)
        interventions = ["A"]
        outcomes = ["Y"]
        ol = identification.OneLineGID(G, interventions, outcomes)
        status = ol.id([G.copy().fix(["A", "X"]), G.copy().fix({"A", "Y"})])
        self.assertFalse(status)

        vertices = ["A", "X", "Y"]
        di_edges = [("A", "X"), ("X", "Y")]
        bi_edges = [("X", "Y")]
        G = ADMG(vertices, di_edges, bi_edges)
        interventions = ["A"]
        outcomes = ["Y"]
        ol = identification.OneLineGID(G, interventions, outcomes)
        status = ol.id([G.copy().fix({"A", "X"}), G.copy().fix({"A", "Y"})])
        self.assertFalse(status)

        vertices = ["A", "W", "Y"]
        di_edges = [("A", "W"), ("W", "Y")]
        bi_edges = [("A", "W"), ("W", "Y")]
        G = ADMG(vertices, di_edges, bi_edges)
        interventions = ["A"]
        outcomes = ["Y"]
        ol = identification.OneLineGID(G, interventions, outcomes)
        status = ol.id([G.copy().fix({"A"}), G.copy().fix({"A", "Y"})])
        self.assertTrue(status)

    def test_that_gid_is_correct(self):
        vertices = ["X1", "X2", "W", "Y"]
        di_edges = [("X1", "W"), ("W", "Y"), ("X2", "Y")]
        bi_edges = [("X1", "X2"), ("X1", "W"), ("X2", "Y")]
        G = ADMG(vertices, di_edges, bi_edges)

        G1 = ADMG(vertices, di_edges, bi_edges)
        G1.fix(["X1"])

        G2 = ADMG(vertices, di_edges, bi_edges)
        G2.fix(["X2"])
        result = identification.OneLineGID(
            graph=G, treatments=["X1", "X2"], outcomes=["Y"]
        ).id(experiments=[G1, G2])


class TestOnelineAID(unittest.TestCase):
    def test_oneline_aid(self):
        vertices = ["X1", "X2", "W", "Y"]
        di_edges = [("X1", "W"), ("W", "Y"), ("X2", "Y")]
        bi_edges = [("X1", "X2"), ("X1", "W"), ("X2", "Y")]
        G = ADMG(vertices, di_edges, bi_edges)

        vertices = ["X1", "W"]
        di_edges = [("X1", "W")]
        bi_edges = [("X1", "W")]
        G1 = ADMG(vertices, di_edges, bi_edges)
        G1.fix(["X1"])

        vertices = ["X1", "X2", "W", "Y"]
        di_edges = [("X1", "W"), ("W", "Y"), ("X2", "Y")]
        bi_edges = [("X1", "X2"), ("X1", "W"), ("X2", "Y")]
        G2 = ADMG(vertices, di_edges, bi_edges)
        G2.fix(["X2"])

        interventions = ["X1", "X2"]
        outcomes = ["Y"]
        ol = identification.OneLineAID(G, interventions, outcomes)

        experiments = [G1, G2]

        self.assertTrue(ol.id(experiments=experiments))
        self.assertEqual(
            "ΣW  p(W | do(X1))ΦX1,W p(W,X1,Y | do(X2))",
            ol.functional(experiments),
        )


class TestValidWitness:
    def test_ananke_witness(self, bow_arc_bayesian_network_models):
        net_1, net_2 = bow_arc_bayesian_network_models
        identification.one_line.assert_valid_witness(
            net_1, net_2, ["Y", "A"], {"A": 0}, ["Y"]
        )

    def test_pgmpy_witness(self, bow_arc_bayesian_network_models):
        net_1, net_2 = bow_arc_bayesian_network_models
        net_1 = net_1.to_pgmpy()
        net_2 = net_2.to_pgmpy()
        identification.one_line.assert_valid_witness(
            net_1, net_2, ["Y", "A"], {"A": 0}, ["Y"]
        )
