import unittest

import numpy as np

import ananke
from ananke.graphs import ADMG, DAG
from ananke.identification import OptAdjustment


class TestComputeCounterfactual(unittest.TestCase):
    def test_generate_opt_adjustmen_case1(self):
        vertices = ["Q", "Z", "O", "E", "A", "M", "Y"]
        di_edges = [
            ("Q", "O"),
            ("Q", "A"),
            ("Z", "A"),
            ("Z", "E"),
            ("O", "M"),
            ("O", "Y"),
            ("E", "M"),
            ("A", "M"),
            ("M", "Y"),
        ]
        G = DAG(vertices, di_edges)
        model = OptAdjustment(G)
        result = model.generate_opt_adjustment_set("A", "Y")
        truth = {"E", "O"}
        assert truth == result

    def test_generate_opt_adjustmen_case2(self):
        vertices = ["Q", "Z", "O", "E", "A", "M", "Y", "L"]
        di_edges = [
            ("Q", "O"),
            ("Q", "A"),
            ("Z", "A"),
            ("Z", "E"),
            ("O", "M"),
            ("O", "Y"),
            ("E", "M"),
            ("A", "M"),
            ("M", "Y"),
            ("L", "M"),
            ("L", "Y"),
        ]
        G = DAG(vertices, di_edges)
        model = OptAdjustment(G)
        result = model.generate_opt_adjustment_set("A", "Y")
        truth = {"E", "O"}
        assert truth == result

    def test_generate_opt_adjustmen_case3(self):
        vertices = ["A", "C", "Y"]
        di_edges = [("A", "C"), ("Y", "C")]
        G = DAG(vertices, di_edges)
        model = OptAdjustment(G)
        result = model.generate_opt_adjustment_set("A", "Y")
        truth = []
        assert truth == result

    def test_generate_opt_adjustmen_case4(self):
        vertices = ["A", "Y"]
        di_edges = [("A", "Y")]
        G = DAG(vertices, di_edges)
        model = OptAdjustment(G)
        result = model.generate_opt_adjustment_set("A", "Y")
        assert result is None

    def test_generate_opt_adjustmen_case5(self):
        vertices = ["A", "Y", "C"]
        di_edges = [("A", "Y"), ("A", "C"), ("C", "Y")]
        G = DAG(vertices, di_edges)
        model = OptAdjustment(G)
        result = model.generate_opt_adjustment_set("A", "Y")
        assert result is None

    def test_admg_caes6(self):
        vertices = ["A", "M", "Y"]
        di_edges = [("A", "M"), ("M", "Y")]
        bi_edges = [("A", "Y")]
        G = ADMG(vertices, di_edges=di_edges, bi_edges=bi_edges)
        model = OptAdjustment(G)
        result = model.generate_opt_adjustment_set("A", "Y")
        assert result is None
