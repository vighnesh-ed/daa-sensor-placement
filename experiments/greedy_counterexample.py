"""Find the smallest graph where greedy-by-degree is worse than optimal, even
with the BEST possible tie-breaking.
Run from the project root:  python -m experiments.greedy_counterexample

Greedy picks a vertex of maximum degree; when several vertices tie, the
choice is arbitrary. A graph where greedy only fails because of an unlucky
tie-break proves nothing, so for every graph we try ALL tie-breaks and keep the
best one. We call it a counterexample only if even that best run is bigger than
the optimum (found by brute force over all subsets).

Search order: every graph with up to 7 vertices (NetworkX's graph atlas, so the
search is exhaustive and the answer really is the smallest), then random graphs
with 8 to 11 vertices if nothing smaller exists. Writes
figures/greedy_counterexample.png."""
import random
from collections import Counter
from functools import lru_cache
from itertools import combinations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

from sensorplace import erdos_renyi, greedy_degree, is_cover


def best_greedy_run(edges):
    """Smallest cover that greedy-by-degree can produce under ANY tie-break,
    as a tuple of the vertices it picks in order."""
    @lru_cache(maxsize=None)
    def go(remaining):                       # remaining: frozenset of uncovered edges
        if not remaining:
            return ()
        deg = Counter()
        for u, v in remaining:
            deg[u] += 1
            deg[v] += 1
        top = max(deg.values())
        runs = [(v,) + go(frozenset(e for e in remaining if v not in e))
                for v in sorted(deg) if deg[v] == top]
        return min(runs, key=len)
    return go(frozenset(edges))


def brute_force_cover(edges):
    """A minimum vertex cover, by trying all subsets in order of size."""
    nodes = sorted({x for e in edges for x in e})
    for k in range(len(nodes) + 1):
        for subset in combinations(nodes, k):
            if is_cover(edges, set(subset)):
                return set(subset)


def candidates():
    """Graphs in increasing size: all graphs up to 7 vertices, then random ones."""
    for G in nx.graph_atlas_g():
        edges = {(min(u, v), max(u, v)) for u, v in G.edges()}
        if edges:
            yield edges
    for n in range(8, 12):
        rng = random.Random(n)
        for _ in range(3000):
            edges = erdos_renyi(n, rng.uniform(0.15, 0.5), seed=rng.randrange(10**6))
            if edges:
                yield edges


def find_smallest():
    best = None                             # (vertices, edges), edges as sorted list
    for edges in candidates():
        n = len({x for e in edges for x in e})
        if best and (n, len(edges)) >= (best[0], len(best[1])):
            continue
        if len(best_greedy_run(edges)) > len(brute_force_cover(edges)):
            best = (n, sorted(edges))
        if best and best[0] <= 7 and n > 7:
            break
    return best


def draw(edges, greedy_picks, optimal, path="figures/greedy_counterexample.png"):
    G = nx.Graph(list(edges))
    pos = nx.spring_layout(G, seed=4)
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    for ax, chosen, title in ((axes[0], set(greedy_picks), f"greedy, best tie-break: {len(greedy_picks)} sensors"),
                              (axes[1], optimal, f"optimal: {len(optimal)} sensors")):
        nx.draw(G, pos, ax=ax, with_labels=True, font_color="white",
                node_color=["tab:red" if v in chosen else "tab:blue" for v in G],
                edge_color="gray")
        ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def main():
    found = find_smallest()
    if not found:
        print("no counterexample found")
        return
    n, edges = found
    E = set(edges)
    picks = best_greedy_run(E)
    opt = brute_force_cover(E)
    print(f"Smallest counterexample: {n} vertices, {len(E)} edges")
    print("edges:", edges)
    print(f"optimal cover ({len(opt)}): {sorted(opt)}")
    print(f"greedy, best possible tie-break ({len(picks)}): picks in order {list(picks)}")
    print(f"greedy_degree as implemented ({len(greedy_degree(E))}): {sorted(greedy_degree(E))}")
    draw(E, picks, opt)
    print("saved figures/greedy_counterexample.png")


if __name__ == "__main__":
    main()
