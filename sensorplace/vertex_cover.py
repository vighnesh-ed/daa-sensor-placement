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


def exact_branch_and_bound(edges, time_limit=10.0, stats=None,
                           use_degree1=True, use_bound=True):
    """Exact search for minimum vertex cover using branch-and-bound.

    Branch on a maximum-degree vertex v:
      (1) include v, or (2) exclude v and include all its neighbours.

    Degree-1 reduction and the edge/max-degree lower bound can be disabled
    independently for experiments. If `stats` is a dictionary, it is updated
    with counts for recursive search nodes and pruning events.
    """
    start = time.time()
    best = [approx_matching(edges)]       # initial feasible upper bound
    finished = [True]
    if stats is not None:
        stats.setdefault("nodes", 0)
        stats.setdefault("degree1_reductions", 0)
        stats.setdefault("bound_prunes", 0)
        stats.setdefault("incumbent_prunes", 0)

    def solve(adj, chosen):
        if stats is not None:
            stats["nodes"] += 1
        if time.time() - start > time_limit:
            finished[0] = False
            return

        adj = {v: set(ns) for v, ns in adj.items() if ns}
        chosen = set(chosen)

        if use_degree1:
            changed = True
            while changed:
                changed = False
                for u in list(adj):
                    if u in adj and len(adj[u]) == 1:
                        w = next(iter(adj[u]))
                        chosen.add(w)
                        if stats is not None:
                            stats["degree1_reductions"] += 1
                        for x in adj[w]:
                            adj[x].discard(w)
                        del adj[w]
                        changed = True
                adj = {v: ns for v, ns in adj.items() if ns}

        if len(chosen) >= len(best[0]):
            if stats is not None:
                stats["incumbent_prunes"] += 1
            return
        if not adj:
            best[0] = chosen
            return

        if use_bound:
            m = sum(len(ns) for ns in adj.values()) // 2
            dmax = max(len(ns) for ns in adj.values())
            lower_bound = -(-m // dmax)
            if len(chosen) + lower_bound >= len(best[0]):
                if stats is not None:
                    stats["bound_prunes"] += 1
                return

        v = max(adj, key=lambda x: len(adj[x]))

        # Branch 1: choose v; all incident edges are then covered.
        a1 = {x: set(ns) for x, ns in adj.items()}
        for u in a1[v]:
            a1[u].discard(v)
        del a1[v]
        solve(a1, chosen | {v})

        # Branch 2: do not choose v; every neighbour must be chosen.
        nb = set(adj[v])
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