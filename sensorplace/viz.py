"""Reproducible graph visualisation for the campus security scenario."""
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


def draw(edges, sensors=None, cut=None, labels=None, path="figure.png"):
    """Draw a network, highlighting selected sensor vertices and cut links.

    Sensors are red, other vertices blue, and cut links are dashed red.
    A fixed spring-layout seed makes repeated figures reproducible.
    Returns the output path.
    """
    graph = nx.Graph()
    graph.add_edges_from(edges)
    sensors = set(sensors or ())
    cut_edges = {frozenset(edge) for edge in (cut or [])}
    labels = labels or {v: str(v) for v in graph.nodes}

    positions = nx.spring_layout(graph, seed=42)
    node_colours = [
        "red" if node in sensors else "steelblue" for node in graph.nodes
    ]

    fig, ax = plt.subplots(figsize=(13, 9))
    nx.draw_networkx_edges(
        graph, positions, ax=ax, edge_color="gray", width=1.4, alpha=0.75
    )
    highlighted = [
        (u, v) for u, v in graph.edges
        if frozenset((u, v)) in cut_edges
    ]
    if highlighted:
        nx.draw_networkx_edges(
            graph, positions, ax=ax, edgelist=highlighted,
            edge_color="red", style="dashed", width=3.0
        )
    nx.draw_networkx_nodes(
        graph, positions, ax=ax, node_color=node_colours,
        node_size=650, edgecolors="black", linewidths=0.7
    )
    nx.draw_networkx_labels(
        graph, positions, ax=ax, labels=labels, font_size=7
    )
    ax.set_axis_off()
    fig.tight_layout()
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return str(output)
