import unittest

import ananke
from ananke.graphs import DAG


class TestDAG(unittest.TestCase):
    def test_dag_can_be_initialised(self):
        di_edges = [("A", "B")]
        vertices = ["A", "B"]
        dag = DAG(vertices, di_edges=di_edges)
        self.assertTrue(DAG)
        # test empty DAG
        DAG()

    def test_dseparation_Y_graph(self):
        vertices = ["X", "Y", "Z", "D"]
        di_edges = [("X", "Y"), ("Z", "Y"), ("Y", "D")]
        G = DAG(vertices, di_edges)
        self.assertFalse(G._d_separated("X", "Z", ["D"]))

    def test_dseparation_W_graph(self):
        vertices = ["A", "B", "C", "D", "E", "F", "G", "H"]
        di_edges = [
            ("A", "B"),
            ("C", "B"),
            ("C", "E"),
            ("D", "E"),
            ("B", "F"),
            ("F", "G"),
            ("F", "H"),
        ]
        G2 = DAG(vertices, di_edges)

        self.assertFalse(G2._d_separated("A", "D", ["F", "E"]))
        self.assertTrue(G2._d_separated("A", "H", ["B"]))
        self.assertFalse(G2._d_separated("A", "C", ["H"]))

    def test_d_separation_M_graph(self):
        vertices = ["Q", "W", "E", "R", "T", "I", "O", "U", "Y"]
        di_edges = [
            ("Q", "W"),
            ("Q", "E"),
            ("E", "R"),
            ("E", "T"),
            ("T", "U"),
            ("T", "Y"),
            ("I", "T"),
            ("I", "O"),
        ]
        G3 = DAG(vertices, di_edges)

        self.assertFalse(G3._d_separated("Q", "R", ["Y"]))
        self.assertTrue(G3._d_separated("Q", "Y", ["E"]))
        self.assertFalse(G3._d_separated("E", "R", ["I", "O"]))

    def test_d_separation_sets(self):
        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("B", "C"), ("C", "D")]
        G = DAG(vertices, di_edges)

        self.assertTrue(G.d_separated("A", ["C", "D"], "B"))
        self.assertFalse(G.d_separated("A", ["C", "D"], []))

    def test_d_separation_fixed_and_random(self):
        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("B", "C"), ("C", "D")]

        G = DAG(vertices, di_edges)
        G.fix("B")

        self.assertTrue(G.d_separated("B", ["A", "D"], ["C"]))

    def test_d_separation_fixed_vertices_only(self):
        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("B", "C"), ("C", "D")]

        G = DAG(vertices, di_edges)
        G.fix(["A", "B"])

        with self.assertRaises(ananke.graphs.dag.UndefinedDAGOperation) as f:
            G.d_separated("B", ["A"], ["C"])

        print(str(f.exception))

    def test_subgraph_is_a_dag(self):
        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("B", "C"), ("C", "D")]

        G = DAG(vertices, di_edges)
        G.fix(["A", "B"])

        subgraph = G.subgraph(["A", "B"])
        assert isinstance(subgraph, DAG)


if __name__ == "__main__":
    unittest.main()
