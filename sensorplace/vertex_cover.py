"""Four Minimum Vertex Cover solvers (= sensor placement). Each takes a set of
edges and returns a set of vertices that covers every edge."""
import time

import pulp

from .graphs import adjacency


def approx_matching(edges):
    """2-approximation: take BOTH endpoints of each edge in a maximal matching.
    Any cover needs >= 1 endpoint per matched edge, we pay 2 -> ratio <= 2."""
    cover = set()
    for u, v in edges:
        if u not in cover and v not in cover:
            cover.update((u, v))
    return cover


def greedy_degree(edges):
    """Repeatedly pick the machine with the most unmonitored links.
    No constant-factor guarantee (O(log n) worst case) but strong in practice."""
    adj = adjacency(edges)
    cover = set()
    while any(adj[v] for v in adj):
        v = max(adj, key=lambda x: len(adj[x]))
        cover.add(v)
        for u in adj[v]:
            adj[u].discard(v)
        adj[v] = set()
    return cover


def exact_branch_and_bound(edges, time_limit=10.0):
    """Exact search. Branch on the max-degree vertex v:
         (1) v is in the cover, or (2) v is not -> all its neighbours are.
    Pruning: degree-1 reduction + lower bound ceil(edges_left / max_degree).
    Returns (cover, finished); finished=False means the time limit was hit and
    the cover is the best found, not proven optimal."""
    start = time.time()
    best = [approx_matching(edges)]       # upper bound to prune against
    finished = [True]

    def solve(adj, chosen):
        if time.time() - start > time_limit:
            finished[0] = False
            return
        adj = {v: set(ns) for v, ns in adj.items() if ns}
        chosen = set(chosen)
        changed = True
        while changed:                    # degree-1 rule: take the leaf's neighbour
            changed = False
            for u in list(adj):
                if u in adj and len(adj[u]) == 1:
                    w = next(iter(adj[u]))
                    chosen.add(w)
                    for x in adj[w]:
                        adj[x].discard(w)
                    del adj[w]
                    changed = True
            adj = {v: ns for v, ns in adj.items() if ns}
        if len(chosen) >= len(best[0]):
            return
        if not adj:
            best[0] = chosen
            return
        m = sum(len(ns) for ns in adj.values()) // 2
        dmax = max(len(ns) for ns in adj.values())
        if len(chosen) + -(-m // dmax) >= len(best[0]):
            return
        v = max(adj, key=lambda x: len(adj[x]))
        a1 = {x: set(ns) for x, ns in adj.items()}       # branch 1: v in cover
        for u in a1[v]:
            a1[u].discard(v)
        del a1[v]
        solve(a1, chosen | {v})
        nb = set(adj[v])                                  # branch 2: v out
        a2 = {x: set(ns) for x, ns in adj.items()}
        for w in nb:
            for u in a2[w]:
                a2[u].discard(w)
            del a2[w]
        a2.pop(v, None)
        solve(a2, chosen | nb)

    solve(adjacency(edges), set())
    return best[0], finished[0]


def ilp(edges, cost=None):
    """min sum c_v x_v  s.t.  x_u + x_v >= 1 per link, x_v in {0,1}.
    `cost` {vertex: price} models machines that are costlier to instrument."""
    if not edges:
        return set()
    nodes = sorted({x for e in edges for x in e})
    prob = pulp.LpProblem("sensors", pulp.LpMinimize)
    x = {v: pulp.LpVariable(f"x{v}", cat="Binary") for v in nodes}
    prob += pulp.lpSum((cost or {}).get(v, 1) * x[v] for v in nodes)
    for u, v in edges:
        prob += x[u] + x[v] >= 1
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    return {v for v in nodes if x[v].value() > 0.5}