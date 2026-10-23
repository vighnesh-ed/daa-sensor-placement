"""Tests for the ILP models. Small graphs (at most 11 vertices) are checked
against brute force; clique is also checked against NetworkX; and the
relationships between the three problems are tested one by one."""
from itertools import combinations

import networkx as nx
import pytest

from sensorplace import erdos_renyi, is_cover
from sensorplace.ilp_models import (complement_edges, max_clique,
                                    max_independent_set, min_vertex_cover)

# 20 random graphs on 5..11 vertices, sparse to dense, many with isolated vertices
GRAPHS = [(5 + s % 7, erdos_renyi(5 + s % 7, 0.1 + 0.05 * (s % 12), seed=s))
          for s in range(20)]


def subsets(n):
    for k in range(n + 1):
        yield from (set(c) for c in combinations(range(n), k))


def is_independent(edges, chosen):
    return not any(u in chosen and v in chosen for u, v in edges)


def is_clique(edges, chosen):
    return all((u, v) in edges for u, v in combinations(sorted(chosen), 2))


def brute_min_cover_cost(edges, n, cost):
    return min(sum(cost.get(v, 1) for v in s)
               for s in subsets(n) if is_cover(edges, s))


def brute_max(n, ok):
    return max(len(s) for s in subsets(n) if ok(s))


@pytest.mark.parametrize("n,edges", GRAPHS)
def test_outputs_are_valid(n, edges):
    nodes = range(n)
    assert is_cover(edges, min_vertex_cover(edges, nodes))
    assert is_independent(edges, max_independent_set(edges, nodes))
    assert is_clique(edges, max_clique(edges, nodes))


@pytest.mark.parametrize("n,edges", GRAPHS)
def test_cover_plus_independent_set_is_all_vertices(n, edges):
    nodes = range(n)
    assert len(min_vertex_cover(edges, nodes)) + len(max_independent_set(edges, nodes)) == n


@pytest.mark.parametrize("n,edges", GRAPHS)
def test_clique_is_independent_set_of_complement(n, edges):
    comp = complement_edges(edges, range(n))
    assert len(max_clique(edges, range(n))) == len(max_independent_set(comp, range(n)))


@pytest.mark.parametrize("n,edges", GRAPHS)
def test_all_three_match_brute_force(n, edges):
    nodes = range(n)
    assert len(min_vertex_cover(edges, nodes)) == brute_min_cover_cost(edges, n, {})
    assert len(max_independent_set(edges, nodes)) == brute_max(n, lambda s: is_independent(edges, s))
    assert len(max_clique(edges, nodes)) == brute_max(n, lambda s: is_clique(edges, s))


@pytest.mark.parametrize("n,edges", GRAPHS)
def test_clique_matches_networkx(n, edges):
    G = nx.Graph(list(edges))
    G.add_nodes_from(range(n))
    _, size = nx.algorithms.clique.max_weight_clique(G, weight=None)
    assert len(max_clique(edges, range(n))) == size


@pytest.mark.parametrize("n,edges", GRAPHS[:10])
def test_weighted_cover_matches_brute_force(n, edges):
    cost = {v: 1 + (3 * v) % 5 for v in range(n)}          # costs between 1 and 5
    cover = min_vertex_cover(edges, range(n), cost)
    assert is_cover(edges, cover)
    assert sum(cost[v] for v in cover) == brute_min_cover_cost(edges, n, cost)


def test_edge_cases():
    assert min_vertex_cover(set(), range(4)) == set()
    assert max_independent_set(set(), range(4)) == {0, 1, 2, 3}   # nobody conflicts
    assert len(max_clique(set(), range(4))) == 1                  # a single machine
    assert max_clique(set(), []) == set()
    assert max_independent_set({(0, 1), (1, 2), (0, 2)}, range(3)) in ({0}, {1}, {2})
    assert max_clique({(0, 1), (1, 2), (0, 2)}, range(3)) == {0, 1, 2}


def test_edges_outside_nodes_are_rejected():
    with pytest.raises(ValueError):
        max_clique({(0, 5)}, range(3))
