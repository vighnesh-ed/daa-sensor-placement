"""Tests for load_topology: messy synthetic GraphML files with a known answer,
plus every real file found in data/topologies/."""
import networkx as nx
import pytest

from sensorplace.topologies import list_topologies, load_topology


def check_clean(edges):
    """Every property the solvers rely on."""
    assert isinstance(edges, set)
    assert all(isinstance(u, int) and isinstance(v, int) for u, v in edges)
    assert all(u < v for u, v in edges)                  # also rules out self-loops
    nodes = {x for e in edges for x in e}
    assert nodes == set(range(len(nodes)))               # relabelled to 0..n-1
    G = nx.Graph(list(edges))
    assert nx.is_connected(G)                            # largest component only


def write(tmp_path, G, name="g.graphml"):
    path = tmp_path / name
    nx.write_graphml(G, path)
    return path


def test_messy_file_gives_known_answer(tmp_path):
    G = nx.MultiGraph()
    G.add_edges_from([("Paris", "Rome"), ("Rome", "Paris"),   # parallel links
                      ("Rome", "Rome"),                       # self-loop
                      ("Rome", "Oslo"),
                      ("A", "B")])                            # smaller fragment
    G.add_node("Lima")                                        # isolated machine
    edges = load_topology(write(tmp_path, G))
    # sorted names Oslo, Paris, Rome -> 0, 1, 2
    assert edges == {(0, 2), (1, 2)}
    check_clean(edges)


def test_directed_input_is_made_undirected(tmp_path):
    G = nx.DiGraph([("1", "2"), ("2", "1"), ("2", "10")])
    edges = load_topology(write(tmp_path, G))
    assert edges == {(0, 1), (1, 2)}                          # "2" < "10" numerically


def test_largest_component_wins(tmp_path):
    G = nx.Graph([("a", "b"), ("c", "d"), ("d", "e"), ("e", "f")])
    edges = load_topology(write(tmp_path, G))
    assert len(edges) == 3 and len({x for e in edges for x in e}) == 4
    check_clean(edges)


def test_no_links_gives_empty_set(tmp_path):
    G = nx.Graph()
    G.add_nodes_from(["x", "y"])
    G.add_edge("x", "x")
    assert load_topology(write(tmp_path, G)) == set()


def test_loading_twice_gives_the_same_graph(tmp_path):
    G = nx.gnm_random_graph(30, 45, seed=3)
    G = nx.relabel_nodes(G, {v: f"n{v}" for v in G})
    path = write(tmp_path, G)
    assert load_topology(path) == load_topology(path)


REAL_FILES = list_topologies()


@pytest.mark.skipif(not REAL_FILES, reason="no files in data/topologies/ yet")
@pytest.mark.parametrize("path", REAL_FILES, ids=lambda p: p.stem)
def test_real_topology_is_clean(path):
    edges = load_topology(path)
    assert edges, f"{path.name} produced no edges"
    check_clean(edges)
