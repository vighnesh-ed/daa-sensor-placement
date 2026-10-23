"""Weighted sensor costs: what does it save to account for price differences?
Run from the project root:  python -m experiments.weighted

Core machines (the highest-degree 20% of each network: servers, routers) cost
5 to instrument, everything else costs 1. For every network we compare:
  (a) the UNWEIGHTED optimum (fewest sensors, price ignored), priced afterwards;
  (b) the WEIGHTED ILP optimum (cheapest total price);
  (c) a weighted greedy: repeatedly take the machine with the most unmonitored
      links per unit of cost.
(b) is optimal by construction, so (b) <= (a) and (b) <= (c). Writes
weighted_results.csv and figures/weighted.png, and prints the table."""
import csv
from collections import defaultdict
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sensorplace import ilp, is_cover, preferential_attachment, erdos_renyi, adjacency

FAMILIES = {
    "hub-heavy": lambda n, seed: preferential_attachment(n, seed=seed),
    "random":    lambda n, seed: erdos_renyi(n, 4 / n * 2, seed=seed),
}
SIZES = [20, 40, 80]
SEEDS = [1, 2, 3, 4, 5]
CORE_COST, CORE_FRACTION = 5, 0.2


def make_costs(edges):
    """{vertex: price}. The highest-degree CORE_FRACTION of machines cost
    CORE_COST, the rest 1. Ties in degree are broken by vertex number so the
    prices are the same on every run."""
    deg = {v: len(ns) for v, ns in adjacency(edges).items()}
    order = sorted(deg, key=lambda v: (-deg[v], v))
    core = set(order[:max(1, round(CORE_FRACTION * len(order)))])
    return {v: CORE_COST if v in core else 1 for v in order}


def weighted_greedy(edges, cost):
    """Repeatedly take the machine with the most unmonitored links per unit of
    cost. With equal costs this is greedy_degree; with unequal costs it stops
    chasing expensive hubs whose price is not worth the links they cover."""
    adj = adjacency(edges)
    cover = set()
    while any(adj[v] for v in adj):
        v = max(adj, key=lambda x: (len(adj[x]) / cost[x], -x))
        cover.add(v)
        for u in adj[v]:
            adj[u].discard(v)
        adj[v] = set()
    return cover


def total_cost(cover, cost):
    return sum(cost[v] for v in cover)


def main():
    rows = []
    for fam, gen in FAMILIES.items():
        for n in SIZES:
            for seed in SEEDS:
                E = gen(n, seed)
                cost = make_costs(E)
                unweighted = ilp(E)
                weighted = ilp(E, cost)
                greedy = weighted_greedy(E, cost)
                for c in (unweighted, weighted, greedy):
                    assert is_cover(E, c)
                a, b, c = (total_cost(s, cost) for s in (unweighted, weighted, greedy))
                assert b <= a and b <= c            # (b) is the true optimum
                rows.append(dict(family=fam, n=n, seed=seed, links=len(E),
                                 unweighted_opt_cost=a, weighted_ilp_cost=b,
                                 weighted_greedy_cost=c,
                                 saving_pct=100 * (a - b) / a))
                print(f"{fam:10} n={n:<3} seed={seed} unweighted-opt={a:<4} "
                      f"weighted-ILP={b:<4} weighted-greedy={c:<4} "
                      f"saving={rows[-1]['saving_pct']:.1f}%")
    with open("weighted_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print("\nMean over seeds:")
    groups = defaultdict(list)
    for r in rows:
        groups[(r["family"], r["n"])].append(r)
    for (fam, n), rs in groups.items():
        print(f"{fam:10} n={n:<3} unweighted-opt={mean(r['unweighted_opt_cost'] for r in rs):6.1f} "
              f"weighted-ILP={mean(r['weighted_ilp_cost'] for r in rs):6.1f} "
              f"weighted-greedy={mean(r['weighted_greedy_cost'] for r in rs):6.1f} "
              f"saving={mean(r['saving_pct'] for r in rs):.1f}%")
    for fam in FAMILIES:
        rs = [r for r in rows if r["family"] == fam]
        print(f"{fam}: weighted ILP is on average "
              f"{mean(r['saving_pct'] for r in rs):.1f}% cheaper than pricing the "
              f"unweighted optimum (max {max(r['saving_pct'] for r in rs):.1f}%).")

    keys = list(groups)
    width = 0.27
    fig, ax = plt.subplots(figsize=(8, 4))
    for i, (col, label) in enumerate([("unweighted_opt_cost", "unweighted optimum, priced"),
                                      ("weighted_ilp_cost", "weighted ILP"),
                                      ("weighted_greedy_cost", "weighted greedy")]):
        ax.bar([k + (i - 1) * width for k in range(len(keys))],
               [mean(r[col] for r in groups[key]) for key in keys], width, label=label)
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels([f"{fam}\nn={n}" for fam, n in keys], fontsize=8)
    ax.set_ylabel("total sensor cost (mean of 5 graphs)")
    ax.legend()
    fig.tight_layout()
    fig.savefig("figures/weighted.png", dpi=150)
    print("saved weighted_results.csv and figures/weighted.png")


if __name__ == "__main__":
    main()
