"""ILP models for the three NP-complete problems that are really one problem:
Vertex Cover, Independent Set and Clique. Each takes the edges and the full
vertex list `nodes`, because isolated machines have no edges and would
otherwise be invisible (they matter for independent set and clique).

All three use one 0/1 variable x_v per machine ("v is chosen"). Only the
objective and the constraints change:

    vertex cover     min  sum cost_v * x_v   x_u + x_v >= 1  for every EDGE
    independent set  max  sum x_v            x_u + x_v <= 1  for every EDGE
    clique           max  sum x_v            x_u + x_v <= 1  for every NON-EDGE

Why: a cover must catch at least one end of every link (>= 1). An independent
set may hold at most one end of any link (<= 1). A clique is the mirror image:
it may hold at most one end of any pair that is NOT linked, so every pair
inside it is linked.
"""
from itertools import combinations

import pulp

from .vertex_cover import ilp


def complement_edges(edges, nodes):
    """Edges of the complement graph: a link exactly where G has none.
    A clique in G is an independent set here (and vice versa)."""
    return {(u, v) for u, v in combinations(sorted(set(nodes)), 2)
            if (u, v) not in edges}


def _check(edges, nodes):
    nodes = sorted(set(nodes))
    missing = {x for e in edges for x in e} - set(nodes)
    if missing:
        raise ValueError(f"edges use vertices not listed in nodes: {sorted(missing)}")
    return nodes


def _max_chosen(nodes, conflicts):
    """Largest set of vertices with at most one end of each pair in `conflicts`."""
    if not nodes:
        return set()
    prob = pulp.LpProblem("choose", pulp.LpMaximize)
    x = {v: pulp.LpVariable(f"x{i}", cat="Binary") for i, v in enumerate(nodes)}
    prob += pulp.lpSum(x.values())
    for u, v in conflicts:
        prob += x[u] + x[v] <= 1
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    return {v for v in nodes if x[v].value() > 0.5}


def min_vertex_cover(edges, nodes, cost=None):
    """Cheapest set of machines touching every link (`cost` {vertex: price}).
    Reuses ilp() from vertex_cover.py. `nodes` is only checked: an isolated
    machine never needs a sensor, so it never appears in the answer."""
    _check(edges, nodes)
    return ilp(edges, cost)


def max_independent_set(edges, nodes):
    """Largest set of machines with no link between any two of them."""
    nodes = _check(edges, nodes)
    return _max_chosen(nodes, edges)


def max_clique(edges, nodes):
    """Largest set of machines that are all directly linked to each other."""
    nodes = _check(edges, nodes)
    return _max_chosen(nodes, complement_edges(edges, nodes))
