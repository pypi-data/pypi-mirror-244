import unittest

import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_allclose

from ananke.graphs import ADMG
from ananke.models import LinearGaussianSEM


class TestLinearGaussianSEM(unittest.TestCase):
    def test_model_creation(self):

        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("B", "C"), ("C", "D")]
        bi_edges = [("B", "D")]
        G = ADMG(vertices, di_edges=di_edges, bi_edges=bi_edges)
        model = LinearGaussianSEM(G)
        self.assertEqual(8, model.n_params)

    def test_verma_model(self):

        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("B", "C"), ("C", "D")]
        bi_edges = [("B", "D")]
        G = ADMG(vertices, di_edges=di_edges, bi_edges=bi_edges)
        model = LinearGaussianSEM(G)

        # generate data from an ADMG A->B->C->D B<->D and try to fit
        N = 50000
        dim = 4

        omega = np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0.8], [0, 0, 1, 0], [0, 0.8, 0, 1]]
        )

        beta = np.array(
            [[0, 0, 0, 0], [3, 0, 0, 0], [0, -1, 0, 0], [0, 0, 2.5, 0]]
        )

        # generate data
        true_sigma = (
            np.linalg.inv(np.eye(dim) - beta)
            @ omega
            @ np.linalg.inv((np.eye(dim) - beta).T)
        )
        X = np.random.multivariate_normal([0] * dim, true_sigma, size=N)
        data = pd.DataFrame(
            {"A": X[:, 0], "B": X[:, 1], "C": X[:, 2], "D": X[:, 3]}
        )

        # test that without fitting you can't compute likelihood
        with self.assertRaises(AssertionError):
            model.neg_loglikelihood(data)

        # test that without fitting you can't draw the model
        with self.assertRaises(AssertionError):
            model.draw()

        # try with trust-exact (the default)
        model = LinearGaussianSEM(G)
        model.fit(data)

        # computation of causal effects
        self.assertEqual(0, model.total_effect(["D"], ["A"]))
        self.assertAlmostEqual(
            -7.5, model.total_effect(["A"], ["D"]), delta=0.5
        )

        model.draw(direction="LR")

    def test_that_beta_and_omega_recovered_correctly(self):
        np.random.seed(123)
        size = 10000
        dim = 4
        # generate data from A->B->C->D, A<->D, A<->C
        beta = np.array(
            [[0, 1.2, 0, 0], [0, 0, -1.5, 0], [0, 0, 0, 1.0], [0, 0, 0, 0]]
        ).T

        omega = np.array(
            [
                [1.2, 0, 0.5, 0.6],
                [0, 1, 0, 0.0],
                [0.5, 0, 1, 0],
                [0.6, 0.0, 0, 1],
            ]
        )

        true_sigma = (
            np.linalg.inv(np.eye(dim) - beta)
            @ omega
            @ np.linalg.inv((np.eye(dim) - beta).T)
        )
        X = np.random.multivariate_normal([0] * dim, true_sigma, size=size)
        X = X - np.mean(X, axis=0)  # centre the data
        data = pd.DataFrame(
            {"A": X[:, 0], "B": X[:, 1], "C": X[:, 2], "D": X[:, 3]}
        )

        # make Ananke ADMG and call RICF
        G = ADMG(
            vertices=["A", "B", "C", "D"],
            di_edges=[("A", "B"), ("B", "C"), ("C", "D")],
            bi_edges=[("A", "D"), ("A", "C")],
        )

        model = LinearGaussianSEM(G)
        model.fit(data, standardize=False)

        assert beta == pytest.approx(model.B_, rel=0.05)
        assert omega == pytest.approx(model.omega_, rel=0.05)

    def test_nested_markov_equivalent_models_are_bic_indistinguishable(self):
        # define number of samples and number of vertices
        np.random.seed(123)
        N = 1000
        dim = 4

        # define the Omega matrix
        omega = np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0.8], [0, 0, 1, 0], [0, 0.8, 0, 1]]
        )

        # define the B matrix
        beta = np.array(
            [[0, 0, 0, 0], [3, 0, 0, 0], [1.2, -1, 0, 0], [0, 0, 2.5, 0]]
        )

        # generate data according to the graph
        true_sigma = (
            np.linalg.inv(np.eye(dim) - beta)
            @ omega
            @ np.linalg.inv((np.eye(dim) - beta).T)
        )
        X = np.random.multivariate_normal([0] * dim, true_sigma, size=N)
        data = pd.DataFrame(
            {"A": X[:, 0], "B": X[:, 1], "C": X[:, 2], "D": X[:, 3]}
        )

        # Set up the true model (arid projection of G)
        vertices = ["A", "B", "C", "D"]
        di_edges = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")]
        bi_edges = [("A", "C"), ("B", "D")]
        G = ADMG(vertices, di_edges=di_edges, bi_edges=bi_edges)
        G_arid = G.maximal_arid_projection()

        # Set up incorrect model

        di_edges = [("A", "B"), ("B", "C"), ("C", "D"), ("B", "D"), ("A", "C")]
        bi_edges = []
        G_incorrect = ADMG(vertices, di_edges=di_edges, bi_edges=bi_edges)

        # calculate BIC for incorrect model
        model_incorrect = LinearGaussianSEM(G_incorrect)
        model_incorrect.fit(data)
        bic_incorrect = model_incorrect.bic(data)

        # calculate BIC for the true model
        model_truth = LinearGaussianSEM(G_arid)
        model_truth.fit(data)
        bic_truth = model_truth.bic(data)

        assert bic_truth < bic_incorrect
        # calculate BIC for the nested Markov equivalent model (A -> B is now A <-> B)
        di_edges = [("A", "C"), ("B", "C"), ("C", "D")]
        bi_edges = [("A", "B"), ("B", "D")]
        G_equivalent = ADMG(vertices, di_edges=di_edges, bi_edges=bi_edges)
        model_equivalent = LinearGaussianSEM(G_equivalent)
        model_equivalent.fit(data)
        bic_equivalent = model_equivalent.bic(data)

        assert model_equivalent.n_params == model_truth.n_params

        # assert BIC is the same for nested Markov equivalent model
        # note that since models have same dimension we can consider only the log-likelihood when checking equality of BIC
        assert model_truth.neg_loglikelihood(data) == pytest.approx(
            model_equivalent.neg_loglikelihood(data)
        )


if __name__ == "__main__":
    unittest.main()
