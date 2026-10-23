"""ILP running time against graph size, next to the exact search.
Run from the project root:  python -m experiments.ilp_runtime
Reads results.csv (made by experiments.benchmark), writes figures/ilp_runtime.png
(log scale) and prints the mean times. An exact-search run that hit its time
limit is drawn as a cross: its time is the limit, not the time it would need."""
import csv
from collections import defaultdict
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_results(path="results.csv"):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main(csv_path="results.csv", out="figures/ilp_runtime.png"):
    rows = read_results(csv_path)
    by = defaultdict(lambda: defaultdict(list))        # family -> n -> rows
    for r in rows:
        by[r["family"]][int(r["n"])].append(r)
    fams = list(by)
    fig, axes = plt.subplots(1, len(fams), figsize=(4 * len(fams), 3.6),
                             sharey=True, squeeze=False)
    for ax, fam in zip(axes[0], fams):
        ns = sorted(by[fam])
        ilp_t = [mean(float(r["ilp_s"]) for r in by[fam][n]) for n in ns]
        ex_t = [mean(float(r["exact_s"]) for r in by[fam][n]) for n in ns]
        ax.plot(ns, ilp_t, marker="o", label="ILP (CBC)")
        ax.plot(ns, ex_t, marker="s", label="exact search")
        cut = [(n, t) for n, t in zip(ns, ex_t)
               if any(r["exact_finished"] != "True" for r in by[fam][n])]
        if cut:
            ax.plot(*zip(*cut), "kx", markersize=10, label="exact hit time limit")
        ax.set_yscale("log")
        ax.set_title(fam)
        ax.set_xlabel("n (vertices)")
        print(f"{fam:10} " + "  ".join(
            f"n={n}: ILP {a * 1000:.0f}ms / exact {b * 1000:.0f}ms"
            for n, a, b in zip(ns, ilp_t, ex_t)))
    axes[0][0].set_ylabel("mean time (seconds, log scale)")
    axes[0][0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
