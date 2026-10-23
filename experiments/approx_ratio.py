"""Approximation ratio (algorithm size / optimal size) against graph size.
Run from the project root:  python -m experiments.approx_ratio
Reads results.csv (made by experiments.benchmark), writes
figures/approx_ratio.png, and prints the mean ratios the plot is drawn from.

One panel per graph family, one line per algorithm, and a horizontal line at 2:
the 2-approximation can never go above it, greedy has no such guarantee."""
import csv
from collections import defaultdict
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ALGORITHMS = [("approx_size", "2-approximation"), ("greedy_size", "greedy")]


def read_results(path="results.csv"):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def mean_ratios(rows):
    """{family: {algorithm column: {n: mean ratio over the graphs of that size}}}"""
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in rows:
        for col, _ in ALGORITHMS:
            grouped[r["family"]][col][int(r["n"])].append(int(r[col]) / int(r["optimal"]))
    return {fam: {col: {n: mean(v) for n, v in sorted(by_n.items())}
                  for col, by_n in cols.items()}
            for fam, cols in grouped.items()}


def main(csv_path="results.csv", out="figures/approx_ratio.png"):
    ratios = mean_ratios(read_results(csv_path))
    fams = list(ratios)
    fig, axes = plt.subplots(1, len(fams), figsize=(4 * len(fams), 3.6),
                             sharey=True, squeeze=False)
    for ax, fam in zip(axes[0], fams):
        for col, label in ALGORITHMS:
            ns, ys = zip(*ratios[fam][col].items())
            ax.plot(ns, ys, marker="o", label=label)
        ax.axhline(2, color="gray", linestyle="--", label="guarantee (2)")
        ax.set_title(fam)
        ax.set_xlabel("n (vertices)")
        ax.set_ylim(0.9, 2.1)
    axes[0][0].set_ylabel("size / optimal size")
    axes[0][0].legend()
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    for fam in fams:
        for col, label in ALGORITHMS:
            vals = list(ratios[fam][col].values())
            print(f"{fam:10} {label:16} mean ratio {mean(vals):.3f}  "
                  f"(range {min(vals):.3f} to {max(vals):.3f})")
    print(f"saved {out}")


if __name__ == "__main__":
    main()
