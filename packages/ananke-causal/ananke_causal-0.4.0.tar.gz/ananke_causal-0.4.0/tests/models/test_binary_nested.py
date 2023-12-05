"""
The code relies on the following papers:

[ER12] Evans, R. J., & Richardson, T. S. (2012). Maximum likelihood fitting of acyclic directed mixed graphs to binary data. arXiv preprint arXiv:1203.3479.
[ER19] Evans, R. J., & Richardson, T. S. (2019). Smooth, identifiable supermodels of discrete DAG models with latent variables. Bernoulli, 25(2), 848-876.

"""
import unittest
from collections import OrderedDict

import numpy as np
import pandas as pd
import pytest
from scipy.special import expit

from ananke.datasets import load_wisconsin_health_study
from ananke.graphs import ADMG, DAG
from ananke.models import binary_nested


def dag_chain_small():
    vertices = ["X_1", "X_2"]
    di_edges = [("X_1", "X_2")]
    G = DAG(di_edges=di_edges, vertices=vertices)

    return G


def wisconsin_fig8b_graph():
    G = ADMG(
        vertices=["X", "E", "M", "Y"],
        di_edges=[("X", "E"), ("E", "M"), ("X", "Y")],
        bi_edges=[("E", "Y")],
    )

    return G


def sixteen_not_eighteen_graph():
    vertices = ["A", "B", "C", "D", "E"]
    di_edges = [("A", "B"), ("B", "C"), ("C", "D")]
    bi_edges = [("E", "D"), ("B", "E")]

    G = ADMG(di_edges=di_edges, bi_edges=bi_edges, vertices=vertices)

    return G


def standard_graph():
    """
    Fig 1 from [ER12]
    :return:
    """
    vertices = ["X1", "X2", "X3", "X4"]
    di_edges = [("X1", "X2"), ("X2", "X4")]
    bi_edges = [("X3", "X2"), ("X3", "X4")]
    G = ADMG(di_edges=di_edges, bi_edges=bi_edges, vertices=vertices)

    return G


def standard_dag():
    vertices = ["X1", "X2", "X3", "X4"]
    di_edges = [("X1", "X2"), ("X2", "X3"), ("X3", "X4")]
    bi_edges = list()
    G = ADMG(di_edges=di_edges, bi_edges=bi_edges, vertices=vertices)

    return G


def fig1b_graph():
    """
     Fig 1b from [ER19]

    :return:
    """
    vertices = ["X", "E", "M", "Y"]
    di_edges = [("X", "E"), ("E", "M"), ("M", "Y")]
    bi_edges = [("E", "Y")]
    G = ADMG(di_edges=di_edges, bi_edges=bi_edges, vertices=vertices)

    return G


def fig2_graph():
    """
    Fig 2 from [ER19]

    :return:
    """
    vertices = ["X1", "X2", "X3", "X4"]
    di_edges = [("X1", "X3"), ("X2", "X4")]
    bi_edges = [("X1", "X4"), ("X2", "X3")]
    G = ADMG(di_edges=di_edges, bi_edges=bi_edges, vertices=vertices)

    return G


def fig3_graph():
    """
    Fig 3 from [ER12]

    :return:
    """
    vertices = ["X1", "X2", "X3"]
    di_edges = [("X1", "X2")]
    bi_edges = [("X3", "X2"), ("X1", "X3")]
    G = ADMG(di_edges=di_edges, bi_edges=bi_edges, vertices=vertices)

    return G


def fig7_graph():
    """
    Fig 7 from [ER19]
    :return:
    """
    vertices = ["2", "3", "4", "5"]
    di_edges = [("2", "3"), ("3", "4")]
    bi_edges = [("2", "5"), ("5", "4")]
    G = ADMG(di_edges=di_edges, bi_edges=bi_edges, vertices=vertices)

    return G


def fig8_graph(k=5):
    """
    Fig 8 from [ER12]
    :param k:
    :return:
    """
    vertices = ["X{}".format(i) for i in range(k)] + [
        "Y{}".format(i) for i in range(k)
    ]
    di_edges = [("X{}".format(i), "Y{}".format(i)) for i in range(k)]
    bi_edges = [
        ("Y{}".format(i), "Y{}".format(i + 1)) for i in range(k - 1)
    ] + [("X{}".format(i), "X{}".format(i + 1)) for i in range(k - 1)]
    G = ADMG(di_edges=di_edges, bi_edges=bi_edges, vertices=vertices)

    return G


def verma_graph(k=5):
    """
    Non-ancestral graph containing Verma constraints
    :param k:
    :return:
    """
    vertices = (
        ["A", "Y"]
        + ["L{}".format(i) for i in range(k)]
        + ["B{}".format(i) for i in range(k)]
    )
    di_edges = (
        [("A", "L0")]
        + [("L{}".format(i), "B{}".format(i)) for i in range(k)]
        + [("B{}".format(i), "Y") for i in range(k)]
    )
    bi_edges = [("L{}".format(i), "Y") for i in range(k)] + [
        ("B{}".format(i), "L{}".format(i + 1)) for i in range(k - 1)
    ]

    G = ADMG(di_edges=di_edges, bi_edges=bi_edges, vertices=vertices)

    return G


def conditional_ignorability_graph():

    vertices = ["A", "C", "Y"]
    di_edges = [("C", "A"), ("C", "Y"), ("A", "Y")]
    G = DAG(di_edges=di_edges, vertices=vertices)

    return G


class TestBinaryNested(unittest.TestCase):
    def test_permutation(self):
        """
        Check that permutation helper function is correct.

        :return:
        """
        result = binary_nested.permutations(2, k=2)
        expected = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.assertEqual(expected, result)
        result = binary_nested.permutations(2, k=3)
        expected = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        ]
        self.assertEqual(expected, result)

    def test_recursive_partition_heads(self):
        """
        Check that recursive partition heads are correctly formed.

        :return:
        """
        G_1 = standard_graph()
        intrinsic_dict, fixing_orders = G_1.get_intrinsic_sets_and_heads()
        heads = binary_nested.recursive_partition_heads(
            {"X1", "X2"}, intrinsic_dict
        )
        self.assertEqual({frozenset({"X2"}), frozenset({"X1"})}, heads)
        heads = binary_nested.recursive_partition_heads(
            {"X3", "X4"}, intrinsic_dict
        )
        self.assertEqual({frozenset({"X3", "X4"})}, heads)

        G_2 = fig1b_graph()
        intrinsic_dict, fixing_orders = G_2.get_intrinsic_sets_and_heads()
        heads = binary_nested.recursive_partition_heads(
            {"X", "E", "Y"}, intrinsic_dict
        )
        self.assertEqual({frozenset({"X"}), frozenset({"E", "Y"})}, heads)
        heads = binary_nested.recursive_partition_heads(
            {"M", "Y"}, intrinsic_dict
        )
        self.assertEqual({frozenset({"M"}), frozenset({"Y"})}, heads)

    def test_maximal_heads(self):
        """
        Check that maximal heads function correctly extracts the maximal head
        :return:
        """
        G = fig1b_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        result = binary_nested.maximal_heads(
            {frozenset({"E"}), frozenset({"E", "Y"})}, intrinsic_dict
        )
        self.assertEqual([frozenset({"Y", "E"})], result)

    def test_q_vector(self):
        """
        Test that q_vector initializes parameters with keys in the expected order. Also checks that the values are
        initialized to represent full independence.

        :return:
        """
        G = fig1b_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        result = binary_nested.initialize_q_vector(intrinsic_dict)
        self.assertIn((frozenset({"E", "Y"}), ("M", "X"), (0, 1)), result)
        self.assertNotIn((frozenset({"E", "Y"}), ("X", "M"), (1, 0)), result)
        expected_keys = [
            (frozenset({"E"}), ("X",), (0,)),
            (frozenset({"E"}), ("X",), (1,)),
            (frozenset({"E", "Y"}), ("M", "X"), (0, 0)),
            (frozenset({"E", "Y"}), ("M", "X"), (0, 1)),
            (frozenset({"E", "Y"}), ("M", "X"), (1, 0)),
            (frozenset({"E", "Y"}), ("M", "X"), (1, 1)),
            (frozenset({"M"}), ("E",), (0,)),
            (frozenset({"M"}), ("E",), (1,)),
            (frozenset({"X"}), (), ()),
            (frozenset({"Y"}), ("M",), (0,)),
            (frozenset({"Y"}), ("M",), (1,)),
        ]

        self.assertEqual(expected_keys, list(result.keys()))

        self.assertAlmostEqual(
            result[(frozenset({"E", "Y"}), ("M", "X"), (1, 1))], 0.25
        )
        self.assertAlmostEqual(result[(frozenset({"Y"}), ("M",), (1,))], 0.5)

    def test_heads_tails_map(self):
        G = fig1b_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        result = binary_nested.get_heads_tails_map(intrinsic_dict)
        self.assertEqual(result[frozenset({"Y", "E"})], ("M", "X"))

    def test_compute_likelihood_district(self):
        """
        Example 1 from [ER12]

        :return:
        """
        G = standard_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        q_vector = binary_nested.initialize_q_vector(intrinsic_dict)
        heads_tails_map = binary_nested.get_heads_tails_map(
            intrinsic_dict=intrinsic_dict
        )

        nu_dict = {"X1": 1, "X2": 1, "X3": 0, "X4": 1}
        lld_value = 1
        for D_j in G.districts:
            # send nu_dict as a dictionary : if you dont want the input that way, include a line to map vector nu to the values in nu_dict
            # nu_dict always contains all vertices V - don't change according to district
            lld_value *= binary_nested.compute_likelihood_district(
                nu_dict, q_vector, D_j, heads_tails_map, intrinsic_dict
            )

        expected = (1 - q_vector[(frozenset({"X1"}), (), ())]) * (
            q_vector[(frozenset({"X3"}), (), ())]
            - q_vector[(frozenset({"X2", "X3"}), ("X1",), (1,))]
            - q_vector[(frozenset({"X3", "X4"}), ("X1", "X2"), (1, 1))]
            + q_vector[(frozenset({"X3", "X4"}), ("X1", "X2"), (1, 1))]
            * q_vector[(frozenset({"X2"}), ("X1",), (1,))]
        )

        self.assertAlmostEqual(expected, lld_value)

    def test_compute_terms(self):
        """
        Check that the terms (product of various q parameters) are computed correctly. These are represented by tuples
        consisting of (all heads, all tails, value of all tails).

        :return:
        """
        G = fig3_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        heads_tails_map = binary_nested.get_heads_tails_map(
            intrinsic_dict=intrinsic_dict
        )
        for D_j in G.districts:
            result = binary_nested.compute_terms(
                D_j, intrinsic_dict, heads_tails_map
            )

            expected = [
                (frozenset(), (), ()),
                (frozenset({"X1"}), (), ()),
                (frozenset({"X2"}), ("X1",), (0,)),
                (frozenset({"X2"}), ("X1",), (1,)),
                (frozenset({"X2", "X1"}), ("X1",), (0,)),
                (frozenset({"X2", "X1"}), ("X1",), (1,)),
                (frozenset({"X3"}), (), ()),
                (frozenset({"X3", "X1"}), (), ()),
                (frozenset({"X2", "X3"}), ("X1",), (0,)),
                (frozenset({"X2", "X3"}), ("X1",), (1,)),
                (frozenset({"X2", "X3", "X1"}), ("X1",), (0,)),
                (frozenset({"X2", "X3", "X1"}), ("X1",), (1,)),
            ]
            self.assertEqual(expected, result)

    def test_compute_M(self):
        """
        Check form of M matrix as shown in [ER12] is correct for provided example graph

        :return:
        """
        G = fig3_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        heads_tails_map = binary_nested.get_heads_tails_map(
            intrinsic_dict=intrinsic_dict
        )
        for D_j in G.districts:
            terms = binary_nested.compute_terms(
                D_j, intrinsic_dict, heads_tails_map
            )
            partition_head_dict = binary_nested.compute_partition_head_dict(
                intrinsic_dict=intrinsic_dict, district=D_j
            )
            result = binary_nested.compute_M(
                G=G,
                partition_head_dict=partition_head_dict,
                district=D_j,
                heads_tails_map=heads_tails_map,
                terms=terms,
            )
        ix = binary_nested.permutations(3).index((1, 0, 1))
        expected = OrderedDict(
            [
                ((frozenset(), (), ()), 0),
                ((frozenset({"X1"}), (), ()), 0),
                ((frozenset({"X2"}), ("X1",), (0,)), 0),
                ((frozenset({"X2"}), ("X1",), (1,)), 1),
                ((frozenset({"X2", "X1"}), ("X1",), (0,)), 0),
                ((frozenset({"X2", "X1"}), ("X1",), (1,)), -1),
                ((frozenset({"X3"}), (), ()), 0),
                ((frozenset({"X3", "X1"}), (), ()), 0),
                ((frozenset({"X3", "X2"}), ("X1",), (0,)), 0),
                ((frozenset({"X3", "X2"}), ("X1",), (1,)), -1),
                ((frozenset({"X2", "X3", "X1"}), ("X1",), (0,)), 0),
                ((frozenset({"X2", "X3", "X1"}), ("X1",), (1,)), 1),
            ]
        )

        self.assertEqual(list(expected.values()), result[ix, :].tolist())
        self.assertEqual(result.shape, (2 ** len(G.vertices), len(terms)))

    def test_compute_P(self):
        """
        Check form of P matrix as shown in [ER12] is correct for provided example graph

        :return:
        """
        G = fig3_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        heads_tails_map = binary_nested.get_heads_tails_map(
            intrinsic_dict=intrinsic_dict
        )
        q_vector = binary_nested.initialize_q_vector(intrinsic_dict)
        # Loops over the whole graph which is a single district
        for D_j in G.districts:
            terms = binary_nested.compute_terms(
                D_j, intrinsic_dict, heads_tails_map
            )
            partition_head_dict = binary_nested.compute_partition_head_dict(
                intrinsic_dict=intrinsic_dict, district=D_j
            )
            result = binary_nested.compute_P(
                partition_head_dict=partition_head_dict,
                q_vector_keys=q_vector,
                heads_tails_map=heads_tails_map,
                terms=terms,
            )

            expected = [1, 0, 0, 0, 0, 1, 0]
            ix = terms.index((frozenset({"X1", "X2", "X3"}), ("X1",), (1,)))
            self.assertEqual(result[ix, :].tolist(), expected)
            self.assertEqual(result.shape, (len(terms), len(q_vector)))

    def test_compute_P_Q_sums_to_1(self):
        """
        Check that the property that probabilities obtained after transformation of q parameters sum to one.
        Note that this property is guaranteed by the correct form of the transformation, and applies to all choices of
        q. However, it is not guaranteed that the probabilities are non-negative.

        :return:
        """
        G = fig2_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        heads_tails_map = binary_nested.get_heads_tails_map(
            intrinsic_dict=intrinsic_dict
        )
        q_vector = binary_nested.initialize_q_vector(intrinsic_dict)
        prob = 1
        for D_j in G.districts:
            terms = binary_nested.compute_terms(
                D_j, intrinsic_dict, heads_tails_map
            )
            partition_head_dict = binary_nested.compute_partition_head_dict(
                intrinsic_dict=intrinsic_dict, district=D_j
            )
            M = binary_nested.compute_M(
                G=G,
                partition_head_dict=partition_head_dict,
                district=D_j,
                heads_tails_map=heads_tails_map,
                terms=terms,
            )
            P = binary_nested.compute_P(
                partition_head_dict=partition_head_dict,
                q_vector_keys=q_vector,
                heads_tails_map=heads_tails_map,
                terms=terms,
            )

            self.assertEqual(M.shape, (2 ** len(G.vertices), len(terms)))
            self.assertEqual(P.shape, (len(terms), len(q_vector)))

            prob *= M @ np.exp(P @ np.log(np.array(list(q_vector.values()))))

        # Initialized q_vector is not guaranteed to satisfy constraints (and thus be within [0,1]), but vector of probs will sum to 1
        self.assertAlmostEqual(1, np.sum(prob))

    def test_a_y1_y2_graph(self):
        """
        Check that q(A) is a parameter prior to fixing, but not after.

        :return:
        """
        vertices = ["A", "Y1", "Y2"]
        di_edges = [("A", "Y1")]
        bi_edges = [("Y1", "Y2"), ("A", "Y1")]
        G = ADMG(di_edges=di_edges, bi_edges=bi_edges, vertices=vertices)
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()

        q_vector = binary_nested.initialize_q_vector(intrinsic_dict)

        self.assertTrue((frozenset({"A"}), (), ()) in q_vector)

        G.fix("A")

        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()

        q_vector = binary_nested.initialize_q_vector(intrinsic_dict)
        self.assertTrue((frozenset({"A"}), (), ()) not in q_vector)

    def test_compute_prob(self):
        """

        :return:
        """
        G = fig2_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        q_vector = binary_nested.initialize_q_vector(intrinsic_dict)
        districts = G.districts
        Ms, Ps = binary_nested.compute_all_M_and_P(
            G=G, intrinsic_dict=intrinsic_dict
        )

        q_indices = binary_nested.compute_q_indices_by_district(
            q_vector_keys=list(q_vector.keys()), districts=districts
        )

        prob = binary_nested._compute_prob(
            q=np.array(list(q_vector.values())),
            q_indices=q_indices,
            districts=districts,
            Ms=Ms,
            Ps=Ps,
        )
        self.assertAlmostEqual(1, np.sum(prob))

    def test_compute_q_constraint_from_A_b_matrices(self):
        """
        Test that the A and b matrices are constructed correctly

        :return:
        """
        G = fig3_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        heads_tails_map = binary_nested.get_heads_tails_map(
            intrinsic_dict=intrinsic_dict
        )
        q_vector = binary_nested.initialize_q_vector(intrinsic_dict)
        for D_j in G.districts:
            terms = binary_nested.compute_terms(
                D_j, intrinsic_dict, heads_tails_map
            )

            partition_head_dict = binary_nested.compute_partition_head_dict(
                intrinsic_dict=intrinsic_dict, district=D_j
            )

            M = binary_nested.compute_M(
                G=G,
                partition_head_dict=partition_head_dict,
                district=D_j,
                heads_tails_map=heads_tails_map,
                terms=terms,
            )
            # Select q parameters whose heads are in district D_j
            new_q = OrderedDict(
                [(k, v) for k, v in q_vector.items() if set(k[0]).issubset(D_j)]
            )
            P = binary_nested.compute_P(
                partition_head_dict=partition_head_dict,
                q_vector_keys=new_q,
                heads_tails_map=heads_tails_map,
                terms=terms,
            )

            variable = "X2"
            variables = list(G.vertices)
            keys = list(q_vector.keys())
            theta_bool_map = {
                v: np.array(
                    [
                        True if v in item[0] else False
                        for i, item in enumerate(keys)
                    ]
                )
                for v in variables
            }
            A, b = binary_nested.construct_A_b(
                variable=variable,
                q=np.array(list(q_vector.values())),
                theta_reindexed_bool_map=theta_bool_map,
                M=M,
                P=P,
            )

            # We check the row 5 corresponding to state 101.
            # This should have A[5, :] = [0, 1-q_1, 0, -1 + q_1] and b[5] = 0

            np.testing.assert_array_almost_equal(
                A[5, :],
                np.array(
                    [
                        0,
                        1 - q_vector[(frozenset({"X1"}), (), ())],
                        0,
                        -1 + q_vector[(frozenset({"X1"}), (), ())],
                    ]
                ),
            )

            self.assertAlmostEqual(b[5], 0)

    def test_that_p_align_from_partial_likelihood_and_prob(self):
        """
        Checks that the probabilities obtained from the full probability function aligns with the method used to compute
        partial probabilities, at the same q value, for multiple districts


        :return:
        """

        G = fig2_graph()

        variables = list(G.vertices)
        districts = [frozenset(x) for x in G.districts]
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        q_vector = binary_nested.initialize_q_vector(intrinsic_dict)
        q = np.array(list(q_vector.values()))
        Ms, Ps = binary_nested.compute_all_M_and_P(
            G=G, intrinsic_dict=intrinsic_dict
        )
        district_bool_map = binary_nested.compute_district_bool_map(
            q_vector_keys=list(q_vector.keys()), districts=districts
        )
        Ms_map = dict(zip(districts, Ms))
        Ps_map = dict(zip(districts, Ps))

        for D_j in districts:
            M = Ms_map[D_j]
            P = Ps_map[D_j]

            for variable in sorted(D_j):
                # problem:
                # theta_bool_map maps variable to set of params
                # M and P map district to set of params
                keys = list(q_vector.keys())
                theta_bool_map = binary_nested.compute_theta_bool_map(
                    q_vector_keys=keys, variables=variables
                )
                theta_reindexed_bool_map = (
                    binary_nested.compute_theta_reindexed_bool_map(
                        q_vector_keys=keys, districts=districts
                    )
                )
                x_dis = q[district_bool_map[D_j]]
                A, b = binary_nested.construct_A_b(
                    variable=variable,
                    q=x_dis,
                    theta_reindexed_bool_map=theta_reindexed_bool_map,
                    M=M,
                    P=P,
                )

                x_var = q[theta_bool_map[variable]]
                result1 = binary_nested._compute_prob_single_district(
                    x_dis, M, P
                )
                result2 = A @ x_var - b
                np.testing.assert_array_almost_equal(result1, result2)

    def test_term_tail_length_on_verma(self):
        """
        Check that the combined tails in each term don't contain repeated variables.

        :return:
        """
        G = verma_graph(k=2)
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        districts = G.districts
        heads_tails_map = binary_nested.get_heads_tails_map(
            intrinsic_dict=intrinsic_dict
        )
        for district in districts:
            # partition_head_dict = binary_nested.compute_partition_head_dict(G=G, intrinsic_dict=intrinsic_dict, district=district)
            terms = binary_nested.compute_terms(
                district=district,
                intrinsic_dict=intrinsic_dict,
                heads_tails_map=heads_tails_map,
            )

            print(terms)
            for head, tail, value in terms:
                # Check that there are no repeats in the tail variables

                self.assertEqual(len(tail), len(set(tail)))

    def test_that_16_not_18_count_correct(self):
        """
        Check that the 16-not-18 graph has 16 parameters as predicted under the nested Markov model, not 18 parameters under the ordinary Markov model.
        :return:
        """
        G = sixteen_not_eighteen_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        q_vector = binary_nested.initialize_q_vector(intrinsic_dict)
        self.assertEqual(len(q_vector), 16)


class TestBinaryNestedModel(unittest.TestCase):
    def test_process_data_on_nonbinary_dataframe_fails(self):
        X = pd.DataFrame({"X1": [0, 0, 2, 1, 1], "X2": [0, 1, 0, 1, 2]})
        with pytest.raises(KeyError):
            result = binary_nested.process_data(X)

    def test_that_process_data_correctly_extracts_counts(self):
        X = pd.DataFrame({"X1": [0, 0, 1, 1, 1], "X2": [0, 1, 0, 1, 1]})
        result = binary_nested.process_data(X)
        expected = np.array([1, 1, 1, 2])
        np.testing.assert_array_equal(result, expected)

        X = pd.DataFrame({"X1": [0, 1, 1, 1, 1], "X2": [0, 1, 0, 1, 1]})
        result = binary_nested.process_data(X)
        expected = np.array([1, 0, 1, 3])
        np.testing.assert_array_equal(result, expected)

    def test_that_process_data_extracts_tabular_summary_correctly(self):
        X = pd.DataFrame(
            {"X2": [0, 0, 1, 1], "X1": [0, 1, 0, 1], "count": [1, 2, 3, 4]}
        )
        result = binary_nested.process_data(X, count_variable="count")
        expected = np.array([1, 3, 2, 4])
        np.testing.assert_array_equal(result, expected)
