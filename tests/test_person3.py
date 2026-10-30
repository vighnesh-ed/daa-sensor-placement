"""Tests for Person 3 exact-search instrumentation and local search."""
from itertools import combinations

import pytest

from sensorplace import (
    erdos_renyi, exact_branch_and_bound, greedy_degree, is_cover, local_search
)


def brute_force_opt(edges):
    nodes = sorted({v for edge in edges for v in edge})
    for k in range(len(nodes) + 1):
        for subset in combinations(nodes, k):
            if is_cover(edges, set(subset)):
                return k
    return 0


@pytest.mark.parametrize("seed", range(8))
def test_instrumented_exact_search_remains_optimal(seed):
    edges = erdos_renyi(9, 0.35, seed=seed)
    stats = {}
    cover, finished = exact_branch_and_bound(edges, stats=stats)
    assert finished
    assert is_cover(edges, cover)
    assert len(cover) == brute_force_opt(edges)
    assert stats["nodes"] >= 1
    assert stats["degree1_reductions"] >= 0
    assert stats["bound_prunes"] >= 0


@pytest.mark.parametrize(
    "degree1,bound", [(False, False), (True, False), (False, True), (True, True)]
)
def test_pruning_switch_combinations_are_exact(degree1, bound):
    edges = erdos_renyi(9, 0.4, seed=21)
    cover, finished = exact_branch_and_bound(
        edges, use_degree1=degree1, use_bound=bound, time_limit=10
    )
    assert finished
    assert is_cover(edges, cover)
    assert len(cover) == brute_force_opt(edges)


@pytest.mark.parametrize("seed", range(12))
def test_local_search_is_valid_and_not_larger_than_greedy(seed):
    edges = erdos_renyi(12, 0.3, seed=seed)
    result = local_search(edges)
    initial = greedy_degree(edges)
    assert is_cover(edges, result)
    assert len(result) <= len(initial)


def test_local_search_empty_graph():
    assert local_search(set()) == set()
