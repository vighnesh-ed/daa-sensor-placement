"""Tests for the labelled campus scenario and unit-capacity edge paths."""
import networkx as nx
import pytest

from sensorplace.mincut import min_cut
from sensorplace.scenario import build_campus_network


def test_campus_network_has_expected_named_components():
    edges, name_to_id, capacities = build_campus_network()
    assert len(name_to_id) == 24
    assert len(edges) == len(capacities)
    assert "internet" in name_to_id
    assert "firewall-1" in name_to_id
    assert "switch-3" in name_to_id
    assert "workstation-15" in name_to_id
    assert "database" in name_to_id
    assert all(u < v for u, v in edges)
    assert all(capacities[e] > 0 for e in edges)


def test_campus_compromised_workstation_cut_cost_matches_flow():
    edges, names, capacities = build_campus_network()
    source, target = names["workstation-01"], names["database"]
    value, cut = min_cut(edges, source, target, capacities)
    assert value == sum(capacities[e] for e in cut)
    remaining = [e for e in edges if e not in set(cut)]
    graph = nx.Graph()
    graph.add_nodes_from(names.values())
    graph.add_edges_from(remaining)
    seen, stack = {source}, [source]
    while stack:
        current = stack.pop()
        for neighbour in graph.neighbors(current):
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    assert target not in seen


@pytest.mark.parametrize("seed", range(10))
def test_unit_capacity_flow_matches_edge_disjoint_paths(seed):
    graph = nx.gnp_random_graph(12, 0.32, seed=seed)
    largest = max(nx.connected_components(graph), key=len)
    graph = graph.subgraph(largest).copy()
    nodes = sorted(graph.nodes)
    if len(nodes) < 2:
        pytest.skip("generated graph has fewer than two connected vertices")
    source, target = nodes[0], nodes[-1]
    edges = {(min(u, v), max(u, v)) for u, v in graph.edges}
    unit_capacities = {edge: 1 for edge in edges}

    flow, _ = min_cut(edges, source, target, unit_capacities)
    expected = len(list(nx.edge_disjoint_paths(graph, source, target)))
    assert flow == expected
