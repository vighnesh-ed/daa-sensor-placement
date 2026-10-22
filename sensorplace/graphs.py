"""Graph generators and helpers. A graph is a set of edges (u, v) with u < v."""
import random
from collections import defaultdict


def preferential_attachment(n, m=2, seed=0):
    """Hub-heavy network (a few big servers, many leaf machines)."""
    rng = random.Random(seed)
    edges, repeated = set(), []          # `repeated` holds each node once per degree
    for v in range(m, n):
        chosen = set()
        while len(chosen) < min(m, v):
            if repeated and rng.random() < 0.8:
                chosen.add(rng.choice(repeated))
            else:
                chosen.add(rng.randrange(v))
        for u in chosen:
            edges.add((min(u, v), max(u, v)))
            repeated += [u, v]
    return edges


def erdos_renyi(n, p, seed=0):
    """Every pair of machines is linked independently with probability p."""
    rng = random.Random(seed)
    return {(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p}


def grid(rows, cols):
    """Office-floor style network: machines on a grid, linked to neighbours."""
    edges = set()
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            if c + 1 < cols:
                edges.add((v, v + 1))
            if r + 1 < rows:
                edges.add((v, v + cols))
    return edges


def adjacency(edges):
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def is_cover(edges, cover):
    """Correctness check used by every test and benchmark."""
    return all(u in cover or v in cover for u, v in edges)