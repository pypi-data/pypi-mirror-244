import unittest

from ananke.graphs import CG


class TestCG(unittest.TestCase):
    def test_cg_boundary(self):
        vertices = ["X_1", "X_2", "X_3", "X_4"]
        di_edges = [("X_1", "X_2")]
        ud_edges = [("X_2", "X_3")]
        G = CG(vertices=vertices, di_edges=di_edges, ud_edges=ud_edges)

        boundary = G.boundary(["X_2"])

        self.assertEqual(boundary, {"X_1", "X_3"})
