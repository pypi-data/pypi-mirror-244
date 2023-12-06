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


class TestFittingModels(unittest.TestCase):
    """
    This suite of tests checks maximum likelihood estimation works correctly in a variety of graphs
    """

    def test_estimate_likelihood(self):
        """
        Test that MLE works for a single district ancestral graph

        :return:
        """
        G = fig3_graph()
        districts = G.districts
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        q_vector = binary_nested.initialize_q_vector(intrinsic_dict)
        q = np.array(list(q_vector.values()))

        counts = np.array(
            [10, 3, 42, 4, 34, 9, 23, 124]
        )  # length of this vector is 2**len(vertices) = 8
        q_indices = binary_nested.compute_q_indices_by_district(
            q_vector_keys=list(q_vector.keys()), districts=districts
        )
        Ms, Ps = binary_nested.compute_all_M_and_P(
            G=G, intrinsic_dict=intrinsic_dict
        )
        prob = binary_nested._compute_prob(q, q_indices, districts, Ms, Ps)

        # Check probs sum to 1 and are not negative
        self.assertAlmostEqual(np.sum(prob), 1)
        self.assertTrue((prob >= 0).all())
        result = binary_nested._compute_likelihood(
            q, counts, q_indices, districts, Ms, Ps
        )

        # Check that likelihood is a number, and check that the probabilities are well formed
        self.assertTrue(~np.isnan(result))
        bnm = binary_nested.BinaryNestedModel(graph=G)
        bnm = bnm.fit(X=counts)
        final_q_vector = bnm.fitted_params
        final_p = binary_nested._compute_prob(
            np.array(list(final_q_vector.values())),
            q_indices,
            districts,
            Ms,
            Ps,
        )
        self.assertAlmostEqual(np.sum(final_p), 1)

    def test_that_dag_can_be_fitted(self):
        """
        Checks that the code works for DAGs, and consequently also checks that code works across more than one district.
        In the case of a DAG, we check that the empirical probabilities p(V = v) are recovered by the Mobius transform.

        :return:
        """
        G = standard_dag()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        rng = np.random.default_rng(4213)
        counts = rng.integers(low=50, high=80, size=(2 ** len(G.vertices),))
        expected_prob = counts / counts.sum()

        bnm = binary_nested.BinaryNestedModel(graph=G)
        bnm = bnm.fit(X=counts)
        result = bnm.fitted_params
        q_indices = binary_nested.compute_q_indices_by_district(
            q_vector_keys=list(result.keys()), districts=G.districts
        )
        Ms, Ps = binary_nested.compute_all_M_and_P(
            G=G, intrinsic_dict=intrinsic_dict
        )
        estimated_prob = binary_nested._compute_prob(
            q=np.array(list(result.values())),
            q_indices=q_indices,
            districts=G.districts,
            Ms=Ms,
            Ps=Ps,
        )

        np.testing.assert_array_almost_equal(
            expected_prob, estimated_prob, decimal=2
        )

    def test_that_parameters_of_dag_are_correctly_recovered(self):
        G = dag_chain_small()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        rng = np.random.default_rng(4213)
        X_1 = rng.binomial(n=1, p=0.5, size=1000)
        X_2 = rng.binomial(n=1, p=expit(1 + X_1))
        df = pd.DataFrame({"X_1": X_1, "X_2": X_2})
        bnm = binary_nested.BinaryNestedModel(graph=G)
        bnm = bnm.fit(X=df)
        results = bnm.fitted_params

        # Check that p(X_2=1 | do(X_1=1)) = 1 - q_{X_2 = 0} (X_1 = 1) = expit(2)
        assert 1 - results[
            (frozenset({"X_2"}), ("X_1",), (1,))
        ] == pytest.approx(expit(2), rel=0.1)
        # Check that p(X_2=1 | do(X_1=0)) = 1 - q_{X_2 = 0} (X_1 = 0) = expit(1)
        assert 1 - results[
            (frozenset({"X_2"}), ("X_1",), (0,))
        ] == pytest.approx(expit(1), rel=0.1)

    def test_estimate_medium_sized_district(self):
        """
        Check that the estimation code works for districts of size 5, based off performance check in Fig 8 of ER13

        :return:
        """
        G = fig8_graph(k=3)
        rng = np.random.default_rng(4213)
        counts = rng.integers(low=60, high=80, size=(2 ** len(G.vertices),))
        expected_prob = counts / counts.sum()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        bnm = binary_nested.BinaryNestedModel(graph=G)
        bnm = bnm.fit(X=counts)
        q_vector = bnm.fitted_params

        q_indices = binary_nested.compute_q_indices_by_district(
            q_vector_keys=list(q_vector.keys()), districts=G.districts
        )
        Ms, Ps = binary_nested.compute_all_M_and_P(
            G=G, intrinsic_dict=intrinsic_dict
        )
        estimated_prob = binary_nested._compute_prob(
            q=np.array(list(q_vector.values())),
            q_indices=q_indices,
            districts=G.districts,
            Ms=Ms,
            Ps=Ps,
        )

        # Check that the fitted Moebius parameters transform back into the empirical probabilities
        np.testing.assert_array_almost_equal(
            expected_prob, estimated_prob, decimal=2
        )

    def test_estimate_verma_graph(self):
        """
        Check that estimation procedure works for verma graph of size 1

        :return:
        """
        G = verma_graph(k=2)
        rng = np.random.default_rng(4213)
        counts = rng.integers(low=60, high=80, size=(2 ** len(G.vertices),))
        expected_prob = counts / counts.sum()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()

        bnm = binary_nested.BinaryNestedModel(graph=G)
        bnm = bnm.fit(X=counts)
        q_vector = bnm.fitted_params

        q_indices = binary_nested.compute_q_indices_by_district(
            q_vector_keys=list(q_vector.keys()), districts=G.districts
        )
        Ms, Ps = binary_nested.compute_all_M_and_P(
            G=G, intrinsic_dict=intrinsic_dict
        )
        estimated_prob = binary_nested._compute_prob(
            q=np.array(list(q_vector.values())),
            q_indices=q_indices,
            districts=G.districts,
            Ms=Ms,
            Ps=Ps,
        )

        # Check that the fitted Moebius parameters transform back into the empirical probabilities
        np.testing.assert_array_almost_equal(
            expected_prob, estimated_prob, decimal=2
        )

    def test_synthetic_evans_richardson_fig_8b(self):
        G = wisconsin_fig8b_graph()
        rng = np.random.default_rng(4213)
        U = rng.binomial(n=1, p=0.5, size=1000)
        X = rng.binomial(n=1, p=0.5, size=1000)
        E = rng.binomial(n=1, p=expit(1 + X - U))
        M = rng.binomial(n=1, p=expit(-1 + E))
        Y = rng.binomial(n=1, p=expit(U + X))
        df = pd.DataFrame({"X": X, "E": E, "M": M, "Y": Y})

        # Compute p(Y=1 | X) = \sum_U p(Y=1 | X, U) p(U)
        py1_x1 = 0.5 * expit(2) + 0.5 * expit(1)
        py1_x0 = 0.5 * expit(1) + 0.5 * expit(0)
        bnm = binary_nested.BinaryNestedModel(graph=G)
        bnm = bnm.fit(X=df)
        bnm = bnm.fit(X=df)
        results = bnm.fitted_params
        assert 1 - results[(frozenset({"Y"}), ("X",), (0,))] == pytest.approx(
            py1_x0, rel=0.05
        )
        assert 1 - results[(frozenset({"Y"}), ("X",), (1,))] == pytest.approx(
            py1_x1, rel=0.05
        )

    def test_evans_richardson_fig_8b(self):
        import logging

        binary_nested.logger.setLevel(logging.DEBUG)

        # logging.getLogger("binary_nested").setLevel(logging.WARNING)
        G = wisconsin_fig8b_graph()
        variables = ["X", "E", "M", "Y", "count"]
        values = np.array(
            [
                [0, 0, 0, 0, 241],
                [0, 0, 0, 1, 162],
                [0, 0, 1, 0, 53],
                [0, 0, 1, 1, 39],
                [1, 0, 0, 0, 161],
                [1, 0, 0, 1, 148],
                [1, 0, 1, 0, 33],
                [1, 0, 1, 1, 29],
                [0, 1, 0, 0, 82],
                [0, 1, 0, 1, 176],
                [0, 1, 1, 0, 13],
                [0, 1, 1, 1, 16],
                [1, 1, 0, 0, 113],
                [1, 1, 0, 1, 364],
                [1, 1, 1, 0, 16],
                [1, 1, 1, 1, 30],
            ]
        )
        df = pd.DataFrame(values, columns=variables)

        # try to work out what variables were flipped in the table
        df["X"] = 1 - df["X"]
        df["Y"] = 1 - df["Y"]

        counts = binary_nested.process_data(df, count_variable="count")
        expected_prob = counts / counts.sum()
        bnm = binary_nested.BinaryNestedModel(graph=G)
        bnm = bnm.fit(X=df, tol=1e-8)
        # TODO: It appears that the linear constraint ensuring non-negative probabilities is violated during the optimize call, despite the fact that keep_feasible=True.

        q_vector = bnm.fitted_params
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        q_indices = binary_nested.compute_q_indices_by_district(
            q_vector_keys=list(q_vector.keys()), districts=G.districts
        )
        Ms, Ps = binary_nested.compute_all_M_and_P(
            G=G, intrinsic_dict=intrinsic_dict
        )
        estimated_prob = binary_nested._compute_prob(
            q=np.array(list(q_vector.values())),
            q_indices=q_indices,
            districts=G.districts,
            Ms=Ms,
            Ps=Ps,
        )
        np.testing.assert_allclose(expected_prob, estimated_prob, atol=0.01)

        # Recall that all q params are evaluated at head=0
        # Compute p(Y=1 | do(X)=1) = 1 - q_Y (X=1) ?= 0.5
        assert 1 - bnm.fitted_params[
            (frozenset({"Y"}), ("X",), (1,))
        ] == pytest.approx(0.5, rel=0.01)
        # Compute p(Y=1 | do(X)=1) = 1 - q_Y (X=0) ?= 0.36
        assert 1 - bnm.fitted_params[
            (frozenset({"Y"}), ("X",), (0,))
        ] == pytest.approx(0.36, rel=0.01)

        assert bnm.estimate(
            treatment_dict={"X": 1}, outcome_dict={"Y": 1}
        ) == pytest.approx(0.5, rel=0.01)

        assert bnm.estimate(
            treatment_dict={"X": 0}, outcome_dict={"Y": 1}
        ) == pytest.approx(0.36, rel=0.01)


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


class TestComputeCounterfactual(unittest.TestCase):
    def test_compute_counterfactual_conditional_ignorability(self):
        G = conditional_ignorability_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        rng = np.random.default_rng(4213)
        C = rng.binomial(n=1, p=0.5, size=1000)
        A = rng.binomial(n=1, p=expit(1 + C))
        Y = rng.binomial(n=1, p=expit(1 + A + C))
        df = pd.DataFrame({"A": A, "C": C, "Y": Y})
        bnm = binary_nested.BinaryNestedModel(graph=G)
        bnm = bnm.fit(X=df)

        q_vector = bnm.fitted_params

        # p(Y(a=0) = 0)
        x_dict = {"A": 0}
        y_dict = {"Y": 0}

        est_ctf = binary_nested.compute_counterfactual_binary_parameters(
            G, q_vector, x_dict, y_dict
        )

        truth = q_vector[(frozenset({"Y"}), ("A", "C"), (0, 0))] * q_vector[
            (frozenset({"C"}), (), ())
        ] + q_vector[(frozenset({"Y"}), ("A", "C"), (0, 1))] * (
            1 - q_vector[(frozenset({"C"}), (), ())]
        )

        assert truth == pytest.approx(est_ctf)

        # p(Y(a=1) = 1)
        x_dict = {"A": 1}
        y_dict = {"Y": 1}

        est_ctf = binary_nested.compute_counterfactual_binary_parameters(
            G, q_vector, x_dict, y_dict
        )

        truth = (
            1 - q_vector[(frozenset({"Y"}), ("A", "C"), (1, 0))]
        ) * q_vector[(frozenset({"C"}), (), ())] + (
            1 - q_vector[(frozenset({"Y"}), ("A", "C"), (1, 1))]
        ) * (
            1 - q_vector[(frozenset({"C"}), (), ())]
        )

        assert truth == pytest.approx(est_ctf)

    def test_compute_counterfactual_front_door(self):
        df = (
            load_wisconsin_health_study()
            .rename(columns={"E": "A"})
            .groupby(["A", "M", "Y"])["count"]
            .sum()
            .reset_index()
        )

        vertices = ["A", "M", "Y"]
        di_edges = [("A", "M"), ("M", "Y")]
        bi_edges = [("A", "Y")]
        front_door = ADMG(vertices, di_edges, bi_edges)
        bnm = binary_nested.BinaryNestedModel(front_door)
        bnm = bnm.fit(X=df, tol=1e-12)
        theta_M0_A0 = bnm.fitted_params[(frozenset({"M"}), ("A",), (0,))]
        theta_M0_A1 = bnm.fitted_params[(frozenset({"M"}), ("A",), (1,))]
        theta_Y0_M0 = bnm.fitted_params[(frozenset({"Y"}), ("M",), (0,))]
        theta_Y0_M1 = bnm.fitted_params[(frozenset({"Y"}), ("M",), (1,))]
        pY1_A0 = (1 - theta_Y0_M0) * theta_M0_A0 + (1 - theta_Y0_M1) * (
            1 - theta_M0_A0
        )
        pY1_A1 = (1 - theta_Y0_M0) * theta_M0_A1 + (1 - theta_Y0_M1) * (
            1 - theta_M0_A1
        )

        assert pY1_A0 == pytest.approx(bnm.estimate({"A": 0}, {"Y": 1}))
        assert pY1_A1 == pytest.approx(bnm.estimate({"A": 1}, {"Y": 1}))

        assert bnm.fitted_params[
            (frozenset({"Y"}), ("M",), (0,))
        ] == bnm.estimate({"M": 0}, {"Y": 0})

    def test_compute_estimate_without_intervention(self):
        rng = np.random.default_rng(4213)
        U = rng.binomial(n=1, p=0.5, size=1000)
        A = rng.binomial(n=1, p=expit(U), size=1000)
        M = rng.binomial(n=1, p=expit(A), size=1000)
        Y = rng.binomial(n=1, p=expit(1 + M + U))
        vertices = ["A", "M", "Y"]
        di_edges = [("A", "M"), ("M", "Y")]
        bi_edges = [("A", "Y")]
        graph = ADMG(vertices, di_edges, bi_edges)
        df = pd.DataFrame({"A": A, "Y": Y, "M": M})

        bnm = binary_nested.BinaryNestedModel(graph)
        bnm = bnm.fit(X=df)

        assert df["Y"].mean() == pytest.approx(
            bnm.estimate(treatment_dict={}, outcome_dict={"Y": 1})
        )
        assert ((df["Y"] == 1) & (df["A"] == 1)).mean() == pytest.approx(
            bnm.estimate(outcome_dict={"Y": 1, "A": 1})
        )

    def test_compute_estimate_not_id(self):
        rng = np.random.default_rng(4213)
        U = rng.binomial(n=1, p=0.5, size=1000)
        A = rng.binomial(n=1, p=expit(U), size=1000)
        Y = rng.binomial(n=1, p=expit(1 + U))

        df = pd.DataFrame({"A": A, "Y": Y})

        vertices = ["A", "Y"]
        di_edges = [("A", "Y")]
        bi_edges = [("A", "Y")]
        graph = ADMG(vertices, di_edges, bi_edges)
        bnm = binary_nested.BinaryNestedModel(graph)
        bnm = bnm.fit(X=df)

        with pytest.raises(AssertionError) as e:
            result = bnm.estimate(
                outcome_dict={"Y": 1}, treatment_dict={"A": 1}
            )


class TestComputeCounterfactual(unittest.TestCase):
    def test_compute_counterfactual_conditional_ignorability(self):
        G = conditional_ignorability_graph()
        intrinsic_dict, _ = G.get_intrinsic_sets_and_heads()
        rng = np.random.default_rng(4213)
        C = rng.binomial(n=1, p=0.5, size=1000)
        A = rng.binomial(n=1, p=expit(1 + C))
        Y = rng.binomial(n=1, p=expit(1 + A + C))
        df = pd.DataFrame({"A": A, "C": C, "Y": Y})
        bnm = binary_nested.BinaryNestedModel(graph=G)
        bnm = bnm.fit(X=df)

        q_vector = bnm.fitted_params

        # p(Y(a=0) = 0)
        x_dict = {"A": 0}
        y_dict = {"Y": 0}

        est_ctf = binary_nested.compute_counterfactual_binary_parameters(
            G, q_vector, x_dict, y_dict
        )

        truth = q_vector[(frozenset({"Y"}), ("A", "C"), (0, 0))] * q_vector[
            (frozenset({"C"}), (), ())
        ] + q_vector[(frozenset({"Y"}), ("A", "C"), (0, 1))] * (
            1 - q_vector[(frozenset({"C"}), (), ())]
        )

        assert truth == pytest.approx(est_ctf)

        # p(Y(a=1) = 1)
        x_dict = {"A": 1}
        y_dict = {"Y": 1}

        est_ctf = binary_nested.compute_counterfactual_binary_parameters(
            G, q_vector, x_dict, y_dict
        )

        truth = (
            1 - q_vector[(frozenset({"Y"}), ("A", "C"), (1, 0))]
        ) * q_vector[(frozenset({"C"}), (), ())] + (
            1 - q_vector[(frozenset({"Y"}), ("A", "C"), (1, 1))]
        ) * (
            1 - q_vector[(frozenset({"C"}), (), ())]
        )

        assert truth == pytest.approx(est_ctf)

    def test_compute_counterfactual_front_door(self):
        df = (
            load_wisconsin_health_study()
            .rename(columns={"E": "A"})
            .groupby(["A", "M", "Y"])["count"]
            .sum()
            .reset_index()
        )

        vertices = ["A", "M", "Y"]
        di_edges = [("A", "M"), ("M", "Y")]
        bi_edges = [("A", "Y")]
        front_door = ADMG(vertices, di_edges, bi_edges)
        bnm = binary_nested.BinaryNestedModel(front_door)
        bnm = bnm.fit(X=df, tol=1e-12)
        theta_M0_A0 = bnm.fitted_params[(frozenset({"M"}), ("A",), (0,))]
        theta_M0_A1 = bnm.fitted_params[(frozenset({"M"}), ("A",), (1,))]
        theta_Y0_M0 = bnm.fitted_params[(frozenset({"Y"}), ("M",), (0,))]
        theta_Y0_M1 = bnm.fitted_params[(frozenset({"Y"}), ("M",), (1,))]
        pY1_A0 = (1 - theta_Y0_M0) * theta_M0_A0 + (1 - theta_Y0_M1) * (
            1 - theta_M0_A0
        )
        pY1_A1 = (1 - theta_Y0_M0) * theta_M0_A1 + (1 - theta_Y0_M1) * (
            1 - theta_M0_A1
        )

        assert pY1_A0 == pytest.approx(bnm.estimate({"A": 0}, {"Y": 1}))
        assert pY1_A1 == pytest.approx(bnm.estimate({"A": 1}, {"Y": 1}))

        assert bnm.fitted_params[
            (frozenset({"Y"}), ("M",), (0,))
        ] == bnm.estimate({"M": 0}, {"Y": 0})

    def test_compute_estimate_without_intervention(self):
        rng = np.random.default_rng(4213)
        U = rng.binomial(n=1, p=0.5, size=1000)
        A = rng.binomial(n=1, p=expit(U), size=1000)
        M = rng.binomial(n=1, p=expit(A), size=1000)
        Y = rng.binomial(n=1, p=expit(1 + M + U))
        vertices = ["A", "M", "Y"]
        di_edges = [("A", "M"), ("M", "Y")]
        bi_edges = [("A", "Y")]
        graph = ADMG(vertices, di_edges, bi_edges)
        df = pd.DataFrame({"A": A, "Y": Y, "M": M})

        bnm = binary_nested.BinaryNestedModel(graph)
        bnm = bnm.fit(X=df)

        assert df["Y"].mean() == pytest.approx(
            bnm.estimate(treatment_dict={}, outcome_dict={"Y": 1})
        )
        assert ((df["Y"] == 1) & (df["A"] == 1)).mean() == pytest.approx(
            bnm.estimate(outcome_dict={"Y": 1, "A": 1})
        )

    def test_compute_estimate_not_id(self):
        rng = np.random.default_rng(4213)
        U = rng.binomial(n=1, p=0.5, size=1000)
        A = rng.binomial(n=1, p=expit(U), size=1000)
        Y = rng.binomial(n=1, p=expit(1 + U))

        df = pd.DataFrame({"A": A, "Y": Y})

        vertices = ["A", "Y"]
        di_edges = [("A", "Y")]
        bi_edges = [("A", "Y")]
        graph = ADMG(vertices, di_edges, bi_edges)
        bnm = binary_nested.BinaryNestedModel(graph)
        bnm = bnm.fit(X=df)

        with pytest.raises(AssertionError) as e:
            result = bnm.estimate(
                outcome_dict={"Y": 1}, treatment_dict={"A": 1}
            )
