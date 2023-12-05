import copy
import itertools
from collections import ChainMap

import numpy as np
import pytest
import sympy as sp

from ananke.estimation import empirical_plugin
from ananke.graphs import ADMG, DAG
from ananke.identification import OneLineID, one_line, oracle
from ananke.inference.variable_elimination import variable_elimination
from ananke.models import bayesian_network


class TestEffectEstimationID:
    def test_estimate_effect_from_distribution(self):
        di_edges = [("A", "Y"), ("C", "A"), ("C", "Y")]
        graph = ADMG(["A", "C", "Y"], di_edges=di_edges)
        cpds = bayesian_network.generate_random_cpds(graph)
        net = bayesian_network.BayesianNetwork(graph, cpds)
        treatment_dict = {"A": 1}
        outcome_dict = {"Y": 1}
        int_net = copy.deepcopy(net)
        int_net.fix(treatment_dict)

        int_inference = variable_elimination(int_net, ["Y"])
        truth = int_inference.get_value(**outcome_dict)

        oid = OneLineID(graph, list(treatment_dict), list(outcome_dict))
        obs_dist = empirical_plugin.get_obs_dist_from_net(net, graph)
        effect = empirical_plugin.estimate_effect_from_discrete_dist(
            oid, obs_dist, treatment_dict, outcome_dict
        )
        assert truth == pytest.approx(effect)

    def test_estimate_effect_front_door(self):
        di_edges = [("A", "M"), ("M", "Y")]
        bi_edges = [("A", "Y")]
        graph = ADMG(
            vertices={"A": 2, "M": 2, "Y": 2},
            di_edges=di_edges,
            bi_edges=bi_edges,
        )
        # TEST FAILING DUE TO BAD CANONICAL DAG CODE
        dag = graph.canonical_dag(cardinality=2)
        cpds = bayesian_network.generate_random_cpds(graph=dag, dir_conc=10)
        net = bayesian_network.BayesianNetwork(graph=dag, cpds=cpds)
        obs_dist = variable_elimination(net, list(graph.vertices))
        # VariableElimination(net).query(list(graph.vertices))
        treatment_dict = {"A": 1}

        outcome_dict = {"Y": 1}

        truth = oracle.compute_effect_from_discrete_model(
            net, treatment_dict, outcome_dict
        )
        oid = OneLineID(graph, list(treatment_dict), list(outcome_dict))
        effect = empirical_plugin.estimate_effect_from_discrete_dist(
            oid, obs_dist, treatment_dict, outcome_dict
        )

        assert truth == pytest.approx(effect)

    def test_effect_estimation_from_symbolic_distribution(self):

        di_edges = [("A", "M"), ("M", "Y")]
        bi_edges = [("A", "Y")]
        graph = ADMG(
            vertices={"A": 2, "M": 2, "Y": 2},
            di_edges=di_edges,
            bi_edges=bi_edges,
        )
        dag = graph.canonical_dag(cardinality=2)
        cpds, all_vars = bayesian_network.create_symbolic_cpds(dag)
        net = bayesian_network.BayesianNetwork(graph=dag, cpds=cpds)
        treatment_dict = {"A": 1}

        outcome_dict = {"Y": 1}
        truth = oracle.compute_effect_from_discrete_model(
            net, treatment_dict, outcome_dict
        )
        oid = OneLineID(graph, list(treatment_dict), list(outcome_dict))
        obs_dist = variable_elimination(net, list(graph.vertices))
        effect = empirical_plugin.estimate_effect_from_discrete_dist(
            oid, obs_dist, treatment_dict, outcome_dict
        )

        assert sp.simplify(truth - effect) == 0

        pass
