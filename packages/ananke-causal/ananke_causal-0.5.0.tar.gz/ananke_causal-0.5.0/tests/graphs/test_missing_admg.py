import unittest

from ananke.graphs import MissingADMG


class TestMissingADMG(unittest.TestCase):
    def test_draw_missing_admg(self):
        vertices = ["X_1", "Xp_1", "R_1", "X_2", "Xp_2", "R_2"]
        di_edges = [("R_1", "R_2"), ("X_1", "X_2")]

        G = MissingADMG(vertices=vertices, di_edges=di_edges)

        # check that no errors come up
        draw = G.draw()
