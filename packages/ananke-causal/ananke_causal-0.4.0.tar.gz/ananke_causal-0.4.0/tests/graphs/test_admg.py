import unittest

import ananke
from ananke.graphs import ADMG, admg


class TestADMG(unittest.TestCase):
    def test_obtaining_districts(self):
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
        self.assertCountEqual(([{"C", "A"}, {"Y", "B", "D"}]), (G.districts))
        self.assertEqual({"C", "A"}, G.district("A"))

    def test_obtaining_districts_large(self):
        vertices = ["X1", "U", "X2", "A1", "A2", "Y1", "Y2"]
        di_edges = [
            ("X1", "A1"),
            ("X1", "Y1"),
            ("A1", "Y1"),
            ("X2", "A2"),
            ("X2", "Y2"),
            ("A2", "Y2"),
            ("U", "A1"),
            ("U", "Y1"),
            ("U", "A2"),
            ("U", "Y2"),
            ("A2", "Y1"),
            ("A1", "Y2"),
        ]
        bi_edges = [("X1", "U"), ("U", "X2"), ("X1", "X2"), ("Y1", "Y2")]
        G = ADMG(vertices, di_edges, bi_edges)
        self.assertCountEqual(
            ([{"X1", "X2", "U"}, {"A1"}, {"A2"}, {"Y1", "Y2"}]), (G.districts)
        )
        self.assertEqual(G.district("X2"), {"X1", "X2", "U"})

    def test_fixed(self):
        vertices = ["X_1", "X_2", "W", "Y"]
        di_edges = [("X_1", "W"), ("W", "Y"), ("X_2", "Y")]
        bi_edges = [("X_1", "W"), ("X_2", "Y"), ("X_1", "X_2")]
        G = ADMG(vertices, di_edges, bi_edges)
        G.fix(["X_1"])
        self.assertEqual(G.fixed, ["X_1"])

    def test_is_subgraph(self):
        vertices = ["X_1", "W"]
        di_edges = [
            ("X_1", "W"),
        ]
        bi_edges = [("X_1", "W")]
        G = ADMG(vertices, di_edges, bi_edges)
        G.fix(["X_1"])
        vertices = ["X_1", "X_2", "W", "Y"]
        di_edges = [("X_1", "W"), ("W", "Y"), ("X_2", "Y")]
        bi_edges = [("X_1", "W"), ("X_2", "Y"), ("X_1", "X_2")]
        G1 = ADMG(vertices, di_edges, bi_edges)
        self.assertTrue(G.is_subgraph(G1))

    def test_is_ancestral_subgraph(self):
        vertices = ["X_1", "W"]
        di_edges = [("X_1", "W")]
        bi_edges = [("X_1", "W")]
        G = ADMG(vertices, di_edges, bi_edges)
        G.fix(["X_1"])
        vertices = ["X_1", "X_2", "W", "Y"]
        di_edges = [("X_1", "W"), ("W", "Y"), ("X_2", "Y")]
        bi_edges = [("X_1", "W"), ("X_2", "Y"), ("X_1", "X_2")]
        G1 = ADMG(vertices, di_edges, bi_edges)
        G1.fix(["X_1"])
        self.assertTrue(G.is_ancestral_subgraph(G1))

        vertices = ["X_2", "W", "Y"]
        di_edges = [("W", "Y"), ("X_2", "Y")]
        bi_edges = [("X_2", "Y")]
        G = ADMG(vertices, di_edges, bi_edges)
        vertices = ["X_1", "X_2", "W", "Y"]
        di_edges = [("X_1", "W"), ("W", "Y"), ("X_2", "Y")]
        bi_edges = [("X_1", "W"), ("X_2", "Y"), ("X_1", "X_2")]
        G1 = ADMG(vertices, di_edges, bi_edges)
        G1.fix(["X_1"])
        self.assertFalse(G.is_ancestral_subgraph(G1))

    def test_subgraph(self):
        vertices = ["A", "B", "C", "D", "Y"]
        di_edges = [("A", "B"), ("C", "D")]
        bi_edges = [("A", "Y"), ("A", "C"), ("A", "B")]
        G = ADMG(vertices, di_edges, bi_edges)
        G.vertices["A"].fixed = True

        Gsub = G.subgraph(["A", "B", "Y"])
        self.assertEqual(set(["A", "B", "Y"]), set(Gsub.vertices))
        self.assertEqual(set([("A", "B")]), Gsub.di_edges)
        self.assertEqual(set([("A", "Y"), ("A", "B")]), Gsub.bi_edges)

    def test_fixing(self):
        G = ADMG(
            vertices=["A", "B", "C"],
            di_edges=[("A", "B"), ("B", "C")],
            bi_edges=[("B", "C")],
        )
        G.fix(["C"])
        self.assertTrue(("B", "C") not in G.di_edges)
        self.assertTrue(("B", "C") not in G.bi_edges)
        self.assertTrue(G.vertices["C"].fixed)

    def test_reachable_closure(self):
        vertices = ["A", "B", "C"]
        di_edges = [("A", "B"), ("C", "B"), ("C", "A")]
        bi_edges = [("A", "B")]
        G = ADMG(vertices=vertices, di_edges=di_edges, bi_edges=bi_edges)
        cl, _, _ = G.reachable_closure(["B"])
        self.assertEqual({"A", "B"}, set(cl))

    def test_marg_dag_projection(self):
        vertices = ["A", "B", "C"]
        di_edges = [("A", "B"), ("B", "C")]
        bi_edges = [("B", "C")]
        G = ADMG(vertices=vertices, di_edges=di_edges, bi_edges=bi_edges)
        marg = G.maximal_arid_projection()
        self.assertEqual(
            set([("A", "B"), ("B", "C"), ("A", "C")]), marg.di_edges
        )
        self.assertEqual(set([]), marg.bi_edges)

    def test_marg_biedge_projection(self):
        vertices = ["A", "B", "C"]
        di_edges = [("B", "A"), ("B", "C")]
        bi_edges = [("A", "B"), ("B", "C")]
        G = ADMG(vertices=vertices, di_edges=di_edges, bi_edges=bi_edges)
        marg = G.maximal_arid_projection()
        self.assertEqual(set([("B", "A"), ("B", "C")]), marg.di_edges)
        self.assertEqual(set([("A", "C")]), marg.bi_edges)

    def test_marg_4var_graph(self):
        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")]
        bi_edges = [("A", "C"), ("B", "D")]
        G = ADMG(vertices, di_edges=di_edges, bi_edges=bi_edges)
        marg = G.maximal_arid_projection()
        self.assertEqual(
            set([("A", "B"), ("B", "C"), ("C", "D"), ("A", "C")]), marg.di_edges
        )
        self.assertEqual(set([("B", "D")]), marg.bi_edges)

    def test_markov_pillow(self):
        vertices = ["A", "B", "C", "D", "Y"]
        di_edges = [("A", "B"), ("B", "C"), ("D", "C"), ("C", "Y")]
        bi_edges = [("A", "C"), ("B", "Y"), ("B", "D")]
        G = ADMG(vertices, di_edges, bi_edges)
        top_order = ["D", "A", "B", "C", "Y"]
        self.assertEqual(G.markov_pillow(["A", "D"], top_order), set())
        self.assertEqual(
            G.markov_pillow(["C"], top_order), set(["A", "B", "D"])
        )

    def test_markov_blanket(self):
        vertices = ["A", "B", "C", "D", "Y"]
        di_edges = [("A", "B"), ("B", "C"), ("D", "C"), ("C", "Y")]
        bi_edges = [("A", "C"), ("B", "Y"), ("B", "D")]
        G = ADMG(vertices, di_edges, bi_edges)
        self.assertEqual(G.markov_blanket(["A", "D"]), set(["C", "B", "Y"]))
        self.assertEqual(G.markov_blanket(["C"]), set(["A", "B", "D"]))

    def test_nps(self):
        vertices = ["Treatment", "M", "L", "Confounders", "Outcome"]
        di_edges = [
            ("Confounders", "M"),
            ("Confounders", "L"),
            ("Treatment", "M"),
            ("Treatment", "Outcome"),
            ("Treatment", "L"),
            ("M", "L"),
            ("L", "Outcome"),
        ]
        bi_edges_G1 = [
            ("Treatment", "Confounders"),
            ("M", "Outcome"),
            ("L", "Outcome"),
        ]
        bi_edges_G2 = [("Treatment", "Confounders"), ("M", "Outcome")]

        G1 = ADMG(vertices, di_edges, bi_edges_G1)
        G2 = ADMG(vertices, di_edges, bi_edges_G2)

        self.assertTrue(G1.nonparametric_saturated())
        self.assertFalse(G2.nonparametric_saturated())

        vertices = ["A", "B", "C"]
        di_edges = [("B", "A"), ("B", "C")]
        bi_edges = [("A", "B"), ("C", "B")]
        G3 = ADMG(vertices, di_edges, bi_edges)

        self.assertTrue(G3.nonparametric_saturated())

    def test_mseparation_chain(self):
        vertices = ["A", "B", "C", "D", "E"]
        di_edges = [("E", "D")]
        bi_edges = [("A", "B"), ("B", "C"), ("C", "D")]
        G = ADMG(vertices, di_edges, bi_edges)

        self.assertFalse(G._m_separated("A", "B", ["D"]))
        self.assertFalse(G._m_separated("A", "B", ["E"]))
        self.assertTrue(G._m_separated("A", "D", ["C"]))
        self.assertTrue(G._m_separated("A", "E", ["B", "C"]))

    def test_m_separation_fixed(self):
        vertices = ["A", "B", "C", "D", "E"]
        di_edges = [("A", "B"), ("C", "E")]
        bi_edges = [("B", "D"), ("D", "E")]
        G2 = ADMG(vertices, di_edges, bi_edges)
        G2.fix("A")
        G2.fix("C")

        self.assertFalse(G2.m_separated("A", "D", ["B"]))
        self.assertFalse(G2.m_separated("A", "B", ["E"]))

    def test_m_separation_no_bidirected(self):
        vertices = ["A", "B", "C", "D", "E"]
        di_edges = [("A", "B"), ("C", "D"), ("D", "E"), ("D", "B")]
        bi_edges = []
        G3 = ADMG(vertices, di_edges, bi_edges)

        self.assertTrue(G3._m_separated("C", "B", ["D"]))
        self.assertFalse(G3._m_separated("A", "B", ["C"]))
        self.assertFalse(G3._m_separated("A", "D", ["B"]))

    def test_m_separation_simple(self):
        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("D", "C")]
        bi_edges = [("B", "C")]
        G4 = ADMG(vertices, di_edges, bi_edges)

        self.assertTrue(G4._m_separated("A", "D", []))
        self.assertFalse(G4._m_separated("A", "D", ["B", "C"]))
        self.assertFalse(G4._m_separated("A", "C", ["B"]))

    def test_m_separation_sets(self):
        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("B", "C"), ("C", "D")]
        bi_edges = [("A", "B")]
        G4 = ADMG(vertices, di_edges, bi_edges)
        self.assertTrue(G4.m_separated(["A", "B"], ["D"], ["C"]))
        self.assertFalse(G4.m_separated("A", ["B", "D"], ["C"]))

    def test_m_separation_undefined(self):
        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("B", "C"), ("C", "D")]
        bi_edges = [("A", "B")]
        G4 = ADMG(vertices, di_edges, bi_edges)
        G4.fix(["A", "D"])
        with self.assertRaises(ananke.graphs.admg.UndefinedADMGOperation) as f:
            G4.m_separated("A", "D")

    def test_m_separation_fixed_vertices(self):
        vertices = ["A", "B", "C", "D", "E"]
        di_edges = [("A", "C"), ("C", "E"), ("D", "E"), ("B", "D")]
        bi_edges = []
        G4 = ADMG(vertices, di_edges, bi_edges)
        G4.fix(["A", "B"])

        self.assertTrue(G4.m_separated("C", "D"))

    def test_m_separation_fixed_vertices_complicated(self):
        vertices = ["A", "B", "C", "D"]
        di_edges = [("B", "C"), ("C", "D")]
        bi_edges = [("A", "D"), ("A", "C")]
        G = ADMG(vertices, di_edges, bi_edges)
        G.fix("B")

        self.assertTrue(G.m_separated("B", "D", ["C"]))
        self.assertFalse(G.m_separated("B", "D", ["C", "A"]))

    def test_latent_projection(self):
        vertices = ["A", "B", "C"]
        di_edges = [("A", "B"), ("B", "C")]
        G = ADMG(vertices, di_edges, list())

        G1 = G.latent_projection(retained_vertices=["A", "C"])

        assert sorted(list(G1.vertices)) == sorted(["A", "C"])
        assert G1.di_edges == {("A", "C")}
        assert G1.bi_edges == set()

        vertices = ["A", "B", "C"]
        di_edges = [("B", "A"), ("B", "C")]
        G = ADMG(vertices, di_edges, list())

        G2 = G.latent_projection(["A", "C"])

        assert sorted(list(G2.vertices)) == sorted(["A", "C"])
        assert G2.di_edges == set()
        assert G2.bi_edges == {("A", "C")}

        vertices = ["A", "B", "C", "D", "E"]
        di_edges = [("B", "A"), ("B", "C"), ("D", "C"), ("D", "E")]
        G = ADMG(vertices, di_edges, list())

        G3 = G.latent_projection(["A", "C", "E"])

        assert G3.bi_edges == {("A", "C"), ("C", "E")}

        vertices = ["A", "B", "C", "D", "E", "F"]
        di_edges = [
            ("C", "A"),
            ("C", "D"),
            ("B", "A"),
            ("B", "D"),
            ("E", "F"),
            ("F", "D"),
        ]
        bi_edges = [("A", "E")]
        G = ADMG(vertices, di_edges, bi_edges)

        G4 = G.latent_projection(["A", "D", "F"])

        assert G4.bi_edges == {("A", "F"), ("A", "D")}

    def test_canonical_dag(self):
        vertices = ["A", "B", "C"]
        di_edges = [("B", "A"), ("B", "C")]
        bi_edges = [("B", "A"), ("B", "C")]
        G = ADMG(vertices, di_edges, bi_edges)

        G_canonical = G.canonical_dag()

        assert set(G_canonical.vertices) == {"A", "B", "C", "U_A_B", "U_B_C"}
        assert G_canonical.bi_edges == set()


if __name__ == "__main__":
    unittest.main()
