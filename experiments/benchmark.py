"""Compare all four solvers across graph families and sizes.
Run from the project root:  python -m experiments.benchmark
Writes results.csv (for plots/report) and prints a table."""
import csv
import time

from sensorplace import (approx_matching, greedy_degree, exact_branch_and_bound,
                         ilp, is_cover, preferential_attachment, erdos_renyi, grid)
from sensorplace.topologies import list_topologies, load_topology

FAMILIES = {
    "hub-heavy": lambda n, seed: preferential_attachment(n, seed=seed),
    "random":    lambda n, seed: erdos_renyi(n, 4 / n * 2, seed=seed),
    "grid":      lambda n, seed: grid(int(n ** 0.5), int(n ** 0.5)),
}
SIZES = [20, 40, 80, 120, 160]          # 320 dropped: ILP on random graphs of degree 8 takes hours there
SEEDS = [1, 2, 3]                       # average over several graphs per size
TIME_LIMIT = 5.0


def timed(fn, *a):
    t0 = time.perf_counter()
    r = fn(*a)
    return r, time.perf_counter() - t0


def instances():
    """Yield (family, n, seed, name, edges): the synthetic families first, then
    every real topology in data/topologies/. One list feeds one loop, so a
    real network is measured exactly like a generated one. A real network is a
    fixed graph, so its n is its vertex count, its seed is 0 and `name` is the
    file name."""
    for fam, gen in FAMILIES.items():
        for n in SIZES:
            for seed in SEEDS:
                yield fam, n, seed, "", gen(n, seed)
    for path in list_topologies():
        E = load_topology(path)
        yield "real", len({v for e in E for v in e}), 0, path.stem, E


def main():
    rows = []
    for fam, n, seed, name, E in instances():
        if not E:
            continue
        opt, t_ilp = timed(ilp, E)
        (ex, done), t_ex = timed(exact_branch_and_bound, E, TIME_LIMIT)
        ap, t_ap = timed(approx_matching, E)
        gr, t_gr = timed(greedy_degree, E)
        for c in (opt, ex, ap, gr):
            assert is_cover(E, c)
        rows.append(dict(
            family=fam, n=n, seed=seed, links=len(E), optimal=len(opt),
            ilp_s=t_ilp, exact_size=len(ex), exact_s=t_ex, exact_finished=done,
            approx_size=len(ap), approx_s=t_ap, greedy_size=len(gr), greedy_s=t_gr,
            instance=name))
        print(f"{fam:10} n={n:<4} seed={seed} opt={len(opt):<4} "
              f"approx={len(ap)/len(opt):.2f}x greedy={len(gr)/len(opt):.2f}x "
              f"exact={t_ex*1000:.0f}ms{'' if done else ' (TIMEOUT)'} {name}")
    with open("results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print("saved results.csv")


if __name__ == "__main__":
    main()