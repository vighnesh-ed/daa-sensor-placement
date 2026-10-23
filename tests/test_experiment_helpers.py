"""Tests for the helper functions behind the weighted and greedy-counterexample
experiments."""
from itertools import combinations

import pytest

from experiments.greedy_counterexample import best_greedy_run, brute_force_cover
from experiments.weighted import make_costs, total_cost, weighted_greedy
from sensorplace import erdos_renyi, greedy_degree, ilp, is_cover

SMALL = [E for E in (erdos_renyi(10, 0.35, seed=s) for s in range(15)) if E]
SPIDER = {(0, 1), (0, 3), (0, 4), (1, 2), (3, 6), (4, 5)}   # hub with three 2-edge legs


@pytest.mark.parametrize("edges", SMALL)
def test_make_costs_is_deterministic_and_prices_the_core(edges):
    cost = make_costs(edges)
    assert cost == make_costs(edges)
    assert set(cost) == {x for e in edges for x in e}
    assert set(cost.values()) <= {1, 5}
    assert 1 <= sum(c == 5 for c in cost.values()) <= len(cost)


@pytest.mark.parametrize("edges", SMALL)
def test_weighted_greedy_is_valid_and_never_beats_the_weighted_ilp(edges):
    cost = make_costs(edges)
    cover = weighted_greedy(edges, cost)
    assert is_cover(edges, cover)
    assert total_cost(ilp(edges, cost), cost) <= total_cost(cover, cost)


@pytest.mark.parametrize("edges", SMALL)
def test_weighted_ilp_is_no_dearer_than_pricing_the_unweighted_optimum(edges):
    cost = make_costs(edges)
    assert total_cost(ilp(edges, cost), cost) <= total_cost(ilp(edges), cost)


def test_weighted_greedy_avoids_an_expensive_hub():
    star = {(0, i) for i in range(1, 5)}              # hub 0 linked to 4 leaves
    assert weighted_greedy(star, {0: 100, 1: 1, 2: 1, 3: 1, 4: 1}) == {1, 2, 3, 4}
    assert weighted_greedy(star, {0: 1, 1: 1, 2: 1, 3: 1, 4: 1}) == {0}


@pytest.mark.parametrize("edges", SMALL)
def test_best_greedy_run_is_between_optimal_and_greedy_degree(edges):
    picks = best_greedy_run(edges)
    assert is_cover(edges, set(picks)) and len(picks) == len(set(picks))
    assert len(brute_force_cover(edges)) <= len(picks) <= len(greedy_degree(edges))


def test_spider_is_a_real_counterexample():
    assert len(best_greedy_run(SPIDER)) == 4          # even the best tie-break
    assert len(brute_force_cover(SPIDER)) == 3        # the hub's three neighbours


def test_brute_force_cover_is_minimum():
    for edges in SMALL[:6]:
        nodes = sorted({x for e in edges for x in e})
        smaller = [s for k in range(len(brute_force_cover(edges)))
                   for s in combinations(nodes, k) if is_cover(edges, set(s))]
        assert smaller == []
