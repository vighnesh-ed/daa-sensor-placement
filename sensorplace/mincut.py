"""Min-cut / max-flow: cheapest set of links to cut to isolate an attacker."""
from collections import defaultdict, deque


def min_cut(edges, s, t, cap=None):
    """Edmonds-Karp (BFS augmenting paths, O(V E^2)) on an undirected network.
    cap[(u, v)] = cost of cutting that link (default 1).
    Returns (flow_value, links_to_cut). By max-flow min-cut they have equal weight."""
    cap = cap or {}
    res, nbrs = defaultdict(int), defaultdict(set)
    for u, v in edges:
        c = cap.get((u, v), cap.get((v, u), 1))
        res[(u, v)] += c
        res[(v, u)] += c
        nbrs[u].add(v)
        nbrs[v].add(u)

    flow = 0
    while True:
        parent = {s: None}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v in nbrs[u]:
                if v not in parent and res[(u, v)] > 0:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            break
        b, v = float("inf"), t
        while parent[v] is not None:
            b = min(b, res[(parent[v], v)])
            v = parent[v]
        v = t
        while parent[v] is not None:
            res[(parent[v], v)] -= b
            res[(v, parent[v])] += b
            v = parent[v]
        flow += b

    side_s = set(parent)                  # still reachable from s in the residual graph
    cut = [(u, v) for u, v in edges if (u in side_s) != (v in side_s)]
    return flow, cut