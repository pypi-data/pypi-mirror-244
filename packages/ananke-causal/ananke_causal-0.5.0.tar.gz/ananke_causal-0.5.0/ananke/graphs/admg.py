"""
Class for acyclic directed mixed graphs (ADMGs) and conditional ADMGs (CADMGs).
"""
import copy
import itertools
import logging
import warnings
from typing import Union

from ananke.utils import powerset

from .ig import IG
from .sg import SG
from .ug import UG

logger = logging.getLogger(__name__)


class UndefinedADMGOperation(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def latent_project_single_vertex(vertex, graph):
    """
    Latent project one vertex from graph

    :param vertex: Name of vertex to be projected
    :param graph: ADMG
    :returns:
    """

    di_edges = graph.di_edges
    bi_edges = graph.bi_edges

    retained_vertices = set(graph.vertices) - {vertex}
    retained_di_edges = [
        x
        for x in di_edges
        if x[0] in retained_vertices and x[1] in retained_vertices
    ]

    retained_bi_edges = [
        x
        for x in bi_edges
        if x[0] in retained_vertices and x[1] in retained_vertices
    ]

    # Construct all directed edge projections
    new_di_edges = [
        (p.name, c.name)
        for p in graph.vertices[vertex].parents
        for c in graph.vertices[vertex].children
    ]

    # Construct all bidirected edge projections

    new_bi_edges = [
        tuple(sorted([s.name, c.name]))
        for s in graph.vertices[vertex].siblings
        for c in graph.vertices[vertex].children
    ] + [
        tuple(sorted([a.name, b.name]))
        for a, b in itertools.combinations(graph.vertices[vertex].children, r=2)
    ]
    final_bi_edges = retained_bi_edges + new_bi_edges

    G = ADMG(
        vertices=set(retained_vertices),
        di_edges=set(retained_di_edges + new_di_edges),
        bi_edges=set(final_bi_edges),
    )

    return G


class ADMG(SG):
    """
    Class for creating and manipulating (conditional) acyclic directed mixed graphs (ADMGs/CADMGs).
    """

    def __init__(self, vertices=[], di_edges=set(), bi_edges=set(), **kwargs):
        """
        Constructor.

        :param vertices: iterable of names of vertices.
        :param di_edges: iterable of tuples of directed edges i.e. (X, Y) = X -> Y.
        :param bi_edges: iterable of tuples of bidirected edges i.e. (X, Y) = X <-> Y.
        """

        # initialize vertices in ADMG
        super().__init__(
            vertices=vertices, di_edges=di_edges, bi_edges=bi_edges, **kwargs
        )

    def markov_pillow(self, vertices, top_order):
        """
        Get the Markov pillow of a set of vertices. That is,
        the Markov blanket of the vertices given a valid topological order
        on the graph.

        :param vertices: iterable of vertex names.
        :param top_order: a valid topological order.
        :return: set corresponding to Markov pillow.
        """

        # get the subgraph corresponding to the vertices and nodes prior to them
        pre = self.pre(vertices, top_order)
        Gsub = self.subgraph(pre + list(vertices))

        # Markov pillow is the Markov blanket (dis(v) union pa(dis(v)) setminus v)
        # in this subgraph
        pillow = set()
        for v in vertices:
            pillow = pillow.union(Gsub.district(v))
        pillow = pillow.union(Gsub.parents(pillow))
        return pillow - set(vertices)

    def markov_blanket(self, vertices):
        """
        Get the Markov blanket of a set of vertices.

        :param vertices: iterable of vertex names.
        :return: set corresponding to Markov blanket.
        """

        blanket = set()
        for v in vertices:
            blanket = blanket.union(self.district(v))
        blanket = blanket.union(self.parents(blanket))
        return blanket - set(vertices)

    @property
    def fixed(self):
        """
        Returns all fixed nodes in the graph.

        :return:
        """
        fixed_vertices = []
        for v in self.vertices:
            if self.vertices[v].fixed:
                fixed_vertices.append(v)

        return fixed_vertices

    def is_subgraph(self, other):
        """
        Check that this graph is a subgraph of other, meaning it has  a subset of edges and nodes of the other.

        :param other: an object of the ADMG class.
        :return: boolean indicating whether the statement is True or not.
        """
        if (
            set(self.vertices).issubset(set(other.vertices))
            and set(self.di_edges).issubset(set(other.di_edges))
            and set(self.bi_edges).issubset(set(other.bi_edges))
        ):
            return True
        return False

    def is_ancestral_subgraph(self, other):
        """
        Check that this graph is an ancestral subgraph of the other.
        An ancestral subgraph over variables S and intervention b G(S(b)) of a larger graph G(V(b)) is defined as a
        subgraph, such that ancestors of each node s in S with respect to the graph G(V(b_i)) are contained in S.

        :param other: an object of the ADMG class.
        :return: boolean indicating whether the statement is True or not.
        """
        if not self.is_subgraph(other):
            return False

        for v in self.vertices:
            self_parents = set([item.name for item in self.vertices[v].parents])
            other_parents = set(
                [item.name for item in other.vertices[v].parents]
            )
            if self_parents != other_parents:
                return False

        return True

    def reachable_closure(self, vertices):
        """
        Obtain reachable closure for a set of vertices.

        :param vertices: set of vertices to get reachable closure for.
        :return: set corresponding to the reachable closure, the fixing order for vertices
                 outside of the closure, and the CADMG corresponding to the closure.
        """

        # initialize set of vertices that must still be fixed
        remaining_vertices = (
            set(self.vertices)
            - set(vertices)
            - set(v for v in self.vertices if self.vertices[v].fixed)
        )
        fixing_order = []  # keep track of the valid fixing order
        fixed = True  # flag to track that a vertex was successfully fixed in a given pass
        G = copy.deepcopy(self)

        # keep iterating over remaining vertices until there are no more or we failed to fix
        while remaining_vertices and fixed:

            fixed = False

            # check if any remaining vertex van be fixed
            for v in remaining_vertices:

                # fixability check
                if len(G.descendants([v]).intersection(G.district(v))) == 1:
                    G.fix([v])
                    remaining_vertices.remove(v)
                    fixing_order.append(v)
                    fixed = True  # flag that we succeeded
                    break  # stop the current pass over vertices

        # compute final reachable closure based on vertices successfully fixed
        reachable_closure = set(G.vertices) - set(
            v for v in G.vertices if G.vertices[v].fixed
        )

        # return the reachable closure, the valid order, and the resulting CADMG
        return reachable_closure, fixing_order, G

    def fixable(self, vertices):
        """
        Check if there exists a valid fixing order and return such
        an order in the form of a list, else returns an empty list.

        :param vertices: set of vertices to check fixability for.
        :return: a boolean indicating whether the set was fixable and a valid fixing order as a stack.
        """

        # keep track of vertices still left to fix (ignoring fixed vertices)
        # and initialize a fixing order
        G = copy.deepcopy(self)
        remaining_vertices = set(vertices) - set(self.fixed)
        fixing_order = []
        fixed = True  # flag to check if we fixed a variable on each pass

        # while we have more vertices to fix, and were able to perform a fix
        while remaining_vertices and fixed:

            fixed = False

            for v in remaining_vertices:

                # Check if any nodes are reachable via -> AND <->
                # by looking at intersection of district and descendants
                if len(G.descendants([v]).intersection(G.district(v))) == 1:
                    G.fix([v])
                    remaining_vertices.remove(v)
                    fixing_order.append(v)
                    fixed = True
                    break

            # if unsuccessful, return failure and
            # fixing order up until point of failure
            if not fixed:
                return False, fixing_order

        # if fixing vertices was successful, return success
        # and the fixing order
        return True, fixing_order

    def subgraph(self, vertices):
        """
        Computes subgraph given a set of vertices.

        Recomputes districts, since these may change when vertices are removed.

        :param vertices: iterable of vertices
        :return: subgraph
        """
        subgraph = super().subgraph(vertices)
        subgraph._calculate_districts()

        return subgraph

    def get_intrinsic_sets(self):
        """
        Computes intrinsic sets (and returns the fixing order for each intrinsic set).

        :returns: list of intrinsic sets and fixing orders used to reach each one
        """

        # create an intrinsic set graph and obtain the intrinsic sets + valid fixing orders leading to them
        ig = IG(copy.deepcopy(self))
        intrinsic_sets = ig.get_intrinsic_sets()
        fixing_orders = ig.iset_fixing_order_map

        return intrinsic_sets, fixing_orders

    def get_intrinsic_sets_and_heads(self):
        """
        Computes intrinsic sets mapped to a tuple of heads and tails of that intrinsic set, and fixing orders for each one.

        :returns: tuple of dict of intrinsic sets to heads and tails, and fixing orders for each intrinsic set

        """
        ig = IG(copy.deepcopy(self))
        intrinsic_sets = ig.get_intrinsic_sets()
        fixing_orders = ig.iset_fixing_order_map
        heads = []
        tails = []
        for intrinsic_set in intrinsic_sets:
            G_sub = self.subgraph(intrinsic_set)
            head = frozenset(
                {
                    s
                    for s in intrinsic_set
                    if len(G_sub.vertices[s].children) == 0
                }
            )
            tail = frozenset(self.parents(intrinsic_set))
            heads.append(head)
            tails.append(tail)
        return dict(zip(intrinsic_sets, zip(heads, tails))), fixing_orders

    def maximal_arid_projection(self):
        """
        Get the maximal arid projection that encodes the same conditional independences and
        Vermas as the original ADMG. This operation is described in Acyclic
        Linear SEMs obey the Nested Markov property by Shpitser et al 2018.

        :return: An ADMG corresponding to the maximal arid projection.
        """

        vertices, di_edges, bi_edges = self.vertices, [], []

        # keep a cached dictionary of reachable closures and ancestors
        # for efficiency purposes
        reachable_closures = {}
        ancestors = {v: self.ancestors([v]) for v in vertices}

        # iterate through all vertex pairs
        for a, b in itertools.combinations(vertices, 2):

            # decide which reachable closure needs to be computed
            # and compute it if one vertex is an ancestor of another
            u, v, rc = None, None, None
            if a in ancestors[b]:
                u, v = a, b
            elif b in ancestors[a]:
                u, v = b, a

            # check parent condition and add directed edge if u is a parent of the reachable closure
            added_edge = False
            if u:
                if v not in reachable_closures:
                    reachable_closures[v] = self.reachable_closure([v])[0]
                rc = reachable_closures[v]
                if u in self.parents(rc):
                    di_edges.append((u, v))
                    added_edge = True

            # if neither are ancestors of each other we need to compute
            # the reachable closure of set {a, b} and check if it is
            # bidirected connected
            if not added_edge:
                rc, _, cadmg = self.reachable_closure([a, b])
                for district in cadmg.districts:
                    if rc <= district:
                        bi_edges.append((a, b))

        return ADMG(vertices=vertices, di_edges=di_edges, bi_edges=bi_edges)

    def mb_shielded(self):
        """
        Check if the ADMG is a Markov blanket shielded ADMG. That is, check if
        two vertices are non-adjacent only when they are absent from each others'
        Markov blankets.

        :return: boolean indicating if it is mb-shielded or not.
        """

        # iterate over all pairs of vertices
        for Vi, Vj in itertools.combinations(self.vertices, 2):
            # check if the pair is not adjacent
            if not (
                Vi in self.siblings([Vj])
                or (Vi, Vj) in self.di_edges
                or (Vj, Vi) in self.di_edges
            ):
                # if one is in the Markov blanket of the other, then it is not mb-shielded
                if Vi in self.markov_blanket([Vj]) or Vj in self.markov_blanket(
                    [Vi]
                ):
                    return False
        return True

    def nonparametric_saturated(self):
        """
        Check if the nested Markov model implied by the ADMG is nonparametric saturated.
        The following is an implementation of Algorithm 1 in Semiparametric Inference for
        Causal Effects in Graphical Models with Hidden Variables (Bhattacharya, Nabi & Shpitser 2020)
        which was shown to be sound and complete for this task.

        :return: boolean indicating if it is nonparametric saturated or not.
        """

        # iterate over all pairs of vertices
        for Vi, Vj in itertools.combinations(self.vertices, 2):

            # check if there is no dense inducing path between Vi and Vj
            # and return not NPS if either of the checks fail
            if not (
                Vi in self.parents(self.reachable_closure([Vj])[0])
                or Vj in self.parents(self.reachable_closure([Vi])[0])
                or Vi in self.reachable_closure([Vi, Vj])[2].district(Vj)
            ):
                return False
        return True

    def m_separated(self, X, Y, separating_set=list()):
        """
        Computes m-separation for set `X` and set `Y` given `separating_set`

        :param X: first vertex set
        :param Y: second vertex set
        :param separating_set: separating set
        :return: boolean result of m-separation
        """
        if type(X) is str:
            X = [X]
        if type(Y) is str:
            Y = [Y]
        for x, y in itertools.product(X, Y):
            if not self._m_separated(x, y, separating_set):
                return False
        return True

    def _m_separated(self, X, Y, separating_set):
        """
        Determine whether `X` and `Y` vertices are m-separated given `separating_set`. Also works on ADMGs which have fixed vertices.

        :param X: first vertex
        :param Y: second vertex
        :param separating_set: list of given vertices

        :return: boolean result of m-separation
        """

        ancestral_vars = [X, Y] + list(separating_set)

        # create a new subgraph of the ancestors of vertex1, vertex2, and given vertices
        ancestral_subgraph = self.subgraph(self.ancestors(ancestral_vars))

        augmented_graph_vertices = list(ancestral_subgraph.vertices)
        augmented_graph_di_edges = list(ancestral_subgraph.di_edges)

        for V in ancestral_subgraph.vertices.values():
            if V.fixed and V.name != X and V.name != Y:
                separating_set.append(V.name)

        # if both vertices are fixed, result is undefined
        if (
            ancestral_subgraph.vertices[X].fixed
            and ancestral_subgraph.vertices[Y].fixed
        ):
            raise UndefinedADMGOperation(
                "{0} and {1} are fixed, so m-separation is undefined.".format(
                    X, Y
                )
            )

        for Vi, Vj in itertools.combinations(augmented_graph_vertices, 2):
            # fixed vertices are connected
            if (
                ancestral_subgraph.vertices[Vi].fixed
                and ancestral_subgraph.vertices[Vj].fixed
            ):
                augmented_graph_di_edges.append((Vi, Vj))

            ancestral_subgraph.vertices[Vi].fixed = False
            ancestral_subgraph.vertices[Vj].fixed = False

        #
        ancestral_subgraph._calculate_districts()

        for Vi, Vj in itertools.combinations(augmented_graph_vertices, 2):

            # checks for common children between any pairs of vertices
            children_i = set(ancestral_subgraph.children([Vi]))

            markov_blanket_Vi = ancestral_subgraph.markov_blanket([Vi])

            # connects vertices if one is in the markov blanket of the other vertex, or markov blanket of child of other vertex
            if (
                Vj in markov_blanket_Vi
                or Vj in ancestral_subgraph.markov_blanket(children_i)
            ):
                augmented_graph_di_edges.append((Vi, Vj))

        # removes given vertices from the graph
        for vertex in augmented_graph_vertices[:]:
            if vertex in separating_set:
                augmented_graph_vertices.remove(vertex)

        # removes any edges from the graph that include any of the given vertices
        for edge in augmented_graph_di_edges[:]:
            if edge[0] in separating_set or edge[1] in separating_set:
                augmented_graph_di_edges.remove(edge)

        # creates a new undirected graph from the updated vertices and edges
        augmented_graph = UG(augmented_graph_vertices, augmented_graph_di_edges)

        # checks if vertex 2 is in the block of vertex 1
        Y_block = augmented_graph.block(X)
        return Y not in Y_block

    def latent_projection(self, retained_vertices):
        """
        Computes latent projection.

        :param retained_vertices: list of vertices to retain after latent projection
        :returns: Latent projection containing retained vertices
        """

        vertices = self.vertices
        di_edges = self.di_edges
        bi_edges = self.bi_edges

        projected_vertices = list(set(vertices) - set(retained_vertices))
        G = self.copy()

        for vertex in projected_vertices:
            G = latent_project_single_vertex(vertex=vertex, graph=G)

        return G

    def canonical_dag(self, cardinality: Union[int, str] = None):
        """
        Computes the canonical DAG from the ADMG by inserting a variable in place of each bidirected edge.

        For each bidirected edge 'X <-> Y', the inserted variable will take names of the form
        'U_XY', the original bidirected edge is removed, and new directed edges 'U_X_Y -> Y' and
        'U_X_Y -> X' are inserted. The variable names are in lexicographic order.

        :params cardinality: The cardinality of the inserted variables
        :type cardinality: Union[int, str]
        :returns: A directed acyclic graph
        :rtype: DAG


        """
        from .dag import DAG

        if cardinality is None:
            warnings.warn(
                "Warning: cardinality of latent variables not set. Please set the cardinality if intending to use ananke.models.discrete functionality."
            )

        G = DAG(vertices=list(self.vertices), di_edges=self.di_edges)
        for _x, _y in self.bi_edges:
            x, y = tuple(sorted([_x, _y]))
            new_var = "U_{}_{}".format(x, y)
            G.add_vertex(name=new_var, cardinality=cardinality)
            G.add_diedge(new_var, x)
            G.add_diedge(new_var, y)

        for v in self.vertices:
            if self.vertices[v].fixed:
                G.vertices[v].fixed = True

        return G
