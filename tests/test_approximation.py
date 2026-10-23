"""Tests for the claims in docs/approximation_proof.md."""
import random

import pytest

from sensorplace import approx_matching, erdos_renyi, is_cover
from sensorplace.ilp_models import min_vertex_cover

PATH = [(0, 1), (1, 2), (2, 3)]                  # a-b-c-d
K33 = [(a, b) for a in range(3) for b in range(3, 6)]


def test_tight_example_path():
    assert approx_matching(PATH) == {0, 1, 2, 3}          # 4 vertices
    assert len(min_vertex_cover(set(PATH), range(4))) == 2  # optimum {1, 2}


def test_path_is_optimal_in_another_edge_order():
    assert approx_matching([(1, 2), (0, 1), (2, 3)]) == {1, 2}


@pytest.mark.parametrize("seed", range(20))
def test_complete_bipartite_is_tight_for_every_order(seed):
    order = K33[:]
    random.Random(seed).shuffle(order)
    assert len(approx_matching(order)) == 6               # twice the optimum, 3


@pytest.mark.parametrize("seed", range(15))
def test_output_is_a_cover_made_of_a_matching_and_within_twice_optimal(seed):
    edges = erdos_renyi(11, 0.3, seed=seed)
    if not edges:
        return
    cover = approx_matching(edges)
    assert is_cover(edges, cover)                         # Lemma 1
    assert len(cover) % 2 == 0                            # 2 vertices per matched edge
    opt = len(min_vertex_cover(edges, range(11)))
    assert opt <= len(cover) <= 2 * opt                   # Lemma 2 and the theorem
