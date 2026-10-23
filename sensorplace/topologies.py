"""Load real network topologies (GraphML files) into our graph format:
a set of edges (u, v) with u < v and integer vertices 0..n-1."""
from pathlib import Path

import networkx as nx

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "topologies"


def _name_key(name):
    """Sort numeric node ids numerically ("2" before "10"), other names as text,
    so the relabelling is the same on every machine."""
    s = str(name)
    return (0, int(s), s) if s.isdigit() else (1, 0, s)


def load_topology(path):
    """Read a GraphML file and return its edges as a set of (u, v), u < v.

    Real files are messy, and the solvers assume a clean simple graph, so we:
    - merge parallel links and ignore direction (nx.Graph),
    - drop self-loops (a link from a machine to itself would force it into
      every cover and is not a link between two machines),
    - keep only the largest connected component (one network, not stray
      fragments; ties go to the component with the smallest node name),
    - relabel the remaining nodes to 0..n-1 in a fixed order.
    Isolated machines have no links, so they disappear with the edge set.
    """
    G = nx.Graph(nx.read_graphml(path))
    G.remove_edges_from(list(nx.selfloop_edges(G)))
    G.remove_nodes_from([v for v in list(G) if G.degree(v) == 0])
    if G.number_of_edges() == 0:
        return set()
    keep = min(nx.connected_components(G),
               key=lambda c: (-len(c), _name_key(min(c, key=_name_key))))
    label = {name: i for i, name in enumerate(sorted(keep, key=_name_key))}
    return {(min(label[a], label[b]), max(label[a], label[b]))
            for a, b in G.subgraph(keep).edges()}


def list_topologies(folder=DATA_DIR):
    """All .graphml files in `folder`, sorted by name (empty list if none)."""
    return sorted(Path(folder).glob("*.graphml"))
