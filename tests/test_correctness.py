"""Correctness tests. Small graphs are checked against brute force; min-cut is
checked against NetworkX, an independent implementation."""
import random
from itertools import combinations

import networkx as nx
import pytest

from sensorplace import (approx_matching, greedy_degree, exact_branch_and_bound,
                         ilp, min_cut, is_cover, erdos_renyi,
                         preferential_attachment, grid, adjacency)


def brute_force_opt(edges):
    nodes = sorted({x for e in edges for x in e})
    for k in range(len(nodes) + 1):
        for subset in combinations(nodes, k):
            if is_cover(edges, set(subset)):
                return k


SMALL = [erdos_renyi(11, 0.3, seed=s) for s in range(15)]
SMALL = [E for E in SMALL if E]           # need at least one edge


@pytest.mark.parametrize("edges", SMALL)
def test_all_solvers_return_valid_covers(edges):
    for cover in (approx_matching(edges), greedy_degree(edges),
                  exact_branch_and_bound(edges)[0], ilp(edges)):
        assert is_cover(edges, cover)


@pytest.mark.parametrize("edges", SMALL)
def test_exact_and_ilp_match_brute_force(edges):
    opt = brute_force_opt(edges)
    assert len(exact_branch_and_bound(edges)[0]) == opt
    assert len(ilp(edges)) == opt


@pytest.mark.parametrize("edges", SMALL)
def test_approximation_ratio_at_most_two(edges):
    assert len(approx_matching(edges)) <= 2 * brute_force_opt(edges)


def test_known_answers():
    star = {(0, i) for i in range(1, 6)}
    assert len(ilp(star)) == 1                      # one sensor on the hub
    path5 = {(0, 1), (1, 2), (2, 3), (3, 4)}
    assert len(ilp(path5)) == 2                     # machines 1 and 3
    assert len(exact_branch_and_bound(grid(3, 3))[0]) == 4   # bipartite: König


def test_weighted_ilp_avoids_expensive_machine():
    star = {(0, i) for i in range(1, 4)}
    # hub costs 10, each leaf costs 1 -> cheaper to instrument the 3 leaves
    cover = ilp(star, cost={0: 10})
    assert cover == {1, 2, 3}


@pytest.mark.parametrize("seed", range(10))
def test_min_cut_matches_networkx_and_disconnects(seed):
    rng = random.Random(seed)
    edges = preferential_attachment(25, seed=seed)
    cap = {e: rng.randint(1, 5) for e in edges}
    s, t = 0, 24
    G = nx.Graph()
    for (u, v), c in cap.items():
        G.add_edge(u, v, capacity=c)
    expected = nx.minimum_cut_value(G, s, t)

    value, cut = min_cut(edges, s, t, cap)
    assert value == expected
    assert sum(cap[e] for e in cut) == value        # cut weight == flow
    rest = adjacency([e for e in edges if e not in set(cut)])
    seen, stack = {s}, [s]
    while stack:
        for v in rest[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    assert t not in seen                             # t really is cut off